from django.db import models

# Create your models here.


class Sticky_Notes(models.Model):

    title = models.CharField(max_length=255)
    things_to_do = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    
    
    

    