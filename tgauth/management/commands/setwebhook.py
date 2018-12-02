import json
import os

from django.core.management.base import BaseCommand
from django.urls import reverse
from django.conf import settings

import requests


class Command(BaseCommand):
    help = 'Setup Telegram Bot API Webhook'

    def add_arguments(self, parser):
        parser.add_argument('--token',
                            default=os.environ.get('TELEGRAM_TOKEN'),
                            help='API token to use (get from @BotFather)')

    def handle(self, token, **kwargs):
        url = 'https://{domain}{path}'.format(
            domain=settings.TGAUTH_DOMAIN,
            path=reverse('tgauth:webhook', args=(settings.TGAUTH_WEBHOOK_SUFFIX,))
        )
        answer = input('''
Are you sure to set webhook to:

%s

Type 'yes' to continue, or 'no' to cancel: ''' % url)
        if answer == 'yes':
            print(requests.post(
                'https://api.telegram.org/bot{}/setWebhook'.format(token),
                data=json.dumps({'url': url}),
                headers={'Content-Type': 'application/json'},
            ).json())
