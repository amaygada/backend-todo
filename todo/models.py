from django.db import models

# Create your models here.

class Group(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False)
    owner = models.ForeignKey('auth.User',related_name='grps' ,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created']



class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    completed = models.BooleanField(default=False)
    belongs_to = models.ForeignKey(Group, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.data

    class Meta:
        ordering = ['created']