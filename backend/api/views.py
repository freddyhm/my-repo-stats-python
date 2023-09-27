from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, Throttled, APIException

from api.services.commit_fetcher import get_part_of_day_percentage_of_commits
from api.services.commit_fetcher import Part_Of_Day

from django.core.exceptions import ValidationError
from django.core import validators

@api_view(["GET"])
def api_home(request, username, repo,  *args, **kwargs):

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
        return Response("Too many requests sent to Github", status=status.HTTP_429_TOO_MANY_REQUESTS)
    except APIException:
        return Response("Could not fetch data from Github API", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(part_of_day)

def validate_timezone(timezone):
    if timezone not in ["America/Montreal"]:
        raise ValidationError("Timezone is not valid")