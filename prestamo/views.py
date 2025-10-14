from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from . forms import PrestamoForm
from . models import Prestamo

# Create your views here.
def prestamo_list(request):
    prestamos = Prestamo.objects.all()
    paginator = Paginator(prestamos, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "prestamos/prestamo_list.html", {"page_obj": page_obj})

def prestamo_create(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prestamos:prestamo_list')
    else:
        form = PrestamoForm()
    return render(request, 'prestamos/prestamo_form.html', {'form': form})

def prestamo_detail(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    return render(request, 'prestamos/prestamo_detail.html', {'prestamo': prestamo})


def prestamo_update(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect('prestamos:prestamo_list')
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, 'prestamos/prestamo_form.html', {'form': form})

def prestamo_delete(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    prestamo.delete()
    return redirect('prestamos:prestamo_list')
