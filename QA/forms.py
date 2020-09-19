from django import forms
from QA.models import QuestionModel, CommentModel, AnswerModel, TagListModel
# from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class QuestionForm(forms.ModelForm):
    title    = forms.CharField(max_length=200, required=True)
    content  = RichTextUploadingFormField()

    class Meta:
        model  = QuestionModel
        fields = ('title', 'content', )



class AnswerForm(forms.ModelForm):
    content = RichTextUploadingFormField()

    class Meta:
        model  = AnswerModel
        fields = ('content', )


class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=500)

    class Meta:
        model  = CommentModel
        fields = ['comment',]
