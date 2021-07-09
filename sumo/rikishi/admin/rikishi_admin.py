from django.contrib import admin

from sumo.rikishi.models.rikishi import Rikishi


@admin.register(Rikishi)
class RikishiAdmin(admin.ModelAdmin):
    fieldsets = ((None, {
        "fields": ("shikona_first", "shikona_second", "is_active"),
    }), ("Career", {
        "fields": ("heya", "shusshin", "shikona_history", "heya_id_history"),
    }), ("Personal Details", {
        "fields": ("birth_name", "date_of_birth", "height", "weight"),
    }))
