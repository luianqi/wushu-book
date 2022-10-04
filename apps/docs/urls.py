from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.docs.views import DocumentView

router = DefaultRouter()
router.register('document', DocumentView)


urlpatterns = [
    path('', include(router.urls)),
]
