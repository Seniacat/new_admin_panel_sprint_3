import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDCreatedMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UUIDCreatedUpdatedMixin(UUIDCreatedMixin):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(UUIDCreatedUpdatedMixin):
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), null=True, blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDCreatedUpdatedMixin):
    full_name = models.CharField(_('full  name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class Filmwork(UUIDCreatedUpdatedMixin):

    class FilmType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv show')

    title = models.CharField(_('title'), max_length=300)
    description = models.TextField(_('description'), null=True, blank=True)
    creation_date = models.DateField(
        _('creation_date'),
        db_index=True,
        null=True,
        blank=True
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreFilmwork',
        verbose_name=_('Genres')
    )
    rating = models.FloatField(
        _('rating'),
        default=0.0,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.CharField(
        _('type'),
        max_length=10,
        choices=FilmType.choices,
        default=FilmType.MOVIE,
    )
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Film')
        verbose_name_plural = _('Films')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDCreatedMixin):
    film_work = models.ForeignKey(
        'Filmwork',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Movie genre')
        verbose_name_plural = _('Movie genre')
        constraints = (
            models.UniqueConstraint(
                fields=('film_work', 'genre'),
                name='unique_genre_filmwork'
            ),
        )


class PersonFilmwork(UUIDCreatedMixin):
    class PersonRole(models.TextChoices):
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')

    film_work = models.ForeignKey(
        'Filmwork',
        on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE
    )
    role = models.CharField(
        _('role'),
        max_length=30,
        choices=PersonRole.choices,
        default=PersonRole.ACTOR)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Memder')
        verbose_name_plural = _('Memders')
        constraints = (
            models.UniqueConstraint(
                fields=('film_work', 'person', 'role'),
                name='unique_person_filmwork_role'
            ),
        )
