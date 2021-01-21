from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.contrib.auth import get_user_model


class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None,**kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user:
            return user
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD, kwargs.get('email'))
        try:
            user = UserModel._default_manager.get(email=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
