from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FriendRequest, Friendship
from rest_framework.validators import UniqueTogetherValidator


class FriendRequestSerializer(serializers.ModelSerializer):

    from_user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault())
    to_user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())
    accepted = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = FriendRequest
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=FriendRequest.objects.all(),
                fields=['from_user', 'to_user']
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['to_user']:
            raise serializers.ValidationError(
                'Нельзя добавить в друзья себя самого')
        return data


class FriendSerializer(serializers.ModelSerializer):

    user1 = serializers.SlugRelatedField(read_only=True, slug_field='username')
    user2 = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Friendship
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=FriendRequest.objects.all(),
                fields=['user1', 'user2']
            )
        ]
