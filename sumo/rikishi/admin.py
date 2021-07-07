from django.contrib import admin

from sumo.rikishi.models.heya import Heya
from sumo.rikishi.models.rikishi import Rikishi
from sumo.rikishi.models.shusshin import Shusshin

admin.site.register(Heya)
admin.site.register(Rikishi)
admin.site.register(Shusshin)
