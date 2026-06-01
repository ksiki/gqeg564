from django.db import models


class Record(models.Model):
    name = models.CharField(max_length=49)
    date = models.DateTimeField()

    class Meta:
        db_table = "dashboard_record"
        verbose_name = "Record"
        verbose_name_plural = "Records"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.name} - {self.date}"
