from django.urls import path, include
from rest_framework import routers

from polls import views
from polls.views import QuestionsView, IndexView

router = routers.DefaultRouter()
router.register(r"questions", views.QuestionViewSet, basename="question")

app_name = "polls"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("questions/", QuestionsView.as_view(), name="questions"),
    path("questions/<str:type>/", QuestionsView.as_view(), name="my-questions"),
    path("api/", include(router.urls)),
]
