from django.core.exceptions import ObjectDoesNotExist

from statreports.models import StatReport
from statreports.serializers import StatReportSerializer

class StatReportRepository:

    def get_stat_report(self, username, repo):
        try:
            instance = StatReport.objects.get(username=username, reponame=repo)
            data = StatReportSerializer(instance).data
        except ObjectDoesNotExist:
            return {"success" : False, "data": None, "errors": "Stat report was not found for username and repo" }

        return {"success" : True, "data": data, "errors": None }
    
    def create_stat_report(self, username, reponame, timezone, stat_content):
        data = {
            "username" : username,
            "reponame" : reponame,
            "timezone" : timezone,
            "stat_content" : stat_content
        }

        serializer = StatReportSerializer(data=data)
        
        if serializer.is_valid():
            instance = serializer.save()
            data = StatReportSerializer(instance).data
            return {"success" : True, "data": data, "errors": None }
        else:
            return {"success" : False, "data": data, "errors": serializer.errors['non_field_errors'] }
