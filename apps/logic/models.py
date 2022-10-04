from django.db import models

from apps.account.models import User, Club, Athlete


class Event(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    start_datetime = models.DateTimeField()
    finish_datetime = models.DateTimeField()
    place = models.CharField(max_length=100, blank=False, null=False)
    lead_judge = models.ForeignKey(User, on_delete=models.PROTECT, related_name='event_lead_judge', blank=True,
                                   null=True)
    assistant = models.ForeignKey(User, on_delete=models.PROTECT, related_name='event_assistant', blank=True, null=True)
    note = models.TextField(default=None, blank=True, null=True)
    is_protocoled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name},{self.start_datetime},{self.finish_datetime}'


class AgeGroup(models.Model):
    name = models.CharField(max_length=100)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    event = models.ForeignKey(Event, related_name='age_groups', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ['event', 'name']
        ordering = ['name']

    def __str__(self):
        return f'{self.event},{self.name}'


class Discipline(models.Model):
    traditional = 1
    sport = 2
    dueling = 3
    CHOICES = [
        (traditional, "Традиционное"),
        (sport, "Спортивное"),
        (dueling, "Дуэлянь")
    ]
    category = models.IntegerField(choices=CHOICES, default=traditional)
    is_individual = models.BooleanField(default=True)
    with_weapon = models.BooleanField(default=False)
    duration = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.category},{self.is_individual},{self.with_weapon}'


class TemplateApplication(models.Model):
    trainers = models.ManyToManyField(User)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    discipline_1 = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='cuanshu')
    discipline_2 = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='cise')

    def __str__(self):
        return f'{self.event}'


class Application(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, blank=True, null=True)
    dueling_partner = models.ForeignKey(Athlete, on_delete=models.CASCADE, null=True, blank=True)
    team_number = models.IntegerField(default=None, blank=True, null=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    is_confirmed = models.BooleanField(null=True, blank=True)
    cuanshu = models.BooleanField(default=False)
    cise = models.BooleanField(default=False)
    taizi_cuanshu = models.BooleanField(default=False)
    taizi_cise = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.trainer},{self.event}'


class AthleteApplication(models.Model):
    athlete = models.ForeignKey(Athlete, related_name='athlete_application', on_delete=models.CASCADE)
    application = models.ForeignKey(Application, related_name='application_athlete', on_delete=models.CASCADE)
    event_age_group = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        age_group = AgeGroup.objects.filter(event=self.application.event)
        for i in age_group:
            if self.athlete.age in range(i.min_age, i.max_age + 1):
                self.event_age_group = f'{i.min_age}-{i.max_age} лет'
            else:
                continue
        super().save(*args, **kwargs)


class Subgroup(models.Model):
    female = 1
    male = 2
    unknown = 3
    CHOICES = [
        (female, "Женский"),
        (male, "Мужской"),
        (unknown, "Неизвестно"),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, limit_choices_to={'is_protocoled': False})
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True, blank=True)
    sex = models.IntegerField(choices=CHOICES, default=unknown)
    age_group = models.CharField(max_length=255, null=True, blank=True)
    areas_quantity = models.IntegerField(default=1)
    top_places_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    rejection_reason = models.CharField(max_length=500, null=True, blank=True)
    is_confirmed = models.BooleanField(null=True, blank=True)
    start_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.event},{self.discipline},{self.age_group},{self.sex}'

    @property
    def athlete_count(self):
        return SubgroupApplication.objects.filter(subgroup=self.pk).count()

    @property
    def child_status(self):
        result = self.age_group.find('12')
        if result >= 0:
            return 1
        else:
            return 2

    @property
    def width_length(self):

        c = self.areas_quantity
        b1 = 10000
        a1 = 0
        for a in range(1, c + 1):
            if c % a == 0:
                b = c // a
                if a != b and abs(b - a) <= abs(b1 - a1) or a == 1 and b == 1:
                    a1 = a
                    b1 = b
            else:
                continue
        return f'{a1},{b1}'


class SubgroupApplication(models.Model):
    subgroup = models.ForeignKey(Subgroup, related_name='subgroup_application', on_delete=models.CASCADE)
    application = models.ForeignKey(AthleteApplication, related_name='application_subgroup', on_delete=models.CASCADE)


class JudgeGroup(models.Model):
    subgroup = models.ForeignKey(Subgroup, on_delete=models.CASCADE, limit_choices_to={'is_confirmed': True})
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.subgroup},{self.start_time}-{self.end_time}'


class JudgeGroupUser(models.Model):
    judge_group = models.ForeignKey(JudgeGroup, on_delete=models.CASCADE, related_name='judge_subgroup')
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
