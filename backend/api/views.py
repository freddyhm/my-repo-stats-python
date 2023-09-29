from rest_framework import status
from rest_framework.exceptions import NotFound, Throttled, APIException
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.repositories.stat_report_repository import StatReportRepository
from api.services.commit_fetcher_service import CommitFetcherService

from django.core.exceptions import ValidationError

from api.utilities.validators import Validator

@api_view(["GET"])
def api_get(request, username, repo, stat_report_repository=None, *args, **kwargs):
    timezone = request.query_params.get('timezone')

    try:
        Validator.validate_input(username, repo, timezone)
    except ValidationError as error:
        return get_error_response(error.message, status.HTTP_400_BAD_REQUEST)
    
    if stat_report_repository is None:
        stat_report_repository = StatReportRepository()
    
    result = stat_report_repository.get_stat_report(username, repo)

    if result.get('success'):
        return Response(result.get('data'), status.HTTP_200_OK)
    else:
        return get_error_response(result.get('errors'), status.HTTP_404_NOT_FOUND)
    
@api_view(["POST"])
def api_post(request, stat_report_repository=None, commit_fetcher_servie=None, *args, **kwargs):
    timezone = request.data['timezone']
    username = request.data['username']
    repo = request.data['reponame']

    try:
        Validator.validate_input(username, repo, timezone)
    except ValidationError as error:
        return get_error_response(error.message, status.HTTP_400_BAD_REQUEST)

    if stat_report_repository is None:
        stat_report_repository = StatReportRepository()

    if commit_fetcher_servie is None:
        commit_fetcher_servie = CommitFetcherService(username, repo, timezone)
    
    try:    
        commit_stats = commit_fetcher_servie.get_stats()
    except NotFound:
        return get_error_response("Username and/or repo name do not exist in Github", status.HTTP_404_NOT_FOUND)
    except Throttled:
        return get_error_response("Exceeded Github rate limit", status.HTTP_429_TOO_MANY_REQUESTS)
    except APIException:
        return get_error_response("Could not fetch data from Github API", status.HTTP_500_INTERNAL_SERVER_ERROR)

    result = stat_report_repository.create_stat_report(username, repo, timezone, commit_stats)

    if result.get('success'):
        return Response(result.get('data'), status=status.HTTP_201_CREATED)
    elif "The fields username, reponame must make a unique set." in result.get('errors'):
         return get_error_response("A report for this username and repo already exists", status.HTTP_400_BAD_REQUEST)
    else:
        return get_error_response(result.errors, status.HTTP_400_BAD_REQUEST)
        
def get_error_response(message, status_code):
    return Response({"error": message}, status=status_code)