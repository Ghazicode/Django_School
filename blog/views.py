from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import ArticleForm, ArticleUpdateForm, CommentForm
from django.http import Http404
from django.contrib import messages
from .models import Article, Comments
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class BlogView(View):
    def get(self, request):
        articles = Article.objects.filter(status=True)
        if s := request.GET.get("s"):
            articles = articles.filter(content__contains=s)

        articles = Paginator(articles, 6)
        try:
            page_number = request.GET.get("page")
            articles = articles.get_page(page_number)
        except PageNotAnInteger:
            articles = articles.get_page(1)
        except EmptyPage:
            articles = articles.get_page(1)

        return render(request, "blog/articles.html", {"articles": articles})


class BlogDetailView(View):
    def get(self, request, search):
        form = CommentForm()

        try:
            article = Article.objects.get(status=True, search=search)
            article.views += 1
            article.save()
            comments = Comments.objects.filter(status=True, article=article)
            comments = Paginator(comments, 4)
            page_number = request.GET.get("page")
            comments = comments.get_page(page_number)
            articles = Article.objects.filter(status=True).exclude(
                search=article.search
            )[:4]
        except Article.DoesNotExist:
            messages.add_message(
                request,
                messages.INFO,
                "مقاله ای که به دنبال ان میگردید وجود ندارد.",
            )
            raise Http404()

        except PageNotAnInteger:
            comments = comments.get_page(1)
        except EmptyPage:
            comments = comments.get_page(1)

        return render(
            request,
            "blog/article_detail.html",
            {
                "article": article,
                "comments": comments,
                "articles": articles,
                "form": form,
            },
        )

    def post(self, request, search):
        user = request.user
        if user.is_authenticated:
            article = get_object_or_404(Article, status=True, search=search)
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(
                    request, messages.SUCCESS, "نظر شما با موفقیت ثبت شد."
                )
                return redirect(f"/blog/detail/{search}")
            else:
                messages.add_message(
                    request, messages.ERROR, "تمامی قسمت ها باید به درستی پرشود."
                )
                return redirect(f"/blog/detail/{search}")

        else:
            messages.add_message(
                request,
                messages.INFO,
                "برای دسترسی به این صفحه باید وارد حساب خود شوید.",
            )
            return redirect("account:login")


class AddArticleView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_teacher:
                form = ArticleForm()
            else:
                raise Http404()
        else:
            raise Http404()
        return render(request, "blog/add_article.html", {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.is_teacher:
                form = ArticleForm(request.POST, request.FILES)
                if form.is_valid():

                    form.save()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "مقاله شما با موفقیت ثبت شد. منتظر تایید مقاله خود از طرف مدیر باشید.",
                    )
                    return redirect("account:teacher_profile")
                else:
                    messages.add_message(
                        request, messages.ERROR, "تمامی قسمت ها باید به درستی پر شوند"
                    )
            else:
                raise Http404()

        else:
            raise Http404()
        return render(request, "blog/add_article.html", {"form": form})


class ArticleUpdateView(View):
    def get(self, request, search):
        user = request.user
        if user.is_authenticated:
            if user.is_teacher:
                try:
                    article = Article.objects.get(author=user, search=search)
                    form = ArticleUpdateForm(instance=article)
                except Article.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.INFO,
                        "مقاله ای که قصد بروزرسانی ان را دارید یا نویسنده آن نیستید یا آن مقاله وجود ندارد.",
                    )
                    raise Http404()
            else:
                raise Http404()
        else:
            raise Http404()

        return render(request, "blog/article_update.html", {"form": form})

    def post(self, request, search):
        user = request.user
        if user.is_authenticated:
            if user.is_teacher:
                try:
                    article = Article.objects.get(author=user, search=search)
                    form = ArticleUpdateForm(
                        instance=article, data=request.POST, files=request.FILES
                    )
                    if form.is_valid():
                        form.save()
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            "مقاله شما با موفقیت بروزرسانی شد.",
                        )
                        return redirect("account:teacher_profile")
                except Article.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.INFO,
                        "مقاله ای که میخواهید ان را بروزرسانی کنید وجود ندارد.",
                    )
                    raise Http404()
            else:
                raise Http404()
        else:
            raise Http404()

        return render(request, "blog/article_update.html", {"form": form})


class ArticleDeleteView(View):
    def get(self, request, search):
        user = request.user
        if user.is_authenticated:
            if user.is_teacher:
                try:
                    article = get_object_or_404(Article, author=user, search=search)
                    article.delete()
                    messages.add_message(
                        request, messages.SUCCESS, "مقاله شما با موفقیت حذف شد."
                    )
                    return redirect("account:teacher_profile")
                except Article.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.INFO,
                        "مقاله ای که میخواهید ان را حذف کنید وجود ندارد.",
                    )
                    raise Http404()
            else:

                raise Http404()
        else:
            raise Http404()
