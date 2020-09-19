from django.urls import path
from QA import views

app_name = 'QA'

urlpatterns = [
    path('', views.questions, name='questions'),
    path('question/<int:id>', views.question, name='question'),
    path('tags/', views.tags, name='tags'),
    path('questions/taged/<int:id>/', views.tag, name='tag'),


    # question CRUD
    path('question/create/', views.createQuestion, name='question_create'),
    path('question/<int:id>/delete', views.deleteQuestion, name='question_delete'),
    path('question/<int:id>/edit', views.editQuestion, name='question_edit'),
    path('question/vote/', views.voteQuestion, name='question_vote'),

    # comment CRUD
    path('question/<int:id>/comment', views.createComment, name='create_comment'),
    path('question/<int:q_id>/comment/<int:c_id>/edit/', views.editComment, name='edit_comment'),
    path('question/<int:q_id>/comment/<int:c_id>/delete/', views.deleteComment, name='delete_comment'),

    # answer CRUD
    path('question/<int:q_id>/answer/<int:a_id>/edit', views.editAnswer, name='answer_edit'),
    path('question/<int:q_id>/answer/<int:a_id>/delete', views.deleteAnswer, name='answer_delete'),
    path('answer/vote/', views.voteAnswer, name='answer_vote'),
    path('answer/approved/', views.approveAnswer, name='answer_approved'),


]
