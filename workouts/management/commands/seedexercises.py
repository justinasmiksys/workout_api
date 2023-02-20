from django.core.management.base import BaseCommand, CommandError
from workouts.models import Muscle, Exercise
from workouts.config.exercises import exercises
from slugify import slugify


class Command(BaseCommand):
    def handle(self, *args, **options):

        for exercise in exercises:

            exercise_object = Exercise.objects.create(
                name=exercise["title"],
                slug=slugify(exercise["title"]),
                equipment=exercise["equipment"],
                description="".join(exercise["description"]),
                url_img=exercise["img_url"],
            )

            for muscle in exercise["primary"]:
                slug = slugify(muscle)
                muscle_object = Muscle.objects.get(slug=slug)
                exercise_object.primary.add(muscle_object)

            for muscle in exercise["secondary"]:
                slug = slugify(muscle)
                muscle_object = Muscle.objects.get(slug=slug)
                exercise_object.secondary.add(muscle_object)
