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
        Estruturas de retorno:

        #####################################

        Historias e suas respectivas tarefas do sprint selecionado.
        -----------------------------------------------------------
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
        ######################################

        Grafico de burndown geral.
        ----------------------------------
        sprint_x = [1,2,3]
        sprint_y = [1,2,3]
    """
    if "sprint_id" in request.GET:
        sprint_id = request.GET['sprint_id']
        historias = {}
        sprint_histories = History.objects.filter(sprint__pk=sprint_id).order_by('priority')
        if sprint_histories:
            for history_sprint in sprint_histories:
                if not history_sprint in historias:
                    historias[history_sprint] = {}
                if not 1 in historias[history_sprint]:
                    historias[history_sprint][1] = []
                if not 2 in historias[history_sprint]:
                    historias[history_sprint][2] = []
                if not 3 in historias[history_sprint]:
                    historias[history_sprint][3] = []
                if not 4 in historias[history_sprint]:
                    historias[history_sprint][4] = []
                for task in history_sprint.task_set.all():
                    task.resp = task.associated_to
                    task.comments = len(task.taskcomment_set.all())
                    task.work_hours = 0
                    for wh in task.workhour_set.all():
                        task.work_hours = task.work_hours + wh.time
                    task.work_hours = int(task.work_hours)
                    historias[history_sprint][int(task.status)].append(task)

        sprint_tt_weight = []
        sprint_tt_days = []

        sprint_days = []
        sprint_weights = []
        sprint = Sprint.objects.get(pk=sprint_id)
        if sprint:
            sprint_tasks = Task.objects.filter(history__sprint__pk=sprint_id)
            dias = sprint.end_at - sprint.start_at
            sprint_tt_days.append(int(dias.days))

            if sprint_tasks:
                tt = 0
                for sprint_task in sprint_tasks:
                    tt = tt + sprint_task.weight

            media = int(tt/dias.days)
            for dia in range(0,dias.days+1):
                last_media = (tt-(media*dia))
                sprint_tt_days.append(int(dia))
                sprint_tt_weight.append(int(last_media))
            sprint_tt_weight[dias.days]=0

            #Pegar quantidade finalizada do dia
            inicio = sprint.start_at
            soma_weight = int(sprint_tt_weight[0])
            for day in range(0,dias.days+1):
                #ADICIONA O DIA NA LISTA DO GRAFICO
                dia = inicio + datetime.timedelta(days=day)
                #if dia <= datetime.date.today():
                sprint_days.append(int(day))
                date_ini = datetime.datetime(dia.year, dia.month, dia.day,0,0,0)
                date_fim = datetime.datetime(dia.year, dia.month, dia.day,23,59,59)

                sprint_tasks = Task.objects.filter(
                                    history__sprint__pk=sprint_id,
                                    completed_at__range=(
                                        date_ini,
                                        date_fim
                                    )
                                )
                if sprint_tasks:
                    for sprint_task in sprint_tasks:
                        soma_weight = soma_weight - sprint_task.weight
                    sprint_weights.append(int(soma_weight))
                else:
                    sprint_weights.append(int(soma_weight))
    else:
        sprints = Sprint.objects.all()
        return render_to_response('inicio.html', locals())
    return render_to_response('scrum-board.html', locals())

def updateTaskStatus(request):
    resultado = "fail"
    if "task_id" in request.GET and "new_status" in request.GET:
        task = Task.objects.get(pk=request.GET['task_id'])
        task.status = request.GET['new_status']
        if int(request.GET['new_status']) == 4:
            task.completed_at = datetime.datetime.now()
        else:
            task.completed_at = None
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
            sprinttask = Task.objects.get(pk=request.GET['task_id'])
            if sprinttask.associated_to:
                resultado = "Essa tarefa ja possui um responsavel: " + sprinttask.associated_to.username
            else:
                sprinttask.associated_to = user
                sprinttask.save()
                resultado = "ok"
        else:
            resultado = "Voce nao possui permissao, voce deve pertencer ao Grupo 'Team'."
    else:
        resultado = "Faltam parametros"
    return HttpResponse(resultado)

def index(request):
    sprints = Sprint.objects.all()
    return render_to_response('index.html', locals())

def lancarHora(request):
    retorno = "Falhou"
    if "task_id" in request.GET and "user_id" in request.GET and "qtd-horas" in request.GET:
        st = Task.objects.filter(task__pk=request.GET['task_id'])[0]
        if str(st.associated_to_id) == str(request.GET['user_id']):
            user = User.objects.get(pk=request.GET['user_id'])
            wh = WorkHour()
            wh.task = st
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
        user_id = request.POST['user_idxxx']
        task_id = request.POST['task_idxxx']
        sprint_id = request.POST['sprint_idxxx']
        task = Task.objects.filter(task__id=task_id)[0]
        task_id = task.pk
        new_request_POST = request.POST.copy()
        if not "sprinttask" in new_request_POST:
            new_request_POST['sprinttask'] = task_id
        else:
            new_request_POST['sprinttask'] = task_id
        if not "created_by" in new_request_POST:
            new_request_POST['created_by'] = user_id
        else:
            new_request_POST['created_by'] = user_id
        #####################################
        user = User.objects.get(pk = user_id)
        form = CommentForm(new_request_POST)
        if form.is_valid():
            form.save()
            form = CommentForm()
    else:
        #####################################
        task_id = request.GET['task_id']
        sprint_id = request.GET['sprint_id']
        user_id = request.GET['user_id']
        sprinttask = Task.objects.filter(task__id=task_id)
        sprinttask_id = sprinttask[0].pk
        #####################################
        form = CommentForm()
    #########################################
    comments = TaskComment.objects.filter(task__id=task_id)
    return render_to_response('comentarios.html', {'form':form,'task_id':task_id,'user_id':user_id,'sprint_id':sprint_id,'sprinttask_id':sprinttask_id,'comments':comments,},context_instance=RequestContext(request))
