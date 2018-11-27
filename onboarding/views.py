from django.shortcuts import render
from onboarding.models import Step

def onboarding(request, step):
    obj = Step.objects.get(id = step)
    return render(request, 'onboarding.html', {
        'text': obj.text,
        'image': obj.image,
        'button': obj.next_button
    })

