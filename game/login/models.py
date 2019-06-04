from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
# Create your models here.

class OwnRegisterForm(UserCreationForm):
    def clean(self):
      cleaned_data = super(UserCreationForm, self).clean()
      if not self.isEnglish(self.cleaned_data.get("username")): 
          raise ValidationError('Only latin letters are allowed.')
      return cleaned_data

    @staticmethod
    def isEnglish(s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True