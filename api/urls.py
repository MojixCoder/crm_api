from django.urls import path, include


app_name = "api"

urlpatterns = [
    path("v1/accounts/", include("account.urls")),
]
