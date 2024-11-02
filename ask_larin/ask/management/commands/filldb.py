import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ask.models import *

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        
        # Создание пользователей
        self.stdout.write(self.style.SUCCESS('filled users'))
        if User.objects.count() < 10000:
            users = [
                User(
                    username=f'user{i}',
                    email=f'user{i}@example.com',
                    password=make_password('password')
                )
                for i in range(1000)
            ]
            for i in range(1000, ratio):
                users.append(User(
                    username=f'user{i}',
                    email=f'user{i}@example.com',
                    password='password'
                ))
            User.objects.bulk_create(users)
        else:
            users = User.objects.filter()
        
        self.stdout.write(self.style.SUCCESS('filled profiles'))
        if Profile.objects.count() < 10000:
            profiles = [
                Profile(
                    user=users[i],
                    image = f'avatars/avatars7x7/avatar_{i}.png',
                    rating=random.randint(1, 100)
                )
                for i in range(ratio)
            ]
            Profile.objects.bulk_create(profiles)
        else:
            profiles = list(Profile.objects.filter())

        self.stdout.write(self.style.SUCCESS('filled tags'))
        # Создание тегов
        if Tag.objects.count() < 10000:
            tags = [
                Tag(name=f'tag{i}')
                for i in range(ratio)
            ]
            Tag.objects.bulk_create(tags)
        else:
            tags = list(Tag.objects.filter())

        # Создание вопросов
        self.stdout.write(self.style.SUCCESS('filled questions'))
        questions = []
        
        if Question.objects.count() < 100_000:
            for i in range(ratio * 10):
                question = Question(
                    title=f'Question {i}',
                    description=f'This is a test question {i}.',
                    profile=random.choice(profiles),
                    rating=random.randint(1, 100)
                )
                num_tags = random.randint(1, 6)
                questions.append(question)
            Question.objects.bulk_create(questions)
         
            for i in range(ratio * 10):
                # Присвоение тегов к вопросам
                selected_tags = random.sample(tags, num_tags)
                questions[i].tags.set(selected_tags)
        else:
            questions = list(Question.objects.filter())
            
        
        self.stdout.write(self.style.SUCCESS('filled answers'))
        # Создание ответов
        answers = []
        if Answer.objects.count() < 1_000_000:
            for i in range(ratio * 100):
                answer = Answer(
                    description=f'This is a test answer {i}. {i} + {i + 1} = {i + i + 1}',
                    profile=random.choice(profiles),
                    question=random.choice(questions),
                    correct=random.choice([True, False]),
                    rating=random.randint(1, 100)
                )
                answers.append(answer)

            # Массовое создание ответов
            Answer.objects.bulk_create(answers)
        else:
            answers = list(Answer.objects.filter())
        
        self.stdout.write(self.style.SUCCESS('filled questions likes'))
        # Создание оценок пользователей
        if QuestionLike.objects.count() < 100_000:
            q_likes = [
                QuestionLike(
                    profile=random.choice(profiles),
                    status=random.randint(1, 2),  # Пример рейтинга от 1 до 5
                    question=random.choice(questions)
                )
                for _ in range(ratio * 20)
            ]
            QuestionLike.objects.bulk_create(q_likes)
        else:
            q_likes = list(QuestionLike.objects.filter())
        self.stdout.write(self.style.SUCCESS('filled answers likes'))
        # Массовое создание оценок пользователей
        if AnswerLike.objects.count() < 1_000_000:
            a_likes = [
                AnswerLike(
                    profile=random.choice(profiles),
                    status=random.randint(1, 2),  # Пример рейтинга от 1 до 5
                    answer=random.choice(answers)
                )
                for _ in range(ratio * 180)
            ]
            # Массовое создание оценок пользователей
            AnswerLike.objects.bulk_create(a_likes)
        else:
            a_likes = list(AnswerLike.objects.filter())
        self.stdout.write(self.style.SUCCESS('Successfully filled the database with test data'))
