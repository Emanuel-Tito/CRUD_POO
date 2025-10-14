from django.shortcuts import render, get_object_or_404, redirect
from .models import Sobretiempo
from .forms import SobretiempoForm
from django.db.models import Q
from django.core.paginator import Paginator

def sobretiempo_list(request):
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

    return render(request, 'sobretiempo/sobretiempo_list.html', {'page_obj': page_obj})

def sobretiempo_create(request):
    form = SobretiempoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('sobretiempo:list')
    return render(request, 'sobretiempo/sobretiempo_form.html', {'form': form})

def sobretiempo_update(request, pk):
    st = get_object_or_404(Sobretiempo, pk=pk)
    form = SobretiempoForm(request.POST or None, instance=st)
    if form.is_valid():
        form.save()
        return redirect('sobretiempo:list')
    return render(request, 'sobretiempo/sobretiempo_form.html', {'form': form})

def sobretiempo_delete(request, pk):
    st = get_object_or_404(Sobretiempo, pk=pk)
    if request.method == 'POST':
        st.delete()
        return redirect('sobretiempo:list')
    return render(request, 'sobretiempo/sobretiempo_confirm_delete.html', {'sobretiempo': st})