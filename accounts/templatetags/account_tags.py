from django import template
from accounts.models import Lesson, AttendanceRecord, Grade, Student

register = template.Library()


@register.filter
def truncate_chars(text, num_chars=30):
    if not text:
        return ""

    text = str(text)
    if len(text) <= num_chars:
        return text

    if num_chars == 1:
        return text[:num_chars]

    else:

        return text[:num_chars] + "..."


@register.simple_tag
def get_lesson_count(user=None):
    return Lesson.objects.filter(student=user).count()


@register.simple_tag
def get_status_grade(user=None, status=None):
    return Grade.objects.filter(student=user, status=status).count()


@register.simple_tag
def attendancerecord_count(user=None, status=None):
    return AttendanceRecord.objects.filter(student=user, status=status).count()
