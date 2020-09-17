from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Applicationuser(models.Model):

    class Meta:
        ordering =['uid']

    choice = (('provider','PROVIDER'),('seeker','SEEKER'))
    service_category = (
        ('cleaning','Cleaning'),
        ('plumbing','Plumbing'),
        ('electrician','Electrician'),
        ('painting','Painting'),
        ('furniture','Furniture Assembly')
    )
    
    uid = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,null=True,on_delete=models.SET_NULL)
    user_satus = models.CharField(max_length=10,choices=choice,null=True,blank=True)
    service_catogory = models.CharField(max_length=50,blank=True,null=True,choices=service_category)
    description = models.TextField(blank=True,null=True)
    phonenumber = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='pic/',blank=True,null=True)
    rating = models.IntegerField(default=0)
    rated_user_count = models.IntegerField(default=0)
    address = models.TextField()
    
    
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    class Meta:
        ordering =['payment_id']
        
    choice = (('pending','PENDING'),('done','DONE'))

    payment_id = models.AutoField(primary_key=True)
    jobId = models.IntegerField(blank=True,null=True)
    genaratedDate = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    labour_cost = models.IntegerField(default=0)
    resource_cost = models.IntegerField(default=0)
    ammount = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=10,choices=choice,default='pending')
    bill_pic = models.ImageField(blank=True,null=True,upload_to='bill/')
    
    def __str__(self):
        return str(self.payment_id)

    def get_total_billamount(self):
        self.ammount = self.labour_cost+self.resource_cost


class Job(models.Model):
    class Meta:
        ordering =['job_id']

    choice = (('request','REQUEST'),('accept','ACCEPT'),('done','DONE'),('reject','REJECT'))
    service_category = (
        ('cleaning','Cleaning'),
        ('plumbing','Plumbing'),
        ('electrician','Electrician'),
        ('painting','Painting'),
        ('furniture','Furniture Assembly')
    )
    job_id = models.AutoField(primary_key=True)
    jobName = models.CharField(max_length=40,null=True,blank=True)
    job_title = models.CharField(max_length=30,null=True,choices=service_category)
    job_discription = models.TextField(blank=True,null=True)
    assignDate = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    payment = models.OneToOneField(Payment,blank=True ,null=True,on_delete=models.SET_NULL)
    seeker = models.ForeignKey(Applicationuser,null=True,on_delete=models.SET_NULL,related_name='job_seeker')
    provider = models.ForeignKey(Applicationuser,null=True,on_delete=models.SET_NULL,related_name='job_provider')
    job_status  = models.CharField(max_length=10,choices=choice,default='request')
    
    def __str__(self):
        return str(self.job_id)+self.job_status+" ("+str(self.seeker.user.username)+")"

    def addpayment(self,paymentObj=None,job_id=None):
        obj = Job.objects.filter(job_id=job_id).update(payment=paymentObj)


class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    job = models.OneToOneField(Job,on_delete=models.CASCADE,null=False,blank=False)
    content = models.CharField(max_length=750,blank=False,null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=False,blank=False)

    class Meta:
        ordering=['cid','rating']
    
    def __str__(self):
        return str(self.cid)+" "+str(self.job.seeker.user.username)