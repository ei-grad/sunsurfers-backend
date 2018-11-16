import logging

from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired


logger = logging.getLogger(__name__)

signer = TimestampSigner()


class TokenBackend(object):

    def authenticate(self, request, token=None):
        if token:
            try:
                username = signer.unsign(token, max_age=600)
                logger.info("Authenticated %s", username)
                return get_user_model().objects.get(username=username)
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
