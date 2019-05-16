from django import  forms
from .models import Document, Comment

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['category', 'title', 'slug', 'text', 'image']
"""
form = CommentForm()
self.instance = Comment()
self.instance.text = request.POST.get('text')
"""

class CommentForm(forms.ModelForm):
    #초기값 설정은 위에서
    # text = forms.TextInput(label="댓글")
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = "댓글"
        self.fields['text'].widget = forms.TextInput()
        self.fields['text'].widget.attrs = {'class':"form-control", 'placeholder':"댓글을 입력하세요"}