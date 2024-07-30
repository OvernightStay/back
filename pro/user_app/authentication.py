from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

Player = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(Player.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            if '@' in username:
                player = Player.objects.get(email=username)
            else:
                player = Player.objects.get(phone=username)
        except Player.DoesNotExist:
            return
        
        if player.check_password(password) and self.user_can_authenticate(player):
            return player
        return None

def get_backend_name():
    return 'user_app.authentication.EmailOrPhoneBackend'
