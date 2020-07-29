import os
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from porsgram.settings import MEDIA_ROOT
from pathlib import Path


from user.models import UserModel, AvatarModel


@receiver(post_save, sender=UserModel)
def create_avatarmodel(sender, instance, created, **kwargs):
    if created:
        AvatarModel.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
def save_avatarmodel(sender, instance, created, **kwargs):
    instance.avatarmodel.save()



def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path) and (Path(path).parent == MEDIA_ROOT):
        os.remove(path)

@receiver(post_delete, sender=AvatarModel)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.avatar:
        _delete_file(instance.avatar.path)
