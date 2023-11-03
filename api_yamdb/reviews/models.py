from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

LENGTH_TEXT_OUTPUT = 30

User = get_user_model()


class Genres(models.Model):
    name = models.TextField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Слаг жанра')


class Categories(models.Model):
    name = models.TextField(max_length=256, verbose_name='Названик категории')
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Слаг категории')


class Title(models.Model):
    name = models.TextField(
        max_length=256, verbose_name='Название произведения')
    year = models.IntegerField(null=True, verbose_name='Год выпуска')
    description = models.TextField(null=True, verbose_name='Описание')
    genre = models.ManyToManyField(Genres, verbose_name='Жанры')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 null=True, verbose_name='Категория',
                                 related_name='titles')
    rating = models.PositiveIntegerField('Рейтинг', null=True, blank=True)


class Review(models.Model):
    text = models.TextField('Текст отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        help_text=('Поставьте оценку от 1 до 10.')
    )
    pub_date = models.DateTimeField(
        'Дата отзывы',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_autor_title',
            ),
        ]

    def __str__(self):
        return self.text[:LENGTH_TEXT_OUTPUT]


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LENGTH_TEXT_OUTPUT]
