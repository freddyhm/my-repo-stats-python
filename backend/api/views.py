from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.services.commit_fetcher import get_part_of_day_percentage_of_commits
from api.services.commit_fetcher import Part_Of_Day

@api_view(["GET"])
def api_home(request, username, repo,  *args, **kwargs):

    timezone = request.query_params.get('timezone')
    part_of_day_percentage_of_commits = get_part_of_day_percentage_of_commits(username, repo, timezone)

    part_of_day = {
        "morning": part_of_day_percentage_of_commits.get(Part_Of_Day.MORNING, 0),
        "afternoon": part_of_day_percentage_of_commits.get(Part_Of_Day.AFTERNOON, 0),
        "evening": part_of_day_percentage_of_commits.get(Part_Of_Day.EVENING, 0),
        "night": part_of_day_percentage_of_commits.get(Part_Of_Day.NIGHT, 0)
    }

    

    return Response(part_of_day)