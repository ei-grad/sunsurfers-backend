from django.contrib import admin


from django.contrib.gis import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from onboarding import models


admin.site.register(models.Step)


