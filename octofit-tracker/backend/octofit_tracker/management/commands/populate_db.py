from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    user = models.CharField(max_length=100)
    points = models.IntegerField()
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    suggested_for = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users
        users = [
            User.objects.create_user(username='ironman', email='ironman@marvel.com', password='pass', first_name='Tony', last_name='Stark'),
            User.objects.create_user(username='captainamerica', email='cap@marvel.com', password='pass', first_name='Steve', last_name='Rogers'),
            User.objects.create_user(username='batman', email='batman@dc.com', password='pass', first_name='Bruce', last_name='Wayne'),
            User.objects.create_user(username='wonderwoman', email='wonderwoman@dc.com', password='pass', first_name='Diana', last_name='Prince'),
        ]

        # Create Activities
        Activity.objects.create(user='ironman', activity_type='Run', duration=30, team='Marvel')
        Activity.objects.create(user='captainamerica', activity_type='Swim', duration=45, team='Marvel')
        Activity.objects.create(user='batman', activity_type='Cycle', duration=60, team='DC')
        Activity.objects.create(user='wonderwoman', activity_type='Yoga', duration=50, team='DC')

        # Create Leaderboard
        Leaderboard.objects.create(user='ironman', points=100, team='Marvel')
        Leaderboard.objects.create(user='captainamerica', points=90, team='Marvel')
        Leaderboard.objects.create(user='batman', points=95, team='DC')
        Leaderboard.objects.create(user='wonderwoman', points=110, team='DC')

        # Create Workouts
        Workout.objects.create(name='Super Strength', description='Strength training for heroes', suggested_for='Marvel')
        Workout.objects.create(name='Stealth Moves', description='Agility and stealth for DC heroes', suggested_for='DC')

        # Create unique index on email for users
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db['auth_user'].create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
