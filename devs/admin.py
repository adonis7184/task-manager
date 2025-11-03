from django.contrib import admin
from .models import Team, Tech, Developer


admin.site.register(Tech)
admin.site.register(Team)
admin.site.register(Developer)
