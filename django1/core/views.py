from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .forms import App_user_form,User_form,Payment_form,jobAssignmentForm,Comment_form
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from .models import Applicationuser,Payment,Job,Comment
from django.db.models import Q 
from json import dumps
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
import math
# Create your views here.

def index(request):
    return render(request,'index.html')


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
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('startpoint'))



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
def seeker_home(request,service_catogory = None):
    Number_of_objects_per_page = 15
    context={}
    
    if request.method == "POST":
        jobAssignmentForm_obj = jobAssignmentForm(request.POST)
        if jobAssignmentForm_obj.is_valid():
            jobAssignmentForm_obj.save()
            jobAssignmentForm_obj = jobAssignmentForm()
    else:
        jobAssignmentForm_obj = jobAssignmentForm()
    if service_catogory == "All":
        obj = Applicationuser.objects.all().exclude(user__username=request.user.username)
    else:
        obj = Applicationuser.objects.filter(Q(service_catogory = service_catogory.lower())).exclude(user__username=request.user.username) or None
    search_query = request.GET.get('search',None)
    if search_query:
        obj = obj.filter(Q(user__username__icontains =search_query)|
                        Q(service_catogory__icontains = search_query)|
                        Q(user_satus__icontains =search_query)|
                        Q(rating__icontains =search_query))
    
    if obj:
        paginated_object_list = Paginator(obj,Number_of_objects_per_page)
        page_number =  request.GET.get('page') 
        obj = paginated_object_list.get_page(page_number)
    
    context['userlist']=obj


    context['form'] =jobAssignmentForm_obj
    return render(request,'seeker.html',context)


@login_required
def seeker_history(request,service_catogory=None,*args,**kwargs):
    Number_of_objects_per_page = 15
    context={}
    
    if request.method == "POST":
            ratingform = Comment_form(request.POST or None)
            if ratingform.is_valid():
                ratingform.save()
            ratingform = Comment_form()
    else:
        ratingform = Comment_form()
    
    if service_catogory == "All":
        obj = Job.objects.filter(seeker__user__username=request.user.username)
    else:
        obj = Job.objects.filter(   Q(seeker__user__username=request.user.username) &
                                    Q(job_title = service_catogory.lower())) or None
    
    filter_query  =  request.GET.get('filter_query',"request")

    if filter_query and obj:
        obj = obj.filter(job_status=filter_query) 
    
    search_query = request.GET.get('search',None)
    if search_query and obj:
        obj = obj.filter(Q(job_title__icontains =search_query)|
                        Q(job_discription__icontains = search_query)|
                        Q(provider__user__username__icontains =search_query))    
    if obj:
        paginated_object_list = Paginator(obj,Number_of_objects_per_page)
        page_number =  request.GET.get('page') 
        obj = paginated_object_list.get_page(page_number)
    
    context['joblist']=obj
    context['ratingform']=ratingform
    return render(request,'seekerHistory.html',context)

@login_required
def provider_home(request,service_status="request",*args,**kwargs):
    Number_of_objects_per_page = 15
    context={}
    

    if request.method == "POST":
        billform = Payment_form(request.POST,request.FILES or None)

        if billform.is_valid():
                billform.save()
                billform = Payment_form()

    else:
        billform = Payment_form()

    obj = Job.objects.filter( Q(provider__user__username=request.user.username) &
                              Q(job_status=service_status))
    
    search_query = request.GET.get('search',None)
    if search_query and obj:
        obj = obj.filter(Q(job_title__icontains =search_query)|
                        Q(job_discription__icontains = search_query)|
                        Q(seeker__user__username__icontains =search_query))    
    if obj:
        paginated_object_list = Paginator(obj,Number_of_objects_per_page)
        page_number =  request.GET.get('page') 
        obj = paginated_object_list.get_page(page_number)
    
    context['joblist']=obj
    context['billform']=billform
    

    
    return render(request,'provider.html',context)

def user_page(request,user_id=None):
    # request.user.applicationuser.uid
    username = Applicationuser.objects.get(uid=user_id).user.username 
    Number_of_objects_per_page = 16
    context={}
    obj = Applicationuser.objects.get(uid=user_id )
    if request.method == "POST":
        form = App_user_form(request.POST,request.FILES,instance=obj)
        if form.is_valid():
            form.save()
    else:
        form = App_user_form( instance=obj)
    
    commentobj = Comment.objects.filter(job__provider__user__username=username)

    filter_rating_query = request.GET.get("filter_rating","accending")
    if filter_rating_query == "accending":
        commentobj = Comment.objects.filter(job__provider__user__username=username).order_by('rating','cid')
    else:
        commentobj = Comment.objects.filter(job__provider__user__username=username).order_by('-rating','cid')

    filter_category_query = request.GET.get("filter_cat","all")
    if filter_category_query == "all":
        pass
    else:
        commentobj = commentobj.filter(Q(job__job_title=filter_category_query))

    
    if commentobj:
        paginated_object_list = Paginator(commentobj,Number_of_objects_per_page)
        page_number =  request.GET.get('page') 
        commentobj = paginated_object_list.get_page(page_number)

    try:
        if int(request.user.applicationuser.uid) == int(user_id):
            context["thirdperson"] = "self"
        else:
            context["thirdperson"] = "thirdperson"
    except Exception as p:
        context["thirdperson"] = "thirdperson"
    context['userobj']= obj
    context['commentobj'] = commentobj
    context['form']=form
    context['image']= Applicationuser.objects.get(uid=user_id).profile_pic.url
    return render(request,'user.html',context)

def update_user_rating(current_rating,new_rating,job_id):
    job_obj = Job.objects.get(job_id=job_id)
    user_obj = Applicationuser.objects.filter(uid=job_obj.provider.uid).first()
    total_user_count = user_obj.rated_user_count
    current_rating = int(user_obj.rating) * total_user_count - current_rating
    new_rating = math.ceil((float(current_rating)+float(new_rating))/(float(total_user_count)))
    user_obj =  Applicationuser.objects.filter(uid=job_obj.provider.uid).update(rating=new_rating)


def job_info(request,job_id=None):
    context={}
    jobj = Job.objects.get(job_id=job_id)

    
    jobform=None
    if request.user.applicationuser.uid == jobj.seeker.uid and jobj.job_status not in "done reject" :
        if request.method == "POST" and request.POST.get('formType') =='jobform':
            jobform = jobAssignmentForm(request.POST)

            if jobform.is_valid():
                Job.objects.filter(job_id=job_id).update(
                    job_discription = jobform.cleaned_data['job_discription'],
                    jobName = jobform.cleaned_data['jobName']
                )
                
                jobform = jobAssignmentForm(instance=jobj)
        else:
            jobform = jobAssignmentForm(instance=jobj)
    
    ratingform = None
    if request.user.applicationuser.uid == jobj.seeker.uid and jobj.job_status =='done':
        comment_obj = Comment.objects.filter(job__job_id = int(job_id)).first() or None
        if request.method == "POST" and request.POST.get('formType') =='ratingform':
               ratingform = Comment_form(request.POST)
               if comment_obj:
                   if ratingform.is_valid():
                        current_rating = int(comment_obj.rating)
                        new_rating = int(ratingform.cleaned_data['rating'])
                        comment_obj = Comment.objects.filter(job__job_id = int(job_id)).update(
                            content = ratingform.cleaned_data['content'],
                            rating = ratingform.cleaned_data['rating']
                        )
                        update_user_rating(current_rating,new_rating,job_id)
                        comment_obj = Comment.objects.filter(job__job_id = int(job_id)).first()
                        ratingform = Comment_form(instance=comment_obj)
               else:
                   if ratingform.is_valid():
                        ratingform.save()
                        comment_obj = Comment.objects.filter(job__job_id = int(job_id)).first()
                        ratingform = Comment_form(instance=comment_obj)
        else:
            if comment_obj:
                ratingform = Comment_form(instance=comment_obj)
            else:
               ratingform = Comment_form() 
    
    billform=None
    if request.user.applicationuser.uid == jobj.provider.uid and jobj.job_status !='request':
        bill_obj = Payment.objects.filter(jobId = int(job_id)).first() or None
        if request.method == "POST" and request.POST.get('formType') =='billform':
               billform = Payment_form(request.POST,request.FILES)
               if bill_obj:
                   if billform.is_valid():
                        bill_obj.labour_cost =billform.cleaned_data['labour_cost']
                        bill_obj.resource_cost=billform.cleaned_data['resource_cost']
                        bill_obj.payment_status = request.POST.get('payment_status','pending')
                        if request.FILES.get('bill_pic'):
                            bill_obj.bill_pic=request.FILES.get('bill_pic')
                        bill_obj.ammount = int(billform.cleaned_data['labour_cost'])+int(billform.cleaned_data['resource_cost'])
                        bill_obj.save()
                        bill_obj = Payment.objects.filter(jobId = int(job_id)).first()
                        billform = Payment_form(instance=bill_obj)
               else:
                   if billform.is_valid():
                        billform.save()
                        bill_obj = Payment.objects.filter(jobId = int(job_id)).first()
                        billform = Payment_form(instance=bill_obj)
        else:
            if bill_obj:
                billform = Payment_form(instance=bill_obj)
            else:
               billform = Payment_form() 
    
    context['jobform']=jobform
    context['ratingform']=ratingform
    context['billform']=billform
    context["Jobobj"]=Job.objects.get(job_id=job_id)    
    return render(request,"jobinfo.html",context)


@login_required
def Cancel_work(request):
    if request.is_ajax():
        Jobobj = Job.objects.filter(job_id=int(request.GET.get('job_id'))).delete()
    return HttpResponse(None)