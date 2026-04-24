from django.test import TestCase
from django.contrib.auth.models import User
from .models import Team, Activity, Workout, LeaderboardEntry
from datetime import date

class TeamModelTest(TestCase):
    def test_create_team(self):
        team = Team.objects.create(name='Test Team')
        self.assertEqual(str(team), 'Test Team')

class ActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.team = Team.objects.create(name='Test Team')

    def test_create_activity(self):
        activity = Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            date=date.today(),
            team=self.team
        )
        self.assertEqual(str(activity), f"{self.user.username} - Running on {activity.date}")

class WorkoutModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')

    def test_create_workout(self):
        workout = Workout.objects.create(
            user=self.user,
            name='Pushups',
            description='Do 3 sets of 15 pushups.'
        )
        self.assertEqual(str(workout), 'Pushups')

class LeaderboardEntryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.team = Team.objects.create(name='Test Team')

    def test_create_leaderboard_entry(self):
        entry = LeaderboardEntry.objects.create(
            user=self.user,
            team=self.team,
            score=100.0
        )
        self.assertEqual(str(entry), f"{self.user.username} - 100.0")
