from django.db import models

class Scenario(models.Model):
    title = models.CharField(max_length=255)  # Scenario title
    category = models.CharField(max_length=100, choices=[
        ('education', 'Education'),
        ('daily_life', 'Daily Life'),
        ('business', 'Business & Travel'),
        ('casual', 'Casual Conversations'),
    ])
    description = models.TextField()  # Brief scenario description
    image = models.CharField(max_length=255, default="default.png") 
    def __str__(self):
        return self.title

class Dialogue(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="dialogues")
    speaker = models.CharField(max_length=50)  # "Teacher" or "Student"
    text = models.TextField()  # Dialogue message
    order = models.PositiveIntegerField()  # Order of messages

    def __str__(self):
        return f"{self.speaker}: {self.text[:30]}"
