from django.contrib.auth.models import User
from django.db import models
import datetime

TASK_TYPE = (
    ('F','Feature'),
    ('R','Refatoracao'),
    ('T','Teste'),
    ('C','Correcao'),
)

TASK_STATUS = (
    ('1','Nova'),
    ('2','Andamento'),
    ('3','Revisando'),
    ('4','Completa'),
)

VALUES = (
    ('0.5','0.5'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('8','8'),
    ('13','13'),
    ('20','20'),
    ('40','40'),
    ('100','100'),
    ('INF','Infinito'),
    ('?','?'),
)

class Organization(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, verbose_name="Created by")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __unicode__(self):
        return self.name

class Backlog(models.Model):
    organization = models.ForeignKey(Organization, null=True)
    name = models.CharField(max_length=100, verbose_name="Project")
    created_by = models.ForeignKey(User, verbose_name="Created by")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Backlog (Produto)"
        verbose_name_plural = "Backlogs (Produtos)"

class History(models.Model):
    backlog = models.ForeignKey(Backlog)
    name = models.CharField(max_length=100)
    weight = models.IntegerField(blank=True, default=0)
    description = models.TextField()
    created_by = models.ForeignKey(User, verbose_name="Created by")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __unicode__(self):
        return self.name

class Task(models.Model):
    history = models.ForeignKey(History)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=1, choices=TASK_TYPE, default="F")
    weight = models.IntegerField(blank=True)
    estimate = models.CharField(max_length=3, choices=VALUES, default="?")
    status = models.CharField(max_length=1, choices=TASK_STATUS, default="1")
    created_by = models.ForeignKey(User, verbose_name="Created by", related_name="created_by")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __unicode__(self):
        return self.name

class Sprint(models.Model):
    name = models.CharField(max_length=100)
    start_at = models.DateField(verbose_name="Start at", null=True, default=datetime.datetime.now())
    end_at = models.DateField(verbose_name="End at", blank=True, default=(datetime.datetime.now() + datetime.timedelta(days=15)))
    created_by = models.ForeignKey(User, verbose_name="Created by")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __unicode__(self):
        return self.name

class SprintTask(models.Model):
    sprint = models.ForeignKey(Sprint)
    task = models.ForeignKey(Task)
    associated_to = models.ForeignKey(User, verbose_name="Associated to", null=True, related_name="associated_to", blank=True)
    associated_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now(), verbose_name="Associated at")
    created_by = models.ForeignKey(User, verbose_name="Created by", null=True)

    def __unicode__(self):
        return self.sprint.name + " - " + self.task.name

class SprintTaskComment(models.Model):
    sprinttask = models.ForeignKey(SprintTask)
    created_by = models.ForeignKey(User)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now(), verbose_name="Created at")

class WorkHour(models.Model):
    user = models.ForeignKey(User)
    sprinttask = models.ForeignKey(SprintTask)
    day = models.DateField(default=datetime.date.today())
    time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)