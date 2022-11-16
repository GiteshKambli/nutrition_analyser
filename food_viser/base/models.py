from django.db import models


class UploadImage(models.Model):
    caption = models.CharField(null=True, max_length=200)
    image = models.ImageField(upload_to='users/%Y/%m/%d/')

    def __str__(self):
        return self.caption
