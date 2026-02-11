from django.urls import path
from . import views
from django.conf import settings


app_name = "home"
urlpatterns = [
    path("", views.HomeView.as_view(), name="main"),
    path("news", views.NewsView.as_view(), name="news"),
    path("news/detail/<str:pk>", views.NewsDetailView.as_view(), name="news_detail"),
    path("gallery", views.GalleryView.as_view(), name="gallery"),
    path("teachers", views.TeachersListView.as_view(), name="teacher"),
    path(
        "teacher/detail/<str:full_name_en>",
        views.TeacherDetailView.as_view(),
        name="teacher_detail",
    ),
    path(
        "teacher/contact/<str:full_name_en>",
        views.TeacherContactView.as_view(),
        name="teacher_contact",
    ),
    path("about", views.AboutView.as_view(), name="about"),
]
