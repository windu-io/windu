from django.contrib import admin


from .models import Chat
from .models import Message
from .models import Contact
from .models import ProfilePicture
from .models import Account

admin.site.register(Account)
admin.site.register(Chat)
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(ProfilePicture)