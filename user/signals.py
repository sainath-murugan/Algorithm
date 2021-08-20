from allauth.account.signals import user_logged_in , user_signed_up
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from algorithm_1.models import History
import pyotp


CustomUser = get_user_model()


@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    
    user = CustomUser.objects.get(email=user.email)
    if user.authenticator_secret_code:
        pass
    else:
        secret_key = pyotp.random_base32()
        user.authenticator_secret_code = secret_key
        user.save()
    try:
        if request.user_agent.is_mobile:
            device = 'mobile'
        elif request.user_agent.is_tablet:
            device = 'tablet'
        elif request.user_agent.is_touch_capable:
            device = 'a touch capable device'
        elif request.user_agent.is_pc:
            device = 'pc'
        else:
            device = 'unknown device'
    except:
        device = 'unknown device'

    try:
        system_os =  request.user_agent.os.family
    except:
        system_os = 'unknown os'
    
    system_os = f"{system_os}(Device: {device})"
    
    try:
        system_name = request.user_agent.browser.family
    except:
        system_name = 'unknown'
    object = History.objects.create(user=user, system_os=str(system_os), system_name=str(system_name))
    object.save()