#! /usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import basename
import requests


class AudioUploader:

    @staticmethod
    def upload_audio(path, mime_type):
        clyp_file_upload_url = 'http://upload.clyp.it/upload'
        audio_file = open(path, 'rb')
        send_files = {'audioFile': (basename(path), audio_file, mime_type)}
        r = requests.post(clyp_file_upload_url, files=send_files)
        audio_file.close()
        if r.status_code != 200 and r.status_code != 201:
            return None
        result = r.json()
        return result.get('Mp3Url')

    def upload_audio_from_url(url):
        clyp_file_upload_url = 'http://upload.clyp.it/uploadurl'
        params = {'url': url}
        r = requests.post(clyp_file_upload_url, params=params)
        if r.status_code != 200 or r.status_code != 201:
            return None
        result = r.json()
        return result.get('Mp3Url')

