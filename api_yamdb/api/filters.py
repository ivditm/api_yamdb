import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      method='filter_genre')
    category = django_filters.CharFilter(field_name='category__slug')
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='year')

    def filter_genre(self, queryset, name, value):
        return queryset.filter(genre__slug=value)

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')
