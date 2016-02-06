#! /usr/bin/env python
# -*- coding: utf-8 -*-


from imgurpython import ImgurClient
from .third_auth import ThirdAuth

from ..models import ImageUpload


class ImageUploader:

    def __init__(self):
        self.auth = None
        self.client = None

    def __get_client(self):

        if self.client is not None:
            return self.client

        self.auth = ThirdAuth.find_credentials('imgur')
        self.client = ImgurClient(self.auth.client_id,
                                  self.auth.client_secret,
                                  self.auth.access_token,
                                  self.auth.refresh_token)
        return self.client

    @staticmethod
    def __check_uploaded_photo(image_hash):

        image_upload = ImageUpload.objects.filter(hash=image_hash).first()
        if image_upload is None:
            return None

        return image_upload

    def upload_photo(self, image_hash, path, check_db_cache=False):

        if check_db_cache:
            upload = ImageUploader.__check_uploaded_photo(image_hash)
            if upload is not None:
                return upload.photo_url

        client = self.__get_client()
        image = client.upload_from_path(path)
        ThirdAuth.update_credentials(self.auth,
                                     self.client.auth.get_current_access_token(),
                                     self.client.auth.get_refresh_token())
        return image['link']

