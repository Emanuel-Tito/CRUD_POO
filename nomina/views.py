from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView, FormView, RedirectView
from django.db.models import Avg
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError, models
from .models import Empleado, Nomina
from .forms import EmpleadoForm, NominaForm, NominaDetalleForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

"""def home(request):
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
    return render(request, "nomina/home.html", context)"""
class HomeView(TemplateView):
    template_name = "nomina/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_empleados = Empleado.objects.count()
        ultima_nomina = Nomina.objects.order_by("-aniomes").first()

        if total_empleados > 0:
            promedio_sueldos = Empleado.objects.aggregate(avg_sueldo=Avg("sueldo"))["avg_sueldo"]
        else:
            promedio_sueldos = 0

        context.update({
            "total_empleados": total_empleados,
            "ultima_nomina": ultima_nomina,
            "promedio_sueldos": promedio_sueldos,
        })
        return context

#EMPLEADOS
"""def empleado_list(request):
    empleados = Empleado.objects.all()
    paginator = Paginator(empleados, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "nomina/empleado_list.html", {"page_obj": page_obj})"""
class EmpleadoListView(ListView):
    model = Empleado
    template_name = "nomina/empleado_list.html"
    context_object_name = "page_obj"
    paginate_by = 10


"""def empleado_create(request):
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado creado exitosamente.")
            return redirect("empleado_list")
    else:
        form = EmpleadoForm()
    return render(request, "nomina/empleado_form.html", {"form": form})"""
class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = "nomina/empleado_form.html"
    success_url = reverse_lazy("nomina:empleado_list")

    def form_valid(self, form):
        messages.success(self.request, "Empleado creado exitosamente.")
        return super().form_valid(form)


"""def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado actualizado exitosamente.")
            return redirect("empleado_list")
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, "nomina/empleado_form.html", {"form": form})"""
class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = "nomina/empleado_form.html"
    success_url = reverse_lazy("nomina:empleado_list")

    def form_valid(self, form):
        messages.success(self.request, "Empleado actualizado exitosamente.")
        return super().form_valid(form)


"""def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        empleado.delete()
        messages.success(request, "Empleado eliminado exitosamente.")
        return redirect("empleado_list")
    return render(
        request, "nomina/empleado_confirm_delete.html", {"empleado": empleado}
    )"""
class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = "nomina/empleado_confirm_delete.html"
    success_url = reverse_lazy("nomina:empleado_list")
    context_object_name = "empleado"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Empleado eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

#NOMINAS
"""def nomina_list(request):
    nominas = Nomina.objects.all().order_by("-aniomes")
    paginator = Paginator(nominas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "nomina/nomina_list.html", {"page_obj": page_obj})"""
class NominaListView(ListView):
    model = Nomina
    template_name = "nomina/nomina_list.html"
    context_object_name = "page_obj"
    paginate_by = 10
    ordering = ["-aniomes"]

"""def nomina_create(request):
    if request.method == "POST":
        form = NominaForm(request.POST)
        if form.is_valid():
            nomina = form.save()
            messages.success(request, "Nómina creada exitosamente.")
            return redirect("nomina_detail", pk=nomina.pk)
    else:
        form = NominaForm()
    return render(request, "nomina/nomina_form.html", {"form": form})"""
class NominaCreateView(CreateView):
    model = Nomina
    form_class = NominaForm
    template_name = "nomina/nomina_form.html"

    def form_valid(self, form):
        nomina = form.save()
        messages.success(self.request, "Nómina creada exitosamente.")
        return redirect("nomina:nomina_detail", pk=nomina.pk)

"""def nomina_detail(request, pk):
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
    )"""
class NominaDetailView(DetailView):
    model = Nomina
    template_name = "nomina/nomina_detail.html"
    context_object_name = "nomina"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detalles"] = self.object.nominadetalle_set.all()
        context["form"] = NominaDetalleForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = NominaDetalleForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.nomina = self.object
            detalle.save()
            messages.success(request, "Detalle agregado exitosamente.")
        return redirect("nomina:nomina_detail", pk=self.object.pk)

"""def nomina_delete(request, pk):
    nomina = get_object_or_404(Nomina, pk=pk)
    if request.method == "POST":
        nomina.delete()
        messages.success(request, "Nómina eliminada exitosamente.")
        return redirect("nomina_list")
    return render(request, "nomina/nomina_confirm_delete.html", {"nomina": nomina})"""
class NominaDeleteView(DeleteView):
    model = Nomina
    template_name = "nomina/nomina_confirm_delete.html"
    success_url = reverse_lazy("nomina:nomina_list")
    context_object_name = "nomina"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Nómina eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)
# Registro de usuario
"""def signup_view(request):
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
                return redirect('nomina:home')
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
                )"""
class SignupView(FormView):
    template_name = "nomina/registro.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("nomina:home")

    def form_valid(self, form):
        password1 = self.request.POST.get("password1")
        password2 = self.request.POST.get("password2")
        if password1 != password2:
            return self.form_invalid(form, error="Contraseña no coincide")

        try:
            user = User.objects.create_user(
                username=self.request.POST.get("username"),
                password=password1,
            )
            login(self.request, user)
            return redirect(self.success_url)
        except IntegrityError:
            return self.form_invalid(form, error="Usuario ya existe")

    def form_invalid(self, form, error=None):
        context = {"form": self.form_class(), "error": error} if error else {"form": form}
        return render(self.request, self.template_name, context)
# Cierre de sesión
"""def signout_view(request):
    logout(request)
    return redirect('nomina:home')"""
class SignoutView(RedirectView):
    pattern_name = "nomina:home"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
# Inicio de sesión
"""def signinn(request):
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
            return redirect('nomina:home')"""
class SigninView(FormView):
    template_name = "nomina/signin.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("nomina:home")

    def form_valid(self, form):
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            return self.form_invalid(form, error="El usuario o contraseña es incorrecta")
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form, error=None):
        context = {"form": self.form_class(), "error": error} if error else {"form": form}
        return render(self.request, self.template_name, context)