from .models import *
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=128)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean_username(self):
        return self.cleaned_data['username'].lower().strip()

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(label="Теги", max_length=128)
    
    def clean_tags(self):
        tags = self.cleaned_data['tags'].split(',')
        result = []
        for i in tags:
            if i.strip() != '':
                result.append(i.strip())
        return result
    
    def clean_title(self):
        title = self.cleaned_data.get('title').strip()
        
        if title == '':
            raise forms.ValidationError('Пустое поле заголовка вопроса')
        return title
    
    def clean_description(self):
        description = self.cleaned_data.get('description').strip()
        
        if description == '':
            raise forms.ValidationError('Пустое поле вопроса')
        return description

    def save(self, profile):
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']
        tags = self.cleaned_data['tags']

        for i in range(len(tags)):
            tags[i], created = Tag.objects.get_or_create(name=tags[i])
        
        question = Question(
            title=title,
            description=description,
            profile=profile,
        )
        question.save() # как оказалось нужно для добавления тегов
        question.tags.set(tags)
        question.save()

        return question
    
    class Meta:
        model = Question
        fields = ("title", "description", "tags")

class AnswerForm(forms.ModelForm):
    def clean_description(self):
        description = self.cleaned_data.get('description').strip()
        
        if description == '':
            raise forms.ValidationError('Пустое поле ответа')
        return self.cleaned_data.get('description')


    def save(self, profile, question):
        answer = Answer(
            description=self.cleaned_data['description'],
            profile=profile,
            question=question
        )
        answer.save()
        
        return answer

    class Meta:
        model = Answer
        fields = ("description",)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    check_password = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)
    nickname = forms.CharField()
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        check_password = cleaned_data.get("check_password")
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        nickname = cleaned_data.get("nickname")
        if nickname == None or nickname.strip() == '':
            cleaned_data["nickname"] = username
        if password and check_password and password != check_password:
            raise forms.ValidationError("Пароли не совпадают")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Этот логин уже зарегистрирован")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        
        profile = Profile(user=user, nickname=self.cleaned_data['nickname'])
        if 'avatar' in self.cleaned_data:
            profile.image = self.cleaned_data['avatar']
        profile.save()


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', required=False)
    nickname = forms.CharField(label='Имя на сайте', required=False)
    email = forms.EmailField(label='Почта')

    def clean(self):
        data = super().clean()

        current_email = self.instance.email
        new_email = data.get('email')

        if new_email != current_email and User.objects.filter(email=new_email).exists():
            self.add_error('email', 'Эта почта уже занята')

        return data

    def save(self, commit=True):
        print(self.cleaned_data)
        user = super().save(commit=False)
        
        if commit:
            user.save()

        if 'avatar' in self.cleaned_data and self.cleaned_data['avatar'] != None:
            profile = Profile.objects.get(user=user)
            profile.image = self.cleaned_data['avatar']
            profile.save()
        
        if 'nickname' in self.cleaned_data and self.cleaned_data['nickname'] != None:
            profile = Profile.objects.get(user=user)
            profile.nickname = self.cleaned_data['nickname']
            profile.save()

        return user
    
    class Meta:
        model = User
        fields = ('email',)