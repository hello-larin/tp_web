"""
URL configuration for ask_larin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ask import views
from ask_larin import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.questions_catalog, name='questions'),
    path('hot', views.hot_questions_catalog, name='hot'),
    path('tag/<str:tag>', views.tag, name='tag'),
    path('<int:id>', views.question, name='question'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),
    path('new_question', views.new_question, name='new_question'),
    path('answer/<int:id>', views.answer, name='answer'),
    path('question_like/<int:id>', views.question_like, name='question_like'),
    path('answer_like/<int:id>', views.answer_like, name='answer_like'),
    path('logout', views.logout, name='logout'),
    path('answer_correct/<int:id>', views.correct_answer, name='answer_correct')
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)