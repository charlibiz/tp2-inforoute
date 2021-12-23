from rest_framework.response import Response
from rest_framework import status, viewsets

from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.core import serializers

from django_app.models import  Chambre, Reservation
from django.contrib.auth.models import User
from django_app.models import ville, Locateur, Locataire
from .serializers import UserSerializer, RoomSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


@swagger_auto_schema(method="get", tags=["Villes"])
@api_view(["GET"])
def towns(request):
    all_towns = ville.objects.all().values('name')
    return Response(
                    all_towns, status=status.HTTP_200_OK
                )


@swagger_auto_schema(method="get", tags=["Utilisateur"])
@swagger_auto_schema(method="put", tags=["Utilisateur"])
@api_view(["GET", "PUT"])
def user(request):
    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    id = Token.objects.filter(key=token_key).first().user_id
    user = User.objects.filter(id=id)
    if (Locataire.objects.filter(user_id=id)):
        profil = Locataire.objects.filter(user_id=id).profil
    if (Locateur.objects.filter(user_id=id)):
        profil = Locateur.objects.filter(user_id=id).profil
    return Response(
                    user, profil, status=status.HTTP_200_OK
                )



@swagger_auto_schema(method="get", tags=["Rooms"])
@swagger_auto_schema(method="post", tags=["Rooms"], request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, properties={
        "town": openapi.Schema(type=openapi.TYPE_STRING, description='Ville dans laquelle se situe la chambre'),
        "landlord": openapi.Schema(type=openapi.TYPE_INTEGER, description='ID du locateur'),
        "capacity": openapi.Schema(type=openapi.TYPE_INTEGER, description='Capacité de la chambre'), 
        "price": openapi.Schema(type=openapi.TYPE_NUMBER, description='Prix quotidien de la chambre'),
        }))
@api_view(["GET", "POST"])
def rooms(request):
    if request.method == "GET":
        rooms_list = Chambre.objects.all()
        return Response(
            {"rooms": rooms_list.values()},
            status=status.HTTP_200_OK,
            )
    if request.method == "POST":
        town = request.data["town"]
        capacity = request.data["capacity"]
        price = request.data["price"]
        landlord_id = request.data["landlord"]
        room = Chambre(town=town, capacity=capacity, price=price, landlord=landlord_id)
        room.save()
        rooms_list = Chambre.objects.all()
        return Response(
            {"rooms": rooms_list.values()},
            status=status.HTTP_200_OK,
            )


@swagger_auto_schema(method="get", tags=["Room"], operation_description="GET api/room/{id}", manual_parameters=[openapi.Parameter('room_id', in_=openapi.IN_PATH, description='ID de la chambre', type=openapi.TYPE_INTEGER)])
@swagger_auto_schema(method="put", tags=["Room"], request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, properties={
        "town": openapi.Schema(type=openapi.TYPE_STRING, description='Ville dans laquelle se situe la chambre'),
        "landlord": openapi.Schema(type=openapi.TYPE_INTEGER, description='ID du locateur'),
        "capacity": openapi.Schema(type=openapi.TYPE_INTEGER, description='Capacité de la chambre'), 
        "price": openapi.Schema(type=openapi.TYPE_NUMBER, description='Prix quotidien de la chambre'),
        }))
@swagger_auto_schema(method="delete", tags=["Room"], manual_parameters=[openapi.Parameter('room_id', in_=openapi.IN_PATH, description='ID de la chambre', type=openapi.TYPE_INTEGER)])
@api_view(["GET", "PUT", "DELETE"])
def room(request, *args, **kwargs):
    pk = kwargs.get('room_id')
    if request.method == "GET":
        room = Chambre.objects.filter(id=pk)
        return Response(
            {"room":room.values()},
            status=status.HTTP_200_OK,
            )
    if request.method == "PUT":
        town = request.data["town"]
        capacity = request.data["capacity"]
        price = request.data["price"]
        landlord_id = request.data["landlord"]
        room = Chambre(id=pk, town=town, capacity=capacity, price=price, landlord=landlord_id)
        room.save()
        rooms_list = Chambre.objects.all()
        return Response(
        {"rooms": rooms_list.values()},
        status=status.HTTP_200_OK,
        )
    if request.method == "DELETE":
        room = Chambre.objects.filter(id=pk).first()
        room.delete()
        rooms_list = Chambre.objects.all()
        return Response(
        {"rooms": rooms_list.values()},
        status=status.HTTP_200_OK,
        )


@swagger_auto_schema(method="get", tags=["Reservations"])
@swagger_auto_schema(method="post", tags=["Reservations"], request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, properties={
        "room": openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la chambre'),
        "tenant": openapi.Schema(type=openapi.TYPE_INTEGER, description='ID du locataire'),
        "landlord": openapi.Schema(type=openapi.TYPE_INTEGER, description='ID du locateur'),
        "nbr_persons": openapi.Schema(type=openapi.TYPE_INTEGER, description='Nombre de personnes dans la réservation'),
        "in_date": openapi.Schema(type=openapi.FORMAT_DATE, description='Nombre de personnes dans la réservation'),
        "out_date": openapi.Schema(type=openapi.FORMAT_DATE, description='Nombre de personnes dans la réservation'),
        "total_price": openapi.Schema(type=openapi.TYPE_NUMBER, description='Prix total'),
        "satus": openapi.Schema(type=openapi.TYPE_STRING, description='Status de la réservation'),
        }))
@api_view(["GET", "POST"])
def reservations(request):
    if request.method == "GET":
        reservations_list = Reservation.objects.all()
        return Response(
            {"reservations": reservations_list.values()},
            status=status.HTTP_200_OK,
            )
    if request.method == "POST":
        room = request.data["room"]
        tenant_id = request.data["tenant"]
        landlord_id = request.data["landlord"]
        nbr_persons = request.data["nbr_persons"]
        in_date = request.data["in_date"]
        out_date = request.data["out_date"]
        total_price = request.data["total_price"]
        reservation = Reservation(room=room, tenant=tenant_id, landlord=landlord_id, nbr_persons=nbr_persons, in_date=in_date, out_date=out_date, total_price=total_price)
        reservation.save()
        reservations_list = Reservation.objects.all()
        return Response(
            {"reservations": reservations_list.values()},
            status=status.HTTP_200_OK,
            )


@swagger_auto_schema(method="get", tags=["Reservation"], operation_description="GET api/reservation/{id}", manual_parameters=[openapi.Parameter('reservation_id', in_=openapi.IN_PATH, description='ID de la chambre', type=openapi.TYPE_INTEGER)])
@swagger_auto_schema(method="put", tags=["Reservation"], request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, properties={
        "room": openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la chambre'),
        "tenant": openapi.Schema(type=openapi.TYPE_INTEGER, description='ID du locataire'),
        "landlord": openapi.Schema(type=openapi.TYPE_INTEGER, description='ID du locateur'),
        "nbr_persons": openapi.Schema(type=openapi.TYPE_INTEGER, description='Nombre de personnes dans la réservation'),
        "in_date": openapi.Schema(type=openapi.FORMAT_DATE, description='Nombre de personnes dans la réservation'),
        "out_date": openapi.Schema(type=openapi.FORMAT_DATE, description='Nombre de personnes dans la réservation'),
        "total_price": openapi.Schema(type=openapi.TYPE_NUMBER, description='Prix total'),
        "satus": openapi.Schema(type=openapi.TYPE_STRING, description='Status de la réservation'),
        }))
@swagger_auto_schema(method="delete", tags=["Reservation"], manual_parameters=[openapi.Parameter('reservation_id', in_=openapi.IN_PATH, description='ID de la chambre', type=openapi.TYPE_INTEGER)])
@api_view(["GET", "PUT", "DELETE"])
def reservation(request, *args, **kwargs):
    pk = kwargs.get('reservation_id')
    if request.method == "GET":
        reservation = Reservation.objects.filter(id=pk)
        return Response(
            {"reservation":reservation.values()},
            status=status.HTTP_200_OK,
            )
    if request.method == "PUT":
        room = request.data["room"]
        tenant_id = request.data["tenant"]
        landlord_id = request.data["landlord"]
        nbr_persons = request.data["nbr_persons"]
        in_date = request.data["in_date"]
        out_date = request.data["out_date"]
        total_price = request.data["total_price"]
        reservation = Reservation(id=pk, room=room, tenant=tenant_id, landlord=landlord_id, nbr_persons=nbr_persons, in_date=in_date, out_date=out_date, total_price=total_price)
        reservation.save()
        reservations_list = Reservation.objects.all()
        return Response(
            {"reservations": reservations_list.values()},
            status=status.HTTP_200_OK,
            )
    if request.method == "DELETE":
        reservation = Reservation.objects.filter(id=pk).first()
        reservation.delete()
        reservations_list = Reservation.objects.all()
        return Response(
        {"reservations": reservations_list.values()},
        status=status.HTTP_200_OK,
        )
