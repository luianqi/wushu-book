from rest_framework import serializers

from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from apps.account.models import User, Athlete
from apps.account.serializers import (
    RegisterUserSerializer,
    AthleteSerializer,
    UserProfileSerializer,
)
from apps.logic.models import (
    AgeGroup,
    Athlete,
    Application,
    Event,
    Discipline,
    Subgroup,
    AthleteApplication,
    TemplateApplication,
    SubgroupApplication,
    JudgeGroup,
    JudgeGroupUser,
)


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = '__all__'
        read_only_fields = ['event']


class EventSerializer(serializers.ModelSerializer):
    age_groups = AgeGroupSerializer(many=True)
    start_datetime = serializers.DateTimeField(format="%d-%m-%Y")
    finish_datetime = serializers.DateTimeField(format="%d-%m-%Y")
    lead_judge = PresentablePrimaryKeyRelatedField(queryset=User.objects.all(),
                                                   presentation_serializer=RegisterUserSerializer)
    assistant = PresentablePrimaryKeyRelatedField(queryset=User.objects.all(),
                                                  presentation_serializer=RegisterUserSerializer)

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        age_groups_data = validated_data.pop('age_groups')
        event = Event.objects.create(**validated_data)
        for age_group_data in age_groups_data:
            AgeGroup.objects.create(event=event, **age_group_data)
        return event


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'


class TemplateApplicationSerializer(serializers.ModelSerializer):
    """Template Application Serializer"""

    event = PresentablePrimaryKeyRelatedField(queryset=Event.objects.all(),
                                              presentation_serializer=EventSerializer)

    class Meta:
        model = TemplateApplication
        fields = '__all__'
        read_only_fields = ['trainers']


class AthleteApplicationSerializer(serializers.ModelSerializer):
    """Athlete-Application serializer"""

    athlete = PresentablePrimaryKeyRelatedField(queryset=Athlete.objects.all(),
                                                presentation_serializer=AthleteSerializer)

    class Meta:
        model = AthleteApplication
        fields = '__all__'
        extra_kwargs = {
            "application": {"read_only": True},
        }


class ApplicationSerializer(serializers.ModelSerializer):
    """Application Serializer"""

    application_athlete = AthleteApplicationSerializer(many=True)
    event = PresentablePrimaryKeyRelatedField(queryset=Event.objects.all(),
                                              presentation_serializer=EventSerializer)
    trainer = PresentablePrimaryKeyRelatedField(queryset=User.objects.all(),
                                                presentation_serializer=RegisterUserSerializer)

    class Meta:
        model = Application
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['discipline'] = DisciplineSerializer(Discipline.objects.get(pk=data['discipline'])).data
        return data

    def create(self, validated_data):
        athletes_data = validated_data.pop('application_athlete')
        dueling_partner_data = validated_data.pop('dueling_partner')
        discipline_data = validated_data.pop('discipline')
        if dueling_partner_data is not None:
            dueling_discipline = Discipline.objects.filter(category=3, is_individual=False, with_weapon=False)
            for discipline in dueling_discipline:
                application = Application.objects.create(discipline=discipline, dueling_partner=dueling_partner_data,
                                                         **validated_data)
                for athlete_data in athletes_data:
                    AthleteApplication.objects.create(application=application, **athlete_data)
                    AthleteApplication.objects.create(application=application, athlete=dueling_partner_data)
                return application
        else:
            application = Application.objects.create(discipline=discipline_data, **validated_data)
            for athlete_data in athletes_data:
                AthleteApplication.objects.create(application=application, **athlete_data)
            return application


class SubgroupApplicationSerializer(serializers.ModelSerializer):
    """Protocol subgroup-application serializer"""

    application = PresentablePrimaryKeyRelatedField(queryset=AthleteApplication.objects.all(),
                                                    presentation_serializer=AthleteApplicationSerializer)

    class Meta:
        model = SubgroupApplication
        fields = '__all__'


class DisciplineField(serializers.RelatedField):
    """Serialization of discipline field """

    def to_representation(self, value):
        """ Serialize discipline instances using a DisciplineSerializer"""

        serializer = DisciplineSerializer(value)
        return serializer.data


class SubgroupSerializer(serializers.ModelSerializer):
    """Protocol subgroup serializer"""

    subgroup_application = SubgroupApplicationSerializer(many=True, read_only=True)
    event = PresentablePrimaryKeyRelatedField(queryset=Event.objects.all(),
                                              presentation_serializer=EventSerializer)
    discipline = DisciplineField(read_only=True)
    athlete_count = serializers.IntegerField(read_only=True)
    child_status = serializers.IntegerField(read_only=True)
    width_length = serializers.CharField(max_length=10, read_only=True)
    start_datetime = serializers.DateTimeField(format="%H:%M(%d-%m-%Y)", required=False)

    class Meta:
        model = Subgroup
        fields = '__all__'
        read_only_fields = [
            'sex',
            'age_group',
        ]


class BulkUpdateSubgroupSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """Serializer for Subgroup bulk update"""

    class Meta:
        model = Subgroup
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class JudgeGroupUserSerializer(serializers.ModelSerializer):
    """JudgeGroup User Serializer"""

    class Meta:
        model = JudgeGroupUser
        fields = '__all__'
        read_only_fields = [
            'judge_group',
        ]


class JudgeGroupSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """JudgeGroup Serializer"""

    judge_subgroup = JudgeGroupUserSerializer(many=True)

    class Meta:
        model = JudgeGroup
        list_serializer_class = BulkListSerializer
        fields = '__all__'

    def create(self, validated_data):
        judges_group_data = validated_data.pop('judge_subgroup')
        group = JudgeGroup.objects.create(**validated_data)
        for judge_group_data in judges_group_data:
            JudgeGroupUser.objects.create(judge_group=group, **judge_group_data)
        return group
