# Generated by Django 4.2.5 on 2023-09-28 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('reponame', models.CharField(max_length=255)),
                ('timezone', models.CharField(max_length=255)),
                ('stat_content', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('username', 'reponame')},
            },
        ),
    ]
