from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone




usercat = [
    ('student','student'),
    ('admin','admin'),
]


stats = [
    (0,'pending'),
    (1,'approved'),
    (2,'rejected'),
]


class Folders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} -> {self.folder_name}"
    
    class Meta:
        ordering = ['folder_name']


class Files(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200, null=True)
    folder_name = models.CharField(max_length=200, null=True)
    file = models.FileField(upload_to="files/", null=False)
    created = models.DateTimeField(default=timezone.now)
    file_type = models.CharField(max_length=200, null=True)
    file_size = models.CharField(max_length=200, null=True)
    status = models.IntegerField(default=0, choices=stats)
    
    def __str__(self):
        return f"{self.user.username} -> {self.folder_name} -> {self.file}"
    
    class Meta:
        ordering = ['-created']
    
    
class Allusers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    usercat = models.CharField(max_length=200, choices=usercat)
    phone_number=models.CharField(max_length=200, null=True)
    email=models.EmailField(max_length=200, null=True)
    image = models.ImageField(upload_to='images/', null=True)
    
    def __str__(self):
        return self.user.username
    
    
    class Meta:
        ordering = ['user']
        
        
class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matric_no = models.CharField(max_length=200, null=False)
    fullname = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, null=True)
    level = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='images/', null=True)
    
    def __str__(self):
        return self.matric_no
    
    class Meta:
        ordering = ['matric_no']
        
        
class Activities(models.Model):
    recipient = models.CharField(max_length=255,null=False, default = '')
    message = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.recipient
    
    class Meta:
        ordering = ['-created']
    