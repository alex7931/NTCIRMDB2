#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

# sex_choices = (
    # ('sex', u'Gender'),
    # ('male', u'Male'),
    # ('female', u'Female'),
# )

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'username',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'password',
            }
        )
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        required=True,
        min_length=6,
        label=u'username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'username (e.g.: user01, user02, etc.)',
            }
        )
    )
    password = forms.CharField(
        required=True,
        min_length=6,
        label=u'password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'password',
            }
        )
    )
    password_retype = forms.CharField(
        required=True,
        min_length=6,
        label=u'Please re-enter the password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'password again',
            }
        )
    )
    email = forms.EmailField(
        required=True,
        label=u'email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'email address',
            }
        )
    )
    # sex = forms.ChoiceField(
    #     required=True,
    #     choices=sex_choices,
    #     label=u'gender',
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'select2-container form-control select select-primary',
    #         }
    #     )
    # )
    # search_frequency = forms.ChoiceField(
    #     required=True,
    #     choices=search_frequency_choices,
    #     label=u'搜索引擎使用频率',
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'select2-container form-control select select-primary',
    #         }
    #     )
    # )


    name = forms.CharField(
        required=True,
        label=u'Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'your name',
            }
        )
    )
    age = forms.IntegerField(
        required=True,
        label=u'age',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'age',
            }
        )
    )

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        password_retype = cleaned_data.get('password_retype')

        if password != password_retype:
            raise forms.ValidationError(
                u'Please re-enter the password'
            )

        return cleaned_data


class EditInfoForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label=u'email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'email',
            }
        )
    )
    # sex = forms.ChoiceField(
    #     required=True,
    #     choices=sex_choices,
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'select2-container form-control select select-primary'
    #         }
    #     )
    # )

    age = forms.IntegerField(
        required=True,
        label=u'age',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'Age',
            }
        )
    )



class EditPasswordForm(forms.Form):

    cur_password = forms.CharField(
        required=True,
        min_length=6,
        label=u'current password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'original password',
            }
        )
    )
    new_password = forms.CharField(
        required=True,
        min_length=6,
        label=u'new password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'new password',
            }
        )
    )
    new_password_retype = forms.CharField(
        required=True,
        min_length=6,
        label=u'Please re-enter the password ',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'Please re-enter the password ',
            }
        )
    )

    def clean(self):
        cleaned_data = super(EditPasswordForm, self).clean()
        password = cleaned_data.get('new_password')
        password_retype = cleaned_data.get('new_password_retype')

        if password != password_retype:
            raise forms.ValidationError(
                u'The password did not match the re-typed password'
            )

        return cleaned_data


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label=u'email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'input email',
            }
        )
    )


class ResetPasswordForm(forms.Form):

    new_password = forms.CharField(
        required=True,
        min_length=6,
        label=u'new password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'password',
            }
        )
    )
    new_password_retype = forms.CharField(
        required=True,
        min_length=6,
        label=u'Please re-enter the password ',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-field',
                'placeholder': u'Please re-enter the password ',
            }
        )
    )

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password = cleaned_data.get('new_password')
        password_retype = cleaned_data.get('new_password_retype')

        if password != password_retype:
            raise forms.ValidationError(
                u'The password did not match the re-typed password'
            )

        return cleaned_data