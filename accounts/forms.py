from django import forms
from .models import Teacher, Grade, Comment
from django.core import validators
from home.models import ContactUs
from django_summernote.widgets import SummernoteWidget


# def start_with_0(value):
#     if value[:2] != "09":
#         raise forms.ValidationError()


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام کاربری خود را وارد نمایید",
            }
        ),
    )
    full_name = forms.CharField(
        label="نام و نام خانوادگی",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام و نام خانوادگی خود را وارد نمایید",
            }
        ),
    )
    phone_number = forms.CharField(
        label="شماره موبایل",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "شماره موبایل خود را وارد نمایید",
                "pattern": "[0-9]*",
                "inputmode": "numeric",
            }
        ),
        max_length=11,
    )
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز خود را وارد نمایید"}
        ),
        validators=[validators.MinLengthValidator(8)],
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "تکرار رمز خود را وارد نمایید",
            }
        ),
        validators=[validators.MinLengthValidator(8)],
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number[:2] != "09":
            raise forms.ValidationError("شماره باید با 09 شروع بشود")
        return phone_number


class LoginForm(forms.Form):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": " نام کاربری خود را وارد نمایید",
            }
        ),
        max_length=250,
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز عبور خود را وارد نمایید",
            }
        ),
        validators=[validators.MinLengthValidator(8)],
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        label="مرا به خاطر بسپار",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
    )


class ScoreUpdateForm(forms.ModelForm):

    # تعریف choices به عنوان متغیر کلاس
    STATUS_CHOICES = [
        ("", "انتخاب وضعیت"),
        ("average", "متوسط"),
        ("good", "خوب"),
        ("great", "عالی"),
    ]

    MONTH_CHOICES = [
        ("", "انتخاب ماه"),
        ("مهر", "مهر"),
        ("آبان", "آبان"),
        ("آذر", "آذر"),
        ("دی", "دی"),
        ("بهمن", "بهمن"),
        ("اسفند", "اسفند"),
        ("فروردین", "فروردین"),
        ("اردیبهشت", "اردیبهشت"),
        ("خرداد", "خرداد"),
    ]

    # استفاده از فرم فیلدهای خاص
    score = forms.FloatField(
        label="نمره جدید",
        min_value=0,
        max_value=20,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "مثال: ۱۷.۵",
                "step": "0.25",
                "required": "required",
            }
        ),
        help_text="نمره باید بین ۰ تا ۲۰ باشد (می‌تواند اعشاری باشد)",
    )

    class_activity = forms.FloatField(
        label="نمره کلاسی (اختیاری)",
        required=False,
        min_value=0,
        max_value=20,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "مثال: ۱۸.۲۵",
                "step": "0.25",
            }
        ),
        help_text="نمره فعالیت کلاسی (بین ۰ تا ۲۰)",
    )

    month = forms.ChoiceField(
        label="ماه تحصیلی",
        choices=MONTH_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        ),
        help_text="ماه مربوط به نمره را انتخاب کنید",
    )

    status = forms.ChoiceField(
        label="وضعیت نمره",
        choices=STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        ),
        help_text="وضعیت کلی نمره را تعیین کنید",
    )

    class Meta:
        model = Grade
        fields = ["score", "class_activity", "month", "status"]

    def clean_score(self):
        score = self.cleaned_data.get("score")
        if score < 0 or score > 20:
            raise forms.ValidationError("نمره باید بین ۰ تا ۲۰ باشد.")
        return score

    def clean_class_activity(self):
        class_activity = self.cleaned_data.get("class_activity")
        if class_activity is not None:
            if class_activity < 0 or class_activity > 20:
                raise forms.ValidationError("نمره کلاسی باید بین ۰ تا ۲۰ باشد.")
        return class_activity


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز عبور فعلی خود را وارد نمایید",
            }
        ),
        validators=[
            validators.MinLengthValidator(8),
            validators.RegexValidator(
                regex=r'^[A-Za-z0-9@#$%^&+=!*()\-_\[\]{};:\'",.<>/?\\|`~]*$',
                message="Password must contain only English letters, numbers and special characters",
                code="invalid_password",
            ),
        ],
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز عبور جدید خود را وارد نمایید",
            }
        ),
        validators=[
            validators.MinLengthValidator(8),
            validators.RegexValidator(
                regex=r'^[A-Za-z0-9@#$%^&+=!*()\-_\[\]{};:\'",.<>/?\\|`~]*$',
                code="invalid_password",
            ),
        ],
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "تکرار رمز عبور را وارد نمایید",
            }
        ),
        validators=[
            validators.MinLengthValidator(8),
            validators.RegexValidator(
                regex=r'^[A-Za-z0-9@#$%^&+=!*()\-_\[\]{};:\'",.<>/?\\|`~]*$',
                code="invalid_password",
            ),
        ],
    )


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        exclude = ("created_date", "read")
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام و نام خانوادگی خود را وارد نمایید.",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "شماره تلفن خود را وارد نمایید",
                    "pattern": "[0-9]*",
                    "inputmode": "numeric",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "پیام خود را وارد نمایید",
                }
            ),
        }


class EditTeacherForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="تصویر")

    class Meta:
        model = Teacher
        exclude = ("created_date", "updated_date", "user")

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "article-title",
                    "placeholder": "نام و نام خانوادگی خود را وارد نمایید",
                }
            ),
            "full_name_en": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "article-title",
                    "placeholder": "نام خود را به انگلیسی وارد نماییید",
                }
            ),
            "description": SummernoteWidget(),
            "teaching_experience": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "سابقه کاری"}
            ),
            "degree": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "article-title",
                    "placeholder": "مدرک تحصیلی",
                }
            ),
        }


class ParentCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ("id", "created_date", "status")

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "parentName",
                    "placeholder": "نام و نام خانوادگی خود را وارد نمایید",
                }
            ),
            "name_st": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "studentName",
                    "placeholder": "نام فرزند خود را وارد نمایید",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "parentPhone",
                    "inputmode": "numeric",
                    "pattern": "[0-9]*",
                    "maxlength": 11,
                    "placeholder": "شماره تلفن خود را وارد نمایید",
                }
            ),
            "subject": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "accountType",
                    "placeholder": "موضوع نظر خود را وارد نمایید",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "feedbackMessage",
                    "placeholder": "نظرات، پیشنهادات و انتقادات خود را در این قسمت بنویسید...",
                }
            ),
        }
