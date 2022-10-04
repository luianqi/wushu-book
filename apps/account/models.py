from datetime import date

from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, **extra_fields):
        """
        Methode creates user
        :param email: str
        :param name: str
        :param surname: str
        :param extra_fields: dict
        :return: user
        """
        if not email:
            raise ValueError("Вы должны ввести свою электронную почту")
        if not name or not surname:
            raise ValueError("Вы должны ввести свое Имя/Фамилию")

        user = self.model(
            email=email,
            name=name,
            surname=surname,
            **extra_fields
        )
        user.set_password()
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Methode creates superuser
        :param email: str
        :param password: str
        :return: superuser
        """
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.role = 1
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""

    ADMIN = 'ADMIN'
    TRAINER = 'TRAINER'
    CHOICES = [
        (ADMIN, "Администратор"),
        (TRAINER, "Тренер"),
    ]

    name = models.CharField(max_length=30, blank=False, null=False)
    surname = models.CharField(max_length=20, blank=False, null=False)
    number = models.CharField(max_length=20, unique=True, null=False)
    email = models.CharField(max_length=30, blank=False, unique=True, null=False)
    # club = models.ForeignKey('Club', on_delete=models.DO_NOTHING, blank=True, null=True)
    role = models.CharField(max_length=30, choices=CHOICES, default=TRAINER)
    achievements = models.TextField(default=None, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    referral_token = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True)
    is_judge = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def save(self, *args, **kwargs):
        self.referral_token = f'{self.email}&{get_random_string(length=30)}'
        super().save(*args, **kwargs)


class Referral(models.Model):
    """
    For capturing who referred whom.
    """
    referred_by = models.ForeignKey(User, unique=False, on_delete=models.DO_NOTHING, related_query_name='my_referral')
    referred_to = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_query_name='has_referred')


class Feedback(models.Model):
    """Feedback model"""

    email = models.EmailField()
    phone = models.CharField(max_length=255)
    text = models.TextField()
    is_applied = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.phone, self.email}'


class Club(models.Model):
    """CLub model"""
    address = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=30, blank=True)
    min_age = models.IntegerField(blank=False, null=False, default=0)
    max_age = models.IntegerField(blank=False, null=False, default=100)

    def __str__(self):
        return f'{self.name}'

    @property
    def sum_of_people(self):
        return Athlete.objects.filter(club=self.pk).count()


class UserClub(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, null=False)


class PhysicalIndicators(models.Model):
    agility = models.DecimalField(max_digits=4, decimal_places=2)
    strength = models.DecimalField(max_digits=4, decimal_places=2)
    stamina = models.DecimalField(max_digits=4, decimal_places=2)
    speed = models.DecimalField(max_digits=4, decimal_places=2)
    stretch = models.DecimalField(max_digits=4, decimal_places=2)


class Athlete(models.Model):
    female = 1
    male = 2
    CHOICES = [
        (female, "Женский"),
        (male, "Мужской"),
    ]
    children_1 = 1
    children_2 = 2
    children_3 = 3
    adult_1 = 4
    adult_2 = 5
    adult_3 = 6
    CMS = 7
    MS = 8
    MSIC = 9
    CATEGORIES = [
        (children_1, "1-й Детский разряд"),
        (children_2, "2-й Детский разряд"),
        (children_3, "3-й Детский разряд"),
        (adult_1, "1-й Взрослый разряд"),
        (adult_2, "2-й Взрослый разряд"),
        (adult_3, "3-й Взрослый разряд"),
        (CMS, "Кандидат в Мастера Спорта"),
        (MS, "Мастер Спорта"),
        (MSIC, "Мастер Спорта международного класса")
    ]
    name = models.CharField(max_length=30, blank=False, null=False)
    surname = models.CharField(max_length=20, blank=False, null=False)
    phone_number = models.CharField(max_length=20, unique=True, null=False)
    achievements = models.CharField(max_length=400, blank=True, null=True)
    birthday = models.DateField(default=None, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    sex = models.IntegerField(choices=CHOICES, default=female)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)
    medical_certificate = models.ImageField(default=None, blank=True, null=True)
    physical_indicators = models.OneToOneField('PhysicalIndicators', on_delete=models.CASCADE, blank=True, null=True)
    sport_category = models.IntegerField(choices=CATEGORIES, default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.phone_number}'

    @property
    def average_of_PHI(self):
        phy = self.physical_indicators
        average_of_PHI = (phy.agility + phy.strength + phy.stamina + phy.speed + phy.stretch) / 5
        return average_of_PHI

    @property
    def age(self):
        age = int((date.today() - self.birthday).days / 365.2425)
        return age
