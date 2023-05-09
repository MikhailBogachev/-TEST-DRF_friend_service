from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendSerializer


class FriendRequestViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        queryset = (FriendRequest.objects.filter(from_user=self.request.user)
                    | FriendRequest.objects.filter(to_user=self.request.user))
        return queryset

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)
        user = User.objects.get(username=serializer.data['to_user'])
        if FriendRequest.objects.filter(from_user=user.id,
                                        to_user=self.request.user).exists():
            queryset1 = FriendRequest.objects.get(from_user=user,
                                                  to_user=self.request.user)
            queryset2 = FriendRequest.objects.get(from_user=self.request.user,
                                                  to_user=user)
            queryset1.accepted = True
            queryset2.accepted = True
            queryset1.save()
            queryset2.save()
            Friendship.objects.create(user1=user, user2=self.request.user)

    def list(self, request):
        outgoing_requests = self.queryset.filter(from_user=request.user)
        incoming_requests = self.queryset.filter(to_user=request.user)
        outgoing_serializer = FriendRequestSerializer(outgoing_requests,
                                                      many=True)
        incoming_serializer = FriendRequestSerializer(incoming_requests,
                                                      many=True)
        return Response({
            'outgoing_requests': outgoing_serializer.data,
            'incoming_requests': incoming_serializer.data,
        })

    @action(detail=True, methods=['get'])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        if friend_request.to_user == self.request.user:
            friend_request.accepted = True
            friend_request.save()
            Friendship.objects.create(user1=friend_request.from_user,
                                      user2=friend_request.to_user)
            return Response({'status': 'Заявка принята'})
        return Response({'Нельзя принять исходящую заявку'})

    @action(detail=True, methods=['get'])
    def reject(self, request, pk=None):
        friend_request = self.get_object()
        if friend_request.to_user == self.request.user:
            friend_request.accepted = False
            friend_request.save()
            return Response({'status': 'Заявка отклонена'})
        return Response({'Нельзя отклонить исходящую заявку'})


class FriendViewSet(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FriendSerializer

    def get_queryset(self):
        queryset = (Friendship.objects.filter(user1=self.request.user)
                    | Friendship.objects.filter(user2=self.request.user))
        return queryset

    def list(self, request):
        friends = Friendship.objects.filter(Q(user1=request.user)
                                            | Q(user2=request.user))
        friends_serializer = FriendSerializer(friends, many=True)
        data = friends_serializer.data

        friend_list = []
        for item in data:
            if item['user1'] != str(request.user):
                friend_list.append({'id_friendship': item['id'],
                                    'friend': item['user1']})
            else:
                friend_list.append({'id_friendship': item['id'],
                                    'friend': item['user2']})

        return Response({
            'friends': friend_list
        })

    def retrieve(self, request, pk=None):
        friend_username = pk
        if not friend_username:
            return Response({'error': 'friend_username is required'})
        friend = get_object_or_404(User, username=pk)
        user = request.user

        if Friendship.objects.filter(user1=user, user2=friend).exists() or \
                Friendship.objects.filter(user1=friend, user2=user).exists():
            return Response({'answer': 'Уже друзья'})
        if FriendRequest.objects.filter(from_user=user,
                                        to_user=friend).exists():
            return Response({'answer': 'Есть исходящая заявка в друзья'})
        if FriendRequest.objects.filter(from_user=friend,
                                        to_user=user).exists():
            return Response({'answer': 'Есть входящая заявка в друзья'})
        return Response({'answer': 'Нет ничего'})

    def destroy(self, request, pk=None):
        friend_username = pk
        if not friend_username:
            return Response({'error': 'friend_username is required'})
        friend = get_object_or_404(User, username=pk)
        user = request.user

        obj = Friendship.objects.filter((Q(user1=user) & Q(user2=friend))
                                        | (Q(user1=friend) & Q(user2=user))
                                        )
        if obj.exists():
            obj.delete()

            if FriendRequest.objects.filter(Q(from_user=user)
                                            & Q(to_user=friend)).exists():
                FriendRequest.objects.get(from_user=user,
                                          to_user=friend).delete()
            if FriendRequest.objects.filter(Q(from_user=friend)
                                            & Q(to_user=user)).exists():
                request = FriendRequest.objects.get(from_user=friend,
                                                    to_user=user)
                request.accepted = False
                request.save()

            return Response({'status': 'Пользователь удален из друзей'})
        return Response({'error': 'Пользователь не числится в друзьях'})
