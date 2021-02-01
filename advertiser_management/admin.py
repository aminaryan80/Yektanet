from django.contrib import admin

from .models import Advertiser, Ad, Click, View


class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'approve',)
    search_fields = ('title',)
    list_filter = ('approve',)


admin.site.register(Advertiser)
admin.site.register(Ad, AdAdmin)
admin.site.register(View)
admin.site.register(Click)
