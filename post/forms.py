from django import forms
from.models import Post 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

bad_words = ['bad', 'ugly', 'nasty', 'stupid', 'dumb', 'foolish', 'idiot', 'fool', 'moron', 'loser']

class PostForm(forms.ModelForm):
    
    title = forms.CharField(required=False) #this is to override the default behavior of the title field in the model to make it required

    content = forms.CharField(required=False) #this is to override the default behavior of the content field in the model to make it required

    
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        
        
    
    def clean_title(self):
    
        title = self.cleaned_data.get('title')
        if (title == ''):
            raise forms.ValidationError('Title cannot be empty')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if (content == ''):
            raise forms.ValidationError('Content cannot be empty')

        found_bad_words = []
        
        for word in bad_words:
            if word in content:
                found_bad_words.append(word)
            
        if len(found_bad_words) > 0:
            raise forms.ValidationError(f'The content cannot contain inappropriate words: {',' .join(found_bad_words)}')
        return content
    
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)
    

    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
    
    def clean_email(self):
        print('hello')
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        print('email test')
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if (first_name == ''):
            raise forms.ValidationError('First name cannot be empty')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if (last_name == ''):
            raise forms.ValidationError('Last name cannot be empty')
        return last_name