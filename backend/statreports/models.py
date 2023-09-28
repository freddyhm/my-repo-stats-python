from django.db import models

class StatReport(models.Model):
    username = models.CharField(max_length=255)
    reponame = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)
    stat_content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('username', 'reponame')
