from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
#Import Personales
from .models import Inscriptos

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, inscripto, timestamp):
        return (
            six.text_type(inscripto.pk) + six.text_type(timestamp) +
            six.text_type(inscripto.activo)
        )
account_activation_token = TokenGenerator()