from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
from django.utils import timezone
from .models import Question, Answer
from django.http import HttpResponseNotAllowed
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator


def index(request):
    #return HttpResponse("안녕하세요. Sunny World에 오신것을 환경합니다.")
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    #context = {'question_list': question_list}
    return render(request, 'sunny/question_list.html', context)

# Create your views here.

def detail(request, question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'sunny/question_detail.html', context);



def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('sunny:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'sunny/question_detail.html', context)

    # 2023.02.22
    #answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    #answer.save()
   

    # 2023.02.21
    #question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())

    # 2023.02.22
    #return redirect('sunny:detail', question_id=question.id)



def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('sunny:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'sunny/question_form.html', context)
