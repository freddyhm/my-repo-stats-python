from rest_framework import status
from rest_framework.exceptions import NotFound, Throttled, APIException
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core import validators
from django.core.exceptions import ValidationError

from api.repositories.stat_report_repository import StatReportRepository

from api.services.commit_fetcher import get_part_of_day_percentage_of_commits, Part_Of_Day

@api_view(["GET"])
def api_get(request, username, repo, stat_report_repository=None, *args, **kwargs):
    timezone = request.query_params.get('timezone')

    validate_input(username, repo, timezone)

    if stat_report_repository is None:
        stat_report_repository = StatReportRepository()
    
    result = stat_report_repository.get_stat_report(username, repo)

    if result.get('success'):
        return Response(result.get('data'), status.HTTP_200_OK)
        
    return get_error_response(result.get('errors'), status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def api_post(request, stat_report_repository=None, *args, **kwargs):
    timezone = request.data['timezone']
    username = request.data['username']
    repo = request.data['reponame']

    validate_input(username, repo, timezone)

    if stat_report_repository is None:
        stat_report_repository = StatReportRepository()

    commit_stats = get_stats(username, repo, timezone)

    result = stat_report_repository.create_stat_report(username, repo, timezone, commit_stats)

    if result.get('success'):
        return Response(result.get('data'), status=status.HTTP_201_CREATED)
    
    elif "The fields username, reponame must make a unique set." in result.get('errors'):
         return get_error_response("A report for this username and repo already exists", status.HTTP_400_BAD_REQUEST)
    else:
        return get_error_response(result.errors, status.HTTP_400_BAD_REQUEST)
    
def validate_timezone(timezone):
    if timezone not in ["America/Montreal"]:
        raise ValidationError("Timezone is not valid")
    
def validate_input(username, repo, timezone):
    try:
        validators.validate_slug(username)
        validators.validate_slug(repo)
    except ValidationError as e:
        return get_error_response("Username or repo name are not valid", status.HTTP_400_BAD_REQUEST)
        
    try:
        validate_timezone(timezone)
    except ValidationError as e:
        return get_error_response(e.message, status.HTTP_400_BAD_REQUEST)
    
def get_error_response(message, status_code):
    return Response({"error": message}, status=status_code)
    

def get_stats(username, repo, timezone):
        try:
            part_of_day_percentage_of_commits = get_part_of_day_percentage_of_commits(username, repo, timezone)

            return {
                "morning": part_of_day_percentage_of_commits.get(Part_Of_Day.MORNING, 0),
                "afternoon": part_of_day_percentage_of_commits.get(Part_Of_Day.AFTERNOON, 0),
                "evening": part_of_day_percentage_of_commits.get(Part_Of_Day.EVENING, 0),
                "night": part_of_day_percentage_of_commits.get(Part_Of_Day.NIGHT, 0)
            }
        except NotFound:
            return get_error_response("Username and/or repo name do not exist in Github", status.HTTP_404_NOT_FOUND)
        except Throttled:
            return get_error_response("Exceeded Github rate limit", status.HTTP_429_TOO_MANY_REQUESTS)
        except APIException:
            return get_error_response("Could not fetch data from Github API", status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def get_error_response(message, status_code):
    return Response({"error": message}, status=status_code)