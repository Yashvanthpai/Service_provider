from django import forms
from .models import Applicationuser,Payment,Job
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
             'address': forms.Textarea(attrs={'rows':2}),
             'service_catogory': forms.Textarea(attrs={'rows':2})
        }

class Payment_form(forms.ModelForm):
    job_id = forms.CharField(max_length=20)
    class Meta:
        model = Payment
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
        obj.job =  Job.objects.get(job_id=self.cleaned_data['job_id'])
        obj = obj.save(commit=True)
        obj.get_total_billamount()

        job_obj = Job.objects.filter(job_id=int(self.cleaned_data['job_id'])).update(job_status='done')
        