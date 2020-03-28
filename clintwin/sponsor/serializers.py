from .models import *
from rest_framework import serializers


class ParticipantQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantQuestion
        fields = ['id','text', 'valueType', 'options']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id','first_name', 'last_name', 'email']


class ParticipantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantResponse
        fields = ['question', 'participant', 'value']

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'
