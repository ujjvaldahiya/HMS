from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadharno = models.BigIntegerField(null = True, unique=True)
    dob = models.DateField(null=True)
    phoneno = models.BigIntegerField(unique=True, null=True)
    address = models.TextField(null=True)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    usertype = models.CharField(default='patient', max_length=100, null=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
