from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.utils import timezone

from polls.models import Question


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
        self.question_1.choice_set.create(choice_text="Choice 1")
        self.question_1.choice_set.create(choice_text="Choice 2")

        # create permissions
        for group in self.user_a.groups.all():
            self.question_1.questionpermission_set.create(user=self.user_a, group=group, can_view=True, can_edit=True)

        # create a question 2
        self.question_2 = Question.objects.create(question_text="Question 2 ?", pub_date=timezone.now())

        # create choices
        self.question_2.choice_set.create(choice_text="Choice 3")
        self.question_2.choice_set.create(choice_text="Choice 4")

        # create permissions
        for group in self.user_b.groups.all():
            self.question_2.questionpermission_set.create(user=self.user_b, group=group, can_view=True, can_edit=True)

    def test_user_a_can_modify_question_1(self):
        self.assertTrue(self.question_1.has_permission(self.user_a, "edit"))

    def test_user_b_can_modify_question_2(self):
        self.assertTrue(self.question_2.has_permission(self.user_b, "edit"))

    def test_user_a_cannot_modify_question_2(self):
        self.assertFalse(self.question_2.has_permission(self.user_a, "edit"))

    def test_user_b_cannot_modify_question_1(self):
        self.assertFalse(self.question_1.has_permission(self.user_b, "edit"))
