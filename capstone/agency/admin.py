from django.contrib import admin
from agency.models import JobCategory, Office, Job, Address, Advert, Application
from accounts.models import User
# Register your models here.

# account
admin.site.register(User)

# agency
admin.site.register(Address)
admin.site.register(JobCategory)
admin.site.register(Office)
admin.site.register(Job)
admin.site.register(Advert)
admin.site.register(Application)
