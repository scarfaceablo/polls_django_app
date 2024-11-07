from django.contrib.auth.models import User, Group
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def has_permission(self, user, permission_type):
        try:
            permission = QuestionPermission.objects.get(question=self, user=user)
            if permission_type == "view":
                return permission.can_view
            elif permission_type == "edit":
                return permission.can_edit
        except QuestionPermission.DoesNotExist:
            return False

        # check if user's group has permission
        user_groups = user.groups.all()
        group_permissions = QuestionPermission.objects.filter(question=self, group__in=user_groups)
        if group_permissions.exists():
            if permission_type == "view":
                return group_permissions.filter(can_view=True).exists()
            elif permission_type == "edit":
                return group_permissions.filter(can_edit=True).exists()
        return False


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', blank=True)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def has_permission(self, user, permission_type):
        # check question's permission
        return self.question.has_permission(user, permission_type)


class QuestionPermission(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)

    class Meta:
        unique_together = ['question', 'user', 'group']
