from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Participant)
admin.site.register(ParticipantBasicHealth)
admin.site.register(ParticipantResponse)
admin.site.register(ClinicalTrialCriteria)
admin.site.register(Sponsor)
admin.site.register(ClinicalTrial)
admin.site.register(ClinicalTrialCriteriaResponse)
admin.site.register(ParticipantQuestion)
admin.site.register(QuestionFlow)
admin.site.register(UserProfile)
admin.site.register(ClinicalTrialMatch)

