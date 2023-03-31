from django.contrib.auth.backends import ModelBackend

# Check if a user can authenticate
class AdminBackend(ModelBackend):
    """ Override authentication form """
    def user_can_authenticate(self, user) -> bool:
        can_authenticate = super().user_can_authenticate(user)
        return can_authenticate
        