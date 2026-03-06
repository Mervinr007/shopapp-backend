from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required

@login_required
def google_callback_complete(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    refresh_token = str(refresh)
    return redirect(
        f'http://localhost:4200/oauth/callback'
        f'?access={access}'
        f'&refresh={refresh_token}'
    )
    