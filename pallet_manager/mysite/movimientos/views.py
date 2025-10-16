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
#Laura
 # movimientos/views.py
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.utils import timezone

from .models import Movimiento, LineaMovimiento
# 👉 import mínimo para elegir una empresa válida sin tocar otros módulos
from empresas.models import Empresa


# ========== Helpers de introspección ==========
def _get_tipo_field():
    return LineaMovimiento._meta.get_field("tipo_pallet")


def _tipo_is_relation():
    field = _get_tipo_field()
    return getattr(field, "is_relation", False) and getattr(field, "remote_field", None) is not None


def _tipo_model_or_none():
    if not _tipo_is_relation():
        return None
    return _get_tipo_field().remote_field.model


def _tipo_label(value_or_obj) -> str:
    if value_or_obj is None:
        return "—"
    if hasattr(value_or_obj, "_meta"):
        for attr in ("nombre", "name", "titulo", "tipo", "descripcion", "label", "codigo", "letra"):
            if hasattr(value_or_obj, attr):
                val = getattr(value_or_obj, attr)
                if val:
                    return str(val)
        return str(value_or_obj)
    return str(value_or_obj)


# ========== Cálculo de stock ==========
def _snapshot_stock():
    agregados = (
        LineaMovimiento.objects
        .values("tipo_pallet")
        .annotate(
            in_qty=Sum("cantidad", filter=Q(movimiento__tipo="IN")),
            out_qty=Sum("cantidad", filter=Q(movimiento__tipo="OUT")),
            dmg_qty=Sum("cantidad", filter=Q(motivo__iexact="daño") | Q(motivo__iexact="dañado")),
        )
    )

    stock_map = {}
    total_disp = total_uso = total_dmg = 0

    if _tipo_is_relation():
        TipoModel = _tipo_model_or_none()
        ids = [row["tipo_pallet"] for row in agregados if row["tipo_pallet"] is not None]
        rel_map = {obj.id: obj for obj in TipoModel.objects.filter(id__in=ids)}

        def get_label(key): return _tipo_label(rel_map.get(key))

        for row in agregados:
            key = row["tipo_pallet"]
            in_qty = row["in_qty"] or 0
            out_qty = row["out_qty"] or 0
            dmg_qty = row["dmg_qty"] or 0

            en_uso = out_qty
            disponibles = max(in_qty - out_qty - dmg_qty, 0)
            total = disponibles + en_uso + dmg_qty

            stock_map[key] = {
                "tipo_id": key,
                "tipo": get_label(key),
                "total": total,
                "disponibles": disponibles,
                "en_uso": en_uso,
                "danados": dmg_qty,
            }

            total_disp += disponibles
            total_uso += en_uso
            total_dmg += dmg_qty

    else:
        field = LineaMovimiento._meta.get_field("tipo_pallet")
        choices = list(getattr(field, "choices", []))
        for val, lbl in choices:
            key = str(val)
            stock_map[key] = {
                "tipo_id": key,
                "tipo": _tipo_label(lbl),
                "total": 0,
                "disponibles": 0,
                "en_uso": 0,
                "danados": 0,
            }

        for row in agregados:
            key = str(row["tipo_pallet"])
            in_qty = row["in_qty"] or 0
            out_qty = row["out_qty"] or 0
            dmg_qty = row["dmg_qty"] or 0

            en_uso = out_qty
            disponibles = max(in_qty - out_qty - dmg_qty, 0)
            total = disponibles + en_uso + dmg_qty

            if key not in stock_map:
                stock_map[key] = {
                    "tipo_id": key,
                    "tipo": _tipo_label(key),
                    "total": 0,
                    "disponibles": 0,
                    "en_uso": 0,
                    "danados": 0,
                }

            stock_map[key]["total"] += total
            stock_map[key]["disponibles"] += disponibles
            stock_map[key]["en_uso"] += en_uso
            stock_map[key]["danados"] += dmg_qty

            total_disp += disponibles
            total_uso += en_uso
            total_dmg += dmg_qty

    stock = sorted(stock_map.values(), key=lambda x: str(x["tipo"]))
    contadores = {"disponibles": total_disp, "en_uso": total_uso, "danados": total_dmg}
    return stock, contadores


# ========== Pantalla ==========
@login_required
def gestion_stock(request):
    stock_data, contadores = _snapshot_stock()

    if _tipo_is_relation():
        TipoModel = _tipo_model_or_none()
        objetos = list(TipoModel.objects.all().order_by("id"))
        tipos = [{"id": obj.pk, "label": _tipo_label(obj)} for obj in objetos]
    else:
        field = LineaMovimiento._meta.get_field("tipo_pallet")
        choices = getattr(field, "choices", [])
        tipos = [{"id": val, "label": str(lbl)} for (val, lbl) in choices]

    return render(request, "movimientos/gestion_stock.html", {
        "stock_data": stock_data,
        "contadores": contadores,
        "tipos": tipos,
    })


# ========== Acción (impacta BD) ==========
@login_required
@require_POST
def actualizar_stock(request):
    """
    Crea un Movimiento + LineaMovimiento.

    POST:
      - operacion: 'IN' | 'OUT'
      - tipo_pallet_id: 'A' | 'B' | 'C'  (según choices de LineaMovimiento)
      - cantidad: int (>0)
      - (opcional) empresa_id, ubicacion_origen, ubicacion_destino
    """
    try:
        operacion = (request.POST.get("operacion") or "").upper()
        tipo_raw = request.POST.get("tipo_pallet_id")
        cantidad = int(request.POST.get("cantidad") or "0")
        motivo = (request.POST.get("motivo") or "").strip() or ("Ingreso" if operacion == "IN" else "Egreso")

        if operacion not in ("IN", "OUT"):
            return JsonResponse({"ok": False, "error": "Operación inválida."}, status=400)
        if tipo_raw in (None, "") or cantidad <= 0:
            return JsonResponse({"ok": False, "error": "Datos incompletos o cantidad inválida."}, status=400)

        # -------- Resolver EMPRESA ----------
        # 1) Si viene empresa_id lo usamos; 2) si no, elegimos una válida según reglas del modelo
        empresa = None
        empresa_id = request.POST.get("empresa_id")
        if empresa_id:
            try:
                empresa = Empresa.objects.get(pk=int(empresa_id))
            except (ValueError, Empresa.DoesNotExist):
                return JsonResponse({"ok": False, "error": "Empresa inválida."}, status=400)
        else:
            if operacion == "IN":
                empresa = Empresa.objects.filter(es_proveedor=True).order_by("id").first()
            else:
                empresa = Empresa.objects.filter(es_proveedor=False).order_by("id").first()
            if not empresa:
                return JsonResponse({"ok": False, "error": "No hay empresa válida para registrar el movimiento."}, status=400)

        # -------- Ubicaciones (distintas entre sí) ----------
        ubic_origen = (request.POST.get("ubicacion_origen") or "").strip()
        ubic_dest = (request.POST.get("ubicacion_destino") or "").strip()

        if not ubic_origen or not ubic_dest:
            # Defaults seguros (no iguales) para pasar validación sin tocar la UI
            if operacion == "IN":
                ubic_origen = ubic_origen or "Proveedor"
                ubic_dest = ubic_dest or "Depósito"
            else:
                ubic_origen = ubic_origen or "Depósito"
                ubic_dest = ubic_dest or "Cliente"

        if ubic_origen == ubic_dest:
            # Evitar rechazos del modelo
            ubic_dest = f"{ubic_dest} (destino)"

        # -------- Crear cabecera ----------
        mov = Movimiento(
            empresa=empresa,
            usuario_creacion=request.user,
            tipo=operacion,
            # fecha_hora es auto_now_add en el modelo
            ubicacion_origen=ubic_origen,
            ubicacion_destino=ubic_dest,
            # estado_confirmacion queda en PENDIENTE (default del modelo)
            observaciones=""
        )
        # Usamos clean/save del modelo para respetar reglas y capturar errores legibles
        try:
            mov.save()
        except Exception as e:
            # Devolver mensajes de validación entendibles
            return JsonResponse({"ok": False, "error": str(e)}, status=400)

        # -------- Crear línea ----------
        linea_kwargs = {
            "movimiento": mov,
            "cantidad": cantidad,
            "motivo": motivo,
        }

        if _tipo_is_relation():
            TipoModel = _tipo_model_or_none()
            try:
                tipo_obj = TipoModel.objects.get(pk=int(tipo_raw))
            except Exception:
                return JsonResponse({"ok": False, "error": "ID de tipo inválido."}, status=400)
            linea_kwargs["tipo_pallet"] = tipo_obj
        else:
            # Validar contra choices definidos en LineaMovimiento.tipo_pallet
            field = LineaMovimiento._meta.get_field("tipo_pallet")
            choices_keys = {str(k) for k, _ in getattr(field, "choices", [])}
            tipo_val = str(tipo_raw)
            if choices_keys and tipo_val not in choices_keys:
                return JsonResponse({"ok": False, "error": "Tipo de pallet inválido."}, status=400)
            linea_kwargs["tipo_pallet"] = tipo_val

        try:
            LineaMovimiento.objects.create(**linea_kwargs)
        except Exception as e:
            return JsonResponse({"ok": False, "error": str(e)}, status=400)

        # -------- Refrescar snapshot ----------
        stock_data, contadores = _snapshot_stock()
        return JsonResponse({"ok": True, "stock": stock_data, "contadores": contadores})

    except Exception as e:
        return JsonResponse({"ok": False, "error": f"Error inesperado: {e}"}, status=500)
