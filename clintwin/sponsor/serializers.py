from collections import OrderedDict

from .models import *
from rest_framework import serializers
import ast
from rest_framework.renderers import JSONRenderer


class ParticipantQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantQuestion
        fields = ['id', 'text', 'valueType', 'options']


class VirtualTrialParticipantQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualTrialParticipantQuestion
        fields = ['id', 'text', 'valueType', 'options']

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "text": instance.text,
            "valueType": instance.valueType,
            "options": ast.literal_eval(instance.options)
        }


class ClinicalTrialCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalTrialCriteria
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "valueType": instance.valueType,
            "options": ast.literal_eval(instance.options),
            "searchable": instance.searchable,
            "parent": instance.parent.id if instance.parent else None,
            "question": instance.question.id if instance.question else None
        }


class ParticipantSerializer(serializers.ModelSerializer):
    basic_health_submitted = serializers.BooleanField(required=False)

    class Meta:
        model = Participant
        fields = ['id', 'email', 'basic_health_submitted']


class ParticipantBasicHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantBasicHealth
        fields = ['participant', 'sex', 'weight', 'height', 'birth_date']


class ParticipantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantResponse
        fields = ['question', 'participant', 'value']


class VirtualTrialParticipantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualTrialParticipantResponse
        fields = ['question', 'participant', 'value']


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class SponsorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorRequest
        fields = '__all__'


class SponsorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['organization', 'contactPerson', 'email']


class ClinicalTrialSerializer(serializers.ModelSerializer):
    recruitmentStartDate = serializers.DateField(format='%B %d, %Y', required=False)
    recruitmentEndDate = serializers.DateField(format='%B %d, %Y', required=False)
    partial = True
    sponsor = SponsorDetailSerializer(read_only=True)

    class Meta:
        model = ClinicalTrial
        fields = ['title', 'objective', 'id', 'sponsor', 'recruitmentStartDate',
                  'recruitmentEndDate', 'enrollmentTarget', 'description', 'url', 'current_recruitment', 'status',
                  'custom_id', 'is_virtual', 'location']


class ClinicalTrialMatchSerializer(serializers.ModelSerializer):
    clinical_trial = ClinicalTrialSerializer(read_only=True)

    class Meta:
        model = ClinicalTrialMatch
        fields = ['clinical_trial', 'expressed_interest', 'id']


class ClinicalTrialField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        pk = super(ClinicalTrialField, self).to_representation(value)
        try:
            item = ClinicalTrial.objects.get(pk=pk)
            serializer = ClinicalTrialSerializer(item)
            return serializer.data
        except ClinicalTrialEnrollment.DoesNotExist:
            return None

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        return OrderedDict([(item.id, str(item)) for item in queryset])


class ClinicalTrialEnrollmentSerializer(serializers.ModelSerializer):
    clinical_trial = ClinicalTrialField(queryset=ClinicalTrial.objects.all())

    class Meta:
        model = ClinicalTrialEnrollment
        fields = ['participant', 'clinical_trial']


class ClinicalTrialCriteriaResponseSerializer(serializers.ModelSerializer):
    clinical_trial = ClinicalTrialSerializer(read_only=True)

    class Meta:
        model = ClinicalTrialCriteriaResponse
        fields = '__all__'

    def to_representation(self, instance):
        if '[' in instance.value:
            value = ast.literal_eval(instance.value)
        else:
            value = instance.value

        return {
            "id": instance.id,
            "value": value,
            "criteriaType": instance.criteriaType,
            "comparison": instance.comparison,
            "negated": instance.negated,
            "criteria": {"id": instance.criteria.id,
                         "name": instance.criteria.name,
                         "valueType": instance.criteria.valueType},
            "trial": instance.trial.id
        }
