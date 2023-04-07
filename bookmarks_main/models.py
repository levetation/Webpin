from django.db import models
from django.contrib.auth.models import User

class Saved_Bookmarks(models.Model):
    bookmark_title = models.CharField(max_length=500, null=True, blank=False)
    bookmark_address = models.CharField(max_length=1_000)
    bookmark_notes = models.CharField(max_length=100_000, null=True, blank=False)
    bookmark_catagory = models.CharField(max_length=250, null=True, blank=False)

    bookmark_save_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.bookmark_title