from home.services.commit_fetcher import get_part_of_day_percentage_of_commits
from home.services.commit_fetcher import Part_Of_Day
from django.shortcuts import render

def home(request):
    part_of_day_percentage_of_commits = get_part_of_day_percentage_of_commits()

    part_of_day = {
        "morning": part_of_day_percentage_of_commits.get(Part_Of_Day.MORNING, 0),
        "afternoon": part_of_day_percentage_of_commits.get(Part_Of_Day.AFTERNOON, 0),
        "evening": part_of_day_percentage_of_commits.get(Part_Of_Day.EVENING, 0),
        "night": part_of_day_percentage_of_commits.get(Part_Of_Day.NIGHT, 0)
    }
    
    return render(request, 'home/index.html', {'part_of_day': part_of_day })
