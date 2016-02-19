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

    def upload_photo(self, path):

        client = self.__get_client()
        image = client.upload_from_path(path)
        ThirdAuth.update_credentials(self.auth,
                                     self.client.auth.get_current_access_token(),
                                     self.client.auth.get_refresh_token())
        return image['link']

    def upload_photo_from_url(self, url):

        try:
            client = self.__get_client()
            image = client.upload_from_url(url)
            ThirdAuth.update_credentials(self.auth,
                                         self.client.auth.get_current_access_token(),
                                         self.client.auth.get_refresh_token())
        except:
            return None

        return image['link']

