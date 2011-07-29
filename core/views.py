from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from core.models import *

from forms import *

@login_required
def scrumBoard(request):
    """
        Estrutura do retorno:
        sprints_historias =
        {
            historia1 : {
                1: [],
                2: [Tarefa6],
                3:[Tarefa9],
                4:[Tarefa10],
            }
            historia1.x = [1,2,,3],
            historia1.y = [1,2,,3],
            historia2: {
                1: [Tarefa2, Tarefa1],
                2: [],
                3:[],
                4:[],
            }
        }
    """
    if "sprint_id" in request.GET:
        sprint_id = request.GET['sprint_id']
        historias = {}
        sprint_tasks = SprintTask.objects.filter(sprint__pk=sprint_id)
        if sprint_tasks:
            for task_sprint in sprint_tasks:
                if not task_sprint.task.history in historias:
                    historias[task_sprint.task.history] = {}
                if not 1 in historias[task_sprint.task.history]:
                    historias[task_sprint.task.history][1] = []
                if not 2 in historias[task_sprint.task.history]:
                    historias[task_sprint.task.history][2] = []
                if not 3 in historias[task_sprint.task.history]:
                    historias[task_sprint.task.history][3] = []
                if not 4 in historias[task_sprint.task.history]:
                    historias[task_sprint.task.history][4] = []
                task_sprint.task.resp = task_sprint.associated_to
                task_sprint.task.comments = len(task_sprint.sprinttaskcomment_set.all())
                task_sprint.task.work_hours = 0
                for wh in task_sprint.workhour_set.all():
                    task_sprint.task.work_hours = task_sprint.task.work_hours + wh.time
                task_sprint.task.work_hours = int(task_sprint.task.work_hours)
                historias[task_sprint.task.history][int(task_sprint.task.status)].append(task_sprint.task)
    return render_to_response('scrum-board.html', {'request':request,'historias' : historias, 'sprint_id': sprint_id, })

def updateTaskStatus(request):
    resultado = "fail"
    if "task_id" in request.GET and "new_status" in request.GET:
        task = Task.objects.get(pk=request.GET['task_id'])
        task.status = request.GET['new_status']
        task.save()
        resultado = "ok"
    else:
        resultado = "Faltam parametros"
    return HttpResponse(resultado)

def updateTaskSprintResponsible(request):
    """
        Metodo utilizado para associar uma task do sprint a um User do group Team.
    """
    resultado = "Falhou"
    if "task_id" in request.GET and "user_id" in request.GET and "sprint_id" in request.GET:
        user = User.objects.get(pk = request.GET['user_id'])
        team = Group.objects.get(name="Team")
        if team in user.groups.all():
            sprinttask = SprintTask.objects.get(task__pk=request.GET['task_id'], sprint__pk=request.GET['sprint_id'])
            if sprinttask.associated_to:
                resultado = "Essa tarefa ja possui um responsavel: " + sprinttask.associated_to.username
            else:
                sprinttask.associated_to = user
                sprinttask.save()
                resultado = "ok"
        else:
            resultado = "Voce nao possui permissao."
    else:
        resultado = "Faltam parametros"
    return HttpResponse(resultado)

def index(request):
    sprints = Sprint.objects.all()
    return render_to_response('index.html', local())

def lancarHora(request):
    retorno = "Falhou"
    if "task_id" in request.GET and "user_id" in request.GET and "sprint_id" in request.GET and "qtd-horas" in request.GET:
        st = SprintTask.objects.filter(task__pk=request.GET['task_id'], sprint__pk=request.GET['sprint_id'])[0]
        print "ST ID ASSOCIATED_TO: " + str(st.associated_to_id)
        print "USER ID: " + str(request.GET['user_id'])
        if str(st.associated_to_id) == str(request.GET['user_id']):
            user = User.objects.get(pk=request.GET['user_id'])
            wh = WorkHour()
            wh.sprinttask = st
            wh.day = datetime.date.today()
            wh.user = user
            wh.time = int(request.GET['qtd-horas'])
            wh.save()
            whs = WorkHour.objects.filter(sprinttask=st)
            tt = 0
            for w in whs:
                tt = tt + w.time
            retorno = "ok:" + str(int(tt))
        else:
            retorno = "Voce nao e o responsavel por esta tarefa."
    else:
        retorno = "Faltam parametros"
    return HttpResponse(retorno)

@csrf_protect
def comentarios(request):
    if request.method == 'POST':
        #####################################
        user_id = request.POST['user_id']
        task_id = request.POST['task_id']
        sprint_id = request.POST['sprint_id']
        sprinttask = SprintTask.objects.filter(sprint__id=sprint_id, task__id=task_id)[0]
        sprinttask_id = sprinttask.pk
        #####################################
        user = User.objects.get(pk = user_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            form = CommentForm()

    else:
        #####################################
        task_id = request.GET['task_id']
        sprint_id = request.GET['sprint_id']
        user_id = request.GET['user_id']
        sprinttask = SprintTask.objects.filter(sprint__id=sprint_id, task__id=task_id)
        sprinttask_id = sprinttask[0].pk
        #####################################
        form = CommentForm()
    #########################################
    comments = SprintTaskComment.objects.filter(sprinttask__id=sprinttask_id)
    return render_to_response('comentarios.html', {'form':form,'task_id':task_id,'user_id':user_id,'sprint_id':sprint_id,'sprinttask_id':sprinttask_id,'comments':comments,},context_instance=RequestContext(request))