from django.urls import path
from .views import home, users, register, login, logout, statistics, towns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Swagger pour TP2",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", home, name="home"),
    path("users", users, name="users"),
    path("register", register, name="register"),
    path("login", login, name="login"),
    path("logout", logout, name="logout"),
    path("statistics", statistics, name="statistics"),
    #path("api/towns", towns, name="towns"),
    #path("api/user", user, name="user"),
    #path("api/swagger", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]