from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
import re

# class ProEssentialsForm(forms.Form):
#
#   def addError(self, message):
#     self._errors[NON_FIELD_ERRORS] = self.error_class([message])
#
# class SignInForm(ProEssentialsForm):
#     username = forms.CharField(required=True, max_length=20)
#     password = forms.CharField(required = True, widget = forms.PasswordInput(render_value = False))
#
# class CardForm(ProEssentialsForm):
#   last_4_digits = forms.CharField(required = True, min_length = 4, max_length = 4, widget = forms.HiddenInput())
#   stripe_token = forms.CharField(required = True, widget = forms.HiddenInput())
#
# class UserForm(CardForm):
#     first_name = forms.CharField(label='Name')
#     last_name = forms.CharField()
#     email = forms.EmailField()
#     username = forms.CharField()
#     password = forms.CharField(max_length=32, widget=forms.PasswordInput)
#     repassword = forms.CharField(max_length=32, widget=forms.PasswordInput, label="Re-enter Password")
#
#     def clean_first_name(self):
#         first_name = self.cleaned_data['first_name']
#         num_words = len(first_name.split())
#         first_name_re = re.compile(r"[a-zA-Z-']")
#         if num_words > 2:
#             raise forms.ValidationError("First name should not have more than two words.")
#         if not(first_name_re.match(first_name)):
#             raise forms.ValidationError("Name should include letters, hyphens and apostrophes.")
#         return first_name
#
#     def clean_last_name(self):
#         last_name = self.cleaned_data['last_name']
#         num_words = len(last_name.split())
#         last_name_re = re.compile(r"[a-zA-Z-']")
#         if num_words > 2:
#             raise forms.ValidationError("Last name should not have more than two words.")
#         if not(last_name_re.match(last_name)):
#             raise forms.ValidationError("Name should include letters, hyphens and apostrophes.")
#         return last_name
#
#     def clean_password(self):
#         password = self.cleaned_data['password']
#         pass_re = re.compile(r"[a-zA-Z0-9_-]")
#         if not(pass_re.match(password)):
#             raise forms.ValidationError("Only enter alphanumeric characters, underscores, and dashes.")
#         return password
#
#     def clean_repassword(self):
#         repassword = self.cleaned_data['repassword']
#         if not(self.cleaned_data.get('password')):
#             raise forms.ValidationError("You didn't enter a valid original password.")
#         else:
#             password = self.cleaned_data['password']
#             if repassword != password:
#                 raise forms.ValidationError("The passwords did not match.")
#         return repassword
#     """
#     Its pretty intuitive and is similar to the models syntax.
#     Django's form system automatically looks for any method whose name starts with "clean_"
#     and ends with the name of a field. If any such method exists, it's called during validation.
#
#     """
#
#
#