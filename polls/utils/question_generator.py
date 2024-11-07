# setup django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polls_django_app.settings')
import django

django.setup()

import random

from django.contrib.auth.models import User
from django.utils import timezone

from polls.models import Question


class QuestionGenerator:
    def __init__(self):
        pass

    def generate_question(self):

        """
        Generate a single question with random number of choices
        and assign permissions for this question to a random user
        :return:
        """

        random_int = random.randint(1, 100)

        question = Question.objects.create(
            question_text=f"Question {random_int} ?",
            pub_date=timezone.now()
        )

        random_nr_or_choices = random.randint(2, 5)
        for i in range(1, random_nr_or_choices):
            question.choices.create(
                choice_text=f"Choice {i}"
            )

        users = User.objects.filter(is_superuser=False, is_staff=False).all()

        # pick a random user
        random_user = random.choice(users)

        for group in random_user.groups.all():
            question.permissions.create(user=random_user, group=group, can_view=True, can_edit=True)
