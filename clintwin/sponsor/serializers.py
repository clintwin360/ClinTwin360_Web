from .models import *
from rest_framework import serializers


class ParticipantQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParticipantQuestion
        fields = ['text', 'valueType', 'options']