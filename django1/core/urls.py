from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
from . import views
urlpatterns = static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+[
    url(r'^login/$',LoginView.as_view(template_name='login.html'),name="login"),
    url(r'^register/$',views.register,name="register"),
    url(r'^logout/$',views.logout,name="logout"),
    url(r'^accept_work_ajax/$', views.accept_work_ajax,name="accept_work"),
    url(r'^reject_work_ajax/$', views.reject_work_ajax,name="reject_work"),
    url(r"^seekerHome/(?P<service_catogory>[A-Za-z]+)/",views.seeker_home,name="Seeker"),
    url(r"^seekerHistory/(?P<service_catogory>[A-Za-z]+)/",views.seeker_history,name="Seeker_history"),
    url(r"^providerHome/(?P<service_status>[A-Za-z]+)/",views.provider_home,name="Provider"),
    url(r'^userHome/(?P<user_id>[0-9]+)/$',views.user_page,name="userhome"),
    url(r'^jobInfo/(?P<job_id>[0-9]+)/',views.job_info,name="jobInfo"),
    url(r'^cancel_work_ajax/$',views.Cancel_work,name="Cancel_work_ajax"),
    url("",views.index,name="startpoint")
]
