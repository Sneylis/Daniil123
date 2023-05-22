from PIL import Image
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    group = models.CharField(max_length=2000)

    def __str__(self):
        return self.group

class Category(models.Model):
    cat = models.CharField(max_length=2000)
    gr = models.ForeignKey(Group,on_delete=models.CASCADE)

    def __str__(self):
        return self.cat

class Unit(models.Model):
    title = models.CharField(max_length=2000)
    about = models.TextField()
    character = models.TextField()
    price = models.IntegerField()
    photo = models.ImageField(upload_to='UnitPh/')
    cat = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self):
        super().save()
        img = Image.open(self.photo.path)

        if img.height > 500 or img.width > 700:
            output_size = (700, 400)
            img.thumbnail(output_size)
            img.save(self.photo.path)


class Backet (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE)
    l = models.IntegerField(default=0)

class comment(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    text = models.TextField(max_length=100000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Like (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE)
    like = models.BooleanField()

    def get_like(self):
        self.like.count()



