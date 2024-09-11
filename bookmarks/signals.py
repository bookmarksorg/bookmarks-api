from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Review)
def award_points_to_user_review(sender, instance, created, **kwargs):
    if created:
        user = instance.id_user
        if user.points is None:
            user.points = 10
        else:
            user.points += 10
        user.save()

@receiver(post_save, sender=Discussion)
def award_points_to_user_discussion(sender, instance, created, **kwargs):
    if created:
        user = instance.id_user
        if user.points is None:
            user.points = 5
        else:
            user.points += 5
        user.save()


@receiver(post_save, sender=Comments)
def award_points_to_user_comments(sender, instance, created, **kwargs):
    if created:
        user = instance.id_user
        if user.points is None:
            user.points = 3
        else:
            user.points += 3
        user.save()