from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .forms import App_user_form,User_form,Payment_form
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from .models import Applicationuser,Payment,Job
from django.db.models import Q 
from json import dumps
from django.forms.models import model_to_dict
# Create your views here.

def index(request):
    return render(request,'one.html')


def register(request):
    register_form_appuser = App_user_form()
    register_form_djangouser = User_form()
    context ={'appuser':register_form_appuser,'djangouser':register_form_djangouser}
    
    if request.method == "POST":
        register_form_appuser = App_user_form(request.POST,request.FILES)
        register_form_djangouser = User_form(request.POST)
        
        if register_form_appuser.is_valid() and register_form_djangouser.is_valid():
            user_django = register_form_djangouser.save()
            user_app = register_form_appuser.save(commit=False)
            
            user_app.user = user_django
            
            user_app = register_form_appuser.save(commit=True)
            return HttpResponseRedirect(reverse('login'))
        else:
            context['appuser']=register_form_appuser
            context['djangouser']=register_form_djangouser
    
    return render(request,'register.html',context)
            
@login_required
def home(request):
    context={}
    page_list_count = {}
    context_key = ['user_paginator','job_request_paginator','currentjob_paginator','serveredjob_paginator']
 
    if request.method == "POST":
        payment_obj =  Payment_form(request.POST,request.FILES)
        if payment_obj.is_valid():
            payment_obj.save()
        else:
            context['payment_form'] =payment_obj
    
    obj = Applicationuser.objects.all()
    search_query = request.GET.get('search',None)
    if search_query:
        obj = obj.filter(Q(user__username__icontains =search_query)|
                        Q(service_catogory__icontains = search_query)|
                        Q(user_satus__icontains =search_query)|
                        Q(rating__icontains =search_query))
    
    context['userlist']=obj
    page_list_count['userlist'] = len(obj)

    work_dic= { 'request': 'job_request_list',
                'accept': 'currentjob_list',
                'done':'serveredjob_list'
              }

    for key , value in work_dic.items():
        list_obj = Job.objects.filter(job_status=key)
        if search_query:
            list_obj = list_obj.filter(
                        Q(seeker__user__username__icontains =search_query)|
                        Q(job_title__icontains =search_query)|
                        Q(job_id__icontains =search_query)|
                        Q(job_discription__icontains =search_query))

        context[value]=list_obj
        page_list_count[value]=len(list_obj)

    i=0
    current_page=1
    object_per_page = 10
    for key , value in page_list_count.items():
        
        page_obj= {
            'previous_page': None,
            'current_page': 1,
            'next_page': 2 if current_page * object_per_page < value else None,
            'offset': 0,
            'limit':  object_per_page if current_page * object_per_page <= value else value,
            'total_page': value// object_per_page + 1 if value % object_per_page !=0 else value // object_per_page,
        }
        context[context_key[i]] = page_obj
        i+=1
        context[key] = context[key][int(page_obj.get('offset')):int(page_obj.get('limit'))]


    context['payment_form'] = context.get('payment_form',Payment_form())
    return render(request,'Logedin.html',context)

@login_required
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('startpoint'))


@login_required
def user_info_ajax(request):
    data = None
    if request.method =="GET" and request.is_ajax():
        user_obj_md = Applicationuser.objects.get(uid=int(request.GET.get('user_id')))
        user_obj = model_to_dict( user_obj_md )
        user_obj['profile_pic'] = user_obj['profile_pic'].url
        user_obj['username'] = user_obj_md.user.username 
        
        data = dumps(user_obj)

    return HttpResponse(data,content_type="application/json")

@login_required
def job_info_ajax(request):
    data = None
    if request.method =="GET" and request.is_ajax():
        job_obj_db = Job.objects.get(job_id=int(request.GET.get('job_id')))
        job_obj = model_to_dict( job_obj_db )
        job_obj['job_phonenumber'] = job_obj_db.seeker.phonenumber
        job_obj['job_provider_username'] = job_obj_db.provider.user.username
        job_obj['job_seeker_username'] = job_obj_db.seeker.user.username
        job_obj['job_provider_pic'] = job_obj_db.provider.profile_pic.url
        job_obj['job_seeker_pic'] = job_obj_db.seeker.profile_pic.url
        
        data = dumps(job_obj)

    return HttpResponse(data,content_type="application/json")

@login_required
def payment_info_ajax(request):
    data = None
    if request.method =="GET" and request.is_ajax():
        payment_obj_db = Payment.objects.get(job__job_id=int(request.GET.get('job_id')))
        payment_obj = model_to_dict( payment_obj_db )
        payment_obj['bill_pic'] = payment_obj['bill_pic'].url
        payment_obj['bill_job_id']= int(request.GET.get('job_id'))
        payment_obj['bill_job_type']= payment_obj_db.job.job_title
        payment_obj['bill_job_desc']= payment_obj_db.job.job_discription
        payment_obj['bill_phonenumber']= payment_obj_db.job.seeker.phonenumber
        payment_obj['bill_username']= payment_obj_db.job.seeker.user.username
        
        data = dumps(payment_obj)

    return HttpResponse(data,content_type="application/json")

@login_required
def accept_work_ajax(request):
    if request.method =="GET" and request.is_ajax():
        job_obj = Job.objects.filter(job_id=int(request.GET.get('job_id'))).update(job_status='accept')
    
    return HttpResponse(None)

@login_required
def reject_work_ajax(request):
    if request.method =="GET" and request.is_ajax():
        job_obj = Job.objects.filter(job_id=int(request.GET.get('job_id'))).update(job_status='reject')
    
    return HttpResponse(None)


@login_required
def ajax_pagination(request):
    search_query = request.GET.get('search_query',None)
    object_per_page = 10
    if request.method=="GET" and request.is_ajax():
        obj_db = None
        obj_list =[]
        if str(request.GET.get('model')) == "user":
            obj_db = Applicationuser.objects.all()

            if search_query:
                obj_db = obj_db.filter(Q(user__username__icontains =search_query)|
                                Q(service_catogory__icontains = search_query)|
                                Q(user_satus__icontains =search_query)|
                                Q(rating__icontains =search_query))

            total_obj = len(obj_db)
            current_page = int(request.GET.get('currentpage'))
            dic_page = {
                'previous_page': current_page-1 if (current_page-1) > 0 else None,
                'current_page': current_page,
                'next_page': current_page+1 if current_page* object_per_page < total_obj else None,
                'offset': (current_page-1)* object_per_page,
                'limit': (current_page)* object_per_page  if (current_page)* object_per_page  <= total_obj else total_obj,
                'total_page': total_obj// object_per_page + 1 if total_obj % object_per_page !=0 else total_obj // object_per_page,
            }

            obj_db = obj_db[int(dic_page['offset']): int(dic_page['limit'])]

            for obj in obj_db:
                obj_d = model_to_dict(obj)
                obj_d['username']= obj.user.username
                obj_d['profile_pic'] = obj.profile_pic.url
                obj_list.append(obj_d)
        
        else:
            obj_db = Job.objects.filter(job_status=request.GET.get('dashoption'))

            if search_query:
                obj_db = obj_db.filter(
                        Q(seeker__user__username__icontains =search_query)|
                        Q(job_title__icontains =search_query)|
                        Q(job_id__icontains =search_query)|
                        Q(job_discription__icontains =search_query))

            total_obj = len(obj_db)
            current_page = int(request.GET.get('currentpage'))

            dic_page = {
                'previous_page': current_page-1 if (current_page-1) > 0 else None,
                'current_page': current_page,
                'next_page': current_page+1 if current_page* object_per_page < total_obj else None,
                'offset': (current_page-1)* object_per_page,
                'limit': (current_page)* object_per_page if (current_page)* object_per_page  <= total_obj else total_obj,
                'total_page': total_obj// object_per_page + 1 if total_obj % object_per_page !=0 else total_obj // object_per_page,
            }

            obj_db = obj_db[int(dic_page['offset']): int(dic_page['limit'])]

            for obj in obj_db:
                obj_d = model_to_dict(obj)
                obj_d['seeker_username']= obj.seeker.user.username
                obj_d['seeker_id'] = obj.seeker.uid
                obj_d['seeker_pic'] = obj.seeker.profile_pic.url
                obj_list.append(obj_d)
        
        dic_page['object_list'] = obj_list

        return HttpResponse(dumps(dic_page),content_type="application/json")
