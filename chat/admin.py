from django.contrib import admin


from .models import Chat
from .models import Message
from .models import Contact
from .models import ProfilePhoto
from .models import Account
from .models import StatusMessage
from .models import ContactsFromMessage
from .models import ContactsNickname
from .models import ThirdAuthToken
from .models import ImageUpload

admin.site.register(Account)
admin.site.register(Chat)
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(ProfilePhoto)
admin.site.register(StatusMessage)
admin.site.register(ContactsFromMessage)
admin.site.register(ContactsNickname)
admin.site.register(ThirdAuthToken)
admin.site.register(ImageUpload)