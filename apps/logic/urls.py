from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter


from apps.logic.views import (
    EventView,
    AgeGroupView,
    DisciplineView,
    ApplicationView,
    AthleteApplicationView,
    TemplateApplicationView,
    SubgroupApplicationView,
    SubgroupView,
    JudgeGroupView,
    JudgeGroupUserView,
    SubgroupBulkUpdateView,
)

router = DefaultRouter()
bulk_router = BulkRouter()
router.register('discipline', DisciplineView)
router.register('template_application', TemplateApplicationView)
router.register('application', ApplicationView)
router.register('athlete_application', AthleteApplicationView)
router.register('event', EventView)
router.register('age_group', AgeGroupView)
router.register('subgroup', SubgroupView)
router.register('subgroup_application', SubgroupApplicationView)
bulk_router.register('judge_group', JudgeGroupView)
router.register('judge_group_user', JudgeGroupUserView)
bulk_router.register('subroup_bulk_update', SubgroupBulkUpdateView)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(bulk_router.urls))
]
