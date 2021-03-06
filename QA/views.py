from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.paginator import Paginator

from QA.forms import QuestionForm, AnswerForm, CommentForm
from QA.models import QuestionModel, CommentModel, AnswerModel, TagListModel, QTagModel, QVote, AVote, AnswerApproved

from user.models import UserModel
# from porsgram.path import *
import datetime

'''
    TODO:
        1.create NOT_FOUND page
'''




# def index(request):
#     return render(request, QA_INDEX, {})



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
            instance.author.questions_no += 1
            instance.author.save()
            instance.save()
            setQTags(tags, instance)

        return redirect('QA:question', id=instance.id)

    else:
        q_form = QuestionForm()
        context = {
            'q_form' : q_form,
            'tags'   : tags_list,   
        }

    return render(request, 'QA/createQuestion.html', context=context)




def questions(request):
    questions   = QuestionModel.objects.all()    
    paginator   = Paginator(questions, 5)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    context     = {
        'page_obj': page_obj,
    }

    return render(request, 'QA/questions.html', context=context)
        



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
                return HttpResponse(status=204)
                
        except ObjectDoesNotExist:

            qvote                 = QVote()        
            qvote.question        = question
            qvote.user            = request.user
            qvote.like_or_dislike = True if _state == "True" else False
            try:
                qvote.save()
            except IntegrityError:
                pass


            return HttpResponse(status=204)

        return HttpResponse(status=204)


    else:
        # EXCEPTION PAGE
        return HttpResponse(status=403)





@login_required
def voteAnswer(request):
    answer = get_object_or_404(AnswerModel, id=request.POST['id'])
    _state = request.POST['state']

    if (request.user.is_authenticated and 
        request.method == "POST" and
        request.is_ajax()):
        try:
            av = AVote.objects.get(answer=answer, user=request.user)
            if (av.like_or_dislike and _state=="False"):
                av.delete()
            elif ((not av.like_or_dislike) and _state=="True"):
                av.delete()
            else:
                pass
        except ObjectDoesNotExist:

            avote                 = AVote()
            avote.user            = request.user
            avote.answer          = answer
            avote.like_or_dislike = True if _state == "True" else False
            try:
                avote.save()            
            except IntegrityError:
                pass

            return HttpResponse(status=204)

        return HttpResponse(status=204)

    else:
        return HttpResponse(status=403)



def question(request, id):
    try:
        question        = QuestionModel.objects.get(id=id)
        answers         = AnswerModel.objects.filter(question=question)
        user_answered   = answers.filter(author=request.user) if request.user.is_authenticated else None
        comments        = CommentModel.objects.filter(question=question)

        if question.author is not request.user :
            question.review += 1
            question.save()

    except ObjectDoesNotExist:
        messages.warning(request, 'سوال پیدا نشد!')
        return HttpResponseRedirect('QA:questions')



    if (request.user.is_authenticated and
        request.method == 'POST' and 
        not(user_answered)):

        answer_form = AnswerForm(request.POST)

        if answer_form.is_valid():
            instance             = answer_form.save(commit=False)
            instance.author      = request.user
            instance.author.answers_no += 1
            instance.author.save()
            question.answers_NO += 1
            question.save()
            instance.question    = question
            instance.save()
            return redirect('QA:question', id=id)

    else:
        try:
            approved_answer = AnswerApproved.objects.get(question=question)
        except ObjectDoesNotExist:
            approved_answer = None
        answer_form  = AnswerForm(request.POST)
        comment_form = CommentForm(request.POST)
        context = {
            'answer_form'     : answer_form,
            'question'        : question,
            'answers'         : answers,
            'user_answered'   : user_answered,
            'approved_answer' : approved_answer,
            'comments'        : comments,
            'comment_form'    : comment_form,
        }

    return render(request, 'QA/question.html', context=context)
        
@login_required
def createComment(request, id):
    try:
        question = QuestionModel.objects.get(id=id)
    except:
        messages.warning(request, 'همچین سوالی نداریم')
        return redirect('QA:questions')

    if (request.method == "POST" and 
        request.user.is_authenticated) :
        # request.user.reputation >= 30):
        form = CommentForm(request.POST)
        if form.is_valid:
            comment          = form.save(commit=False)
            comment.author   = request.user
            comment.question = question
            comment.save()
            return redirect('QA:question', id=id)

        else:
            messages.warning(request, 'ایراد در ارسال نظر')
            return redirect('QA:question', id=id)

    else:
        return redirect('QA:question', id=id)


@login_required
def editComment(request, q_id, c_id):

    try:
        # question = QuestionModel.objects.get(id=q_id)
        comment  = CommentModel.objects.get(id=c_id)
    except:
        messages.warning(request, 'همچین سوالی نداریم')
        return redirect('QA:questions')

    if (request.method == "POST" and 
        request.user.is_authenticated) :
        # request.user.reputation >= 30):
        form = CommentForm(request.POST)
        if form.is_valid:
            content         = request.POST.get('comment')
            comment.comment = content
            comment.date    = datetime.datetime.now() 
            comment.save()
            return redirect('QA:question', id=q_id)

        else:
            messages.warning(request, 'ایراد در ارسال نظر')
            return redirect('QA:question', id=q_id)

    else:
        return redirect('QA:question', id=q_id)



@login_required
def deleteComment(request, q_id, c_id):

    try:
        comment  = CommentModel.objects.get(id=c_id)
    except:
        messages.warning(request, 'همچین سوالی نداریم')
        return redirect('QA:questions')

    if (request.user == comment.author and
        request.user.is_authenticated) :
        comment.delete()
        return redirect('QA:question', id=q_id)

    else:
        messages.warning(request, 'ایراد در حذف نظر')
        return redirect('QA:question', id=q_id)


@login_required
def approveAnswer(request):

    try:
        a_id     = request.POST['answer_id']
        answer   = AnswerModel.objects.get(id=a_id)
        question = answer.question

    except ObjectDoesNotExist:
        return HttpResponse(status=303)

    if (request.user.is_authenticated and 
        request.user == question.author and
        request.method == "POST" and
        request.is_ajax()):
        

        try:
            approved_answer = AnswerApproved.objects.get(question=question)        
        except ObjectDoesNotExist:
            approved_answer = None
        
        if approved_answer == None:
            answer.is_approved        = True
            approved_answer           = AnswerApproved()
            approved_answer.answer    = answer
            approved_answer.question  = question
            try:
                answer.save()                
                approved_answer.save()        
            except IntegrityError:
                pass

        elif approved_answer.answer == answer:
            answer.is_approved       = False
            approved_answer.delete()
        else:
            approved_answer.answer.is_approved = False
            approved_answer.answer.save()
            answer.is_approved                 = True
            approved_answer.answer             = answer
            try:
                answer.save()                
                approved_answer.save()      

            except IntegrityError:
                pass


    return HttpResponse(status=204)



@login_required
def editQuestion(request, id):

    try:
        question      = QuestionModel.objects.get(id=id)
        selected_tags = QTagModel.objects.filter(question=question).values_list('tag', flat=True)
        tags          = TagListModel.objects.all()
    except ObjectDoesNotExist:
        messages.warning(request, 'سوال پیدا نشد!')
        return HttpResponseRedirect('QA:questions')
        

    if request.user == question.author:
            
        if request.method == 'POST' :
            q_form   = QuestionForm(request.POST, instance=question)
            new_tags = request.POST.getlist('tags')

            if q_form.is_valid():
                content          = q_form.cleaned_data['content']
                title            = q_form.cleaned_data['title']
                instance         = q_form.save(commit=False)
                instance.edited  = True           
                instance.title   = title           
                instance.content = content
                instance.date    = datetime.datetime.now()       
                instance.save()
                QTagModel.objects.filter(question=question).delete()
                setQTags(new_tags, instance)

            return redirect('QA:question', id=id)

        else:
            q_form = QuestionForm(instance=question)
            context = {
                'q_form'        : q_form,
                'selected_tags' : selected_tags,   
                'tags'          : tags,   
            }

        return render(request, 'QA/editQuestion.html', context=context)

    else:
        messages.warning(request, 'سوال پیدا نشد!')
        return HttpResponseRedirect('QA:questions')





@login_required
def deleteQuestion(request, id):

    try:
        question = QuestionModel.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.warning(request, 'سوال پیدا نشد!')
        return HttpResponseRedirect('QA:questions')
        
    if request.user == question.author:
        question.author.questions_no -= 1
        question.author.save()
        question.delete()        
        messages.warning(request, 'سوال شما حذف شد!')
        return redirect('QA:questions')

    else:
        messages.warning(request, 'شما اجازه ندارید')
        return HttpResponseRedirect('QA:questions')

def tags(request):
    try:
        tags = TagListModel.objects.all()
    except ObjectDoesNotExist:
        tags = None
    return render(request, 'QA/tags.html', {'tags': tags})



def tag(request, id):
    _tag        = TagListModel.objects.get(id=id)
    tags        = QTagModel.objects.filter(tag=_tag)
    questions   = [i.question for i in tags]
    paginator   = Paginator(questions, 5)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    context     = {
        'page_obj': page_obj,
    }

    return render(request, 'QA/questionsTaged.html', context=context)
        


@login_required
def editAnswer(request, q_id, a_id):
    try:
        question = QuestionModel.objects.get(id=q_id)
        answer   = AnswerModel.objects.get(id=a_id)

    except ObjectDoesNotExist:
        messages.warning(request, 'پیدا نشد!')
        return redirect('QA:question', id=q_id)



    if request.user == answer.author:

        if (request.user.is_authenticated and
            request.method == 'POST'):

            answer_form = AnswerForm(request.POST, instance=answer)

            if answer_form.is_valid():
                instance        = answer_form.save(commit=False)
                instance.edited = True
                instance.date   = datetime.datetime.now()
                instance.save()
                return redirect('QA:question', id=q_id)

        else:
            answer_form = AnswerForm(instance=answer)
            context = {
                'answer_form'   : answer_form,
                'question'      : question,
            }

        return render(request, 'QA/editAnswer.html', context=context)
        
    else:
        
        messages.error(request, 'برو بچه!')
        return redirect('QA:question', id=q_id)



@login_required
def deleteAnswer(request, q_id, a_id):
    try:
        answer   = AnswerModel.objects.get(id=a_id)
        question = QuestionModel.objects.get(id=q_id)
    except ObjectDoesNotExist:
        messages.warning(request, 'پیدا نشد!')
        return redirect('QA:question', id=q_id)



    if request.user == answer.author:
        question.answers_NO      -= 1
        answer.author.answers_no -= 1
        answer.author.save()
        answer.delete()
        question.save()

        return redirect('QA:question', id=q_id)

    else:
        messages.error(request, 'برو بچه!')
        return redirect('QA:question', id=q_id)




