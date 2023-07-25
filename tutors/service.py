from django_filters import  rest_framework as filters
from .models import *


class TutorFilter(filters.FilterSet):
    salary = filters.RangeFilter()
    experience = filters.ChoiceFilter(choices=TutorUser.EXPERIENCE_CHOICES)

    class Meta:
        model = TutorUser
        fields = ('salary','experience',)