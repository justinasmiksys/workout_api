from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Muscle(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    url_main = models.URLField(max_length=200)
    url_sec = models.URLField(max_length=200)


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    equipment = models.CharField(max_length=100)
    primary = models.ManyToManyField(Muscle, related_name="primary")
    secondary = models.ManyToManyField(Muscle, related_name="secondary")
    description = models.TextField()
    url_img = models.URLField(max_length=200)


class Workout(models.Model):
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=10)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("title", "user")


class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    reps = models.IntegerField()
    priority = models.IntegerField()

    class Meta:
        unique_together = ("exercise", "workout", "priority")


class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date = models.DateTimeField()
