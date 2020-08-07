from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Applicationuser(models.Model):
    choice = (('provider','PROVIDER'),('seeker','SEEKER'))
    
    uid = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,null=True,on_delete=models.SET_NULL)
    user_satus = models.CharField(max_length=10,choices=choice)
    service_catogory = models.TextField(blank=True,null=True)
    phonenumber = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='pic/',blank=True,null=True)
    rating = models.IntegerField(default=0)
    rated_user_count = models.IntegerField(default=0)
    address = models.TextField()
    
    
    def __str__(self):
        return self.user.username

class Job(models.Model):
    choice = (('request','REQUEST'),('accept','ACCEPT'),('done','DONE'),('reject','REJECT'))
    
    job_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=30,null=True)
    job_discription = models.TextField(blank=True,null=True)
    seeker = models.ForeignKey(Applicationuser,null=True,on_delete=models.SET_NULL,related_name='job_seeker')
    provider = models.ForeignKey(Applicationuser,null=True,on_delete=models.SET_NULL,related_name='job_provider')
    job_status  = models.CharField(max_length=10,choices=choice,default='request')
    
    def __str__(self):
        return self.job_title+" ("+str(self.seeker.user.username)+")"

class Payment(models.Model):
    choice = (('pending','PENDING'),('done','DONE'))

    payment_id = models.AutoField(primary_key=True)
    job = models.OneToOneField(Job, null=True,on_delete=models.SET_NULL)
    labour_cost = models.IntegerField(default=0)
    resource_cost = models.IntegerField(default=0)
    ammount = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=10,choices=choice,default='pending')
    bill_pic = models.ImageField(blank=True,null=True,upload_to='bill/')
    
    def __str__(self):
        return str(self.payment_id)

    def get_total_billamount(self):
        self.ammount = self.labour_cost+self.resource_cost