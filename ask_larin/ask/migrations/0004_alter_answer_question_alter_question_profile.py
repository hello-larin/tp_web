# Generated by Django 5.1.2 on 2024-11-02 20:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0003_rename_question_answerlike_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='ask.question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='question',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='ask.profile', verbose_name='Профиль'),
        ),
    ]
