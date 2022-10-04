from django.contrib import admin
from apps.logic.models import (
    Event,
    AgeGroup,
    Discipline,
    Application,
    AthleteApplication,
    Subgroup,
    SubgroupApplication,
    JudgeGroup,
    TemplateApplication,
)

admin.site.register(Event)
admin.site.register(AgeGroup)
admin.site.register(Discipline)
admin.site.register(Application)
admin.site.register(AthleteApplication)
admin.site.register(Subgroup)
admin.site.register(SubgroupApplication)
admin.site.register(JudgeGroup)
admin.site.register(TemplateApplication)
