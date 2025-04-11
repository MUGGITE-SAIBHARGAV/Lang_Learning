from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    points=models.IntegerField(default=0)
    badges=models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.user.username} - {self.points} Points"
    def add_points(self,amount):
        """Increase points and assign badges if needed."""
        self.points += amount
        self.assign_badges()
        self.save()

    def assign_badges(self):
        """Assign badges based on points."""
        badge_thresholds = {
            "Beginner": 100,
            "Intermediate": 500,
            "Advanced": 1000,
            "Champion": 5000,
        }
        for badge, threshold in badge_thresholds.items():
            if self.points >= threshold and badge not in self.badges:
                self.badges.append(badge)
        self.save()
