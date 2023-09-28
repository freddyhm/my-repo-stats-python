from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, Throttled, APIException

from api.services.commit_fetcher import get_part_of_day_percentage_of_commits
from api.services.commit_fetcher import Part_Of_Day

from django.core.exceptions import ValidationError
from django.core import validators

from statreports.models import StatReport
from statreports.serializers import StatReportSerializer

@api_view(["GET"])
def api_get(request, username, repo,  *args, **kwargs):

    timezone = request.query_params.get('timezone')

    try:
        validators.validate_slug(username)
        validators.validate_slug(repo)
    except ValidationError as e:
        return Response({"error": "Username or repo name are not valid"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validate_timezone(timezone)
    except ValidationError as e:
        return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
    

    
    instance = StatReport.objects.get(username=username, reponame=repo)

    if instance:
        data = StatReportSerializer(instance).data
    
    

    return Response(data)



@api_view(["POST"])
def api_post(request, *args, **kwargs):

    timezone = request.data['timezone']
    username = request.data['username']
    repo = request.data['repo']

    try:
        validators.validate_slug(username)
        validators.validate_slug(repo)
    except ValidationError as e:
        return Response({"error": "Username or repo name are not valid"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validate_timezone(timezone)
    except ValidationError as e:
        return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

    try:
        part_of_day_percentage_of_commits = get_part_of_day_percentage_of_commits(username, repo, timezone)

        part_of_day = {
            "morning": part_of_day_percentage_of_commits.get(Part_Of_Day.MORNING, 0),
            "afternoon": part_of_day_percentage_of_commits.get(Part_Of_Day.AFTERNOON, 0),
            "evening": part_of_day_percentage_of_commits.get(Part_Of_Day.EVENING, 0),
            "night": part_of_day_percentage_of_commits.get(Part_Of_Day.NIGHT, 0)
        }
    except NotFound:
        return Response("Username and/or repo name do not exist in Github", status=status.HTTP_404_NOT_FOUND)
    except Throttled:
        return Response("Exceeded Github rate limit", status=status.HTTP_429_TOO_MANY_REQUESTS)
    except APIException:
        return Response("Could not fetch data from Github API", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    data = {
        "username" : username,
        "reponame" : repo,
        "timezone" : timezone,
        "stat_content" : part_of_day
    }

    serializer = StatReportSerializer(data=data)
    if serializer.is_valid():
        instance = serializer.save()
        print(instance)
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def validate_timezone(timezone):
    if timezone not in ["America/Montreal"]:
        raise ValidationError("Timezone is not valid")
    

