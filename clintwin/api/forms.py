from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
"""
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
