from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()

urlpatterns = [
    path(r'accounts/', include((router.urls, 'accounts'))),
    path(r'accounts/token/', TokenObtainPairViewCustom.as_view(), name='token_obtain_pair'),
    path(r'accounts/token/refresh/', TokenRefreshViewCustom.as_view(), name='token_refresh'),
    path(r'accounts/logout/', BlackListRefreshView.as_view(), name='logout'),

    path('send-verification-code/', SendVerificationCodeView.as_view(), name='send_verification_code'),
    path('validate-verification-code/', ValidateVerificationCodeView.as_view(), name='validate_verification_code'),

    path('accounts/password-reset/code/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('accounts/password-reset/verify/', PasswordResetVerifyView.as_view(), name='password-reset-verify'),
    path('accounts/password-reset/', PasswordResetView.as_view(), name='password-reset'),

]