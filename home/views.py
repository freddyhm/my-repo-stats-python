from github_data_fetcher import get_github_commits
from github_data_fetcher import Part_Of_Day
from django.shortcuts import render

def home(request):
    github_commits = get_github_commits()

    part_of_day = {
        "morning": github_commits.get(Part_Of_Day.MORNING, 0),
        "afternoon": github_commits.get(Part_Of_Day.AFTERNOON, 0),
        "evening": github_commits.get(Part_Of_Day.EVENING, 0),
        "night": github_commits.get(Part_Of_Day.NIGHT, 0)
    }
    
    return render(request, 'home/index.html', {'part_of_day': part_of_day })
