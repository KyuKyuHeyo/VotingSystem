from django.db import models

# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=255)
    user_limit = models.PositiveIntegerField()
    voting_security_email = models.BooleanField(default=True)
    display_names = models.BooleanField(default=False)

    def str(self):
        return self.title


class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def str(self):
        return self.text


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=255, blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'email')

    def __str__(self):
        return f"{self.email} - {self.option}"

