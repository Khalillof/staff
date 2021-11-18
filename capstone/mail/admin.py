from django.contrib import admin
from .models import Contact, Email
# Register your models here.

# agency
admin.site.register(Contact)
admin.site.register(Email)
