import json
import logging

import emoji

from django.conf import settings
from django.contrib import auth
from django.urls import reverse
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model

from tgauth.auth import signer
from surfers.models import LatestPoint

logger = logging.getLogger(__name__)


def emojize(msg):
    return emoji.emojize(msg, use_aliases=True)


@csrf_exempt
@require_http_methods(["POST"])
def botapi(request, token):

    if token != settings.TGAUTH_WEBHOOK_SUFFIX:
        raise Http404()

    update = json.loads(request.body.decode(request.encoding or 'utf-8'))

    logger.info("Got update: %s", update)

    if 'message' in update:

        msg = update['message']

        if 'from' not in msg:
            logger.error("Got message from without 'from': %s", msg)
            return JsonResponse({
                'method': 'sendMessage',
                'chat_id': msg['chat']['id'],
                'text': 'Что-то пошло не так, боту пришло сообщение из группы.',
            })

        try:

            if msg.get('text', '')[:1] == '/':
                cmd = msg['text']
                if cmd in COMMANDS:
                    return COMMANDS[cmd](request, msg)
                else:
                    return JsonResponse({
                        'method': 'sendMessage',
                        'chat_id': msg['chat']['id'],
                        'text': 'No such command',
                    })

            elif 'location' in msg:
                return update_location(msg)

            else:
                return JsonResponse({
                    'method': 'sendMessage',
                    'chat_id': msg['chat']['id'],
                    'text': 'Обновление статуса пока не реализовано! :-)',
                })

        except Exception:
            logger.error("Failed processing %s:", msg, exc_info=True)
            return JsonResponse({
                'method': 'sendMessage',
                'chat_id': msg['chat']['id'],
                'text': 'Что-то пошло не так, сообщите администратору.',
            })

    else:
        logger.error("Unsupported update: %s", update)
        return JsonResponse({
            'method': 'sendMessage',
            'chat_id': msg['chat']['id'],
            'text': emojize('Бот не понимает сообщения такого типа :confused:'),
        })


def update_location(msg):

    user = auth.get_user_model().objects.get(username=msg['from']['username'])

    try:
        lp = LatestPoint.objects.get(user=user)
    except LatestPoint.DoesNotExist:
        lp = LatestPoint(user=user)

    lp.point = 'POINT(%s %s)' % (msg['location']['longitude'],
                                 msg['location']['latitude'])
    lp.save()

    return JsonResponse({
        'method': 'sendMessage',
        'chat_id': msg['chat']['id'],
        'text': (
            'Ваше местоположение обновлено! https://%s'
        ) % settings.TGAUTH_DOMAIN,
    })


def start_cmd(request, msg):

    info = (
        ":world_map: Карта сансёрферов - https://%s\n\n"
        ":lock: Чтобы получить доступ - отправь /login\n\n"
        ":round_pushpin: Чтобы поделиться со всеми своим местоположением просто отправь "
        "его сюда. После этого оно появится на :world_map:.\n\n"
        "Благодарим за интерес к использованию приложения! :pray:"
    ) % settings.TGAUTH_DOMAIN

    if msg['chat']['type'] != 'private':
        return JsonResponse({
            'method': 'sendMessage',
            'chat_id': msg['chat']['id'],
            'text': 'Эта команда должна быть отправлена личным сообщением, '
                    'а не публично в группе.',
        })

    user, created = auth.get_user_model().objects.get_or_create(
        username=msg['from']['username']
    )

    if created:
        user.first_name = msg['from']['first_name']
        user.last_name = msg['from'].get('last_name', '')
        user.save()

    return JsonResponse({
        'method': 'sendMessage',
        'chat_id': msg['chat']['id'],
        'reply_markup': {
            'keyboard': [[{
                'text': 'Поделиться местоположением',
                'request_location': True,
            }]],
            'resize_keyboard': True,
        },
        'text': emojize((
            'Привет, @{username}!\n\n'
            '{info}'
        ).format(username=user.username, info=info)),
    })


def login_cmd(request, msg):

    if msg['chat']['type'] != 'private':
        return JsonResponse({
            'method': 'sendMessage',
            'chat_id': msg['chat']['id'],
            'text': 'Эта команда должна быть отправлена личным сообщением, '
                    'а не публично в группе.',
        })

    username = msg['from']['username']
    user, created = get_user_model().objects.get_or_create(username=username)
    if created:
        user.first_name = msg['from']['first_name']
        user.last_name = msg['from'].get('last_name')
        user.save()
        logger.info("Created user %s", username)

    return JsonResponse({
        'method': 'sendMessage',
        'chat_id': msg['chat']['id'],
        'disable_web_page_preview': True,
        'text': (
            "Ссылка для входа на сайт (действует 10 минут):\n"
            "https://{domain}{url}"
        ).format(
            domain=settings.TGAUTH_DOMAIN,
            url=reverse("login", args=[signer.sign(username)])
        )})


COMMANDS = {
    '/login': login_cmd,
    '/start': start_cmd,
}


def login(request, token):
    user = auth.authenticate(token=token)
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
        raise Http404()
