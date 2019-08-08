from django.db import models

# Create your models here.
class Youtuber(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=50)
    yt_url = models.URLField(max_length=200)
    youtuber = models.ForeignKey("Youtuber", verbose_name="youtuber", on_delete=models.CASCADE)
    cosmetic = models.ManyToManyField("Cosmetic")
    upload_at = models.DateField(auto_now=False, auto_now_add=False)
    hits = models.IntegerField()

    class Meta:
        ordering = ['hits', 'title']

    def __str__(self):
        return self.title

class Bigcate(models.Model):
    name = models.CharField(max_length=50)
    eng_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Smallcate(models.Model):
    bigcate = models.ForeignKey("Bigcate", verbose_name="bigcate", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    eng_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Cosmetic(models.Model):
    category = models.ForeignKey("Smallcate", verbose_name="category", on_delete=models.CASCADE)
    name = models.CharField(max_length=240, db_index=True)

    def __str__(self):
        return self.name

# class Viuser(models.Model):
#     name = models.CharField(max_length=50)
#     pw = models.CharField(max_length=50)
#     birth = models.DateField(auto_now=False, auto_now_add=False)
#     age = models.IntegerField()
#     cosmetic = models.ManyToManyField("Cos")

#     def __str__(self):
#         return self.name

