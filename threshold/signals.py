from django.db.models.signals import post_migrate
from django.core.management import call_command
from django.dispatch import receiver

@receiver(post_migrate)
def load_fixtures(sender, **kwargs):
    if sender.name == 'threshold':
        call_command('loaddata', 'threshold/fixtures/pond_quality_threshold.json')