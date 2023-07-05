from django.shortcuts import render, redirect
from .forms import FileUploadForm, XrdFileUploadForm
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
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            
            labels = ['Sample ' + str(i) for i in range(len(files))]
            input_labels = form.cleaned_data.get('legend_labels')
            legend_labels = input_labels.split(',') if input_labels else labels

            title = form.cleaned_data.get('title') or 'Absorbance & Photoluminescence'
            x_label = 'Wavelength (nm)'
            y_label = 'Intensity (a.u.)'

            script, div = abspl_plotter(files, legend_labels, title, x_label, y_label)
            # Redirect to a success page or render a success message
            return render(request, 'plot.html', {'script': script, 'div': div, 'title': title, 'x_label': x_label, 'y_label': y_label})
    else:
        form = FileUploadForm()
        plot_type = '/abspl'
    return render(request, 'upload.html', {'form': form, 'plot_type': plot_type})

def xrd(request):
    if request.method == 'POST':
        form = XrdFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cardFiles = request.FILES.getlist('cardFiles')
            files = request.FILES.getlist('files')
            
            cardlabels = ['Card File ' + str(i) for i in range(len(files))]
            card_input_labels = form.cleaned_data.get('legend_labels')
            card_legend_labels = card_input_labels.split(',') if card_input_labels else cardlabels

            labels = ['File ' + str(i) for i in range(len(files))]
            input_labels = form.cleaned_data.get('legend_labels')
            legend_labels = input_labels.split(',') if input_labels else labels
 
            title = form.cleaned_data.get('title') or 'Powder XRD'
            x_label = r'2θ (degree)'
            y_label = 'Intensity (a.u.)'

            script, div = xrd_plotter(cardFiles, files, card_legend_labels, legend_labels, title, x_label, y_label)
            # Redirect to a success page or render a success message
            return render(request, 'plot.html', {'script': script, 'div': div, 'title': title, 'x_label': x_label, 'y_label': y_label})
    else:
        form = XrdFileUploadForm()
        plot_type = '/pxrd'
    return render(request, 'upload.html', {'form': form, 'plot_type': plot_type})
