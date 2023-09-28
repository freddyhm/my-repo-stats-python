from rest_framework import serializers
from .models import StatReport

class StatReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatReport
        fields = [
            'username',
            'reponame',
            'timezone',
            'stat_content'
        ]
    
    def create(self, validated_data):
        # Custom logic for creating the instance
        print("sent to create")
        return StatReport.objects.create(**validated_data)
