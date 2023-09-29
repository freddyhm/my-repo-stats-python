from rest_framework.exceptions import NotFound, Throttled, APIException
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist

from statreports.models import StatReport
from statreports.serializers import StatReportSerializer

from api.services.commit_fetcher import get_part_of_day_percentage_of_commits, Part_Of_Day

class StatReportRepository:

    def get_stat_report(self, username, repo):
        try:
            instance = StatReport.objects.get(username=username, reponame=repo)
            data = StatReportSerializer(instance).data
        except ObjectDoesNotExist:
            return {"success" : False, "data": None, "errors": "Stat report was not found for username and repo" }

        return {"success" : True, "data": data, "errors": None }
    
    def create_stat_report(self, username, repo, timezone):
        data = {
            "username" : username,
            "reponame" : repo,
            "timezone" : timezone,
            "stat_content" : self.get_stats(username, repo, timezone)
        }

        serializer = StatReportSerializer(data=data)
        
        if serializer.is_valid():
            instance = serializer.save()
            data = StatReportSerializer(instance).data
            return {"success" : True, "data": data, "errors": None }
        else:
            return {"success" : False, "data": data, "errors": serializer.errors['non_field_errors'] }

    def get_stats(self, username, repo, timezone):
        try:
            part_of_day_percentage_of_commits = get_part_of_day_percentage_of_commits(username, repo, timezone)

            return {
                "morning": part_of_day_percentage_of_commits.get(Part_Of_Day.MORNING, 0),
                "afternoon": part_of_day_percentage_of_commits.get(Part_Of_Day.AFTERNOON, 0),
                "evening": part_of_day_percentage_of_commits.get(Part_Of_Day.EVENING, 0),
                "night": part_of_day_percentage_of_commits.get(Part_Of_Day.NIGHT, 0)
            }
        except NotFound:
            return self.get_error_response("Username and/or repo name do not exist in Github", status.HTTP_404_NOT_FOUND)
        except Throttled:
            return self.get_error_response("Exceeded Github rate limit", status.HTTP_429_TOO_MANY_REQUESTS)
        except APIException:
            return self.get_error_response("Could not fetch data from Github API", status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get_error_response(self, message, status_code):
        return Response({"error": message}, status=status_code)
