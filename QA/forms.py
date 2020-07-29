from django import forms
from QA.models import QuestionModel, AnswerModel, TagListModel
# from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class QuestionForm(forms.ModelForm):
    title    = forms.CharField(max_length=200, required=True)
    content  = RichTextUploadingFormField()

    class Meta:
        model = QuestionModel
        fields = ('title', 'content', )



class AnswerForm(forms.ModelForm):
    content = RichTextUploadingFormField()

    class Meta:
        model  = AnswerModel
        fields = ('content', )



# class QImageForm(forms.ModelForm):
#     q_img = forms.ImageField(label='Image')    
    
#     class Meta:
#         model = QImageModel
#         fields = ('q_img', )




