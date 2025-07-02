from django.contrib import admin
from .models import SubmittedRecord, Plant

class SubmittedRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'first_name', 'last_name', 'email', 'photoshoot_date', 'location', 'plant_name_serbian', 'plant_name_latin', 'plant_species_serbian', 'plant_species_latin', 'about', 'file_names', 'file_urls', 'session_id', 'approved', 'approved_by', 'rejected_by', 'last_update')
    list_filter = ('plant_name_serbian', 'plant_species_serbian', 'created_at', 'approved', 'approved_by', 'rejected_by', 'last_update')
    search_fields = ('plant_name_serbian', 'plant_species_serbian', 'created_at', 'approved', 'approved_by', 'rejected_by', 'last_update')

admin.site.register(SubmittedRecord, SubmittedRecordAdmin)

class PlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'serbian_name', 'latin_name')
    list_filter = ('id', 'serbian_name', 'latin_name')
    search_fields = ('id', 'serbian_name', 'latin_name')

admin.site.register(Plant, PlantAdmin)