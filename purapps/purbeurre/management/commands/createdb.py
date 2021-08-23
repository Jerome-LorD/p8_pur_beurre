from django.core.management.base import BaseCommand, CommandError
from purapps.purbeurre.utils import Downloader, OffCleaner, Insert
from django.core import management
from purapps.purbeurre.models import Product


from purapps.purbeurre.models import Nutriscore


class Command(BaseCommand):
    """Command class."""

    help = "Install or update the database"

    def construct_db(self):
        """Commands to construct the db."""
        for page in range(1, 2):
            down_off = Downloader(page)
            extracted = down_off.extract_data()
            cleaner = OffCleaner()
            cleaned = cleaner.clean(extracted)
            construct = Insert(cleaned)
            construct.insert_data()

    def handle(self, *args, **kwargs):
        """Handle the database creation."""
        # ./manage.py sqlcreate | psql -U postgres -h localhost -W
        management.call_command("migrate", verbosity=0, interactive=False)

        if Nutriscore.objects.filter(type="e").exists():
            print("The db will be emptied and updated")
            Product.objects.all().delete()
            self.construct_db()
            print("Done, the db is ready.")
        else:
            print("The db is empty. Wait a few moments..")
            self.construct_db()
            print("Done, the db is ready.")
