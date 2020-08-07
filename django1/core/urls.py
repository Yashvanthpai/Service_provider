from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
from . import views
urlpatterns = static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+[
    url(r'^login/$',LoginView.as_view(template_name='login.html'),name="login"),
    url(r'^register/$',views.register,name="register"),
    url(r'^home/$',views.home,name="home"),
    url(r'^logout/$',views.logout,name="logout"),
    url(r'^user_detaile_ajax/$', views.user_info_ajax,name="user_info_ajax"),
    url(r'^payment_detaile_ajax/$', views.payment_info_ajax,name="payment_info_ajax"),
    url(r'^job_detaile_ajax/$', views.job_info_ajax,name="job_info_ajax"),
    url(r'^accept_work_ajax/$', views.accept_work_ajax,name="accept_work"),
    url(r'^reject_work_ajax/$', views.reject_work_ajax,name="reject_work"),
    url(r'^pagination_ajax/$', views.ajax_pagination,name="ajax_pagination"),
    url("",views.index,name="startpoint")
]
