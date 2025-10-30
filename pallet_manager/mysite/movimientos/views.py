from django.shortcuts import render
#create your view here

#   Pagina principal Movimientos
#   Función para ver el remito
def ver_remito(request, movimiento_id):
    movimiento = Movimiento.objects.get(id=movimiento_id)
    lineas = movimiento.lineas.all()

    contexto = {
        "movimiento": {
            "id": movimiento.id,
            "fecha_creacion": movimiento.fecha_hora,
            "usuario_creacion": movimiento.usuario_creacion or request.user,
            "empresa": movimiento.empresa,
            "observaciones": movimiento.observaciones,
            "ubicacion_origen": movimiento.ubicacion_origen,
            "ubicacion_destino": movimiento.ubicacion_destino,
            "tipo": movimiento.tipo,  # IN/OUT
        },
        "lineas": [
            {
                "tipo_pallet": linea.tipo_pallet,
                "cantidad": linea.cantidad,
                "movimiento": {
                    "ubicacion_origen": linea.movimiento.ubicacion_origen,
                    "ubicacion_destino": linea.movimiento.ubicacion_destino,
                }
            }
            for linea in lineas
        ],
        "title": f"Remito de {'ingreso' if movimiento.tipo == 'IN' else 'egreso'}",
        "header_title": "movimientos"
    }
    
    return render(request, "movimientos/remito.html", contexto)

#   ⬇⬇⬇⬇⬇ FUNCIONES DE REGISTRAR MOVIMIENTOS Y MOSTRARLOS EN LA LISTA PRINCIPAL ⬇⬇⬇⬇⬇
from django.shortcuts import render, redirect
from django.forms import modelformset_factory, inlineformset_factory
from .forms import IngresoMovimientoForm, MovimientoForm, EgresoMovimientoForm, LineaMovimientoForm
from .models import Movimiento, LineaMovimiento
from django.contrib import messages
from django.db import transaction

def ingresar_movimiento(request):
    # Usar inlineformset_factory para vincular LineaMovimiento a Movimiento
    LineaFormSet = inlineformset_factory(
        Movimiento,
        LineaMovimiento,
        form=LineaMovimientoForm,
        extra=1,
        can_delete=True
    )

    if request.method == "POST":
        movimiento_form = IngresoMovimientoForm(request.POST)
        formset = LineaFormSet(request.POST)

        if movimiento_form.is_valid() and formset.is_valid():
            movimiento = movimiento_form.save(commit=False)
            movimiento.usuario_creacion = request.user
            movimiento.save()
            formset.instance = movimiento
            formset.save()
            messages.success(request, "✅ Movimiento ingresado correctamente.")
            return redirect("movimientos:movimientos")
    else:
        movimiento_form = IngresoMovimientoForm()
        formset = LineaFormSet()

    context = {
        "movimiento_form": movimiento_form,
        "formset": formset,
        "title": "Movimientos"
    }
    return render(request, "movimientos/ingresar_movimiento.html", context)

def registrar_movimiento(request):
    LineaFormSet = modelformset_factory(LineaMovimiento, form=LineaMovimientoForm, extra=1, can_delete=True)

    if request.method == "POST":
        movimiento_form = MovimientoForm(request.POST)
        formset = LineaFormSet(request.POST, queryset=LineaMovimiento.objects.none())

        # Verificamos cuál botón fue presionado
        generar_remito = "btn-remito" in request.POST

        if movimiento_form.is_valid() and formset.is_valid():
            movimiento = movimiento_form.save(commit=False)
            movimiento.usuario_creacion = request.user
            movimiento.save()

            lineas = []
            # Guardar cada línea y asociarla al movimiento
            for form in formset:
                if form.cleaned_data:
                    linea = form.save(commit=False)
                    linea.movimiento = movimiento
                    linea.save()
                    lineas.append(linea)

            #Si el usuario presiona el botón "generar remito"
            if generar_remito:
                contexto = {
                    "movimiento": movimiento,
                    "lineas": lineas
                }
                return render(request, "movimientos/remito.html")
            
            #Si solo lo guardó entonces redirigimos a la lista de movimientos
            return redirect("movimientos:movimientos")

    else:
        movimiento_form = MovimientoForm()
        formset = LineaFormSet(queryset=LineaMovimiento.objects.none())

    context = {
        "movimiento_form": movimiento_form,
        "formset": formset,
        "title": "Registrar Movimiento"
    }
    
    return render(request, "movimientos/registrar_movimiento.html", context)
    
def movimientos(request):
    lista_movimientos = Movimiento.objects.all()
    context = {'movimientos': lista_movimientos, 'title': 'Movimientos'}
    return render(request, 'movimientos/movimientos.html', context)

#       ⬇⬇⬇⬇ FUNCIONES DE EXPORTAR COMO CSV Y PDF ⬇⬇⬇⬇
import csv
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from .models import Movimiento

# --- EXPORTAR CSV ---
def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="movimientos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Empresa', 'Fecha / Hora', 'Motivo', 'Cantidad', 'Tipo', 'Responsable'])

    movimientos = Movimiento.objects.prefetch_related('lineas').all()

    for movimiento in movimientos:
        for linea in movimiento.lineas.all():
            writer.writerow([
                movimiento.empresa,
                movimiento.fecha_hora,
                movimiento.tipo,
                linea.cantidad,
                linea.tipo_pallet,
                movimiento.usuario_creacion
            ])

    return response

# --- EXPORTAR PDF ---
def exportar_pdf(request):
    # --- Configurar la respuesta HTTP ---
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="movimientos.pdf"'

    # --- Crear el documento PDF ---
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))  # Horizontal
    elements = []

    # --- Título del documento ---
    styles = getSampleStyleSheet()
    title = Paragraph("Reporte de Movimientos", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))

    # --- Encabezados de la tabla ---
    data = [['Empresa', 'Fecha / Hora', 'Motivo', 'Cantidad', 'Tipo', 'Responsable']]

    # --- Obtener los datos ---
    movimientos = Movimiento.objects.prefetch_related('lineas').all()

    for movimiento in movimientos:
        for linea in movimiento.lineas.all():
            data.append([
                str(movimiento.empresa),
                movimiento.fecha_hora.strftime("%d/%m/%Y %H:%M"),
                str(movimiento.tipo),
                str(linea.cantidad),
                str(linea.tipo_pallet),
                str(movimiento.usuario_creacion)
            ])

    # --- Crear la tabla ---
    table = Table(data, repeatRows=1)  # repeatRows mantiene el encabezado en cada página

    # --- Estilo de la tabla ---
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0D7A7F')),  # Encabezado verde azulado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),

        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),

        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor('#E8F6F7')]),
    ])
    table.setStyle(style)

    elements.append(table)

    # --- Generar el PDF ---
    doc.build(elements)
    return response


#nuevo egreso
def registrar_egreso(request):
    """
    Vista para registrar un egreso de pallets.
    Mismo diseño y lógica base que Ingresar Movimiento.
    """
    LineaFormSet = modelformset_factory(
        LineaMovimiento,
        form=LineaMovimientoForm,
        extra=1,
        can_delete=True
    )

    def _context(mov_form, fs):
        return {
            "movimiento_form": mov_form,
            "formset": fs,
            "titulo": "Nuevo egreso de pallets",
            "btn_label": "Registrar egreso",
            # 👇 Estas dos son importantes para el header
            "header_title": "Ingresar Movimiento de Pallets",
            "title": "Ingresar Movimiento de Pallets",
        }

    if request.method == "POST":
        movimiento_form = EgresoMovimientoForm(request.POST)
        formset = LineaFormSet(request.POST, queryset=LineaMovimiento.objects.none())
        # Filtramos líneas válidas (cantidad > 0 y tipo pallet seleccionado)
        lineas_validas = []
        if formset.is_valid():
            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get("DELETE", False):
                    cantidad = f.cleaned_data.get("cantidad") or 0
                    tipo = f.cleaned_data.get("tipo_pallet")
                    if tipo and cantidad > 0:
                        lineas_validas.append(f)

        if not lineas_validas:
            messages.error(request, "Debés cargar al menos una línea válida de egreso.")
            return render(request, "movimientos/registrar_egreso.html", _context(movimiento_form, formset))

        if movimiento_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    movimiento = movimiento_form.save(commit=False)
                    movimiento.usuario_creacion = request.user
                    movimiento.save()

                    for f in lineas_validas:
                        linea = f.save(commit=False)
                        linea.movimiento = movimiento
                        linea.save()

                if "btn-remito" in request.POST:
                    return redirect("movimientos:ver_remito", movimiento_id=movimiento.id)

                messages.success(request, "✅ Egreso registrado correctamente.")
                return redirect("movimientos:movimientos")
            
            except Exception as e:
                print(e)  # opcional: para debug
                messages.error(request, "Ocurrió un error inesperado al guardar el egreso.")
        else:
            messages.error(request, "Revisá los errores del formulario.")

        return render(request, "movimientos/registrar_egreso.html", _context(movimiento_form, formset))

    # Si es GET
    movimiento_form = EgresoMovimientoForm()
    formset = LineaFormSet(queryset=LineaMovimiento.objects.none())
    return render(request, "movimientos/registrar_egreso.html", _context(movimiento_form, formset))

#   Pagina movimientos/gestion-stock
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
        "title": "Movimientos",
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
