from django.contrib.auth.models import User, Group
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        # create groups
        for group in ["group_a", "group_b"]:
            if not Group.objects.filter(name=group).exists():
                group = Group.objects.create(name=group)

        for user in ["user_a", "user_b", "user_c"]:
            if not User.objects.filter(username=user).exists():
                user = User.objects.create_user(user)
                user.set_password("password")
                user.save()

        # add users to groups
        for user in User.objects.all():
            if user.username == "user_a":
                user.groups.add(Group.objects.get(name="group_a"))
            elif user.username == "user_b":
                user.groups.add(Group.objects.get(name="group_b"))
            else:
                user.groups.add(Group.objects.get(name="group_a"))
                user.groups.add(Group.objects.get(name="group_b"))
            user.save()
