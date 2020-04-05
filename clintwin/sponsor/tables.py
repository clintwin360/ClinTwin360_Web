from django_tables2 import tables, TemplateColumn
from .models import ClinicalTrial

class ClinicalTrialTable(tables.Table):
    class Meta:
         model = ClinicalTrial
         template_name = "django_tables2/bootstrap.html"
         attrs = {'class': 'table table-sm'}
         fields = ['trialId', 'sponsor', 'title', 'recruitmentStartDate', 'recruitmentEndDate', 'enrollmentTarget', 'edit']
         
    #edit = TemplateColumn(template_name='sponsor/trial_view_column.html') # Throws NoReverseMatch error when rendering template 