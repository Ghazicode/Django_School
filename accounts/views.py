from django.shortcuts import render, redirect
from .forms import (
    LoginForm,
    ChangePasswordForm,
    EditTeacherForm,
    ContactUsForm,
    RegisterForm,
    ScoreUpdateForm,
    ParentCommentForm,
)
from blog.forms import ArticleForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from .models import (
    User,
    Teacher,
    Comment,
    Lesson,
    Grade,
    Student,
    TeacherContact,
    Parents,
    AttendanceRecord,
    NewUser,
)
from django.http import Http404
from blog.models import Article
from django.core.exceptions import PermissionDenied
import jdatetime
from django.utils import timezone
from datetime import datetime


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home:main")
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("home:main")
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])

            if user is not None:
                login(request, user)
                remember_me = cd.get("remember_me")

                if remember_me:
                    request.session.set_expiry(604800)
                    request.session["remember_me"] = True
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "شما با موفقیت وارد شدید. وضعیت شما به مدت 1 هفته حفظ خواهد شد.",
                    )
                else:
                    request.session.set_expiry(0)
                    request.session["remember_me"] = False
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "شما با موفقیت وارد شدید. پس از بستن مرورگر از حساب خارج خواهید شد.",
                    )
                if next_page := request.GET.get("next_page"):
                    return redirect(next_page)

                return redirect("home:main")
            else:
                messages.add_message(
                    request, messages.WARNING, "کاربری با چنین اطلاعاتی وجود ندارد"
                )
        else:
            messages.add_message(
                request, messages.ERROR, "اطلاعات وارد شده صحیح نمیباشد"
            )

        return render(request, "accounts/login.html", {"form": form})


class ChangePasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = ChangePasswordForm()
        else:
            messages.add_message(
                request,
                messages.INFO,
                "قبل از تغییر رمز عبور باید وارد حساب خود شوید.",
            )
            return redirect("account:login")
        return render(request, "accounts/change_password.html", {"form": form})

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            messages.add_message(
                request, messages.INFO, "قبل از تغییر رمز عبور باید وارد شوید."
            )
            return redirect("account:login")

        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            old_password = cd["old_password"]
            new_password1 = cd["new_password1"]
            new_password2 = cd["new_password2"]
            if not user.check_password(old_password):
                messages.add_message(
                    request, messages.ERROR, "رمز قبلی شما درست نمیباشد"
                )

            else:
                if new_password1 != new_password2:

                    messages.add_message(
                        request,
                        messages.ERROR,
                        "رمز های جدید شما با یکدیگر مطابقت ندارند!",
                    )

                else:
                    if old_password != new_password1:
                        user.set_password(new_password1)
                        user.save()
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            "رمز شما با موفقیت تغییر یافت.حالا وارد حساب خود شوید.",
                        )
                        return redirect("account:login")
                    else:
                        messages.add_message(
                            request, messages.WARNING, "رمز قبلی با رمز جدید برابر است."
                        )
        else:
            messages.add_message(
                request, messages.ERROR, "تمامی قسمت ها باید به درستی پر شوند."
            )
            return redirect("account:change_password")
        return render(request, "accounts/change_password.html", {"form": form})


class ContactUsView(View):
    def get(self, request):
        form = ContactUsForm()
        return render(request, "accounts/contact.html", {"form": form})

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
                request, messages.ERROR, "تمامی قسمت ها باید به درستی پر شوند."
            )

        return render(request, "accounts/contact.html", {"form": form})


class TeacherEdit(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_teacher:

                try:
                    teacher = Teacher.objects.get(user=user)
                    form = EditTeacherForm(instance=teacher)
                except Teacher.DoesNotExist:
                    messages.add_message(
                        request, messages.INFO, "هنوز حسابی برای شما ساخته نشده است"
                    )
                    raise Http404()
            else:
                raise Http404()
        else:
            raise Http404()

        return render(request, "accounts/teacher_edit.html", {"form": form})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_teacher:
                try:
                    teacher = Teacher.objects.get(user=user)
                    form = EditTeacherForm(
                        instance=teacher, data=request.POST, files=request.FILES
                    )
                    if form.is_valid():
                        form.save()
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            "اطلاعات شما با موفقیت تغییریافت.",
                        )
                        return redirect("account:teacher_profile")
                except Teacher.DoesNotExist:
                    messages.add_message(
                        request, messages.INFO, "هنوز حسابی برای شما ساخته نشده است"
                    )
                    raise Http404()
            else:
                raise Http404()
        else:
            raise Http404()

        return render(request, "accounts/teacher_edit.html", {"form": form})


# class TeacherProfileView(View):
#     def get(self, request):
#         user = request.user
#         if user.is_authenticated:
#             if user.is_teacher:
#                 try:
#                     articles = Article.objects.filter(author=user)
#                     teacher = Teacher.objects.get(user=user)
#                     lessons = Lesson.objects.filter(teacher=teacher)
#                     teacher_contact = TeacherContact.objects.filter(teacher=teacher)

#                 except Teacher.DoesNotExist:
#                     messages.add_message(
#                         request,
#                         messages.WARNING,
#                         "هنوز هیج حسابی به عنوان معلم برای شما ساخته نشده است.",
#                     )
#                     raise Http404()
#             else:
#                 raise Http404()
#         else:
#             raise Http404()
#         return render(
#             request,
#             "accounts/teacher_panel.html",
#             {
#                 "lessons": lessons,
#                 "teacher_contact": teacher_contact,
#                 "articles": articles,
#             },
#         )

#     def post(self, request):
#         user = request.user
#         if user.is_authenticated:
#             if user.is_teacher:
#                 form = ArticleForm()
#                 try:
#                     articles = Article.objects.filter(author=user)
#                     teacher = Teacher.objects.get(user=user)
#                     lessons = Lesson.objects.filter(teacher=teacher)
#                     teacher_contact = TeacherContact.objects.filter(teacher=teacher)
#                     student = request.POST.get("student")
#                     lesson = request.POST.get("lesson")
#                     score = request.POST.get("score")
#                     class_activity = request.POST.get("class_activity")
#                     month = request.POST.get("month")
#                     status = request.POST.get("status")
#                     required_fields = [
#                         student,
#                         lesson,
#                         score,
#                         class_activity,
#                         month,
#                         status,
#                     ]
#                     if not all(required_fields):
#                         messages.add_message(
#                             request, messages.ERROR, "تمامی قسمت ها باید به درستی پر شوند."
#                         )
#                     else:
#                         try:
#                             user = User.objects.get(username=student)
#                             st = Student.objects.get(user=user)
#                             les = Lesson.objects.get(name=lesson)
#                             Grade.objects.create(
#                             student=st,
#                             lesson=les,
#                             score=score,
#                             class_activity=class_activity,
#                             month=month,
#                             status=status)
#                             messages.add_message(
#                             request,
#                             messages.SUCCESS,
#                             f"نمره {st.first_name} {st.last_name} با موفقیت ثبت شد.")
#                             return redirect("account:teacher_profile")
#                         except (
#                             User.DoesNotExist,
#                             Student.DoesNotExist,
#                             Lesson.DoesNotExist,
#                             ):
#                             raise Http404()
#                 except Teacher.DoesNotExist:
#                     messages.add_message(
#                         request,
#                         messages.WARNING,
#                         "هنوز هیج حسابی به عنوان معلم برای شما ساخته نشده است.",
#                     )
#                     raise Http404()
#             else:
#                 raise Http404()
#         else:
#             raise Http404()
#         return render(
#             request,
#             "accounts/teacher_panel.html",
#             {
#                 "lessons": lessons,
#                 "form": form,
#                 "teacher_contact": teacher_contact,
#                 "articles": articles,
#             },
#         )


class TeacherProfileView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_teacher:
                try:
                    articles = Article.objects.filter(author=user)
                    teacher = Teacher.objects.get(user=user)
                    lessons = Lesson.objects.filter(teacher=teacher)
                    teacher_contact = TeacherContact.objects.filter(teacher=teacher)

                except Teacher.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        "هنوز هیج حسابی به عنوان معلم برای شما ساخته نشده است.",
                    )
                    raise Http404()
            else:
                raise Http404()
        else:
            raise Http404()
        return render(
            request,
            "accounts/teacher_panel.html",
            {
                "lessons": lessons,
                "teacher_contact": teacher_contact,
                "articles": articles,
            },
        )

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_teacher:
                try:
                    teacher = Teacher.objects.get(user=user)
                    lessons = Lesson.objects.filter(teacher=teacher)
                    teacher_contact = TeacherContact.objects.filter(teacher=teacher)
                    articles = Article.objects.filter(author=user)

                    # دریافت آرایه‌های نمرات از فرم
                    students = request.POST.getlist("students[]")
                    lesson_names = request.POST.getlist("lessons[]")
                    scores = request.POST.getlist("scores[]")
                    class_activities = request.POST.getlist("class_activities[]")
                    months = request.POST.getlist("months[]")
                    statuses = request.POST.getlist("statuses[]")

                    # بررسی اینکه آیا فرم نمرات ارسال شده است
                    if students and len(students) > 0:
                        success_count = 0
                        error_count = 0

                        # حلقه بر روی تمامی نمرات ارسال شده
                        for i in range(len(students)):
                            student = students[i]
                            lesson_name = lesson_names[i]
                            score = scores[i]
                            class_activity = class_activities[i]
                            month = months[i]
                            status = statuses[i]

                            # بررسی فیلدهای الزامی
                            if (
                                student
                                and lesson_name
                                and score
                                and class_activity
                                and month
                                and status
                            ):
                                try:
                                    # پیدا کردن کاربر دانش‌آموز
                                    user_obj = User.objects.get(username=student)
                                    student_obj = Student.objects.get(user=user_obj)
                                    lesson_obj = Lesson.objects.get(
                                        name=lesson_name, teacher=teacher
                                    )

                                    # ایجاد نمره جدید
                                    Grade.objects.create(
                                        student=student_obj,
                                        lesson=lesson_obj,
                                        score=float(score),
                                        class_activity=float(class_activity),
                                        month=month,
                                        status=status,
                                    )
                                    success_count += 1

                                except (
                                    User.DoesNotExist,
                                    Student.DoesNotExist,
                                    Lesson.DoesNotExist,
                                    ValueError,
                                ) as e:
                                    error_count += 1
                                    print(
                                        f"Error creating grade for student {student}: {str(e)}"
                                    )
                            else:
                                error_count += 1

                        # نمایش پیام مناسب
                        if success_count > 0:
                            messages.add_message(
                                request,
                                messages.SUCCESS,
                                f"{success_count} نمره با موفقیت ثبت شد. {error_count} نمره با خطا مواجه شد.",
                            )
                        elif error_count > 0:
                            messages.add_message(
                                request,
                                messages.ERROR,
                                "متاسفانه ثبت نمرات با خطا مواجه شد. لطفا دوباره تلاش کنید.",
                            )

                        return redirect("account:teacher_profile")

                except Teacher.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        "هنوز هیج حسابی به عنوان معلم برای شما ساخته نشده است.",
                    )
                    raise Http404()
            else:
                raise Http404()
        else:
            raise Http404()

        return render(
            request,
            "accounts/teacher_panel.html",
            {
                "lessons": lessons,
                "teacher_contact": teacher_contact,
                "articles": articles,
            },
        )


class CommentView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_parents:
                form = ParentCommentForm()
                comments = Comment.objects.filter(show=True)
                return render(
                    request,
                    "accounts/comment.html",
                    {"form": form, "comments": comments},
                )
            else:
                messages.add_message(
                    request, messages.WARNING, "فقط والدین به این بخش دسترسی دارند."
                )
                raise PermissionDenied()
        else:
            messages.add_message(
                request, messages.INFO, "برای دسترسی به این قسمت باید وارد شوید."
            )
            return redirect("account:login")

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_parents:
                form = ParentCommentForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.add_message(
                        request, messages.SUCCESS, "نظر شما با موفقیت ثبت شد"
                    )
                    return redirect("home:main")
                else:
                    messages.add_message(
                        request, messages.ERROR, "تمامی قسمت ها باید به درستی پر شوند."
                    )
            else:
                messages.add_message(
                    request, messages.WARNING, "فقط والدین به این بخش دسترسی دارند."
                )
                raise PermissionDenied()
        else:
            messages.add_message(
                request, messages.INFO, "برای دسترسی به این قسمت باید وارد شوید."
            )
            return redirect("account:login")

        return render(request, "accounts/comment.html", {"form": form})


class StudentPanel(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_student:
                try:
                    student = Student.objects.get(user=user)
                    attendancerecords = AttendanceRecord.objects.filter(
                        student=student
                    )[:5]
                    grades = Grade.objects.filter(student=student)
                    return render(
                        request,
                        "accounts/student_panel.html",
                        {
                            "student": student,
                            "grades": grades,
                            "attendancerecords": attendancerecords,
                        },
                    )

                except Student.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        "حساب دانش اموزی برای شما ساخته نشده است.",
                    )
                    raise Http404()
                except Grade.DoesNotExist:
                    messages.add_message(
                        request, messages.INFO, "نمره ای برای شما ثبت نشده است"
                    )
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "فقط دانش آموزان به این صفحه دسترسی دارند.",
                )
                raise PermissionDenied()
        else:

            return Http404()


class ParentsPanel(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_parents:
                try:
                    parent = Parents.objects.get(user=user)
                except Parents.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        "هنوز حسابی برای شما ساخته نشده.",
                    )
                    raise Http404()
            else:
                raise Http404()
        else:
            raise Http404()

        return render(request, "accounts/parents_panel.html", {"parent": parent})


class LessonListView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_superuser:
                lessons = Lesson.objects.all()
            elif user.is_teacher:
                lessons = Lesson.objects.filter(teacher=user.teachers)
            else:
                messages.add_message(
                    request, messages.WARNING, "شما به این بخش دسترسی ندارید"
                )
                raise PermissionDenied()
        else:
            messages.add_message(
                request, messages.WARNING, "برای دسترسی به صفحه باید وارد شوید"
            )
            return redirect("account:login")
        return render(request, "accounts/lesson_list.html", {"lessons": lessons})


class ScoreListView(View):
    def get(self, request, pk):
        user = request.user
        if user.is_authenticated:
            if user.is_superuser:
                try:
                    lesson = Lesson.objects.get(id=pk)
                    grades = Grade.objects.filter(lesson=lesson)
                except Lesson.DoesNotExist:
                    raise Http404()
            elif user.is_teacher:
                try:
                    teacher = Teacher.objects.get(user=user)
                    lesson = Lesson.objects.get(id=pk, teacher=teacher)
                    grades = Grade.objects.filter(lesson=lesson)
                except (Lesson.DoesNotExist, Teacher.DoesNotExist):
                    raise Http404()

            else:
                raise PermissionDenied()
        else:
            raise Http404()
        return render(
            request, "accounts/score_list.html", {"lesson": lesson, "grades": grades}
        )


class ScoreUpdateView(View):
    def get(self, request, pk, le):
        user = request.user
        if user.is_authenticated:
            if user.is_teacher:
                try:
                    lesson = Lesson.objects.get(id=le, teacher=user.teachers)
                    grade = Grade.objects.get(id=pk, lesson=lesson)
                    form = ScoreUpdateForm(instance=grade)
                except (Grade.DoesNotExist, Lesson.DoesNotExist):
                    raise Http404()
            else:
                raise Http404()
        else:
            raise Http404()
        return render(
            request,
            "accounts/score_update.html",
            {"form": form, "lesson": le, "pk": pk, "grade": grade},
        )

    def post(self, request, pk, le):
        user = request.user
        if user.is_authenticated:
            if user.is_teacher:
                try:
                    lesson = Lesson.objects.get(id=le, teacher=user.teachers)
                    grade = Grade.objects.get(id=pk, lesson=lesson)
                    form = ScoreUpdateForm(request.POST, instance=grade)
                    if form.is_valid():
                        form.save()
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            "نمره دانش اموز با موفقیت تغییر کرد",
                        )
                        return redirect("account:score_list", le)
                except (Grade.DoesNotExist, Lesson.DoesNotExist):
                    raise Http404()
            else:
                raise Http404()
        else:
            raise Http404()
        return render(
            request,
            "accounts/score_update.html",
            {"form": form, "lesson": le, "grade": grade},
        )


class ScoreDeleteView(View):
    def get(self, request, pk, le):
        user = request.user
        if user.is_authenticated:
            if user.is_teacher:
                try:
                    lesson = Lesson.objects.get(id=le, teacher=user.teachers)
                    grade = Grade.objects.get(id=pk, lesson=lesson)
                    grade.delete()
                    messages.add_message(
                        request, messages.SUCCESS, "نمره با موفقیت حذف شد"
                    )
                    return redirect(f"/account/score/list/{le}")
                except (Lesson.DoesNotExist, Grade.DoesNotExist):
                    raise Http404()
            else:
                raise Http404()
        else:
            raise Http404()


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home:main")
        form = RegisterForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("home:main")
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(username=cd["username"]).exists():
                messages.add_message(request, messages.INFO, "نام کاربری رزرو شده است")
            else:
                if cd["password1"] == cd["password2"]:
                    user = User.objects.create_user(
                        username=cd["username"], password=cd["password1"]
                    )
                    NewUser.objects.filter(user=user).update(
                        full_name=cd["full_name"], phone_number=cd["phone_number"]
                    )
                    login(request, user)
                    request.session.set_expiry(604800)
                    request.session["remember_me"] = True
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "شما با موفقیت وارد شدید. وضعیت شما به مدت 1 هفته حفظ خواهد شد.",
                    )
                    return redirect("home:main")
                else:
                    messages.add_message(
                        request, messages.WARNING, "رمز ها با یکدیگر مطابقت ندارند"
                    )
        else:
            messages.add_message(
                request, messages.ERROR, "اطلاعات وارد شده صحیح نمیباشد"
            )
        return render(request, "accounts/register.html", {"form": form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("account:login")
    else:
        messages.add_message(
            request,
            messages.INFO,
            "برای خارج شدن اول باید وارد حساب خود شوید تا بتوانید از ان خارج شوید.",
        )
        return redirect("account:login")


class AttendanceRecordView(View):

    def get(self, request, pk):
        user = request.user
        if not user.is_authenticated or not user.is_teacher:
            raise Http404()

        try:
            lesson = Lesson.objects.get(id=pk, teacher=user.teachers)
            students = lesson.student.all().order_by("last_name")

            # تاریخ جلالی امروز برای نمایش
            today_jalali = jdatetime.datetime.now().date()
            today_jalali_str = today_jalali.strftime("%Y/%m/%d")

            # تاریخ میلادی امروز برای کوئری
            today_gregorian = jdatetime.date.today().togregorian()

            try:
                existing_records = AttendanceRecord.objects.filter(
                    lesson=lesson, created_date__date=today_gregorian
                ).select_related("student")
            except:
                # روش 2: روش جایگزین برای دیتابیس‌هایی که __date را پشتیبانی نمی‌کنند
                start_of_day = datetime.combine(today_gregorian, datetime.min.time())
                end_of_day = datetime.combine(today_gregorian, datetime.max.time())

                # اگر از timezone استفاده می‌کنید:
                if timezone.is_aware(start_of_day):
                    start_of_day = timezone.make_aware(start_of_day)
                    end_of_day = timezone.make_aware(end_of_day)

                existing_records = AttendanceRecord.objects.filter(
                    lesson=lesson,
                    created_date__gte=start_of_day,
                    created_date__lte=end_of_day,
                ).select_related("student")

            # ایجاد دیکشنری برای وضعیت‌های امروز
            status_dict = {}
            for record in existing_records:
                # تبدیل تاریخ میلادی به جلالی برای نمایش
                jalali_date = jdatetime.datetime.fromgregorian(
                    datetime=record.created_date
                ).strftime("%Y/%m/%d")

                status_dict[record.student.id] = {
                    "record": record,
                    "status": record.status,
                    "created_date": record.created_date,
                    "jalali_date": jalali_date,
                    "time": record.created_date.strftime("%H:%M"),  # ساعت
                }

            return render(
                request,
                "accounts/attendancerecord.html",
                {
                    "lesson": lesson,
                    "students": students,
                    "existing_records": status_dict,
                    "today_jalali": today_jalali_str,
                },
            )
        except Lesson.DoesNotExist:
            raise Http404()
        except Exception as e:
            messages.error(request, f"❌ خطا: {str(e)}")
            return redirect("home")

    def post(self, request, pk):
        user = request.user
        if not user.is_authenticated or not user.is_teacher:
            raise Http404()

        try:
            lesson = Lesson.objects.get(id=pk, teacher=user.teachers)
            students = lesson.student.all()

            # تاریخ‌های امروز
            today_jalali = jdatetime.datetime.now().date()
            today_jalali_str = today_jalali.strftime("%Y/%m/%d")
            today_gregorian = jdatetime.date.today().togregorian()

            # محاسبه شروع و پایان امروز برای کوئری
            start_of_day = datetime.combine(today_gregorian, datetime.min.time())
            end_of_day = datetime.combine(today_gregorian, datetime.max.time())

            if timezone.is_aware(start_of_day):
                start_of_day = timezone.make_aware(start_of_day)
                end_of_day = timezone.make_aware(end_of_day)

            with transaction.atomic():
                saved_count = 0
                updated_count = 0

                for student in students:
                    field_name = f"attendance_{student.id}"
                    status = request.POST.get(field_name)

                    if status and status in ["present", "absent", "late"]:
                        # بررسی آیا رکورد امروز وجود دارد؟
                        existing_record = AttendanceRecord.objects.filter(
                            student=student,
                            lesson=lesson,
                            created_date__gte=start_of_day,
                            created_date__lte=end_of_day,
                        ).first()

                        if existing_record:
                            # به‌روزرسانی رکورد موجود
                            existing_record.status = status
                            existing_record.save()
                            updated_count += 1
                        else:
                            # ایجاد رکورد جدید
                            # اگر created_date auto_now_add=True دارد، خودش پر می‌شود
                            AttendanceRecord.objects.create(
                                student=student,
                                lesson=lesson,
                                status=status,
                                # created_date به صورت خودکار پر می‌شود اگر auto_now_add=True باشد
                            )
                            saved_count += 1

                # پیام موفقیت
                if saved_count > 0 or updated_count > 0:
                    message_parts = []
                    if saved_count > 0:
                        message_parts.append(f"{saved_count} رکورد جدید")
                    if updated_count > 0:
                        message_parts.append(f"{updated_count} رکورد به‌روزرسانی")

                    message = f'✅ حضور و غیاب تاریخ {today_jalali_str} با موفقیت ثبت شد. ({", ".join(message_parts)})'
                    messages.success(request, message)
                else:
                    messages.warning(request, "⚠️ هیچ وضعیتی انتخاب نشده بود.")

                return redirect("account:attendancerecord", pk)

        except Lesson.DoesNotExist:
            raise Http404()
        except Exception as e:
            messages.error(request, f"❌ خطا در ذخیره‌سازی: {str(e)}")
            return redirect("account:attendancerecord", pk)
