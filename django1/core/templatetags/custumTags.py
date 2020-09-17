from django import template
from core.models import Applicationuser,Comment
register = template.Library()


@register.filter(name="Check_rated")
def getUidFromName(value):
    ans = Comment.objects.filter(job__job_id=int(value)) or None
    if ans:
        return "yes"
    return "no"

@register.filter(name="getServiceType")
def getServiceTypeFromUsername(value):
    ans = Applicationuser.objects.get(user__username=value).user_satus
    return ans.upper() or None
