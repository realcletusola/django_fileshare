from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    SignUpRequest,SignInRequest,SignOutRequest,
    ChangePasswordRequest
)

urlpatterns = [
    path('signup/', SignUpRequest.as_view(), name='signup'),
    path('signin/', SignInRequest.as_view(), name='signin'),
    path('signout/', SignOutRequest.as_view(), name='signout'),
    path('change_password/', ChangePasswordRequest.as_view(), name='change_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)