from django.contrib import admin

from .models import Protein, Database, Kingdom, Organism, Load, Cluster, New

admin.site.register(Protein)
admin.site.register(Database)
admin.site.register(Kingdom)
admin.site.register(Organism)
admin.site.register(Load)
admin.site.register(Cluster)
admin.site.register(New)
