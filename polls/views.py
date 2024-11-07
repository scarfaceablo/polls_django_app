from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets

from polls.models import Question, QuestionPermission
from polls.permissions import QuestionPermissionMixin
from polls.serializers import QuestionSerializer


# Create your views here.

@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class QuestionViewSet(QuestionPermissionMixin, viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Question.objects.filter(pk__in=[
            question_permission.question_id for question_permission in
            QuestionPermission.objects.filter(user=self.request.user)
        ])
