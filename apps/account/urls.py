from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.account.views import (
    FeedbackView,
    RegisterUserView,
    LoginUserView,
    UserProfileView,
    ClubView,
    PhysicalIndicatorsView,
    AthleteView,
    UserClubView,
)


router = DefaultRouter()
router.register(r'feedback', FeedbackView)
router.register('club', ClubView)
router.register('user', UserProfileView)
router.register('user_club', UserClubView)
router.register('athletes', AthleteView)
router.register('physical_indicators', PhysicalIndicatorsView)

urlpatterns = [
    path('', include(router.urls)),
    path("registration/", RegisterUserView.as_view(), name="create_user"),
    path("login/", LoginUserView.as_view(), name="login_user"),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset_by_email')),
]