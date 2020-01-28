from django.db import models
from django.db.models.functions import datetime
from django.utils import timezone

class Database(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Kingdom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Organism(models.Model):
    organism = models.CharField(max_length=100)
    group = models.ForeignKey(Kingdom, on_delete=models.CASCADE, related_name='group')

    def __str__(self):
        return self.organism


class Protein(models.Model):
    protein_id = models.CharField(max_length=100)
    sequece = models.CharField(max_length=10000, default="")
    sequece_len = models.IntegerField(default=0)
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE, related_name='proteins')

    def __str__(self):
        return self.protein_id


class GeneOntology(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Region(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE, related_name='regions')
    begin = models.IntegerField(null=False)
    end = models.IntegerField(null=False)
    sequence = models.CharField(max_length=10000, null=True)
    header = models.CharField(max_length=10000, null=True)
    go = models.ManyToManyField(GeneOntology)

    def __str__(self):
        return str(self.pk)


class Load(models.Model):
    load_time = models.DateTimeField(max_length=100)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.load_time <= now


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    load_number = models.ForeignKey(Load, on_delete=models.CASCADE, related_name='clusters')
    regions = models.ManyToManyField(Region)

    def __str__(self):
        return self.name


class New(models.Model):
    event = models.CharField(max_length=1000)
    load_time = models.DateTimeField(max_length=100)
