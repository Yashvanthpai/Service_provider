from django import forms
from .models import Applicationuser,Payment,Job,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import F
from math import ceil
class User_form(UserCreationForm):
     class Meta:
         model = User
         fields =  ('username','password1','password2')
         labels ={
            'username' : "Enter Unique username",
            'password1':"Enter password",
            'password2':  "Conform password"
        }
         

class App_user_form(forms.ModelForm):
    class Meta:
        model = Applicationuser
        fields = '__all__'
        exclude= ('uid','user','rating','rated_user_count')
        labels ={
            'user_satus' :'Select UserType',
            'phonenumber' : "Enter Phone Number",
            'profile_pic':"Select Profilepicture",
            'address':  "Enter Address",
            'service_catogory': "Enter service option"
        }
        widgets = {
             'description': forms.Textarea(attrs={'rows':2}),
             'address': forms.Textarea(attrs={'rows':2}),
        }

class Payment_form(forms.ModelForm):
    job_id = forms.CharField(max_length=20)
    class Meta:
        model = Payment
        exclude=('jobId',)
        fields = ('job_id','labour_cost','resource_cost','job_id','bill_pic')
        labels ={
            'job_id':"Job Id",
            'labour_cost':"Enter Labour cost",
            'resource_cost':"Enter Labour cost",
            'bill_pic':"Choose Bill image"
        }
        widgets ={
            'labour_cost' : forms.NumberInput(attrs={'required':'True'}),
            'resource_cost' : forms.NumberInput(attrs={'required':'True'}),
            'job_id' : forms.TextInput(attrs={'required':'True'})
        }
        
    def save(self,**kwargs):
        obj = super(Payment_form,self).save(commit=False)        
        obj.get_total_billamount()
        obj.jobId = int(self.cleaned_data['job_id'])
        obj = obj.save()
        payment_obj = Payment.objects.get(jobId=int(self.cleaned_data['job_id']))
        job_obj = Job.objects.filter(job_id=int(self.cleaned_data['job_id'])).update(job_status='done',payment=payment_obj)
        

class jobAssignmentForm(forms.ModelForm):
    seeker_id = forms.IntegerField(widget=forms.TextInput(attrs={'style':'display:none'}))
    provider_id = forms.IntegerField(widget=forms.TextInput(attrs={'style':'display:none'}))
    seeker_name = forms.CharField(label="Job Seeker Name",widget=forms.TextInput(attrs={'readonly':'readonly'}))
    provider_name = forms.CharField(label="Job Provider Name",widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Job
        fields = ('job_title','jobName','job_discription','seeker_id','seeker_name','provider_id','provider_name')
        labels = {
            'jobName':"Enter the job title",
            'job_title':"Job Type",
            'job_discription':"Enter the job discription",
        }
        widgets = {
            'job_discription': forms.Textarea(attrs={"rows":"2"})
        }
    
    def save(self,**kwargs):
        obj = super(jobAssignmentForm,self).save(commit=False)
        obj.seeker =  Applicationuser.objects.get(uid=self.cleaned_data['seeker_id'])
        obj.provider =  Applicationuser.objects.get(uid=self.cleaned_data['provider_id'])
        obj = obj.save()

class Comment_form(forms.ModelForm):
    comment_job_id = forms.IntegerField(widget=forms.TextInput(attrs={"style":"display:none"}))
    class Meta:
        model=Comment
        fields = ('comment_job_id','content','rating')
        labels = {
            'comment_job_id ':"Enter the job title",
            'content':"Leave Comment",
            'rating':"Do rate out of 5",
        }
        widgets = {
            'content':forms.Textarea(attrs={"rows":"2"}),
            'rating': forms.NumberInput(attrs={'type':'range', 'step': '1', 'min': '1', 'max': '5','required':"True"})
        }
    
    def save(self):
        obj = super(Comment_form,self).save(commit=False)
        job_obj = Job.objects.get(job_id=int(self.cleaned_data['comment_job_id']))
        obj.job = job_obj

        user_obj = Applicationuser.objects.get(uid=job_obj.provider.uid)

        user_obj.rating = ceil(
            ((float(user_obj.rating)+float(self.cleaned_data['rating']))*(float(user_obj.rated_user_count)+1))/(float(user_obj.rated_user_count)+1)
            )
        user_obj.rated_user_count = F('rated_user_count')+1
        user_obj = user_obj.save()

        obj = obj.save()
