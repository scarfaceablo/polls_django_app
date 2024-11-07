from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from polls.models import Question, Choice


# Create your tests here.
class PermissionsTestCase(TestCase):
    def setUp(self):
        # create 2 users
        self.user_a = User.objects.create_user(username="user_a", password="password")
        self.user_b = User.objects.create_user(username="user_b", password="password")

        # create 2 groups
        self.group_a = Group.objects.create(name="group_a")
        self.group_b = Group.objects.create(name="group_b")

        # add users to groups
        self.user_a.groups.add(self.group_a)
        self.user_b.groups.add(self.group_b)

        # create a question 1
        self.question_1 = Question.objects.create(question_text="Question 1 ?", pub_date=timezone.now())

        # create choices
        self.question_1.choices.create(choice_text="Choice 1")
        self.question_1.choices.create(choice_text="Choice 2")

        # create permissions
        for group in self.user_a.groups.all():
            self.question_1.permissions.create(user=self.user_a, group=group, can_view=True, can_edit=True)

        # create a question 2
        self.question_2 = Question.objects.create(question_text="Question 2 ?", pub_date=timezone.now())

        # create choices
        self.question_2.choices.create(choice_text="Choice 3")
        self.question_2.choices.create(choice_text="Choice 4")

        # create permissions
        for group in self.user_b.groups.all():
            self.question_2.permissions.create(user=self.user_b, group=group, can_view=True, can_edit=True)

    def test_user_a_can_modify_question_1(self):
        self.assertTrue(self.question_1.has_permission(self.user_a, "edit"))

    def test_user_b_can_modify_question_2(self):
        self.assertTrue(self.question_2.has_permission(self.user_b, "edit"))

    def test_user_a_cannot_modify_question_2(self):
        self.assertFalse(self.question_2.has_permission(self.user_a, "edit"))

    def test_user_b_cannot_modify_question_1(self):
        self.assertFalse(self.question_1.has_permission(self.user_b, "edit"))


class PollsApiTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="testpass")
        self.client = APIClient()
        self.client.login(username="test_user", password="testpass")

        self.group = Group.objects.create(name="test_group")

        self.user.groups.add(self.group)

        self.question = Question.objects.create(question_text="What's your favorite color?", pub_date=timezone.now())
        self.choice = Choice.objects.create(question=self.question, choice_text="Blue")

        # create permissions
        for group in self.user.groups.all():
            self.question.permissions.create(user=self.user, group=group, can_view=True, can_edit=True)

        self.list_url = reverse('polls:question-list')
        self.detail_url = reverse('polls:question-detail', args=[self.question.id])

    def test_create_question(self):
        data = {
            "question_text": "What is your favorite programming language?",
            "pub_date": timezone.now(),
            "choices": [{"choice_text": "Python"}, {"choice_text": "JavaScript"}]
        }

        res = self.client.post(self.list_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Choice.objects.filter(question__question_text=data['question_text']).count(), 2)

    def test_update_question(self):
        data = {
            "question_text": "Updated question text?",
            "pub_date": timezone.now(),
            "choices": [
                {"id": self.choice.id, "choice_text": "Updated Choice Text"},
                {"choice_text": "New Choice"}
            ]
        }
        res = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.question.refresh_from_db()

        self.assertEqual(self.question.question_text, "Updated question text?")
        self.assertEqual(self.question.choices.count(), 2)

    def test_retrieve_question(self):
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['question_text'], self.question.question_text)
        self.assertIn('choices', res.data)
        self.assertEqual(len(res.data['choices']), 1)

    def test_delete_question(self):
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Choice.objects.count(), 0)
