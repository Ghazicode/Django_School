from django.db import models
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels


User = get_user_model()


class News(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="news", verbose_name="نویسنده"
    )
    title = models.CharField(max_length=250, verbose_name="عنوان")
    content = models.TextField(verbose_name="محتوا")
    image = models.ImageField(upload_to="news", verbose_name="عکس")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    read = models.IntegerField(default=0, verbose_name="زمان خواندن")
    views = models.IntegerField(default=0, verbose_name="بازدید")
    status = models.BooleanField(default=False, verbose_name="وضعیت")
    special = models.BooleanField(default=False, verbose_name="ویژه")
    created_date = jmodels.jDateField(auto_now_add=True, verbose_name="اپدیت")
    updated_date = jmodels.jDateField(auto_now=True, verbose_name="اپدیت")

    class Meta:
        ordering = ("-id",)
        verbose_name = "خبر"
        verbose_name_plural = "خبر‌ها‌"

    def __str__(self):
        return self.title


class Image(models.Model):
    title = models.CharField(max_length=250, verbose_name="عنوان")
    category = models.ManyToManyField("GalleryCategories", related_name="images")
    image = models.ImageField(upload_to="gallerys", verbose_name="عکس")
    status = models.BooleanField(default=False, verbose_name="وضعیت")
    created_date = jmodels.jDateField(auto_now_add=True, verbose_name="زمان ثبت")

    class Meta:
        ordering = ("-id",)
        verbose_name = "عکس"
        verbose_name_plural = "عکس ها"

    def __str__(self):
        return self.title


class GalleryCategories(models.Model):
    title = models.CharField(max_length=250, verbose_name="عنوان")

    class Meta:
        ordering = ("-id",)
        verbose_name = "دسته‌بندی گالری"
        verbose_name_plural = "دسته‌بندی‌های گالری"

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    phone_number = models.CharField(max_length=11, verbose_name="شماره تلفن")
    message = models.TextField(verbose_name="پیام")
    read = models.BooleanField(default=False, verbose_name="خوانده شده")
    created_date = jmodels.jDateField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"

    def __str__(self):
        return self.full_name
