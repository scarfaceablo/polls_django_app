from django.urls import path, include
from rest_framework import routers

from polls import views

router = routers.DefaultRouter()
router.register(r"questions", views.QuestionViewSet, basename="question")

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include(router.urls)),
]
