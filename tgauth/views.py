import json
import logging

import emoji

from django.conf import settings
from django.contrib import auth
from django.urls import reverse
from django.http import Http404
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from tgauth.auth import signer
from surfers.models import LatestPoint

logger = logging.getLogger(__name__)


def emojize(msg):
    return emoji.emojize(msg, use_aliases=True)


@csrf_exempt
def botapi(request, token):

    if token != settings.TGAUTH_TOKEN:
        raise Http404()

    if request.method == 'POST':

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

            except:
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
    else:
        return HttpResponseNotAllowed()


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
        "Текущий адрес карты - https://%s\n\n"
        "Чтобы получить доступ - отправь /login\n\n"
        "Чтобы поделиться со всеми своим местоположением просто отправь "
        "его сюда. После этого оно появится на карте.\n\n"
        "На текущий момент это всё! :pray:"
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
        user.last_name = msg['from'].get('last_name')

        password = auth.get_user_model().objects.make_random_password()
        user.set_password(password)

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
            'text': emojize("""Добро пожаловать в Sunsurfers Map! :pray:
Для тебя создан новый аккаунт:
Логин - {username}
Пароль - {password}

{info}
""".format(username=user.username, password=password, info=info)),
        })

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
            'Какие люди! :-) Привет, @{username}!\n\n'
            'Напоминаю правила! :-)\n\n'
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

    return JsonResponse({
        'method': 'sendMessage',
        'chat_id': msg['chat']['id'],
        'text': (
            "Ссылка для входа на сайт (действует 10 минут):\n"
            "https://{domain}{url}"
        ).format(
            domain=settings.TGAUTH_DOMAIN,
            url=reverse("login", args=(signer.sign(msg['from']['username']),))
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
