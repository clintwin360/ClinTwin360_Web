from django.db import models
#from django.contrib.postgres.fields import ArrayField
# New additions
from django.urls import reverse
from datetime import date
import datetime
from django.utils.timezone import now
from django.utils import timezone
# End of new additions

# Create your models he

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
    email = models.EmailField()
    comment = models.CharField(max_length=1000)

class Sponsor(models.Model):
    sponsor_id= models.CharField('Sponsor ID', max_length=30,primary_key=True, help_text='Unique Sponsor ID')
    organization = models.CharField('Organization Name', max_length=50, help_text='Name of Sponsor')
    date_joined= models.DateField('Date of Registration')
    dateDeregistered=models.DateField('Date of De-Regstration', null=True, blank=True)
    contactPerson=models.CharField('Contact Person', max_length=50)
    email = models.EmailField('Email')
    phone= models.IntegerField('Phone')
    location=models.CharField('Location',max_length=100)
    notes = models.TextField('Comments', null=True, blank=True)

    def __str__(self):
        ret = self.sponsor_id + ',' + self.organization
        return ret

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Sponsor.
        return reverse('sponsor-detail', args=[str(self.sponsor_id)])

class SponsorRequest(models.Model):
    sponsor_id = models.CharField(max_length=50)
    criterion_req = models.CharField(null=True, max_length=200)
    values = models.CharField(null=True, max_length=500)
    notes = models.CharField(max_length=1000)


class ClinicalTrial(models.Model):
    trialId = models.CharField('Trial ID', max_length=30,primary_key=True)
    sponsorId = models.ForeignKey('Sponsor', on_delete=models.SET_NULL, null=True)
    title=  models.CharField('Trial Title', max_length=100)
    objective = models.CharField('Objective', max_length=100)
    recruitmentStartDate= models.DateField('Recruitment Start Date', help_text='MM/DD/YY')
    recruitmentEndDate= models.DateField('Recruitment End Date', help_text='MM/DD/YY')
    enrollmentTarget= models.IntegerField('Enrollment Target',null=True, blank=True)
    url=models.URLField('URL', null=True,blank=True)
    followUp= models.TextField('Followup Notes',null=True, blank=True)
    location=  models.CharField('Location',max_length=100)
    comments = models.TextField('Comments', null=True, blank=True)
    createdTimeStamp=models.DateTimeField(auto_now_add = True)

    def __str__(self):
        ret = self.trialId + self.title
        return ret

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Clinical Trial.
        return reverse('clinicalTrial-detail', args=[str(self.trialId)])


class ClinicalTrialCriteriaResponse(models.Model):
    value = models.CharField(max_length=50)
    criteriaType = models.CharField(max_length=50)
    negated = models.BooleanField()


class QuestionCategory(models.Model):
    name = models.CharField(max_length=50)

class Participant(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)

    def name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.name()


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
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.question__text


"""

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
    first_name = models.CharField(null=True,max_length=50)
    last_name = models.CharField(null=True,max_length=50)
    organization=models.CharField(null=True,max_length=50)
    email = models.EmailField()
    comment = models.TextField


class Sponsor(models.Model):
    sponsorId= models.CharField('Sponsor ID', max_length=30,primary_key=True, help_text='Unique Sponsor ID')
    OrganizationName = models.CharField('Organization Name', max_length=50, help_text='Name of Sponsor')
    dateRegistered= models.DateField('Date of Registration')
    dateDeregistered=models.DateField('Date of De-Regstration', null=True, blank=True)
    contactPerson=models.CharField('Contact Person', max_length=50)
    email = models.EmailField('Email')
    phone= models.IntegerField('Phone')
    location=models.CharField('Location',max_length=100)

    def __str__(self):
        ret = self.sponsorId + ',' + self.OrganizationName
        return ret

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Sponsor.
        return reverse('sponsor-detail', args=[str(self.sponsorId)])


class Participant(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    participantId= models.CharField('Participant ID', max_length=30,primary_key=True)
    firstName = models.CharField('First Name', max_length=50)
    lastName = models.CharField('Lasst Name', max_length=50)
    gender=models.CharField('Gender', max_length=1, choices=GENDER)
    weight=models.FloatField('Weight')
    height=models.FloatField('Height')
    dateBirth=models.DateField('Date of Birth',help_text='MM/DD/YY')
    dateRegistered= models.DateField('Date of Registration', help_text='MM/DD/YY')
    dateDeregistered=models.DateField('Date of De-Registration', help_text='MM/DD/YY',null=True, blank=True)
    email = models.EmailField('Email')
    phone= models.IntegerField('Phone')
    location=models.CharField('Location',max_length=100)
    lastLogin=models.DateTimeField(auto_now = True)

    def __str__(self):
        ret = self.participantId + ',' + self.firstName + ',' + self.lastName
        return ret

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Participant.
        return reverse('participant-detail', args=[str(self.participantId)])



class Criteria (models.Model):
    criteriaId=models.CharField('Criteria ID', max_length=30,primary_key=True)
    name=models.CharField('Criteria Name',max_length=50)
    value=models.CharField('Criteria Value', max_length=50)
    valueType=models.CharField('Criteria Type', max_length=50)

    def __str__(self):
        ret = self.criteriaId + ',' + self.name
        return ret

    def get_absolute_url(self):
        Returns the url to access a detail record for the Criteria.

        return reverse('criteria-detail', args=[str(self.criteriaId)])

class Categories (models.Model):
    categoryId=models.CharField('Category ID', max_length=30,primary_key=True)
    name=models.CharField('Category Name', max_length=50)
    value=models.CharField('Category Value',max_length=50)
    valueType=models.CharField('Value Type',max_length=50)

    def __str__(self):
        ret = self.categoryId + ',' + self.name
        return ret

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Category.
        return reverse('category-detail', args=[str(self.categoryId)])


class ClinicalTrial(models.Model):
    trialId = models.CharField('Trial ID', max_length=30,primary_key=True)
    sponsorId = models.ForeignKey('Sponsor', on_delete=models.SET_NULL, null=True)
    title=  models.CharField('Trial Title', max_length=100)
    objective = models.CharField('Objective', max_length=100)
    recruitmentStartDate= models.DateField('Recruitment Start Date', help_text='MM/DD/YY')
    recruitmentEndDate= models.DateField('Recruitment End Date', help_text='MM/DD/YY')
    enrollmentTarget= models.IntegerField('Enrollment Target',null=True, blank=True)
    inclusionCriteria= models.CharField('Inclusion Criteria', max_length=100,null=True, blank=True)
    exclusionCriteria= models.CharField('Exclusion Criteria', max_length=100,null=True, blank=True)
    url=models.URLField('URL', null=True,blank=True)
    followUp= models.TextField('Followup Notes',null=True, blank=True)
    location=  models.CharField('Location',max_length=100)
    comments = models.TextField('Comments', null=True, blank=True)
    createdTimeStamp=models.DateTimeField(auto_now_add = True)

    def __str__(self):
        ret = self.trialId + self.title
        return ret

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Clinical Trial.
        return reverse('clinicalTrial-detail', args=[str(self.trialId)])


class ClinicalTrialCriteriaResponse (models.Model):
    responseId=models.CharField('Response ID',max_length=30,primary_key=True)
    trialId=models.ForeignKey('ClinicalTrial', on_delete=models.SET_NULL, null=True)
    value=models.CharField('Value',max_length=50)

    def __str__(self):
        ret = self.responseId + ',' + self.trialId + ',' + self.value
        return

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Trial response.
        return reverse('trialResponse-detail', args=[str(self.responseId)])

class QuestionSchema (models.Model):
    questionId=models.CharField('Question ID',max_length=30,primary_key=True)
    questionText=models.TextField('Question Text',  null=True, blank=True)
    responseId=models.ForeignKey('ClinicalTrialCriteriaResponse', on_delete=models.SET_NULL, null=True)
    type=models.CharField('Type', max_length=50, null=True, blank=True)
    categories=models.ForeignKey('Categories',on_delete=models.SET_NULL, null=True)
    nextQuestion=models.CharField ('Next Question', max_length=30, null=True, blank=True)

    def __str__(self):
        ret = self.questionId
        return ret

    def get_absolute_url(self):
        #Returns the url to access a detail record for the Question Schema.
        return reverse('questionSchema-detail', args=[str(self.questionId)])
"""
