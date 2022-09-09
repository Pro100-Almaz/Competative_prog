from django.db import models

class UsersList(models.Model):
    index = models.IntegerField(default=0)
    name = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=32, unique=True)
    number_of_problems = models.IntegerField(default=0)
    rating = models.IntegerField(default=1400)
    image_url = models.URLField()
    ez_problems = models.IntegerField(default=0)
    medium_problems = models.IntegerField(default=0)
    hard_problems = models.IntegerField(default=0)
    contest_num = models.IntegerField(default=0)

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return self.name

    def get_rank(self):
        return self.rating

class Contest(models.Model):
    weekly_contest = models.IntegerField(default=308)
    biweekly_contest = models.IntegerField(default=86)
    biweekly_date = models.DateTimeField()