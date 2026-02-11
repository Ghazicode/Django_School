from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . import models


class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = ("title", "author", "status", "views")
    list_filter = ("status", "title")
    search_fields = ("title", "content")


class ImageAdmin(SummernoteModelAdmin):
    list_display = ("title", "status")
    list_filter = ("title", "status")
    search_fields = ("title",)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", "read")
    list_filter = ("read",)
    search_fields = ("full_name", "phone_number", "message")


admin.site.register(models.News, NewsAdmin)
admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.GalleryCategories)
admin.site.register(models.ContactUs, ContactUsAdmin)
