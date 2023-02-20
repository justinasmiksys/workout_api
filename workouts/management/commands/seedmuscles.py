from django.core.management.base import BaseCommand, CommandError
from workouts.models import Muscle
from workouts.config.muscles import muscles


class Command(BaseCommand):
    def handle(self, *args, **options):

        for muscle in muscles:
            Muscle.objects.create(
                name=muscle["name"],
                slug=muscle["slug"],
                url_main=muscle["url_main"],
                url_sec=muscle["url_sec"],
            )
