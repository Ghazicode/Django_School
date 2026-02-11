from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.BlogView.as_view(), name="main"),
    path("detail/<str:search>", views.BlogDetailView.as_view(), name="detail"),
    path("add", views.AddArticleView.as_view(), name="addarticle"),
    path(
        "update/<str:search>", views.ArticleUpdateView.as_view(), name="article_update"
    ),
    path(
        "delete/<str:search>", views.ArticleDeleteView.as_view(), name="article_delete"
    ),
]
