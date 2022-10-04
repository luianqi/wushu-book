from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins

from django_filters.rest_framework import DjangoFilterBackend

from apps.account.models import (
    User,
    Feedback,
    Club,
    Athlete,
    PhysicalIndicators,
    UserClub,
)
from apps.account.serializers import (
    RegisterUserSerializer,
    UserProfileSerializer,
    LoginUserSerializer,
    FeedbackSerializer,
    ClubSerializer,
    AthleteSerializer,
    PhysicalIndicatorsSerializer,
    UserClubSerializer
)


class RegisterUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()


class LoginUserView(CreateAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("Пользователь с такими учетными данными не найден!")
        if user.is_active is False:
            raise AuthenticationFailed("Ваша учетная запись еще не подтверждена администратором!")
        if not user.check_password(password):
            raise AuthenticationFailed("Неверный пароль!")

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": "Вы, успешно авторизовались!",
                "user_id": str(user.id),
                "user role": str(user.role),
                "assistant": str(user.is_assistant),
                "judge": str(user.is_judge),
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class UserProfileView(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['is_assistant', 'is_judge', 'role', 'is_active']
    search_fields = ['name', 'surname', 'email', 'number']

    def partial_update(self, request, *args, **kwargs):
        """Updating user profile data and profile password"""

        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            if instance.password:
                instance.set_password(instance.password)
                instance.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class FeedbackView(ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['is_applied']
    search_fields = ['email', 'phone']


class ClubView(ModelViewSet):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'address']


class AthleteView(ModelViewSet):
    serializer_class = AthleteSerializer
    queryset = Athlete.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['club', 'sport_category', 'sex']
    search_fields = ['name', 'surname', 'phone_number', 'address']


class PhysicalIndicatorsView(ModelViewSet):
    serializer_class = PhysicalIndicatorsSerializer
    queryset = PhysicalIndicators.objects.all()


class UserClubView(ModelViewSet):
    serializer_class = UserClubSerializer
    queryset = UserClub.objects.all()
     
    def retrieve(self, request, pk):
        queryset = UserClub.objects.filter(club=pk)
        serializer_class = UserClubSerializer(queryset, many=True)
        return Response(serializer_class.data)