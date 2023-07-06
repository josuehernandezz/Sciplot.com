from django.shortcuts import render, redirect
from .forms import AbsForm, XrdForm
from django.http import JsonResponse
from .plots import abspl_plotter, xrd_plotter
from .exampleplots import exampleplot

# Create your views here.

def home(request):
    files = ['static/files/Absorbance.txt','static/files/Photoluminesence.txt']
    legend_labels = ['Abs','PL']
    title = 'Absorbance & Photoluminesence'
    x_label = 'Wavelength (nm)'
    y_label = 'Intensity (a.u.)'
    script, div = exampleplot(files, legend_labels, title, x_label, y_label)
    return render(request, 'home.html', {'script': script, 'div': div})

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
            x_label = 'Wavelength (nm)'
            y_label = 'Intensity (a.u.)'

            script, div = abspl_plotter(abs_files, pl_files, abs_labels, pl_labels, title, x_label, y_label)
            # Redirect to a success page or render a success message
            return render(request, 'plot.html', {'script': script, 'div': div, 'title': title, 'x_label': x_label, 'y_label': y_label})
    else:
        form = AbsForm()
        plot_type = '/abspl'
        return render(request, 'upload.html', {'form': form, 'plot_type': plot_type})

def xrd(request):
    if request.method == 'POST':
        form = XrdForm(request.POST, request.FILES)
        if form.is_valid():
            cardFiles = request.FILES.getlist('card_files')
            # print('cardFiles')
            # print(cardFiles)
            files = request.FILES.getlist('xrd_files')

            card_input_labels = form.cleaned_data.get('card_file_labels')
            card_legend_labels = card_input_labels.split(',') if card_input_labels else [f'Card {i+1}' for i in range(len(cardFiles))]

            input_labels = form.cleaned_data.get('xrd_labels')
            legend_labels = input_labels.split(',') if input_labels else [f'xrd {i+1}' for i in range(len(files))]            
 
            title = form.cleaned_data.get('title') or 'Powder XRD'
            x_label = r'2θ (degree)'
            y_label = 'Intensity (a.u.)'

            script, div = xrd_plotter(cardFiles, files, card_legend_labels, legend_labels, title, x_label, y_label)
            # Redirect to a success page or render a success message
            return render(request, 'plot.html', {'script': script, 'div': div, 'title': title, 'x_label': x_label, 'y_label': y_label})
    else:
        form = XrdForm()
        plot_type = '/pxrd'
        return render(request, 'upload.html', {'form': form, 'plot_type': plot_type})
