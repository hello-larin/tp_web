from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads')
    rating = models.IntegerField()
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.TextField("Заголовок")
    description = models.TextField("Содержание")
    profile = models.ForeignKey(Profile, verbose_name="Профиль", on_delete=models.CASCADE)
    created_date = models.DateField("Дата создания", auto_now=False, auto_now_add=True)
    rating = models.IntegerField("Рейтинг")
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title[:30] + '...'

class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE)
    description = models.TextField("Ответ")
    profile = models.ForeignKey(Profile, verbose_name="Автор", on_delete=models.CASCADE)
    created_date = models.DateField("Дата создания", auto_now=False, auto_now_add=True)
    correct = models.BooleanField("Правильный ответ")
    rating = models.IntegerField("Рейтинг")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.description[:30] + '...'


class QuestionLike(models.Model):
    STATUS_CHOICES = (
        (1, "Нравится"),
        (0, "Не нравится")
    )
    status = models.IntegerField("Статус", choices=STATUS_CHOICES)
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name="Профиль", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Оценка вопроса"
        verbose_name_plural = "Оценки вопросов"

    def __str__(self):
        return self.question.title


class AnswerLike(models.Model):
    STATUS_CHOICES = (
        (1, "Нравится"),
        (0, "Не нравится")
    )
    status = models.IntegerField("Статус", choices=STATUS_CHOICES)
    answer = models.ForeignKey(Answer, verbose_name="Ответ", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name="Профиль", on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = "Оценка ответа"
        verbose_name_plural = "Оценки ответов"

    def __str__(self):
        return self.answer.title[:30] + '...'



