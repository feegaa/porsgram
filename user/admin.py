from django.contrib import admin
from user.models import UserModel, AvatarModel
# Register your models here.

admin.site.register(UserModel)
admin.site.register(AvatarModel)

