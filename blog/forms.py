from django import forms
from .models import Article, Comments
from django_summernote.widgets import SummernoteWidget


class ArticleForm(forms.ModelForm):
    image = forms.ImageField(required=True, label="تصویر مقاله")

    class Meta:
        model = Article
        exclude = ("like", "views", "status", "updated_date", "created_date")

        widgets = {
            "author": forms.TextInput(),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "article-title",
                    "placeholder": "عنوان مقاله را وارد کنید",
                }
            ),
            "content": SummernoteWidget(),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "article-title",
                    "placeholder": "موضوع مقاله را وارد کنید",
                }
            ),
            "categorys": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                    "placeholder": "دسته بندی مقاله را انتخاب کنید",
                }
            ),
            "tags": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                }
            ),
            "read": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "زمان خواندن مقاله",
                    "inputmode": "numeric",
                }
            ),
            "search": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ادرس مقاله را وارد کنید",
                }
            ),
        }


class ArticleUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="تصویر مقاله")

    class Meta:
        model = Article
        exclude = ("author", "views", "status", "updated_date", "created_date")

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "article-title",
                    "placeholder": "عنوان مقاله را وارد کنید",
                }
            ),
            "content": SummernoteWidget(),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "article-title",
                    "placeholder": "موضوع مقاله را وارد کنید",
                }
            ),
            "categorys": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                    "placeholder": "دسته بندی مقاله را انتخاب کنید",
                }
            ),
            "tags": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                }
            ),
            "read": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "زمان خواندن مقاله",
                    "inputmode": "numeric",
                }
            ),
            "search": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ادرس مقاله را وارد کنید",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ("id", "status", "created_date")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام خود را وارد کنید",
                    "id": "name",
                    "type": "text",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "شماره تلفن خود را وارد کنید",
                    "id": "phone_number",
                    "type": "text",
                    "pattern": "[0-9]*",
                    "inputmode": "numeric",
                    "maxlength": 11,
                    "minlength": 11,
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "نظر خود را بنویسید",
                    "rows": 5,
                    "id": "comment",
                }
            ),
        }
