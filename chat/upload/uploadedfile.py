
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files import temp as temp_file
from django.conf import settings

class TemporaryNamedUploadedFile(TemporaryUploadedFile):
    """
    A file uploaded to a temporary location with name as suffix (i.e. stream-to-disk).
    """
    def __init__(self, name, content_type, size, charset, content_type_extra=None):
        if settings.FILE_UPLOAD_TEMP_DIR:
            file = temp_file.NamedTemporaryFile(suffix=name,
                dir=settings.FILE_UPLOAD_TEMP_DIR)
        else:
            file = temp_file.NamedTemporaryFile(suffix=name)
        super(TemporaryUploadedFile, self).__init__(file, name, content_type, size, charset, content_type_extra)