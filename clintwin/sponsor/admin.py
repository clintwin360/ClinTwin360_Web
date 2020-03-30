from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ParticipantQuestion)
admin.site.register(Participant)
admin.site.register(ParticipantResponse)
admin.site.register(ClinicalTrialCriteria)