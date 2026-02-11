from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views import View
from .models import News, Image
from blog.models import Article
from accounts.forms import ContactUsForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from accounts.models import Teacher, Student
from .forms import TeacherContactForm
from django.contrib import messages
from django.http import Http404
from django.core.exceptions import PermissionDenied


User = get_user_model()


class HomeView(View):
    def get(self, request):
        form = ContactUsForm()
        news = News.objects.filter(status=True)[:3]
        articles = Article.objects.filter(status=True)[:3]
        gallerys = Image.objects.filter(status=True)[:8]
        return render(
            request,
            "home/index.html",
            {"news": news, "articles": articles, "gallerys": gallerys, "form": form},
        )

    def post(self, request):

        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "پیام شما با موفقیت ثبت شد."
            )
            return redirect("home:main")
        else:
            messages.add_message(
                request, messages.ERROR, "تمامی قسمت ها به درستی پر شوند."
            )
        return render(request, "home/index.html", {"form": form})


class GalleryView(View):
    def get(self, request):
        gallerys = Image.objects.filter(status=True)

        gallerys = Paginator(gallerys, 9)
        try:
            page_number = request.GET.get("page")
            gallerys = gallerys.get_page(page_number)
        except PageNotAnInteger:
            gallerys = gallerys.get_page(1)
        except EmptyPage:
            gallerys = gallerys.get_page(1)
        return render(request, "home/gallery.html", {"gallerys": gallerys})


class NewsView(View):
    def get(self, request):

        news = News.objects.filter(status=True)
        if s := request.GET.get("s"):
            news = news.filter(content__contains=s)
        special = news.filter(special=True).order_by("id").last()

        news = Paginator(news, 6)
        try:
            page_number = request.GET.get("page")
            news = news.get_page(page_number)
        except PageNotAnInteger:
            news = news.get_page(1)
        except EmptyPage:
            news = news.get_page(1)

        return render(request, "home/news.html", {"news": news, "special": special})


class NewsDetailView(View):
    def get(self, request, pk):
        try:
            news = News.objects.get(status=True, id=pk)
            news.views += 1
            news.save()
        except News.DoesNotExist:
            messages.add_message(
                request, messages.INFO, "خبری که به دنبال ان هستید وجود ندارد."
            )
            raise Http404()
        recent_news = News.objects.filter(status=True).exclude(id=pk)[:4]
        return render(
            request,
            "home/news-detail.html",
            {"news": news, "recent_news": recent_news},
        )


class TeachersListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        teachers = Paginator(teachers, 6)
        try:
            page_number = request.GET.get("page")
            teachers = teachers.get_page(page_number)
        except PageNotAnInteger:
            teachers = teachers.get_page(1)
        except EmptyPage:
            teachers = teachers.get_page(1)
        return render(request, "home/teachers_list.html", {"teachers": teachers})


class TeacherDetailView(View):
    def get(self, request, full_name_en):

        try:
            teacher = Teacher.objects.get(full_name_en=full_name_en)

        except Teacher.DoesNotExist:
            messages.add_message(
                request, messages.INFO, "معلمی که به دنبال ان هستید وجود ندارد."
            )
            raise Http404()
        return render(request, "home/teacher_profile.html", {"teacher": teacher})


class TeacherContactView(View):
    def get(self, request, full_name_en):
        user = request.user
        if user.is_authenticated:
            if user.is_student:
                try:
                    teacher = Teacher.objects.get(full_name_en=full_name_en)
                    teachers = Teacher.objects.all()
                    student = Student.objects.get(user=user)
                    form = TeacherContactForm()
                    return render(
                        request,
                        "home/teacher_contact.html",
                        {
                            "teacher": teacher,
                            "form": form,
                            "teachers": teachers,
                            "student": student,
                        },
                    )

                except Teacher.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.INFO,
                        "معلمی که به دنبال ان هستید وجود ندارد.",
                    )
                    raise Http404()
                except Student.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.INFO,
                        "حسابی به عنوان دانش اموز برای شما ساخته نشده",
                    )
                    raise Http404()

            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "فقط دانش اموزان به این قسمت دسترسی دارند",
                )
                raise PermissionDenied()

        else:
            messages.add_message(
                request, messages.INFO, "برای دسترسی به این قسمت باید وارد سایت شوید."
            )
            return redirect("account:login")

    def post(self, request, full_name_en):
        user = request.user
        if user.is_authenticated:
            if user.is_student:
                try:
                    form = TeacherContactForm(request.POST)
                    teacher = Teacher.objects.get(full_name_en=full_name_en)
                    teachers = Teacher.objects.all()
                    student = Student.objects.get(user=user)
                    if form.is_valid():
                        form.save()
                        messages.add_message(
                            request, messages.SUCCESS, "پیام شما با موفقیت ارسال شد."
                        )
                        return redirect("home:main")
                    else:
                        messages.add_message(
                            request,
                            messages.ERROR,
                            "تمامی قسمت ها باید به درستی پر شوند.",
                        )

                except Teacher.DoesNotExist:
                    messages.add_message(
                        request, messages.INFO, "معلم مورد نظر یافت نشد."
                    )
                    raise Http404()
                except Student.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.INFO,
                        "حسابی به عنوان دانش اموز برای شما ساخته نشده",
                    )
                    raise Http404()
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "فقط دانش اموزان به این قسمت دسترسی دارند",
                )
                raise PermissionDenied("شما دسترسی به این صفحه ندارید")
        else:
            messages.add_message(
                request, messages.INFO, "برای دسترسی  به این بخش باید وارد شوید."
            )
            return redirect("account:login")

        return render(
            request,
            "home/teacher_contact.html",
            {
                "form": form,
                "teachers": teachers,
                "teacher": teacher,
                "student": student,
            },
        )


class AboutView(View):
    def get(self, request):
        management_team = User.objects.filter(is_staff=True).order_by("-id")
        return render(request, "home/about.html", {"management_team": management_team})
