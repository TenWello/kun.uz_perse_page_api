from celery import shared_task
from .management.commands.fetch_kunuz import Command

@shared_task
def fetch_kunuz_task():
    Command().handle()
