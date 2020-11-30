from django.contrib import admin
from manager.models import project_lead
from manager.models import members

# Register your models here.
admin.site.register(project_lead)
admin.site.register(members)
