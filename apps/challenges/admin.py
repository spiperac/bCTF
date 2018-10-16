from django.contrib import admin
from apps.challenges.models import Category, Challenge, Flag, Attachment, Hint, Solves


class CategoryAdmin(admin.ModelAdmin):
    pass

class ChallengeAdmin(admin.ModelAdmin):
    pass

class FlagAdmin(admin.ModelAdmin):
    pass

class AttachmentAdmin(admin.ModelAdmin):
    pass

class HintAdmin(admin.ModelAdmin):
    pass

class SolvesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Flag, FlagAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Hint, HintAdmin)
admin.site.register(Solves, SolvesAdmin)