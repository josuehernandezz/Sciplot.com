from django.shortcuts import render, redirect
from .forms import AbsForm, XrdForm, PLQYForm, FTIRForm, UniversalForm
from django.http import JsonResponse
from logic import bokehPlots as bpl
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

    theme = 'dark' 

    p = bpl.abspl_plotter([abs_path], [pl_path], [abs_label], [pl_label], theme=theme)
    p2 = bpl.xrd_plotter([card_path], [xrd_path], [card_label], [xrd_label], theme=theme)
    
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

            norm_num_abs = form.cleaned_data.get('norm_num_abs') or None
            title = form.cleaned_data.get('title') or 'Absorbance & Photoluminescence'
            theme = form.cleaned_data.get('theme')

            p = bpl.abspl_plotter(abs_files, pl_files, abs_labels, pl_labels, norm_num_abs, title=title, theme=theme)
            vars = {'p1': p[0], 'p2': p[1], 'title': title}
            return render(request, 'plot.html', vars)
        else:
            vars = {'form': form}
            return render(request, 'upload.html', vars)
    else:
        form = AbsForm()
        title = 'Absorbance and Photoluminescence'
        vars = {'form': form, 'title': title, 'plot_type': '/abspl'}
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
            theme = form.cleaned_data.get('theme')

            p = bpl.xrd_plotter(cardFiles, xrd_files, card_labels, xrd_labels, title, theme=theme)
            vars = {'p1': p[0], 'p2': p[1], 'title': title}
            return render(request, 'plot.html', vars)
        else:            
            vars = {'form': form}
            return render(request, 'upload.html', vars)
    else:
        form = XrdForm()
        title = 'Powder X-ray Diffraction'
        vars = {'form': form, 'title': title, 'plot_type': '/pxrd'}
        return render(request, 'upload.html', vars)

def ftir(request):
    if request.method == 'POST':
        form = FTIRForm(request.POST, request.FILES)
        if form.is_valid():
            # Abs file handle
            ftir_files = request.FILES.getlist('ftir_files')
            input_ftir_labels = form.cleaned_data.get('ftir_labels')
            ftir_labels = input_ftir_labels.split(',') if input_ftir_labels else [f'FTIR {i+1}' for i in range(len(ftir_files))]

            title = form.cleaned_data.get('title') or 'FTIR'
            theme = form.cleaned_data.get('theme')

            p = bpl.ftir_plotter(ftir_files, ftir_labels, title, theme=theme)
            vars = {'p1': p[0], 'p2': p[1], 'title': title}
            return render(request, 'plot.html', vars)
        else:
            vars = {'form': form}
            return render(request, 'upload.html', vars)
    else:
        form = FTIRForm()
        title = 'FTIR'
        vars = {'form': form, 'title': title, 'plot_type': '/ftir'}
        return render(request, 'upload.html', vars)

def plqy(request):
    if request.method == 'POST':
        form = PLQYForm(request.POST, request.FILES)
        if form.is_valid():
            # Correction file handle
            cor_file = request.FILES.getlist('cor_file')
            input_cor_label = form.cleaned_data.get('cor_label')
            cor_label = input_cor_label.split(',') if input_cor_label else [f'Blank {i+1}' for i in range(len(cor_file))]

            # Blank file handle
            blk_file = request.FILES.getlist('blk_file')
            input_blk_label = form.cleaned_data.get('blk_label')
            blk_label = input_blk_label.split(',') if input_blk_label else [f'Blank {i+1}' for i in range(len(blk_file))]

            # Scatter file handle
            sct_file = request.FILES.getlist('sct_file')
            input_sct_label = form.cleaned_data.get('sct_label')
            sct_label = input_sct_label.split(',') if input_sct_label else [f'Scatter {i+1}' for i in range(len(sct_file))]

            # Emission file handle
            emi_file = request.FILES.getlist('emi_file')
            input_emi_label = form.cleaned_data.get('emi_label')
            emi_label = input_emi_label.split(',') if input_emi_label else [f'Emission {i+1}' for i in range(len(emi_file))]
            
            reabsorbance_checkbox = form.cleaned_data.get('checkbox') or False

            title = form.cleaned_data.get('title') or 'Quantum Yield'
            theme = form.cleaned_data.get('theme')
            
            p, plqy = bpl.plqy_plotter(cor_file, blk_file, sct_file, emi_file, cor_label, blk_label, sct_label, emi_label, reabsorbance_checkbox, title, theme=theme)
            vars = {'p1': p[0], 'p2': p[1], 'title': title, 'plqy': plqy, 'plot_type': '/plqy'}
            return render(request, 'plot.html', vars)
        else:
            vars = {'form': form}
            return render(request, 'upload.html', vars)
    else:
        form = PLQYForm()
        title = 'Quantum Yield'
        vars = {'form': form, 'title': title, 'plot_type': '/plqy'}
        return render(request, 'upload.html', vars)

def universal(request):
    if request.method == 'POST':
        form = UniversalForm(request.POST, request.FILES)
        if form.is_valid():
            # Abs file handle
            files = request.FILES.getlist('files')
            input_labels = form.cleaned_data.get('labels')
            labels = input_labels.split(',') if input_labels else [f'Abs {i+1}' for i in range(len(files))]

            title = form.cleaned_data.get('title') or 'Universal'
            theme = form.cleaned_data.get('theme')

            p = bpl.universal_plotter(files, labels, title=title, theme=theme)
            vars = {'p1': p[0], 'p2': p[1], 'title': title}
            return render(request, 'plot.html', vars)
        else:
            vars = {'form': form}
            return render(request, 'upload.html', vars)
    else:
        form = UniversalForm()
        title = 'Universal'
        vars = {'form': form, 'title': title}
        return render(request, 'upload.html', vars)
