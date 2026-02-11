from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = models.User
        fields = ("username",)


class CustomUserAdmin(UserAdmin):
    model = models.User
    add_form = CustomUserCreationForm
    list_display = (
        "username",
        "is_superuser",
        "is_teacher",
        "is_student",
        "is_active",
        "is_user",
        "created_date",
    )
    list_filter = (
        "is_superuser",
        "is_active",
        "is_parents",
        "is_student",
        "is_staff",
        "is_teacher",
        "is_user",
    )
    searching_fields = ("username",)
    ordering = ("username",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                ),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_teacher",
                    "is_student",
                    "is_parents",
                    "is_user",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_teacher",
                    "is_student",
                    "is_parents",
                    "is_user",
                ),
            },
        ),
    )


class CustomUserProfile(SummernoteModelAdmin):
    summernote_fields = ("description",)
    list_display = ("user", "first_name", "role", "created_date")
    search_fields = ("first_name", "last_name")


class TeacherContactInline(admin.TabularInline):
    model = models.TeacherContact  # مطمئن شوید این مدل وجود دارد
    extra = 1
    can_delete = True
    verbose_name = "پیام"
    verbose_name_plural = "پیام ها"
    classes = ["collapse"]


class LessonInline(admin.TabularInline):
    model = models.Lesson  # مطمئن شوید این مدل وجود دارد
    extra = 1
    can_delete = True
    verbose_name = "درس"
    verbose_name_plural = "درس ها"
    classes = ["collapse"]


class TeacherAdmin(SummernoteModelAdmin):
    summernote_fields = ("description",)
    list_display = (
        "user",
        "full_name",
        "status"
    )
    search_fields = ("full_name",)
    inlines = [TeacherContactInline, LessonInline]


class ParentsAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name")
    search_fields = ("last_name", "first_name")


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "full_name",
        "phone_number",
        "status",
        "show",
        "created_date",
    )
    list_filter = ("status",)


class GradeInline(admin.TabularInline):
    model = models.Grade
    extra = 1
    can_delete = True
    verbose_name = "نمره"
    verbose_name_plural = "نمره ها"
    classes = ["collapse"]


class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "grade")
    list_filter = ("grade",)
    search_fields = ("user", "last_name", "fist_name")
    inlines = [
        GradeInline,
    ]


class GradeAdmin(admin.ModelAdmin):
    list_display = ["student", "lesson", "status", "month", "score", "updated_date"]
    list_filter = ["status", "month"]
    search_fields = ["student"]


class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher")
    list_filter = ("name",)


class TeacherContactAdmin(admin.ModelAdmin):
    list_display = ("teacher", "student", "student_name", "subject")


class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "status", "created_date")
    list_filter = ("status", "lesson")


class NewUserAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "phone_number", "created_date")


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.ProfileAdmin, CustomUserProfile)
admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Parents, ParentsAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.TeacherContact, TeacherContactAdmin)
admin.site.register(models.Lesson, LessonAdmin)
admin.site.register(models.Grade, GradeAdmin)
admin.site.register(models.AttendanceRecord, AttendanceRecordAdmin)
admin.site.register(models.NewUser, NewUserAdmin)
