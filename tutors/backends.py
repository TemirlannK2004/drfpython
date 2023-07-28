from django.contrib.auth.backends import ModelBackend
from .models import TutorUser, ClientUser

class MultiUserModelBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = TutorUser.objects.get(email=email)
        except TutorUser.DoesNotExist:
            try:
                user = ClientUser.objects.get(email=email)
            except ClientUser.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None