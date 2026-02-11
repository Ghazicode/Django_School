from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . import models


class CommentsInline(admin.TabularInline):
    model = models.Comments  # مطمئن شوید این مدل وجود دارد
    extra = 1
    can_delete = True
    verbose_name = "نظر اضافه"
    verbose_name_plural = "نظرهای اضافه"
    classes = ["collapse"]


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "phone_number", "status")
    list_filter = ("name", "status")
    search_fields = ("title", "email")


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = (
        "title",
        "author",
        "status",
        "views",
        "created_date",
        "updated_date",
    )
    list_filter = ("status", "title")
    search_fields = ("title", "content")
    inlines = [CommentsInline]


admin.site.register(models.Comments, CommentsAdmin)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Article, ArticleAdmin)
