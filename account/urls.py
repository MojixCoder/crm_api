from django.contrib.auth.models import UserManager
from django.urls import path, include
from .apis import UserViewSet
from .routers import UserRouter


app_name = "account"

router = UserRouter()

router.register("", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),   
]
