import logging

from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

from social_django.models import UserSocialAuth


logger = logging.getLogger(__name__)

signer = TimestampSigner()


class TokenBackend(object):

    def authenticate(self, request, token=None):
        if token:
            try:
                uid = signer.unsign(token, max_age=600)
                social = UserSocialAuth.objects.get(uid=uid, provider='telegram')
                logger.info("Authenticated %s", social.user.username)
                return social.user
            except SignatureExpired:
                logger.warning("Expired signature: %s", token)
            except BadSignature:
                logger.warning("Bad token: %s", token, exc_info=True)
        return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
