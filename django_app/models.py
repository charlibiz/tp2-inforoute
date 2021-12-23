from django.db import models
from django.contrib.auth.models import User

#from django_app.views import users
# Create your models here. 


class Reservation(models.Model):
    STATUS_CHOICES = [
    ('p', 'Pending'),
    ('A', 'Active'),
    ('E', 'Expired'),
    ]
    id = models.AutoField(primary_key=True)
    room = models.IntegerField()
    tenant = models.IntegerField()
    landlord = models.IntegerField()
    nbr_persons = models.IntegerField()
    in_date = models.DateField()
    out_date =models.DateField()
    total_price = models.FloatField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

# class Utilisateur(models.Model):
#     identifiant = models.AutoField(primary_key=True)
#     first_name= models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     mail_adresse = models.EmailField(max_length=50)
#     birth_date = models.DateTimeField()
#     gender = models.CharField(max_length=50)
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)



class Chambre(models.Model):
    id = models.AutoField(primary_key=True)
    town = models.CharField(max_length=50)
    landlord = models.IntegerField()
    capacity = models.IntegerField()
    price = models.FloatField()


class Locateur(models.Model):
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    chambre = models.ForeignKey("Chambre",on_delete=models.CASCADE)
    benefits = models.FloatField()
    #birth_date = models.DateField()
    town = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


class Locataire(models.Model):
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    reservation = models.ForeignKey("Reservation",on_delete=models.CASCADE)
    balance = models.FloatField()
    #birth_date = models.DateField()
    town = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


class ville(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.FloatField()
    #chambre = models.ForeignKey("Chambre",on_delete=models.CASCADE)

   


   