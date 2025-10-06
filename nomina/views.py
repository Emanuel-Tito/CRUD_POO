from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError, models
from .models import Empleado, Nomina
from .forms import EmpleadoForm, NominaForm, NominaDetalleForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate


# Vistas para Empleados
def empleado_list(request):
    empleados = Empleado.objects.all()
    paginator = Paginator(empleados, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "nomina/empleado_list.html", {"page_obj": page_obj})


def empleado_create(request):
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado creado exitosamente.")
            return redirect("empleado_list")
    else:
        form = EmpleadoForm()
    return render(request, "nomina/empleado_form.html", {"form": form})


def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado actualizado exitosamente.")
            return redirect("empleado_list")
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, "nomina/empleado_form.html", {"form": form})


def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        empleado.delete()
        messages.success(request, "Empleado eliminado exitosamente.")
        return redirect("empleado_list")
    return render(
        request, "nomina/empleado_confirm_delete.html", {"empleado": empleado}
    )


# Vistas para Nóminas
def nomina_list(request):
    nominas = Nomina.objects.all().order_by("-aniomes")
    paginator = Paginator(nominas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "nomina/nomina_list.html", {"page_obj": page_obj})


def nomina_create(request):
    if request.method == "POST":
        form = NominaForm(request.POST)
        if form.is_valid():
            nomina = form.save()
            messages.success(request, "Nómina creada exitosamente.")
            return redirect("nomina_detail", pk=nomina.pk)
    else:
        form = NominaForm()
    return render(request, "nomina/nomina_form.html", {"form": form})


def nomina_detail(request, pk):
    nomina = get_object_or_404(Nomina, pk=pk)
    detalles = nomina.nominadetalle_set.all()

    if request.method == "POST":
        form = NominaDetalleForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.nomina = nomina
            detalle.save()
            messages.success(request, "Detalle agregado exitosamente.")
            return redirect("nomina_detail", pk=nomina.pk)
    else:
        form = NominaDetalleForm()

    return render(
        request,
        "nomina/nomina_detail.html",
        {"nomina": nomina, "detalles": detalles, "form": form},
    )


def nomina_delete(request, pk):
    nomina = get_object_or_404(Nomina, pk=pk)
    if request.method == "POST":
        nomina.delete()
        messages.success(request, "Nómina eliminada exitosamente.")
        return redirect("nomina_list")
    return render(request, "nomina/nomina_confirm_delete.html", {"nomina": nomina})


def home(request):
    # Obtener estadísticas
    total_empleados = Empleado.objects.count()
    ultima_nomina = Nomina.objects.order_by("-aniomes").first()

    # Calcular promedio de sueldos
    if total_empleados > 0:
        promedio_sueldos = Empleado.objects.aggregate(avg_sueldo=models.Avg("sueldo"))[
            "avg_sueldo"
        ]
    else:
        promedio_sueldos = 0

    context = {
        "total_empleados": total_empleados,
        "ultima_nomina": ultima_nomina,
        "promedio_sueldos": promedio_sueldos,
    }
    return render(request, "nomina/home.html", context)


def signup_view(request):
    if request.method == "GET":
        return render(request, "nomina/registro.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(
                    request,
                    "nomina/registro.html",
                    {"form": UserCreationForm, "error": "Usuario ya existe"},
                )
        return render(
                    request,
                    "nomina/registro.html",
                    {"form": UserCreationForm, "error": "Contraseña no coincide"},
                )

def signout_view(request):
    logout(request)
    return redirect('home')

def signinn(request):
    if request.method == 'GET':
        return render(request, 'nomina/signin.html', {
        'form': AuthenticationForm
    })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'nomina/signin.html', {
        'form': AuthenticationForm,
        'error': 'El usuario o contraseña es incorrecta'
    })
        else: 
            login(request, user)
            return redirect('home')