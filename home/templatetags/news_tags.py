from django import template
from home.models import News
from accounts.models import Teacher, Student

register = template.Library()


@register.filter
def truncate_chars(text, num_chars=30):
    if not text:
        return ""

    text = str(text)
    if len(text) <= num_chars:
        return text

    # if num_chars == 1:
    #     return text[:num_chars]

    return text[:num_chars] + "..."


@register.simple_tag
def get_news_count():
    return News.objects.filter(status=True).count()


@register.simple_tag
def get_latest_news():
    try:
        return News.objects.filter(status=True).latest("created_date")
    except News.DoesNotExist:
        return None


@register.simple_tag
def get_teacher_count():
    return Teacher.objects.all().count()


@register.simple_tag
def get_student_count(number):
    if number == 1:
        return Student.objects.all().count()
    elif number == 2:
        return Teacher.objects.all().count()
