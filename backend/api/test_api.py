from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
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

    @parameterized.expand([
        ("&&&&)$", "**()#"),
        ("@(998*)$", "valid-repo-name"),
        ("valid-username", "*()$@"),
    ])
    def test_api_get_stat_report_with_malformed_reponame_username(self, invalid_username, invalid_reponame):

        # Arrange
        url = reverse('api_get', args=[invalid_username, invalid_reponame])

        # Act
        response = self.client.get(url, data={"timezone" : self.timezone})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_api_create_stat_report_with_valid_data_and_existing_github_info(self):

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

    def test_api_create_stat_report_with_valid_data_and_non_existing_github_info(self):

        # Arrange
        url = reverse('api_post')
        data = {
            "username": "thisusernamedoesnotexist",
            "reponame": "thisrepodoesnotexist",
            "timezone": self.timezone
        }

        # Act
        response = self.client.post(url, data, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @parameterized.expand([
        ("&&&&)$", "**()#", "Invalid_Timezone"),
        ("valid-username", "valid-repository", "Invalid_Timezone"),
        (":()%&", "valid-repository", "Invalid_Timezone"),
        ("valid-username", "!)(***)", "Invalid_Timezone"),
         ("*()*$@", "!)(***)", "America/Montreal"),
    ])
    def test_api_post_invalid_data(self, invalid_username, invalid_reponame, invalid_timezone):

        # Arrange
        url = reverse('api_post')
        data = {
            "username": invalid_username,
            "reponame": invalid_reponame,
            "timezone": invalid_timezone
        }

        # Act
        response = self.client.post(url, data, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
