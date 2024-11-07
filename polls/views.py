from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
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


class IndexView(TemplateView):
    template_name = "index.html"


class QuestionsView(TemplateView):
    template_name = "questions.html"
    queryset = Question.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get('type') == 'my':
            self.queryset = self.queryset.filter(pk__in=[
                question_permission.question_id for question_permission in
                QuestionPermission.objects.filter(user=self.request.user)
            ])

        context['questions'] = self.queryset
        context['type'] = self.kwargs.get('type')
        return context
