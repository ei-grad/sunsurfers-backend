from django.shortcuts import render
from onboarding.models import Step

def oboarding(request, step):
    obj = Step.objects.filter(id = step)
    return render(request, 'onboarding.html', {
        'text': obj.text, 
        'image': obj.image,
        'button': obj.next_button  
    })

