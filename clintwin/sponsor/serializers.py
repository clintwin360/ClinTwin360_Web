from .models import *
from rest_framework import serializers


class ParticipantQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantQuestion
        fields = ['id', 'text', 'valueType', 'options']

class ClinicalTrialCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalTrialCriteria
        fields = '__all__'



class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'first_name', 'last_name', 'email']


class ParticipantBasicHealthSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParticipantBasicHealth
        fields = ['participant', 'gender', 'weight', 'height', 'birth_date']


class ParticipantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantResponse
        fields = ['question', 'participant', 'value']


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class SponsorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['organization', 'contactPerson', 'email']


class ClinicalTrialListSerializer(serializers.ModelSerializer):
    sponsor = SponsorDetailSerializer(read_only=True)

    class Meta:
        model = ClinicalTrial
        fields = ['title', 'objective', 'id', 'sponsor', 'recruitmentStartDate',
                  'recruitmentEndDate', 'enrollmentTarget', 'description', 'url', 'current_recruitment', 'status', 'custom_id',]


class ClinicalTrialDetailSerializer(serializers.ModelSerializer):
    sponsor = SponsorDetailSerializer(read_only=True)

    class Meta:
        model = ClinicalTrial
        fields = ['title', 'objective', 'description', 'recruitmentStartDate',
                  'recruitmentEndDate', 'id', 'sponsor', 'url',  'current_recruitment', 'status', 'custom_id',]


class ClinicalTrialMatchSerializer(serializers.ModelSerializer):
    clinical_trial = ClinicalTrialListSerializer(read_only=True)

    class Meta:
        model = ClinicalTrialMatch
        fields = ['clinical_trial']


class ClinicalTrialCriteriaResponseSerializer(serializers.ModelSerializer):
    clinical_trial = ClinicalTrialDetailSerializer(read_only=True)

    class Meta:
        model = ClinicalTrialCriteriaResponse
        fields = '__all__'