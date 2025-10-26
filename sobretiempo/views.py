from .models import Sobretiempo
from .forms import SobretiempoForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


"""def sobretiempo_list(request):
    qs = Sobretiempo.objects.all().order_by('-fecha_registro')

    # Filtros
    empleado = request.GET.get('empleado')
    tipo = request.GET.get('tipo')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    if empleado:
        qs = qs.filter(empleado_id=empleado)
    if tipo:
        qs = qs.filter(tipo_sobretiempo_id=tipo)
    if desde:
        qs = qs.filter(fecha_registro__gte=desde)
    if hasta:
        qs = qs.filter(fecha_registro__lte=hasta)

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'sobretiempo/sobretiempo_list.html', {'page_obj': page_obj})"""
class SobretiempoListView(LoginRequiredMixin, ListView):
    model = Sobretiempo
    template_name = 'sobretiempo/sobretiempo_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        qs = Sobretiempo.objects.all().order_by('-fecha_registro')

        # Filtros GET
        empleado = self.request.GET.get('empleado')
        tipo = self.request.GET.get('tipo')
        desde = self.request.GET.get('desde')
        hasta = self.request.GET.get('hasta')

        if empleado:
            qs = qs.filter(empleado_id=empleado)
        if tipo:
            qs = qs.filter(tipo_sobretiempo_id=tipo)
        if desde:
            qs = qs.filter(fecha_registro__gte=desde)
        if hasta:
            qs = qs.filter(fecha_registro__lte=hasta)

        return qs
    
"""def sobretiempo_create(request):
    form = SobretiempoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('sobretiempo:list')
    return render(request, 'sobretiempo/sobretiempo_form.html', {'form': form})"""
class SobretiempoCreateView(LoginRequiredMixin, CreateView):
    model = Sobretiempo
    form_class = SobretiempoForm
    template_name = 'sobretiempo/sobretiempo_form.html'
    success_url = reverse_lazy('sobretiempo:sobretiempo_list')

"""def sobretiempo_update(request, pk):
    st = get_object_or_404(Sobretiempo, pk=pk)
    form = SobretiempoForm(request.POST or None, instance=st)
    if form.is_valid():
        form.save()
        return redirect('sobretiempo:list')
    return render(request, 'sobretiempo/sobretiempo_form.html', {'form': form})"""
class SobretiempoUpdateView(LoginRequiredMixin, UpdateView):
    model = Sobretiempo
    form_class = SobretiempoForm
    template_name = 'sobretiempo/sobretiempo_form.html'
    success_url = reverse_lazy('sobretiempo:sobretiempo_list')

"""def sobretiempo_delete(request, pk):
    st = get_object_or_404(Sobretiempo, pk=pk)
    if request.method == 'POST':
        st.delete()
        return redirect('sobretiempo:list')
    return render(request, 'sobretiempo/sobretiempo_confirm_delete.html', {'sobretiempo': st})"""
class SobretiempoDeleteView(LoginRequiredMixin, DeleteView):
    model = Sobretiempo
    template_name = 'sobretiempo/sobretiempo_confirm.html'
    success_url = reverse_lazy('sobretiempo:sobretiempo_list')
    context_object_name = 'sobretiempo'
