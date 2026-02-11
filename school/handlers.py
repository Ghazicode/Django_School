from django.shortcuts import render


def handler404(request, exception):
    return render(request, "errors/404.html", status=404)


def handler500(request):
    return render(request, "errors/500.html", status=500)


def handler403(request, exception):
    response = render(request, "errors/403.html")
    response.status_code = 403
    return response
