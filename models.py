from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class SubmittedRecord(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    photoshoot_date = models.DateField()
    location = models.CharField(max_length=100)
    plant_name_serbian = models.CharField(max_length=100)
    plant_name_latin = models.CharField(max_length=100)
    plant_species_serbian = models.CharField(max_length=100)
    plant_species_latin = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    file_names = models.JSONField(default=list, blank=True)
    file_urls = models.JSONField(default=list, blank=True)
    session_id = models.CharField(max_length=100)
    approved = models.BooleanField(default=None, null=True)
    approved_by = models.ForeignKey(User, related_name='approved_records', on_delete=models.SET_NULL, null=True, blank=True)
    rejected_by = models.ForeignKey(User, related_name='rejected_records', on_delete=models.SET_NULL, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
    
class Plant(models.Model):
    id = models.AutoField(primary_key=True)
    serbian_name = models.CharField(max_length=100)
    latin_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)
