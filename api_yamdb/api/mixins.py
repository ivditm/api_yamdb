from rest_framework import mixins, viewsets


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Кастомный вьюсет."""
    pass
