from django.shortcuts import render
from django.http import HttpResponse

def index(request, *args, **kwargs):
    texte = "Je suis de débuter django python avec github"
    return HttpResponse(texte)
