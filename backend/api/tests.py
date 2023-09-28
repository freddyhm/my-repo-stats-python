from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from statreports.models import StatReport

class StatReportAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "freddyhm"
        self.repo = "my-repo-stats-python"
        self.timezone = "America/Montreal"

    def test_api_get_existing_stat_report(self):
        
        # Arrange
        stat_report = StatReport.objects.create(
            username=self.username,
            reponame=self.repo,
            timezone=self.timezone,
            stat_content={"morning": 30, "afternoon": 40, "evening": 20, "night": 10}
        )

        url = reverse('api_get', args=[self.username, self.repo])

        # Act
        response = self.client.get(url, data={"timezone" : self.timezone})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stat_content'], stat_report.stat_content)

    def test_api_get_nonexistent_stat_report(self):

        # Arrange
        url = reverse('api_get', args=[self.username, self.repo])

        # Act
        response = self.client.get(url, data={"timezone" : self.timezone})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_post_valid_data(self):

        # Arrange
        url = reverse('api_post')
        data = {
            "username": self.username,
            "reponame": self.repo,
            "timezone": self.timezone
        }

        # Act
        response = self.client.post(url, data, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data['stat_content'], None)
        self.assertNotEqual(response.data['stat_content'], "")

    def test_api_post_duplicate_report(self):

        # Arrange
        StatReport.objects.create(
            username=self.username,
            reponame=self.repo,
            timezone=self.timezone,
            stat_content={"morning": 30, "afternoon": 40, "evening": 20, "night": 10}
        )

        url = reverse('api_post')
        data = {
            "username": self.username,
            "reponame": self.repo,
            "timezone": self.timezone
        }

        # Act
        response = self.client.post(url, data, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
