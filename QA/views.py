from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from QA.forms import QuestionForm, AnswerForm
from QA.models import QuestionModel, AnswerModel, TagListModel, QTagModel, QVote

from user.models import UserModel

'''
    TODO:
        1.create NOT_FOUND page
        2.create suitable redirect when user_authentication

'''


def index(request):
    return render(request, 'qa/index.html', {})



def setQTags(tags, question):
    tags_id = TagListModel.objects.values_list('id', flat=True)
    for tag in tags:
        tag_tuple = QTagModel()
        if tag.isdigit() and int(tag) in tags_id:
            tag_tuple.tag = TagListModel.objects.get(id=int(tag))
        else:
            tag_obj     = TagListModel()        
            tag_obj.tag = tag
            tag_obj.save()
            tag_tuple.tag  = tag_obj
        tag_tuple.question = question 
        tag_tuple.save()


@login_required
def createQuestion(request):
  
    try:
        tags_list = TagListModel.objects.all()
    except ObjectDoesNotExist:
        return redirect('qa:index')

    if request.method == 'POST':
        q_form = QuestionForm(request.POST)
        tags   = request.POST.getlist('tags')
        if q_form.is_valid():
            instance        = q_form.save(commit=False)            
            instance.author = request.user
            instance.save()
            setQTags(tags, instance)

        return redirect('QA:index')

    else:
        q_form = QuestionForm()
        context = {
            'q_form' : q_form,
            'tags'   : tags_list,   
        }

    return render(request, 'qa/createQuestion.html', context=context)




def questions(request):
    questions = QuestionModel.objects.all()    
    return render(request, 'qa/questions.html', {'questions': questions})
        



@login_required
def voteQuestion(request):
    question = get_object_or_404(QuestionModel, id=request.POST['id'])
    _state = request.POST['state']

    if (request.user.is_authenticated and 
        request.method == "POST" and
        request.is_ajax()):
        try:
            qv = QVote.objects.get(question=question, user=request.user)
            if (qv.like_or_dislike and _state=="False"):
                qv.delete()
            elif ((not qv.like_or_dislike) and _state=="True"):
                qv.delete()
            else:
                pass
        except ObjectDoesNotExist:
            qvote                 = QVote()        
            qvote.user            = request.user
            qvote.question        = question
            qvote.like_or_dislike = True if _state == "True" else False
            qvote.save()

        return HttpResponse(status=204)

    else:
        # EXCEPTION PAGE
        return redirect('QA:index')


def question(request, id):
    try:
        question      = QuestionModel.objects.get(id=id)
        answers       = AnswerModel.objects.filter(question=question)
        user_answered = answers.filter(author=request.user) if request.user.is_authenticated else None

    except ObjectDoesNotExist:
        return HttpResponseRedirect('QA:index')

    if (request.user.is_authenticated and
        request.method == 'POST' and 
        not(user_answered)):

        answer_form = AnswerForm(request.POST)

        if answer_form.is_valid():
            instance          = answer_form.save(commit=False)
            instance.author   = request.user
            instance.question = question
            instance.save()
            return redirect('QA:question', id=id)

    else:
        answer_form = AnswerForm()
        context = {
            'answer_form'   : answer_form,
            'question'      : question,
            'answers'       : answers,
            'user_answered' : user_answered,
        }

    return render(request, 'qa/question.html', context=context)
        



@login_required
def editQuestion(request, id):

    try:
        question      = QuestionModel.objects.get(id=id)
        selected_tags = QTagModel.objects.filter(question_id=question).values_list('tag', flat=True)
        tags          = TagListModel.objects.all()
    except ObjectDoesNotExist:
        return redirect('QA:index')
        

    if request.user == question.author:
            
        if request.method == 'POST' :
            q_form   = QuestionForm(request.POST, instance=question)
            new_tags = request.POST.getlist('tags')

            if q_form.is_valid():
                instance        = q_form.save(commit=False)
                instance.author = request.user
                instance.save()
                QTagModel.objects.filter(question_id=question).delete()
                setQTags(new_tags, instance)

            return redirect('QA:question', id=id)

        else:
            q_form = QuestionForm(instance=question)
            context = {
                'q_form'        : q_form,
                'selected_tags' : selected_tags,   
                'tags'          : tags,   
            }

        return render(request, 'qa/editQuestion.html', context=context)

    else:
        return redirect('QA:index')




@login_required
def deleteQuestion(request, id):

    try:
        question = QuestionModel.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect('QA:index')
        
    if request.user == question.author:

        question.delete()        
        messages.warning(request, 'سوال شما حذف شد!')
        return redirect('QA:questions')

    else:
        return redirect('QA:index')



@login_required
def editAnswer(request, q_id, a_id):
    try:
        question = QuestionModel.objects.get(id=q_id)
        answer   = AnswerModel.objects.get(id=a_id)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('QA:index')

    if request.user == answer.author:

        if (request.user.is_authenticated and
            request.method == 'POST'):

            answer_form = AnswerForm(request.POST, instance=answer)

            if answer_form.is_valid():
                instance          = answer_form.save(commit=False)
                instance.author   = request.user
                instance.question = question
                instance.save()
                return redirect('QA:question', id=q_id)

        else:
            answer_form = AnswerForm(instance=answer)
            context = {
                'answer_form'   : answer_form,
                'question'      : question,
            }

        return render(request, 'qa/editAnswer.html', context=context)
        
    else:
        messages.error(request, 'برو بچه!')
        return redirect('QA:question', id=q_id)



@login_required
def deleteAnswer(request, q_id, a_id):
    try:
        answer   = AnswerModel.objects.get(id=a_id)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('QA:index')

    if request.user == answer.author:

        answer.delete()
        return redirect('QA:question', id=q_id)

    else:
        messages.error(request, 'برو بچه!')
        return redirect('QA:question', id=q_id)




