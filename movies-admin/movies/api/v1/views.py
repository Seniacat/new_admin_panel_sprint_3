from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from movies.models import Filmwork

from .serializers import FilmworkSerializer


class MoviesViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
):
    serializer_class = FilmworkSerializer

    def aggregate_person(self, role: str):
        return ArrayAgg(
            'personfilmwork__person__full_name',
            filter=Q(personfilmwork__role=role),
            distinct=True,
        )

    def get_queryset(self):
        queryset = Filmwork.objects.prefetch_related(
            'genres', 'persons').all()
        queryset = queryset.annotate(
            actors=self.aggregate_person('actor'),
            directors=self.aggregate_person('director'),
            writers=self.aggregate_person('writer')
        )
        return queryset
