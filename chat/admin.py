from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Chat
from .models import Message
from .models import Contact
from .models import ProfilePhoto
from .models import Account
from .models import StatusMessage
from .models import ContactsFromMessage
from .models import ContactsNickname
from .models import ThirdAuthToken
from .models import FileUpload
from .models import CodeVerification

admin.site.register(Account)
admin.site.register(Chat)
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(ProfilePhoto)
admin.site.register(StatusMessage)
admin.site.register(ContactsFromMessage)
admin.site.register(ContactsNickname)
admin.site.register(ThirdAuthToken)
admin.site.register(FileUpload)
admin.site.register(CodeVerification)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class CodeVerificationInline(admin.StackedInline):
    model = CodeVerification
    can_delete = False
    verbose_name_plural = 'code verifications'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (CodeVerificationInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)