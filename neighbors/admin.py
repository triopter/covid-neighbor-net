from django.contrib import admin

from neighbors.models import Role, NeighborProfile, Address

# @TODO: flesh out neighbor admin
admin.site.register(Role)
admin.site.register(NeighborProfile)
admin.site.register(Address)
