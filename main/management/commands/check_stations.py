from main.transliterator import Lat2Cyr
from django.core.management.base import BaseCommand
from main.models import Station


class Command(BaseCommand):
    help = 'Check stations'

    def handle(self, *args, **options):
        stations = Station.objects.all()
        for i in stations:
            if Lat2Cyr().detect(i.name_uz):
                i.is_uzbek = True
            else:
                i.is_uzbek = False
            i.save()

