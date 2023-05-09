from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='friend_requests_sent',
        on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User,
        related_name='friend_requests_received',
        on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')


class Friendship(models.Model):
    user1 = models.ForeignKey(
        User, related_name='friendship1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(
        User, related_name='friendship2', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user1', 'user2')
