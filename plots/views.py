from django.shortcuts import render, redirect
from .forms import FileUploadForm, XrdFileUploadForm
from django.http import JsonResponse
from .plots import abspl_plotter, xrd_plotter
from .exampleplots import exampleplot

# Create your views here.

def update_title(request):
    if request.method == 'POST':
        new_title = request.POST.get('title')
        # Update the title as desired
        print('success ' + new_title)

        form = FileUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        legend_labels = form.cleaned_data.get('legend_labels').split(',')
        title = form.cleaned_data.get('title')
        x_label = 'Wavelength (nm)'
        y_label = 'Intensity (a.u.)'

        script, div = abspl_plotter(files, legend_labels, title, x_label, y_label)
        # Redirect to a success page or render a success message
        return render(request, 'plot.html', {'script': script, 'div': div, 'title': title, 'x_label': x_label, 'y_label': y_label})
    else:
        print('Failure')
        # Return an error response if the request method is not POST
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def home(request):
    files = ['static/files/Absorbance.txt','static/files/Photoluminesence.txt']
    legend_labels = ['Abs','PL']
    title = 'Absorbance & Photoluminesence'
    x_label = 'Wavelength (nm)'
    y_label = 'Intensity (a.u.)'
    script, div = exampleplot(files, legend_labels, title, x_label, y_label)
    return render(request, 'home.html', {'script': script, 'div': div})

def your_view(request):
    link = "/xrd"  # Replace with the actual link value
    context = {'link': link}
    return render(request, 'your_template.html', context)

def abspl(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            legend_labels = form.cleaned_data.get('legend_labels').split(',')
            title = form.cleaned_data.get('title')
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
            cardfile_labels = form.cleaned_data.get('cardfile_labels').split(',')
            legend_labels = form.cleaned_data.get('legend_labels').split(',')
            title = form.cleaned_data.get('title')
            # x_label = '2'r'$\theta$ (degree)'
            x_label = r'2θ (degree)'
            y_label = 'Intensity (a.u.)'

            script, div = xrd_plotter(cardFiles, files, cardfile_labels, legend_labels, title, x_label, y_label)
            # Redirect to a success page or render a success message
            return render(request, 'plot.html', {'script': script, 'div': div, 'title': title, 'x_label': x_label, 'y_label': y_label})
    else:
        form = XrdFileUploadForm()
        plot_type = '/pxrd'
    return render(request, 'upload.html', {'form': form, 'plot_type': plot_type})

def plot(request):
    return render(request, 'plot.html')
