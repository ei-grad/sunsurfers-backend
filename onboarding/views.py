from django.shortcuts import render
from onboarding.models import OnBoard

def oboarding(request, i):
    onb = OnBoard.objects.filter(id = i)
    text = onb.text
    image = onb.image
    button = onb.next_button
    return render(request, 'onboarding_i.html', {
        'text': text, 
        'image': image,
        'button': button  
    })

