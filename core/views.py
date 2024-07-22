from django.http import HttpResponse
from django.shortcuts import render


def calculate():
    x = 1
    y = 3
    return x


def index(request):
    x = calculate()
    context = {
        "title": "Django example",
        "name": "Ashiq"
    }
    return render(request, "index.html", context)


def say_hello(request, e, x):
    return HttpResponse(f"Hello world  {e + x}")


def about(request):
    return HttpResponse("About Django")
