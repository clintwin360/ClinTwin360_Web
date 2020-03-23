from django.db import models
from django.contrib.postgres.fields import ArrayField
# New additions
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


class ClinicalTrial(models.Model):
    name = models.CharField(max_length=500)
    targetRecruitment = models.IntegerField()
    currentRecruitment = models.IntegerField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ClinicalTrialCriteria(models.Model):
    name = models.CharField(max_length=500)
    valueType = models.CharField(max_length=50)
    options = ArrayField(models.CharField(max_length=256))


class ClinicalTrialCriteriaResponse(models.Model):
    value = models.CharField(max_length=50)
    criteriaType = models.CharField(max_length=50)
    negated = models.BooleanField()


class QuestionCategory(models.Model):
    name = models.CharField(max_length=50)


class ParticipantQuestion(models.Model):
    text = models.TextField()
    valueType = models.CharField(max_length=50)
    options = ArrayField(models.CharField(max_length=256))
    categories = models.ManyToManyField(QuestionCategory)


class ParticipantQuestionResponse(models.Model):
    text = models.TextField()
    valueType = models.CharField(max_length=50)
    options = ArrayField(models.CharField(max_length=256))
    categories = models.ManyToManyField(QuestionCategory)

