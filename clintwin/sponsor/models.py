from django.db import models
#from django.contrib.postgres.fields import ArrayField
# New additions
from django.urls import reverse
from datetime import date
import datetime
from django.utils.timezone import now
from django.utils import timezone
# End of new additions

# Create your models here


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if (postData['first_name'].isalpha()) == False:
            if len(postData['first_name']) < 2:
                errors['first_name'] = "First name can not be shorter than 2 characters"

        if (postData['last_name'].isalpha()) == False:
            if len(postData['last_name']) < 2:
                errors['last_name'] = "Last name can not be shorter than 2 characters"

        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"

        if len(postData['password']) < 8:
            errors['password'] = "Password is too short!"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class Contact(models.Model):
    first_name = models.CharField(null=True, max_length=50)
    last_name = models.CharField(null=True, max_length=50)
    email = models.EmailField(null=True)
    comment = models.CharField(max_length=1000, null=True,)


class Sponsor(models.Model):
    organization = models.CharField('Organization Name', max_length=500, help_text='Name of Sponsor')
    date_joined = models.DateField('Date of Registration', null=True)
    dateDeregistered = models.DateField('Date of De-Regstration', null=True, blank=True)
    contactPerson = models.CharField('Contact Person', null=True, max_length=500)
    email = models.EmailField('Email', null=True)
    phone = models.CharField('Phone', null=True, max_length=20)
    location = models.CharField('Location', null=True, max_length=100)
    notes = models.TextField('Comments', null=True, blank=True)

    def __str__(self):
        ret = str(self.id) + ',' + self.organization
        return ret
    
	# New method
    def get_absolute_url(self):
        #Returns the url to access a detail record for the Sponsor.
        return reverse('sponsor-detail', args=[str(self.id)])
		
class SponsorRequest(models.Model):
    sponsor_id = models.CharField(max_length=50)
    criterion_req = models.CharField(null=True, max_length=200)
    values = models.CharField(null=True, max_length=500)
    notes = models.CharField(max_length=1000)


class ClinicalTrial(models.Model):
    trialId = models.CharField('Trial ID', max_length=30,primary_key=True)
    sponsor = models.ForeignKey('Sponsor', null=True, on_delete=models.SET_NULL)
    title = models.CharField('Trial Title', null=True, max_length=100)
    objective = models.TextField('Objective', null=True)
    description = models.TextField('Description', null=True, blank=True)
    recruitmentStartDate = models.DateField('Recruitment Start Date', null=True, help_text='MM/DD/YY')
    recruitmentEndDate = models.DateField('Recruitment End Date', null=True, help_text='MM/DD/YY')
    enrollmentTarget = models.IntegerField('Enrollment Target', null=True, blank=True)
    url = models.URLField('URL', null=True, blank=True)
    followUp = models.TextField('Followup Notes', null=True, blank=True)
    location = models.CharField('Location', null=True, max_length=100)
    comments = models.TextField('Comments', null=True, blank=True)
    createdTimeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = self.trialId + self.title
        return ret

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Clinical Trial.
        return reverse('clinicalTrial-detail', args=[str(self.trialId)])



class QuestionCategory(models.Model):
    name = models.CharField(max_length=50)


"""	OLD
class Participant(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)

    def name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.name()
"""

# NEW 
class Participant(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Lasst Name', max_length=50)
    gender=models.CharField('Gender', max_length=1, choices=GENDER)
    weight=models.FloatField('Weight')
    height=models.FloatField('Height')
    dateBirth=models.DateField('Date of Birth',help_text='MM/DD/YY',null=True, blank=True)
    date_joined= models.DateField('Date of Registration', help_text='MM/DD/YY',null=True, blank=True)
    date_deregistered=models.DateField('Date of De-Registration', help_text='MM/DD/YY',null=True, blank=True)
    email = models.EmailField('Email')
    phone= models.IntegerField('Phone')
    location=models.CharField('Location',max_length=100)
    last_login=models.DateTimeField(auto_now = True)

    def __str__(self):
        ret = self.first_name + ',' + self.last_name
        return ret

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Participant.
        return reverse('participant-detail', args=[str(self.id)])

class ClinicalTrialMatch(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='trial_matches')
    clinical_trial = models.ForeignKey(ClinicalTrial, on_delete=models.CASCADE, related_name='trial_matches')


class ParticipantQuestion(models.Model):
    text = models.TextField()
    valueType = models.CharField(max_length=50)
    #options = ArrayField(models.CharField(max_length=256))
    options = models.TextField()
    categories = models.ManyToManyField(QuestionCategory)

    def __str__(self):
        return self.text


class ParticipantResponse(models.Model):
    question = models.ForeignKey(ParticipantQuestion, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='responses')
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.question__text


class ClinicalTrialCriteria(models.Model):
    name = models.CharField(max_length=500)
    valueType = models.CharField(max_length=50)
    options = models.TextField()
    #options = ArrayField(models.CharField(max_length=256))
    searchable = models.BooleanField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='subcriteria')
    question = models.ForeignKey(ParticipantQuestion, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class ClinicalTrialCriteriaResponse(models.Model):
    criteria = models.ForeignKey(ClinicalTrialCriteria, on_delete=models.CASCADE, null=True)
    trial = models.ForeignKey(ClinicalTrial, on_delete=models.CASCADE, null=True, related_name='criteria')
    value = models.CharField(max_length=1024)
    comparison = models.CharField(max_length=50)
    criteriaType = models.CharField(max_length=50)
    negated = models.BooleanField()



# NEW		
class QuestionSchema (models.Model):
    questionText=models.TextField('Question Text',  null=True, blank=True)
    responseId=models.ForeignKey('ClinicalTrialCriteriaResponse', on_delete=models.SET_NULL, null=True)
    type=models.CharField('Type', max_length=50, null=True, blank=True)
    criteria=models.ForeignKey('ClinicalTrialCriteria',on_delete=models.SET_NULL, null=True)
    nextQuestion=models.CharField ('Next Question', max_length=30, null=True, blank=True)

    def __str__(self):
        ret = self.questionId
        return ret

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Question Schema.
        return reverse('questionSchema-detail', args=[str(self.id)])

