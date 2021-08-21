from allauth.account.signals import user_logged_in 
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.files import File
from algorithm_1.models import History
from django.conf import settings
import pyotp
import qrcode
import os
from decouple import config

CustomUser = get_user_model()


@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    
    user = CustomUser.objects.get(email=user.email)
    if user.authenticator_secret_code:
        pass
    else:
        if config("USE_S3", cast=bool) == True:
            secret_key = pyotp.random_base32()
            user.authenticator_secret_code = secret_key

            # aws settings
            AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
            AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
            PUBLIC_MEDIA_LOCATION = "mediafilies"
            MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
            DEFAULT_FILE_STORAGE = 'webapp.storage_backends.PublicMediaStorage'

            picture_path = os.path.join(settings.BASE_DIR, f"{MEDIA_URL}/user_authenticator_qrcode_image/", f"{user.id}.jpg") 
            qrcode_image =  qrcode.make(pyotp.totp.TOTP(secret_key).provisioning_uri(name=f"{user.email}", issuer_name='Algorithm'))
            qrcode_image.save(picture_path)
            user.authenticator_qrcode = "user_authenticator_qrcode_image/" + f"{user.id}.jpg"
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