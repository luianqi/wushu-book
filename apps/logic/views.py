from django.db.models import Count

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_bulk import BulkModelViewSet

from apps.logic.filters import ApplicationFilter
from apps.logic.models import (
    Event,
    AgeGroup,
    Discipline,
    Application,
    AthleteApplication,
    TemplateApplication,
    SubgroupApplication,
    Subgroup,
    JudgeGroup,
    JudgeGroupUser,
)
from apps.logic.serializers import (
    EventSerializer,
    AgeGroupSerializer,
    DisciplineSerializer,
    ApplicationSerializer,
    AthleteApplicationSerializer,
    TemplateApplicationSerializer,
    SubgroupSerializer,
    SubgroupApplicationSerializer,
    JudgeGroupSerializer,
    JudgeGroupUserSerializer,
    BulkUpdateSubgroupSerializer,
)


class AgeGroupView(ModelViewSet):
    serializer_class = AgeGroupSerializer
    queryset = AgeGroup.objects.all()


class EventView(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'start_datetime', 'finish_datetime', 'place', 'note', 'lead_judge__name',
                     'lead_judge__surname', 'assistant__name', 'assistant__surname']

    def create(self, request, *args, **kwargs):
        """Update user.is_judge status after creating """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            lead_judge = serializer.validated_data['lead_judge']
            lead_judge.is_judge = True
            lead_judge.save()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class DisciplineView(ModelViewSet):
    serializer_class = DisciplineSerializer
    queryset = Discipline.objects.all()


class TemplateApplicationView(ModelViewSet):
    serializer_class = TemplateApplicationSerializer
    queryset = TemplateApplication.objects.all()


class ApplicationView(ModelViewSet):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    filter_class = ApplicationFilter
    filter_backends = [SearchFilter]
    search_fields = ['event']

    def get_queryset(self):
        """Filter queryset by user role"""

        user = self.request.user
        if user.role == 'TRAINER' and user.is_assistant is False:
            return self.queryset.filter(trainer=self.request.user)
        elif user.role == 'TRAINER' and user.is_assistant is True:
            return self.queryset.filter(event__assistant=self.request.user)

    def create(self, request, *args, **kwargs):
        """Creating multiple objects with one request"""

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

    def perform_create(self, serializer):
        """Auto save trainer value"""

        serializer.save(trainer=self.request.user)


class AthleteApplicationView(ModelViewSet):
    serializer_class = AthleteApplicationSerializer
    queryset = AthleteApplication.objects.all()


class SubgroupBulkUpdateView(BulkModelViewSet):
    serializer_class = BulkUpdateSubgroupSerializer
    queryset = Subgroup.objects.all()


class SubgroupView(ModelViewSet):
    serializer_class = SubgroupSerializer
    queryset = Subgroup.objects.all()

    def create(self, request, *args, **kwargs):
        """Business logic of generating protocol subgroups"""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            event = serializer.validated_data['event']
            athlete_application = AthleteApplication.objects.filter(application__event=event.pk, application__is_confirmed=True)\
                .values('application__discipline', 'application__event', 'athlete__sex', 'event_age_group')\
                .annotate(total=Count('id'))
            if athlete_application:
                for i in athlete_application:
                    discipline = Discipline.objects.filter(pk=i['application__discipline'])
                    for f in discipline:
                        subgroup = Subgroup.objects.create(discipline=f, sex=i['athlete__sex'],
                                                           age_group=i['event_age_group'], event=event)
                        for athlete_data in AthleteApplication.objects.filter(application__event=subgroup.event,
                                                                              application__discipline=subgroup.discipline,
                                                                              event_age_group=subgroup.age_group,
                                                                              athlete__sex=subgroup.sex):
                            SubgroupApplication.objects.create(application=athlete_data, subgroup=subgroup)
                        serializer.save()
                Subgroup.objects.filter(sex=3, discipline__isnull=True).delete()
                event.is_protocoled = True
                event.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response('Одобренных заявок для данного мероприятия не найдено')


class SubgroupApplicationView(ModelViewSet):
    serializer_class = SubgroupApplicationSerializer
    queryset = SubgroupApplication.objects.all()


class JudgeGroupView(BulkModelViewSet):
    serializer_class = JudgeGroupSerializer
    queryset = JudgeGroup.objects.all()


class JudgeGroupUserView(ModelViewSet):
    serializer_class = JudgeGroupUserSerializer
    queryset = JudgeGroupUser.objects.all()
