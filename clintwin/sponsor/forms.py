from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ClinicalTrial
from bootstrap_datepicker_plus import DatePickerInput

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class NewTrialForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['name', 'targetRecruitment', 'startDate', 'endDate']

    name = forms.CharField(max_length=500)
    targetRecruitment = forms.IntegerField()
    startDate = forms.DateField()
    endDate = forms.DateField()
    widgets = {
             'startDate': DatePickerInput(format='%m/%d/%Y'),
             'endDate': DatePickerInput(format='%m/%d/%Y'),
         }


class NewSponsorForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['sponsor__name', 'information_provided_by']

    sponsor__name = forms.CharField(max_length=500)
    information_provided_by = forms.CharField(max_length=500)

"""	
class EditTrialModelForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['custom_id', 'title', 'objective', 'is_virtual', 'url', 'location', 'recruitmentStartDate', 'recruitmentEndDate', 'enrollmentTarget', 'description', 'comments', 'followUp']

    
    #targetRecruitment = forms.IntegerField()
    #recruitmentStartDate= formsDateField()
    #recruitmentEndDate = forms.DateField()
    #widgets = {
             #'recruitmentStartDate': DatePickerInput(format='%m/%d/%Y'),
             #'recruitmentEndDate': DatePickerInput(format='%m/%d/%Y'),
         #}
"""	

"""
widget=forms.Select(choices=TITLE_CHOICES)

class ContactForm(forms.ModelForm):
      class Meta:
            model = Contact
            fields = '__all__'
"""

"""
class CriteriaForm(forms.ModelForm):
    name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        criterias = TrialCriteria.objects.filter(
            trial=self.instance
        )
        for i in range(len(criterias) + 1):
            field_name = 'criteria_%s' % (i,)
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = criterias[i].criteria
            except IndexError:
                self.initial[field_name] = “”
        # create an extra blank field
        field_name = 'criteria_%s' % (i + 1,)
        self.fields[field_name] = forms.CharField(required=False)

    def clean(self):
        criterias = set()
        i = 0
        field_name = 'criteria_%s' % (i,)
        while self.cleaned_data.get(field_name):
           criteria = self.cleaned_data[field_name]
           if criteria in criterias:
               self.add_error(field_name, 'Duplicate')
           else:
               criterias.add(criteria)
           i += 1
           field_name = 'criteria_%s' % (i,)
       self.cleaned_data[“criterias”] = criterias

    def save(self):
        trial = self.instance
        trial.name = self.cleaned_data[“name”]


        trial.criteria_set.all().delete()
        for criteria in self.cleaned_data[“criterias”]:
           TrialCriteria.objects.create(
               trial=trial,
               criteria=criteria,
           )
    def get_criteria_fields(self):
    for field_name in self.fields:
        if field_name.startswith(‘criteria_’):
            yield self[field_name]
"""
