# from django import forms
# from .models import CsvBulkUpload

# class CsvBulkUploadForm(forms.ModelForm):
#   class Meta:
#     model = CsvBulkUpload
#     fields = ("csv_file",)

from django import forms
from .models import Csv

class CsvForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('file_name',)