#! /usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import mimetypes
import os
import base64


def process_file(path):

    if not path or not os.path.isfile(path):
        return None

    h = hashlib.sha256()

    file = open(path, "rb")
    picture_data = file.read()
    length  = file.tell()
    file.close()
    mime_type = mimetypes.guess_type(path)

    h.update(picture_data)
    b64_digest = base64.b64encode(h.digest())

    return {
            'code': '200',
            'path': path,
            'picture_data': picture_data,
            'mime_type': mime_type,
            'hash': b64_digest,
            'length': length
            }