from allauth.account.signals import user_logged_in 
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from algorithm_1.models import History
import random
from .models import UserQrcode

CustomUser = get_user_model()


@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    
    user = CustomUser.objects.get(email=user.email)
    if user.qr_code:
        pass
    else:
        random_qr_code = random.choice(UserQrcode.objects.all())
        user.qr_code = random_qr_code
        user.authenticator_secret_code = str(random_qr_code.authenticator_secret_code)
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