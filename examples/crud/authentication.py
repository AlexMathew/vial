from functools import wraps

from .models import User


class AuthenticationService:
    def get_profile_from_token(self, token):
        user = User.get(where={'auth_token': token})
        if not user:
            raise Exception("No profile for this token")

        return user

    def is_maintainer(self, user):
        if not user.get('maintainer', ''):
            raise Exception("Not a maintainer profile")

    def is_authenticated(self, func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                token = request.headers.get('authorization', '').replace("Bearer", "").strip()

                if not token:
                    raise Exception("No auth_token in header")

                user = self.get_profile_from_token(token)
                self.is_maintainer(user)

            except Exception as e:
                return {"status": 401, "message": str(e), "success": False}

            return func(request, *args, **kwargs)

        return wrapper
