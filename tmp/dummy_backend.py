from __future__ import absolute_import

from django.utils.functional import cached_property
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
from django.conf import settings

from ckeditor_uploader import utils

from PIL import Image



class DummyBackend(object):
    
    def __init__(self, storage_engine, file_object):
        self.file_object    = file_object
        self.storage_engine = storage_engine
        self.SIZE           = 720, 980


    def save_as(self, filepath):
        return self.checkSize(self.storage_engine.save(filepath, self.file_object))
        


    # def checkSize(self, filepath):
    #     img  = Image.open(self.file_object)
    #     name = self.file_object.name
    #     if img.size > self.SIZE:        
    #         try:
    #             print(self.file_object.size)
    #             img.thumbnail(self.SIZE, Image.ANTIALIAS)
    #             print(img.size)
    #             self.file_object = InMemoryUploadedFile(File(img, name), None, name, 'image/jpeg', img.size, None)
    #             # self.file_object = File(img, name)
    #             print(self.file_object.size)
    #         except IOError:
    #             pass

    def checkSize(self, filepath):
        try:
            pathfile = settings.MEDIA_ROOT + filepath
            img  = Image.open(pathfile)
            if img.size > self.SIZE:        
                try:
                    img.thumbnail(self.SIZE, Image.ANTIALIAS)
                    img.save(pathfile)
                except IOError:
                    pass
        except IOError:
            pass

        return filepath


    @cached_property
    def is_image(self):
        return utils.is_valid_image_extension(self.file_object.name)
