
from django.core.files.uploadhandler import TemporaryFileUploadHandler

from .uploadedfile import TemporaryNamedUploadedFile

class TemporaryNamedFileUploadHandler(TemporaryFileUploadHandler):
    """
    Upload handler that streams data into a temporary file.
    """
    def __init__(self, *args, **kwargs):
        super(TemporaryNamedFileUploadHandler, self).__init__(*args, **kwargs)

    def new_file(self, *args, **kwargs):
        """
        Create the file object to append to as data is coming in.
        """
        super(TemporaryNamedFileUploadHandler, self).new_file(*args, **kwargs)
        self.file = TemporaryNamedUploadedFile(self.file_name, self.content_type, 0, self.charset, self.content_type_extra)