from django.shortcuts import render
from channels import Group


def welcome(request):
    return render(request, 'reg/welcome.html')
