from django.contrib import admin

# Register your models here.
from .models import Batter, Pitcher, League

admin.site.register(Batter)
admin.site.register(Pitcher)
admin.site.register(League)