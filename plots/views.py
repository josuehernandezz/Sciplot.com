from django.shortcuts import render, redirect
from .forms import AbsForm, XrdForm
from django.http import JsonResponse
from . import bokehPlots as bpl

# Create your views here.

def home(request):
    abs_path = 'static/files/AbsPl/Absorbance.txt'
    pl_path = 'static/files/AbsPl/Photoluminesence.txt'
    
    abs_label = 'Abs'
    pl_label = 'PL'
    
    card_path ='static/files/Xrd/CsPbBr3_ortho_pnma.txt'
    xrd_path = 'static/files/Xrd/xrd.txt'

    card_label = 'Orthorhombic'
    xrd_label = 'XRD 1'

    p= bpl.abspl_plotter([abs_path], [pl_path], [abs_label], [pl_label])
    p2 = bpl.xrd_plotter([card_path], [xrd_path], [card_label], [xrd_label])
    
    vars = {'p1': p[0], 'p2': p[1], 
            'p3': p2[0], 'p4': p2[1]}
    return render(request, 'home.html', vars)

def abspl(request):
    if request.method == 'POST':
        form = AbsForm(request.POST, request.FILES)
        if form.is_valid():
            # Abs file handle
            abs_files = request.FILES.getlist('abs_files')
            input_abs_labels = form.cleaned_data.get('abs_labels')
            abs_labels = input_abs_labels.split(',') if input_abs_labels else [f'Abs {i+1}' for i in range(len(abs_files))]

            # PL file handle
            pl_files = request.FILES.getlist('pl_files')
            input_pl_labels = form.cleaned_data.get('pl_labels')
            pl_labels = input_pl_labels.split(',') if input_pl_labels else [f'PL {i+1}' for i in range(len(pl_files))]

            title = form.cleaned_data.get('title') or 'Absorbance & Photoluminescence'

            p = bpl.abspl_plotter(abs_files, pl_files, abs_labels, pl_labels, title)
            vars = {'p1': p[0], 'p2': p[1], 'title': title}
            return render(request, 'plot.html', vars)
        else:
            vars = {'form': form}
            return render(request, 'upload.html', vars)
    else:
        form = AbsForm()
        plot_type = '/abspl'
        vars = {'form': form, 'plot_type': plot_type}
        return render(request, 'upload.html', vars)

def xrd(request):
    if request.method == 'POST':
        form = XrdForm(request.POST, request.FILES)
        if form.is_valid():
            # Card file handle
            cardFiles = request.FILES.getlist('card_files')
            card_input_labels = form.cleaned_data.get('card_file_labels')
            card_labels = card_input_labels.split(',') if card_input_labels else [f'Card {i+1}' for i in range(len(cardFiles))]
            
            # XRD file handle
            xrd_files = request.FILES.getlist('xrd_files')
            xrd_input_labels = form.cleaned_data.get('xrd_labels')
            xrd_labels = xrd_input_labels.split(',') if xrd_input_labels else [f'xrd {i+1}' for i in range(len(xrd_files))]            
 
            title = form.cleaned_data.get('title') or 'Powder XRD'

            p = bpl.xrd_plotter(cardFiles, xrd_files, card_labels, xrd_labels, title)
            vars = {'p1': p[0], 'p2': p[1], 'title': title}
            return render(request, 'plot.html', vars)
        else:            
            vars = {'form': form}
            return render(request, 'upload.html', vars)
    else:
        form = XrdForm()
        plot_type = '/pxrd'
        vars = {'form': form, 'plot_type': plot_type}
        return render(request, 'upload.html', vars)
