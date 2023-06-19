from django.contrib import admin

from .models import Files, Folders, Activities, Allusers, Students


for x in [Files, Folders, Activities, Allusers, Students]:
    admin.site.register(x)