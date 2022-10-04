from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from apps.account.models import Feedback, User, Referral, Club, Athlete, PhysicalIndicators, UserClub
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            "id",
            "email",
            "phone",
            "text",
        ]


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    referral_code = serializers.CharField(max_length=255, write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "number",
            "name",
            "surname",
            "password",
            "referral_code",
            "role",
            "achievements",
            "address",
        ]
        read_only_fields = ['is_confirmed']
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """
        Creates new user with/without referral code.
        """

        referred_by = ''
        referral_code = validated_data.pop('referral_code')
        try:
            referred_by = User.objects.get(referral_token=referral_code)
        except ObjectDoesNotExist:
            pass
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        if referred_by:
            referral = Referral.objects.create(referred_by=referred_by, referred_to=user)
            referral.save()
        return user


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password"
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'groups',
            'user_permissions',
        ]
        read_only_fields = [
            'last_login',
            'is_superuser',
            'referral_token',
        ]
        extra_kwargs = {
            "password": {"required": False},
        }


class ClubSerializer(serializers.ModelSerializer):
    sum_of_people = serializers.IntegerField()

    class Meta:
        model = Club
        fields = '__all__'
        read_only_fields = ['sum_of_people']


class PhysicalIndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalIndicators
        fields = '__all__'


class AthleteSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    average_of_PHI = serializers.DecimalField(max_digits=9, decimal_places=1, read_only=True)
    physical_indicators = PresentablePrimaryKeyRelatedField(queryset=PhysicalIndicators.objects.all(),
                                                            presentation_serializer=PhysicalIndicatorsSerializer)
    club = PresentablePrimaryKeyRelatedField(queryset=Club.objects.all(),
                                             presentation_serializer=ClubSerializer)

    class Meta:
        model = Athlete
        fields = '__all__'


class UserClubSerializer(serializers.ModelSerializer):
    user = PresentablePrimaryKeyRelatedField(queryset=User.objects.all(),
                                             presentation_serializer=RegisterUserSerializer)
    club = PresentablePrimaryKeyRelatedField(queryset=Club.objects.all(),
                                             presentation_serializer=ClubSerializer)

    class Meta:
        model = UserClub
        fields = '__all__'
