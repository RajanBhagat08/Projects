from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

class project_lead(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    description=models.CharField(max_length=60)
    project=models.CharField(max_length=60)
    work_given=models.CharField(max_length=100)
    work_given_to=models.CharField(max_length=30)
    deadline=models.DateField(null=True)
    isdone=models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.user)


def create_project_lead(sender, instance, created, **kwargs):
    if created:
        project_lead.objects.create(user=instance)

post_save.connect(create_project_lead, sender=User)





class members(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    task=models.CharField(max_length=40)
    project=models.CharField(max_length=60)
    head=models.CharField(max_length=30)
    deadline=models.DateField()
    is_done=models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.user)
