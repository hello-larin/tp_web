from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F, Count, Q
from django.db.models.functions import Coalesce

# Create your models here.

class QuestionManager(models.Manager):
    def get_question(self, id):
        return self.get(id=id)

    def new_questions(self):
        return self.order_by('-id')

    def hot_questions(self):
        return self.annotate(rating=Coalesce(Sum("questionlike__status"), 0)).order_by('-rating')

    def tag_questions(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-id')

class AnswerManager(models.Manager):
    def question_answers(self, id):
        return self.filter(question__id=id).order_by('id')

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    nickname = models.CharField("Отображаемое имя", max_length=150)
    image = models.ImageField(upload_to='uploads')
    
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
    title = models.CharField("Заголовок", max_length=150)
    description = models.TextField("Содержание")
    profile = models.ForeignKey(Profile, verbose_name="Профиль", on_delete=models.CASCADE, related_name='questions')
    created_date = models.DateField("Дата создания", auto_now=False, auto_now_add=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    objects = QuestionManager()
    
    def answer_count(self):
        return Answer.objects.filter(question=self).count()
    
    def rating(self):
        return self.questionlike_set.aggregate(rating=models.Sum('status'))['rating'] or 0
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title[:30] + '...'

class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE, related_name='answers')
    description = models.TextField("Ответ")
    profile = models.ForeignKey(Profile, verbose_name="Автор", on_delete=models.CASCADE)
    created_date = models.DateField("Дата создания", auto_now=False, auto_now_add=True)
    correct = models.BooleanField("Правильный ответ", default=False)
    objects = AnswerManager()
    
    def rating(self):
        return self.answerlike_set.aggregate(rating=models.Sum('status'))['rating'] or 0

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.description[:30] + '...'


class QuestionLike(models.Model):
    STATUS_CHOICES = (
        (1, "Нравится"),
        (-1, "Не нравится")
    )
    status = models.IntegerField("Статус", choices=STATUS_CHOICES, default=1)
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name="Профиль", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Оценка вопроса"
        verbose_name_plural = "Оценки вопросов"
        unique_together = [["question", "profile"]]

    def __str__(self):
        return self.question.title


class AnswerLike(models.Model):
    STATUS_CHOICES = (
        (1, "Нравится"),
        (-1, "Не нравится")
    )
    status = models.IntegerField("Статус", choices=STATUS_CHOICES, default=1)
    answer = models.ForeignKey(Answer, verbose_name="Ответ", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name="Профиль", on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = "Оценка ответа"
        verbose_name_plural = "Оценки ответов"
        unique_together = [["answer", "profile"]]


    def __str__(self):
        return self.answer.title[:30] + '...'


