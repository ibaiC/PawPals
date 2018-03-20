from pawpals.models import *
import django_filters

class DogFilter(django_filters.FilterSet):
    
    name = django_filters.CharFilter(label = "Name", lookup_expr="contains")
    breed = django_filters.CharFilter(label = "Breed", lookup_expr="contains")
    
    CHOICES = (
        (True, "Yes"),
        (False, "No")
        )
    is_puppy = django_filters.ChoiceFilter(label = "Puppy", choices = CHOICES)
    is_childfriendly = django_filters.ChoiceFilter(label = "Child-friendly", choices = CHOICES)
    
    difficulty = django_filters.NumberFilter()
    difficulty__gte = django_filters.NumberFilter(label = "Minimum difficulty", name='difficulty', lookup_expr='gte')
    difficulty__lte = django_filters.NumberFilter(label = "Maximum difficulty", name='difficulty', lookup_expr='lte')
    
    class Meta:
        model = Dog
        fields = ["name" ,"breed" ,"difficulty" ,"size" ,"gender" ,"is_puppy" ,"is_childfriendly"]