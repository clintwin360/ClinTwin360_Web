from datetime import date
from django.core.validators import URLValidator, validate_email, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import User
from django.db import models
# from django.contrib.postgres.fields import ArrayField
# New additions
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from push_notifications.models import APNSDevice
from .validators import *


# End of new additions

# Create your models here


def is_clintwin(self):
    return self.groups.filter(name='clintwin').exists()


def is_sponsor_admin(self):
    return self.groups.filter(name='sponsor_admin').exists()

def is_sponsor(self):
    return self.groups.filter(name='sponsor').exists()


def is_participant(self):
    return self.groups.filter(name='participant').exists()


User.add_to_class("is_clintwin", is_clintwin)
User.add_to_class("is_sponsor", is_sponsor)
User.add_to_class("is_participant", is_participant)
User.add_to_class("is_sponsor_admin", is_sponsor_admin)

class Contact(models.Model):
    organization = models.CharField('Organization Name', max_length=500)
    first_name = models.CharField(null=True, max_length=50)
    last_name = models.CharField(null=True, max_length=50)
    email = models.EmailField(null=True,validators= [validate_email])
    phone = PhoneNumberField(null=True)
    location = models.CharField('Location', null=True, max_length=100)
    comment = models.CharField(max_length=1000, null=True, )
    createdAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField('Status', null=True, max_length=100, default='Open')


class Sponsor(models.Model):
    organization = models.CharField('Organization Name', max_length=500)
    date_joined = models.DateField('Date of Registration', null=True, auto_now_add=True,validators= [validate_date])
    dateDeregistered = models.DateField('Date of De-Regstration', null=True, blank=True,validators= [validate_date])
    contactPerson = models.CharField('Contact Person', null=True, max_length=500)
    email = models.EmailField('Email', null=True,validators= [validate_email])
    phone = PhoneNumberField(null=True)
    location = models.CharField('Location', null=True, max_length=100)
    notes = models.TextField('Comments', null=True, blank=True)

    def __str__(self):
        ret = str(self.id) + ',' + self.organization
        return ret

    # New method
    def get_absolute_url(self):
        # Returns the url to access a detail record for the Sponsor.
        return reverse('sponsor-detail', args=[str(self.id)])


class SponsorRequest(models.Model):
    sponsor = models.ForeignKey(Sponsor, null=True, on_delete=models.CASCADE)
    criterion_req = models.CharField(null=True, max_length=200)
    values = models.CharField(null=True, max_length=500)
    notes = models.CharField(max_length=1000)
    status = models.CharField('Status', null=True, max_length=100, default='Open')
    createdAt = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    sponsor = models.ForeignKey(Sponsor, null=True, on_delete=models.SET_NULL, related_name='user_profiles')

    def __str__(self):
        ret = self.user.username + ":" + self.sponsor.organization
        return ret


class ClinicalTrial(models.Model):
    custom_id = models.CharField('Trial ID', max_length=100, null=True)
    sponsor = models.ForeignKey('Sponsor', null=True, on_delete=models.SET_NULL)
    title = models.CharField('Trial Title', null=True, max_length=500)
    objective = models.TextField('Objective', null=True)
    description = models.TextField('Description', null=True, blank=True)
    recruitmentStartDate = models.DateField('Recruitment Start Date', null=True)
    recruitmentEndDate = models.DateField('Recruitment End Date', null=True)
    enrollmentTarget = models.IntegerField('Enrollment Target', null=True, blank=True, validators=[MinValueValidator(0, "You can not enter a negative value")])
    url = models.URLField('URL', null=True, blank=True,validators=[URLValidator])
    followUp = models.TextField('Followup Notes', null=True, blank=True)
    location = models.CharField('Location', null=True, max_length=100)
    comments = models.TextField('Comments', null=True, blank=True)
    createdTimeStamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField('Status', null=True, max_length=100, default='Draft', validators= [validate_status])
    current_recruitment = models.IntegerField('Current Recruitment', default=0, null=True, blank=True, validators=[MinValueValidator(0, "You can not enter a negative value")])
    is_virtual = models.BooleanField('Virtual Trial', null=True, help_text='Do you plan to administer this trial online?')

    def __str__(self):
        ret = str(self.id) + ":" + self.title
        return ret

    def get_absolute_url(self):
        # Returns the url to access a detail record for the Clinical Trial.
        return reverse('clinicalTrial-detail', args=[str(self.id)])


class QuestionCategory(models.Model):
    name = models.CharField(max_length=50)


class Participant(models.Model):
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    email = models.EmailField(validators= [validate_email])
    date_joined = models.DateTimeField(auto_now_add=True, null=True,validators= [validate_date])
    phone = PhoneNumberField(null=True)
    location = models.CharField(null=True, max_length=100)
    last_login = models.DateTimeField(auto_now=True, null=True)
    basic_health = models.IntegerField(default=0, null=True)

    def name(self):
        return str(self.email)

    def __str__(self):
        return self.name()


class ParticipantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participant')
    participant = models.ForeignKey(Participant, null=True, on_delete=models.SET_NULL, related_name='participant_profiles')

    def __str__(self):
        ret = self.user.username + ":" + self.participant.email
        return ret


class ParticipantBasicHealth(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    participant = models.OneToOneField("Participant", on_delete=models.CASCADE)
    gender = models.CharField('Gender', max_length=1, null=True, choices=GENDER)
    weight = models.FloatField('Weight', null=True,validators=[MinValueValidator(0, "You can not enter a negative value")])
    height = models.FloatField('Height', null=True,validators=[MinValueValidator(0, "You can not enter a negative value")])
    birth_date = models.DateField('Date of Birth', help_text='MM/DD/YY', null=True, blank=True)

    def bmi(self):
        return 703 * (self.weight / (self.height * self.height))

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - \
               ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        return self.participant.name() + " Basic Health Info"


class ClinicalTrialMatch(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='trial_matches')
    clinical_trial = models.ForeignKey(ClinicalTrial, on_delete=models.CASCADE, related_name='trial_matches')
    match = models.BooleanField(null=True)
    expressed_interest = models.BooleanField(null=True)

    def __str__(self):
        return self.participant.name() + ":" + self.clinical_trial.title + ">>" + str(self.match)


class ClinicalTrialEnrollment(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='enrollments')
    clinical_trial = models.ForeignKey(ClinicalTrial, on_delete=models.CASCADE, related_name='enrollments')

    def __str__(self):
        return self.participant.name() + ":" + self.clinical_trial.title


class ParticipantQuestion(models.Model):
    text = models.TextField()
    valueType = models.CharField(max_length=50)
    # options = ArrayField(models.CharField(max_length=256))
    options = models.TextField()
    categories = models.ManyToManyField(QuestionCategory)

    def __str__(self):
        return self.text


class VirtualTrialParticipantQuestion(models.Model):
    clinical_trial = models.ForeignKey(ClinicalTrial, on_delete=models.CASCADE, related_name='virtual_questions')
    text = models.TextField()
    valueType = models.CharField(max_length=50)
    # options = ArrayField(models.CharField(max_length=256))
    options = models.TextField()

    # categories = models.ManyToManyField(QuestionCategory)

    def __str__(self):
        return self.text


class QuestionFlow(models.Model):
    question = models.ForeignKey(ParticipantQuestion, on_delete=models.CASCADE, related_name='question_flow')
    response = models.CharField(max_length=128)
    next_question = models.ForeignKey(ParticipantQuestion, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.question.text + ">>>" + self.response + ">>>" + self.next_question.text


class ParticipantResponse(models.Model):
    question = models.ForeignKey(ParticipantQuestion, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='responses')
    value = models.CharField(max_length=50)
    last_answered = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.question.text

    class Meta:
        unique_together = ('question', 'participant')


class VirtualTrialParticipantResponse(models.Model):
    question = models.ForeignKey(VirtualTrialParticipantQuestion, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='virtual_responses')
    value = models.CharField(max_length=50)
    answered_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.question.text



class ClinicalTrialCriteria(models.Model):
    name = models.CharField(max_length=500)
    valueType = models.CharField(max_length=50)
    options = models.TextField()
    # options = ArrayField(models.CharField(max_length=256))
    searchable = models.BooleanField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='subcriteria')
    question = models.ForeignKey(ParticipantQuestion, on_delete=models.CASCADE, null=True, related_name="criteria")

    def __str__(self):
        return self.name


class ClinicalTrialCriteriaResponse(models.Model):
    criteria = models.ForeignKey(ClinicalTrialCriteria, on_delete=models.CASCADE, null=True,
                                 related_name='trial_responses')
    trial = models.ForeignKey(ClinicalTrial, on_delete=models.CASCADE, null=True, related_name='criteria')
    value = models.CharField(max_length=1024)
    comparison = models.CharField(max_length=50)
    criteriaType = models.CharField(max_length=50)
    negated = models.BooleanField()


# Code to send push notifications
class PushNotification(models.Model):
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    sendResponse = models.CharField(max_length=1024, null=True, blank=True)
    createdTimeStamp = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=PushNotification)
def send_new_message_notification(sender, **kwargs):
    message = kwargs['instance']
    r = send_new_message_push_notification(recipient=message.recipient,
                                           content=message.content)
    message.sendResponse = r
    post_save.disconnect(send_new_message_notification, sender=PushNotification)
    message.save()
    post_save.connect(send_new_message_notification, sender=PushNotification)


def send_new_message_push_notification(**kwargs):
    content = kwargs.get("content")

    device = APNSDevice.objects.filter(name=kwargs.get("recipient").username)
    if not device:
        return 'Unable to retrieve a device for the user!'
    else:
        return device.send_message(content)

# End code to send push notifications
