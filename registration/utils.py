import random
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError

def generate_otp():
    return random.randint(100000, 999999)

def get_token_for_user(user):
    if user.refresh_token and user.access_token:
        try:
            AccessToken(user.access_token)
            return {
                "access_token":user.access_token,
                "refresh_token":user.refresh_token
            }
            
        except TokenError:
            pass
        
        refresh = RefreshToken.for_user(user)
        user.access_token = str(refresh.access_token)
        user.refresh_token = str(refresh)
        
        user.save()
        
        return {
                "access_token":user.access_token,
                "refresh_token":user.refresh_token
            }
        