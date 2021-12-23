from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.conf.urls import url
from django_app.models import ville, Locateur, Locataire
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.utils.timezone import get_current_timezone
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema

#from .models import History
from .serializers import LoginSerializer

# Create your views here.


def home(request):
    return render(request, "django_app/home.html")

@permission_classes([IsAuthenticated])
def users(request):
    if request.method == "POST":
        profil = request.POST.get("profil")
        if profil == "locataire":
            return render(request, "django_app/users.html", {"users": User.objects.all().values(), "locataires": Locataire.objects.all().values()})
        if profil == "locateur":
            return render(request, "django_app/users.html", {"users": User.objects.all().values(), "locateurs": Locateur.objects.all().values()})
        else:
            return render(request, "django_app/users.html", {"users": User.objects.all().values(), "locataires": Locataire.objects.all().values(), "locateurs": Locateur.objects.all().values()})

    else:
        return render(request, "django_app/users.html", {"users": User.objects.all().values(), "locataires": Locataire.objects.all().values(), "locateurs": Locateur.objects.all().values()})


def register(request):
    if request.method == "GET":
        return render(request, "django_app/register.html", {"towns": ville.objects.all().values('name')})
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        town = request.POST.get("town")
        profil = request.POST.get("profil")
        if (profil == "locataire"):
            user = User(username=username, password=make_password(password))
            user.save()
            locataire = Locataire(user.pk, gender=gender, town=town)
            locataire.save()
        if (profil == "locateur"):
            user = User(username=username, password=make_password(password))
            user.save()
            locateur = Locateur(user.pk, gender=gender, town=town)
            locateur.save()

        return render(request, "django_app/register.html", {"status": True})



#@api_view(["POST"])
def login(request):
    username = request.data["username"]
    password = request.data["password"]

    user = User.objects.filter(username=username)

    if user.exists():
        auth_success = check_password(password, user.first().password)

        if auth_success:
            token = Token.objects.filter(user=user.first())

            if token.exists(): 
                return render(request, "django_app/home.html", {"token": "Token {}".format(token.first().key)})
            else:
                token = Token.objects.create(user=user.first())
                return Response(
                    {"token": "Token {}".format(token.key)}, status=status.HTTP_200_OK
                )
        else:
            return Response(
                {"message": "Mot de passe incorrect !"},
                status=status.HTTP_404_NOT_FOUND,
            )
    else:
        return Response(
            {"message": "L'utilisateur n'existe pas !"},
            status=status.HTTP_404_NOT_FOUND,
        )


#@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout(request):
    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]

    invalidated_token = Token.objects.filter(key=token_key).first()
    invalidated_token.delete()

    return Response(
        {"message": "Deconnexion effectuée avec succès !"}, status=status.HTTP_200_OK
    )

def statistics(request):
    return render(request, "django_app/statistics.html")


#@swagger_auto_schema(method="get", tags=["Villes"])
#@api_view(["GET"])
def towns(request):
    all_towns = ville.objects.all().values('name')
    return Response(
                    all_towns, status=status.HTTP_200_OK
                )



