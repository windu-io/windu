from django.contrib import admin


from .models import Chat
from .models import Message
from .models import Contact
from .models import ProfilePicture
from .models import Account
from .models import StatusMessage
from .models import ContactsFromMessage
from .models import ContactsNickname

admin.site.register(Account)
admin.site.register(Chat)
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(ProfilePicture)
admin.site.register(StatusMessage)
admin.site.register(ContactsFromMessage)
admin.site.register(ContactsNickname)