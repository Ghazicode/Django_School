from django.urls import path
from . import views


app_name = "account"
urlpatterns = [
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("change_password", views.ChangePasswordView.as_view(), name="change_password"),
    path("teacher/edit", views.TeacherEdit.as_view(), name="edit_teacher"),
    #   start panel
    path("teacher", views.TeacherProfileView.as_view(), name="teacher_profile"),
    path(
        "lesson/<int:pk>", views.AttendanceRecordView.as_view(), name="attendancerecord"
    ),
    path("student", views.StudentPanel.as_view(), name="student_profile"),
    path("parents", views.ParentsPanel.as_view(), name="parents_profile"),
    path("lessons", views.LessonListView.as_view(), name="lessons"),
    path("score/list/<int:pk>", views.ScoreListView.as_view(), name="score_list"),
    path(
        "score/update/<int:le>/<int:pk>",
        views.ScoreUpdateView.as_view(),
        name="score_update",
    ),
    path(
        "score/delete/<int:le>/<int:pk>",
        views.ScoreDeleteView.as_view(),
        name="score_delete",
    ),
    #   end panel
    path("comment", views.CommentView.as_view(), name="comment"),
    path("contact", views.ContactUsView.as_view(), name="contact"),
    path("logout", views.user_logout, name="logout"),
]
