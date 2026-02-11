from django import forms
from accounts.models import TeacherContact


class TeacherContactForm(forms.ModelForm):
    class Meta:
        model = TeacherContact
        exclude = ("created_date",)

        widgets = {
            "student_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "article-title",
                    "placeholder": "نام و نام خانوادگی خود را وارد کنید",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "article-title",
                    "placeholder": "موضوع پیام را وارد کنید",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "messageContent",
                    "placeholder": "متن پیام خود را بنویسید...",
                }
            ),
        }
