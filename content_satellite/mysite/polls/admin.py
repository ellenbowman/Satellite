from django.contrib import admin

from polls.models import Question,Choice,Outfit

admin.site.register(Question)

admin.site.register(Choice)

admin.site.register(Outfit)