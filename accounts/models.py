from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from django.core.validators import MinValueValidator, MaxValueValidator


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):

        if not username:
            raise ValueError(_("The username must be set"))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_user", False)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    custom User model for our app
    """

    username = models.CharField(max_length=250, unique=True, verbose_name="نام کاربری")
    is_superuser = models.BooleanField(
        default=False, verbose_name="ادمین"
    )  # میتونه پنل رو ببینه
    is_teacher = models.BooleanField(default=False, verbose_name="معلم")
    is_staff = models.BooleanField(default=False, verbose_name="مدیر")  # اصلی
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_student = models.BooleanField(default=False, verbose_name="دانش اموز")
    is_parents = models.BooleanField(default=False, verbose_name="والدین")
    is_user = models.BooleanField(default=True, verbose_name="کاربر")
    created_date = jmodels.jDateTimeField(auto_now_add=True)
    updated_date = jmodels.jDateTimeField(auto_now=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        ordering = ("-id",)
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"

    def __str__(self):
        return self.username


class ProfileAdmin(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profiles", verbose_name="کاربر"
    )
    first_name = models.CharField(max_length=250, default="کاربر", verbose_name="نام")
    last_name = models.CharField(max_length=250, verbose_name="نام خانوادگی")
    image = models.ImageField(
        upload_to="profiles", blank=True, null=True, verbose_name="تصویر"
    )
    description = models.TextField(verbose_name="توضیحات")
    role = models.CharField(max_length=250, verbose_name="نقش")
    created_date = jmodels.jDateField(auto_now_add=True)
    updated_date = jmodels.jDateField(auto_now=True)

    class Meta:
        verbose_name = "ادمین"
        verbose_name_plural = "ادمین ها"

    def __str__(self):
        return self.user.username


class NewUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="newusers", verbose_name="کاربر"
    )
    full_name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی")
    phone_number = models.CharField(max_length=11, verbose_name="شماره تلفن")
    created_date = jmodels.jDateField(auto_now_add=True)

    class Meta:
        verbose_name = "کاربر جدید"
        verbose_name_plural = "کاربرهای جدید"

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="teachers", verbose_name="کاربر"
    )
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    full_name_en = models.CharField(
        max_length=250, verbose_name="نام و نام خانوادگی به انگلیسی", unique=True
    )
    image = models.ImageField(
        upload_to="teacher", verbose_name="عکس", null=True, blank=True
    )
    description = models.TextField(verbose_name="توضیحات")
    degree = models.CharField(max_length=250, verbose_name="مدرک")
    teaching_experience = models.IntegerField(default=0, verbose_name="سابقه دریس")
    status = models.BooleanField(default=False, verbose_name='نمره گذاشتن')
    created_date = jmodels.jDateField(auto_now_add=True, verbose_name="زمان ثبت")
    updated_date = jmodels.jDateField(auto_now=True, verbose_name="زمان اپدیت")

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ("-id",)
        verbose_name = "معلم"
        verbose_name_plural = "معلم ها"


class TeacherContact(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="teachercontacts",
        verbose_name="معلم",
    )
    student = models.ForeignKey(
        "Student",
        on_delete=models.CASCADE,
        related_name="teachercontacts",
        verbose_name="دانش اموز",
    )
    student_name = models.CharField(max_length=250, verbose_name="نام دانش اموز")
    subject = models.CharField(max_length=250, verbose_name="موضوع پیام")
    message = models.TextField(verbose_name="متن پیام")

    created_date = jmodels.jDateField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "پیام معلم"
        verbose_name_plural = "پیام های معلم"

    def __str__(self):
        return self.teacher.full_name


class Parents(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="parents", verbose_name="کاربر"
    )
    first_name = models.CharField(max_length=250, verbose_name="نام")
    last_name = models.CharField(max_length=250, verbose_name="نام خانوادگی")
    child = models.ManyToManyField(
        "Student", related_name="parents", verbose_name="فرزند ها"
    )
    created_date = jmodels.jDateField(auto_now_add=True, verbose_name="زمان ثبت")
    updated_date = jmodels.jDateField(auto_now=True, verbose_name="زمان اپدیت")

    class Meta:
        ordering = ("-id",)
        verbose_name = "والدین"
        verbose_name_plural = "والدین"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="students", verbose_name="کاربر"
    )
    grades = {
        "هفتم": "هفتم",
        "هشتم": "هشتم",
        "نهم": "نهم",
        "دهم کامپیوتر": "دهم کامپیوتر",
        "دهم حسابداری": "دهم حسابداری",
        "یازدهم کامپیوتر": "یازدهم کامپیوتر",
        "یازدهم حسابداری": "یازدهم حسابداری",
        "دوازدهم کامپیوتر": "دوازدهم کامپیوتر",
        "دوازدهم حسابداری": "دوازدهم حسابداری",
    }

    first_name = models.CharField(max_length=250, verbose_name="نام")
    last_name = models.CharField(max_length=250, verbose_name="نام خانوادگی")
    grade = models.CharField(
        choices=grades, default="دهم کامپیوتر", verbose_name="پایه‌ی تحصیلی"
    )
    created_date = jmodels.jDateField(auto_now_add=True, verbose_name="زمان ثبت")
    updated_date = jmodels.jDateField(auto_now=True, verbose_name="زمان اپدیت")

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.get_grade_display()}"

    class Meta:
        ordering = ("-id",)
        verbose_name = "دانش آموز"
        verbose_name_plural = "دانش آموزان"


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser != True:
            if instance.is_user:
                NewUser.objects.create(user=instance)
            elif instance.is_teacher:
                Teacher.objects.create(user=instance)
            elif instance.is_student:
                Student.objects.create(user=instance)
            elif instance.is_parents:
                Parents.objects.create(user=instance)

        else:

            ProfileAdmin.objects.create(user=instance)


class Comment(models.Model):
    subjects = {
        "School facilities": "امکانات مدرسه",
        "teaching method": "روش تدریس",
        "behavior": "رفتار معلمان",
        "other": "سایر",
    }
    user = models.ForeignKey(
        Parents,
        on_delete=models.CASCADE,
        related_name="comments_Parents",
        verbose_name="والدین",
    )
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    name_st = models.CharField(max_length=250, verbose_name="نام دانش اموز")
    phone_number = models.CharField(max_length=11, verbose_name="شماره موبایل")
    subject = models.CharField(
        max_length=250, verbose_name="موضوع", choices=subjects, default="other"
    )
    comment = models.TextField(verbose_name="نظر شما")
    status = models.BooleanField(default=False, verbose_name="وضعیت")
    show = models.BooleanField(default=False, verbose_name="نمایش")

    created_date = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return self.full_name


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم درس")
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="lessons", verbose_name="معلم"
    )
    student = models.ManyToManyField(
        Student, related_name="lessons", verbose_name="دانش اموزان"
    )
    grade = models.CharField(max_length=200, verbose_name="پایه تحصیلی")
    year = models.CharField(max_length=200, verbose_name="سال تحصیلی")

    class Meta:
        ordering = ("-id",)
        verbose_name = "درس"
        verbose_name_plural = "درس ها"

    def __str__(self):
        return self.name


class Grade(models.Model):
    months = {
        "فروردین": "فروردین",
        "اردیبهشت": "اردیبهشت",
        "خرداد": "خرداد",
        "مهر": "مهر",
        "آبان": "آبان",
        "آذر": "آذر",
        "دی": "دی",
        "بهمن": "بهمن",
        "اسفند": "اسفند",
    }
    status_dict = {"average": "متوسط", "good": "خوب", "great": "عالی"}
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="grades",
        verbose_name="دانش آموز",
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="درس", related_name="grades"
    )
    month = models.CharField(choices=months, default="مهر", verbose_name="ماه")
    score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(20.0)],
        verbose_name="نمره",
        help_text="نمره باید بین ۰ تا ۲۰ باشد",
    )
    class_activity = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(20.0)],
        verbose_name="فعالیت کلاسی",
        help_text="نمره فعالیت کلاسی باید بین ۰ تا ۲۰ باشد",
    )
    status = models.CharField(
        max_length=250, choices=status_dict, default="good", verbose_name="وضعیت"
    )
    created_date = jmodels.jDateField(auto_now_add=True)
    updated_date = jmodels.jDateField(auto_now=True, verbose_name="بروزرسانی")

    class Meta:
        ordering = ("-month",)
        verbose_name = "نمره"
        verbose_name_plural = "نمره ها"

    def __str__(self):
        return f"{self.student} {self.lesson} {self.score}"


class AttendanceRecord(models.Model):
    sta = {"present": "حاضر", "absent": "غایب", "late": "تاخیر"}
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendancerecords",
        verbose_name="دانش آموز",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="attendancerecords",
        verbose_name="درس",
    )
    status = models.CharField(
        max_length=20,
        verbose_name="وضعیت",
        choices=sta,
        default="present",
    )

    created_date = jmodels.jDateField(auto_now_add=True, verbose_name="ناریخ")

    class Meta:
        ordering = ("-id",)
        verbose_name = "حضور و غیاب"
        verbose_name_plural = "حضور و غیاب ها"

    def __str__(self):
        return self.student.first_name
