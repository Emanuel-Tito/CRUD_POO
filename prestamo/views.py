from . forms import PrestamoForm
from . models import Prestamo
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
"""def prestamo_list(request):
    prestamos = Prestamo.objects.all()
    paginator = Paginator(prestamos, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "prestamos/prestamo_list.html", {"page_obj": page_obj})"""
class PrestamoListView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'prestamos/prestamo_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

"""def prestamo_create(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prestamos:prestamo_list')
    else:
        form = PrestamoForm()
    return render(request, 'prestamos/prestamo_form.html', {'form': form})"""
class PrestamoCreateView(LoginRequiredMixin, CreateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamos/prestamo_form.html'
    success_url = reverse_lazy('prestamos:prestamo_list')

"""def prestamo_detail(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    return render(request, 'prestamos/prestamo_detail.html', {'prestamo': prestamo})"""
class PrestamoDetailView(LoginRequiredMixin, DetailView):
    model = Prestamo
    template_name = 'prestamos/prestamo_detail.html'
    context_object_name = 'prestamo'

"""def prestamo_update(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect('prestamos:prestamo_list')
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, 'prestamos/prestamo_form.html', {'form': form})"""
class PrestamoUpdateView(LoginRequiredMixin, UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamos/prestamo_form.html'
    success_url = reverse_lazy('prestamos:prestamo_list')

"""def prestamo_delete(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    prestamo.delete()
    return redirect('prestamos:prestamo_list')"""
class PrestamoDeleteView(LoginRequiredMixin, DeleteView):
    model = Prestamo
    template_name = 'prestamos/prestamo_confirm_delete.html'
    success_url = reverse_lazy('prestamos:prestamo_list')
    context_object_name = 'prestamo'
