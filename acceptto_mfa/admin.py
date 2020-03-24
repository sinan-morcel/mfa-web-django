from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import AccepttoCredentials

# Register your models here.
class AccepttoCredentialsInline(admin.StackedInline):
  model = AccepttoCredentials
  can_delete = False
  show_full_result_count = False
  verbose_name = "MFA Email"
  verbose_name_plural = "Acceptto Credentials"

class UserAdmin_(UserAdmin):
  inlines = [AccepttoCredentialsInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin_)

