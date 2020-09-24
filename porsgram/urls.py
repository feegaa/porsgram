"""porsgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from django.conf import settings
from porsgram import settings
from django.conf.urls.static import static
from ckeditor_uploader import views as uploader_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from porsgram import views

urlpatterns = [
    path('', include('QA.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/upload', uploader_views.upload, name='ckeditor_upload'),
    path('ckeditor/browse', uploader_views.browse, name='ckeditor_browse'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()

print('medis is here')
# print('home'+static('/home/sadegh'))
print(settings.MEDIA_URL, settings.MEDIA_ROOT)
# handler400 = 'porsgram.views.bad_request'
# handler403 = 'porsgram.views.permission_denied'
handler404 = views.handler404
handler400 = views.handler400
handler403 = views.handler403
handler500 = views.handler500
# handler404 = 'porsgram.views.handler404'
# handler500 = 'porsgram.views.handler500'

