import math
from django_filters import  rest_framework as filters
from .models import *


class TutorFilter(filters.FilterSet):
    salary = filters.RangeFilter()
    experience = filters.RangeFilter()
    degree = filters.ChoiceFilter(choices=TutorUser.DEGREE_CHOICES)
    rating = filters.NumberFilter(method='filter_by_rating')
    course = filters.CharFilter(field_name='courses__name')

    class Meta:
        model = TutorUser
        fields = ('salary', 'experience', 'degree','rating','course')

    def filter_by_rating(self, queryset, name, value):
        return queryset.filter(reviews__rating__gte=value).distinct()