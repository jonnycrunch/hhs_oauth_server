from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


def load_fixture():
    myfix = os.path.join(os.path.dirname(__file__), "fhir_server.json")
    call_command('loaddata', myfix)


class Command(BaseCommand):
    help = 'Create FHIR resource router and other FHIR tables'

    def handle(self, *args, **options):
        load_fixture()
