from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(FeitioProfile)

admin.site.register(SocialNetwork)

admin.site.register(Band)

admin.site.register(Tour)

admin.site.register(Concert)

admin.site.register(Contact)

admin.site.register(Release)

admin.site.register(ReleaseCredits)

admin.site.register(BandSocialNetwork)

admin.site.register(BandFeitioProfile)

admin.site.site_header = "Feitio Admin"


"""
#Testes com o admin personalizados
@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'html_icon')
    search_fields = ('name',)

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('band', 'year')
    search_fields = ('band__name', 'year')
    ordering = ('-year',)
"""
