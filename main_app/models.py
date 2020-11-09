from django.db import models


class Currency(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    char_code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.char_code}: {self.name}"
