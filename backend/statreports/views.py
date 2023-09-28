from rest_framework import viewsets
from django.shortcuts import render
from .models import StatReport
from serializers import StatReportSerializer

# Create your views here.
class StatReportViewSet(viewsets.ModelViewSet):
    queryset = StatReport.objects.all()
    serializer_class = StatReportSerializer
    http_method_names = ['get', 'post']  # Define allowed HTTP methods

    def perform_create(self, serializer):
        # You can implement logic to generate and save the stat report here
        serializer.save()

    def get_queryset(self):
        # Implement logic to fetch stat reports based on input parameters
        username = self.kwargs.get('username')
        repo = self.kwargs.get('repo')
        timezone = self.kwargs.get('timezone')
        return StatReport.objects.filter(username=username, repo=repo, timezone=timezone)