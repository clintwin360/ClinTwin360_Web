from django.contrib import admin
from .models import *
from .forms import NewAccountForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

class UserAdmin(BaseUserAdmin):
    """
    A UserAdmin that sends a password-reset email when creating a new user,
    unless a password was entered.
    """
    add_form = NewAccountForm
    add_fieldsets = (
        (None, {
            'description': (
                "Enter the new user's name and email address and click save."
                " The user will be emailed a link allowing them to login to"
                " the site and set their password."
            ),
            'fields': ('email', 'name',),
        }),
        ('Password', {
            'description': "Optionally, you may set the user's password here.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change and not obj.has_usable_password():
            # Django's PasswordResetForm won't let us reset an unusable
            # password. We set it above super() so we don't have to save twice.
            obj.set_password(get_random_string())
            reset_password = True
        else:
            reset_password = False

        super(UserAdmin, self).save_model(request, obj, form, change)

        if reset_password:
            reset_form = PasswordResetForm({'email': obj.email})
            assert reset_form.is_valid()
            reset_form.save(
                subject_template_name='registration/account_creation_subject.txt',
                html_email_template_name='registration/account_creation_email.html',
            )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Register your models here.
admin.site.register(Participant)
admin.site.register(ParticipantBasicHealth)
admin.site.register(ParticipantResponse)
admin.site.register(ClinicalTrialCriteria)
admin.site.register(Sponsor)
admin.site.register(ClinicalTrial)
admin.site.register(ClinicalTrialCriteriaResponse)
admin.site.register(ParticipantQuestion)
admin.site.register(QuestionFlow)
admin.site.register(UserProfile)
admin.site.register(ClinicalTrialMatch)
admin.site.register(PushNotification)
admin.site.register(VirtualTrialParticipantQuestion)
admin.site.register(VirtualTrialParticipantResponse)
admin.site.register(Contact)
admin.site.register(SponsorRequest)

from signal import *
