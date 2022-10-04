from django_filters import (
    FilterSet,
    NumberFilter,
    DateTimeFilter,
    BooleanFilter,
    CharFilter,
)


class ApplicationFilter(FilterSet):
    trainer = NumberFilter(field_name='trainer')
    new_application = DateTimeFilter(field_name='event__finish_datetime', lookup_expr='gte')
    old_application = DateTimeFilter(field_name='event__finish_datetime', lookup_expr='lt')
    team_number = CharFilter(field_name='team_number')
    team_discipline = BooleanFilter(field_name='discipline__is_individual')
    is_confirmed = BooleanFilter(field_name='is_confirmed')
