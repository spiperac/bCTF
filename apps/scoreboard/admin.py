from django.contrib import admin
from apps.scoreboard.models import News


class NewsAdmin(admin.ModelAdmin):
    pass


admin.site.register(News, NewsAdmin)
