from django.db import models

class CryptoReview(models.Model):
    """ 
    Model for a review of a cryptocurrency. 
    """
    symbol = models.CharField(max_length=10, unique=True)
    good = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)
    last_reset_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.symbol
    