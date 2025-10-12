from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .forms import MovimientoForm, LineaMovimientoForm
from .models import LineaMovimiento, Movimiento

def registrar_movimiento(request):
    LineaFormSet = modelformset_factory(LineaMovimiento, form=LineaMovimientoForm, extra=1, can_delete=True)

    if request.method == "POST":
        movimiento_form = MovimientoForm(request.POST)
        formset = LineaFormSet(request.POST, queryset=LineaMovimiento.objects.none())

        if movimiento_form.is_valid() and formset.is_valid():
            movimiento = movimiento_form.save(commit=False)
            movimiento.usuario_creacion = request.user
            movimiento.save()

            # Guardar cada línea y asociarla al movimiento
            for form in formset:
                if form.cleaned_data:
                    linea = form.save(commit=False)
                    linea.movimiento = movimiento
                    linea.save()

            return redirect("movimientos")  # tenés que crear esta vista

    else:
        movimiento_form = MovimientoForm()
        formset = LineaFormSet(queryset=LineaMovimiento.objects.none())

    return render(request, "movimientos/registrar_movimiento.html", {
        "movimiento_form": movimiento_form,
        "formset": formset,
    })
    
def movimientos(request):
    movimientos = Movimiento.objects.all()
    return render(request, "movimientos/movimientos.html", {"movimientos": movimientos})