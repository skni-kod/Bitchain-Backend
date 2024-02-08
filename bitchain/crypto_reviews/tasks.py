from celery import shared_task
from django.utils import timezone
from .models import CryptoReview
from django.db.utils import ProgrammingError as django_db_ProgrammingError

@shared_task
def reset_counts():
    """
     Resets 'good' and 'bad' counts for all CryptoReview objects. This task is executed every day at 00:00.
    """
    try:
        CryptoReview.objects.all().update(good=0, bad=0, last_reset_date=timezone.now().date())
        print("CryptoReview counts reset")
    except django_db_ProgrammingError:
        print("Database not ready yet. Skipping reset_counts task.")

@shared_task
def initialize_on_startup_check_update_crypto_review():
    """
    This task is executed when the Docker container starts. It checks whether the crypto review data needs to be updated,
    and resets the rating counts for crypto reviews if required.

    The task retrieves the last update date from the database and compares it with the current date. If the dates do not match,
    it performs the update by resetting the 'good' and 'bad' counts for all crypto reviews and updates the 'last_reset_date'.
    If no update is needed, it prints a message indicating that no update is required.

    """
    try: 
        last_update_date = CryptoReview.objects.values_list('last_reset_date', flat=True).first()
        if last_update_date != timezone.now().date() and last_update_date != None:
            # Perform the update if needed
            CryptoReview.objects.all().update(good=0, bad=0, last_reset_date=timezone.now().date())
            print("Initialization task on Docker startup - Data updated\n")
        else:
            print("Initialization task on Docker startup - No update needed\n")
    except django_db_ProgrammingError:
        print("Database not ready yet. Skipping initialization task.")