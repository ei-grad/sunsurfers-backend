from datetime import date
import logging

from cairosvg import svg2png
import svgwrite

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from checklist.models import Checklist


def checklists(request):
    return render(request, 'checklists.html', {'object_list': Checklist.objects.filter(is_active=True)})


def checklist(request, slug):
    try:
        checklist = Checklist.objects.get(slug=slug)
        items = list(checklist.item_set.order_by('ordernum'))
    except Checklist.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    today = date.today()
    if request.method == 'GET':
        return render(request, 'checklist.html', {
            'checklist': checklist,
            'items': items,
            'today': today.strftime('%a %b %d %Y'),
            'today_iso': today.isoformat(),
        })
    elif request.method == 'POST':

        width = 440
        line_height = 25
        padding_top = 100
        height = padding_top + line_height * (len(items) + 1)

        dwg = svgwrite.Drawing()
        dwg['width'] = width
        dwg['height'] = height
        path = (
            "M16.667,62.167c3.109,5.55,7.217,10.591,10.926,15.75 "
            "c2.614,3.636,5.149,7.519,8.161,10.853c-0.046-0.051,"
            "1.959,2.414,2.692,2.343c0.895-0.088,6.958-8.511,6.014-7.3 "
            "c5.997-7.695,11.68-15.463,16.931-23.696c6.393-10.025,"
            "12.235-20.373,18.104-30.707C82.004,24.988,84.802,20.601,87,16"
        )
        dwg.defs.add(dwg.path(path, fill='none', stroke='blue', stroke_width='.7em', id='checkmark'))
        r = dwg.add(dwg.rect((0, 0), rx=6, ry=6))
        r['width'] = width
        r['height'] = height
        r['fill'] = 'white'
        g = dwg.add(dwg.g(font_family='Amatic SC', font_weight="bold", font_size=24))
        if checklist.logo_image:
            img = g.add(dwg.image(checklist.logo_image.path))
            img['x'] = 20
            img['y'] = 20
            img['width'] = 60
            img['height'] = 60
        g.add(dwg.text("My checklist for %s:" % today.strftime('%a %b %d %Y'),
                       (120, 60)))
        for n, i in enumerate(items):
            y = padding_top + n*line_height
            item_g = g.add(dwg.g(transform='translate(10,%d)' % y))
            r = item_g.add(dwg.rect(fill='none', stroke_width=".1em", stroke='black'))
            r['x'] = line_height * .5
            r['y'] = int(line_height * .35)
            r['width'] = int(line_height * .6)
            r['height'] = int(line_height * .6)
            if request.POST.get(str(i.id)) == 'on':
                item_g.add(dwg.use('#checkmark', transform='translate(7, -8) scale(0.3)'))
            item_g.add(dwg.text(i.text, (45, line_height)))
        svg = dwg.tostring()

        logging.debug('Generated SVG: %s', svg)
        png = svg2png(bytestring=svg)
        response = HttpResponse(png, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="%s-%s.png"' % (
            checklist.slug, today.isoformat())
        return response
    else:
        return HttpResponseNotAllowed('<h1>Response not allowed</h1>')
