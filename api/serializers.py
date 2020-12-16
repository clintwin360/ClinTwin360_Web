from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from sponsor.models import Participant

from sponsor.models import ParticipantProfile

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['email'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        # Assign the participant group to the user
        try:
            g = Group.objects.get(name='participant')
            g.user_set.add(user)
        except Group.DoesNotExist:
            print('Group Participant does not exists')
            pass

        # Create a Participant object for the new user
        participant = Participant.objects.create(
            email=validated_data['email']
        )
        participant.save()

        participant_profile = ParticipantProfile.objects.create(
            user=user,
            participant=participant
        )
        participant_profile.save()

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ("password", "email")

