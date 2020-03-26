from .models import *
from rest_framework import serializers


class ParticipantQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParticipantQuestion
        fields = ['id','text', 'valueType', 'options']


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Participant
        fields = ['id','first_name', 'last_name', 'email']


class ParticipantResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParticipantResponse
        fields = ['question', 'participant', 'value']

