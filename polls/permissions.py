from django.http import HttpResponseForbidden
from rest_framework.exceptions import PermissionDenied

from polls.models import Question, Choice


class QuestionPermissionMixin:
    def has_permission(self, obj, permission_type):
        user = self.request.user
        if isinstance(obj, Question):
            return obj.has_permission(user, permission_type)
        elif isinstance(obj, Choice):
            return obj.question.has_permission(user, permission_type)
        return False

    def dispatch(self, request, *args, **kwargs):
        """
        Overrides dispatch to add a permission check for each request.
        """
        permission_type = "edit" if self.request.method in ["POST", "PUT", "PATCH", "DELETE"] else "view"

        # Check permission on the object
        if not self.has_permission(self.get_object(), permission_type):
            raise HttpResponseForbidden("You do not have permission to access this resource.")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        Overrides get_object to add a permission check for each request.
        """
        obj = super().get_object()  # Get the object
        permission_type = "edit" if self.request.method in ["POST", "PUT", "PATCH", "DELETE"] else "view"

        # Check permission on the object
        if not self.has_permission(obj, permission_type):
            raise PermissionDenied("You do not have permission to access this resource.")

        return obj  # Return the object if permission is granted
