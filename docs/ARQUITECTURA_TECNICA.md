# 🏗️ ARQUITECTURA TÉCNICA - SISTEMA DE HISTÓRICO

## Diagrama de Relaciones

```
FLUJO DE DATOS:

┌─────────────────────────────────────────────────────────────────┐
│                       USUARIO                                   │
│  (Navega: Cliente → Sucursal → Áreas → Activos Totales)       │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ├─► Click "Ver Histórico" (Vibraciones)
                     │
                     ▼
        ┌────────────────────────────────┐
        │ historico_vibraciones()        │
        │ (views.py)                     │
        └────────────┬───────────────────┘
                     │
         ┌───────────┴───────────┬────────────────┐
         │                       │                │
         ▼                       ▼                ▼
    Obtiene:              Obtiene:          Construye:
    - Activos             - Fechas únicas   - Matriz
    - de sucursal         - de análisis     - Activo → Fecha
                                            - → Análisis

         │                       │                │
         └───────────────────────┴────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────────┐
        │ BASE DE DATOS                          │
        │ ┌─────────────────────────────────┐   │
        │ │ VibracionesAnalisis             │   │
        │ ├─────────────────────────────────┤   │
        │ │ • activo_id                     │   │
        │ │ • fecha_muestreo                │   │
        │ │ • velocidad_rms                 │   │
        │ │ • aceleración                   │   │
        │ │ • resultado (NORMAL/ALERTA/CRI)│   │
        │ │ • creado                        │   │
        │ └─────────────────────────────────┘   │
        │                                        │
        │ ┌─────────────────────────────────┐   │
        │ │ TermografiaAnalisis             │   │
        │ ├─────────────────────────────────┤   │
        │ │ • activo_id                     │   │
        │ │ • fecha_muestreo                │   │
        │ │ • temperatura_maxima            │   │
        │ │ • temperatura_minima            │   │
        │ │ • resultado (NORMAL/ALERTA/CRI)│   │
        │ │ • creado                        │   │
        │ └─────────────────────────────────┘   │
        │                                        │
        │ ┌─────────────────────────────────┐   │
        │ │ Activo                          │   │
        │ ├─────────────────────────────────┤   │
        │ │ • nombre                        │   │
        │ │ • equipo_id                     │   │
        │ │ • estado                        │   │
        │ └─────────────────────────────────┘   │
        └────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │ Contexto Template                  │
        │ {                                  │
        │   datos_historico: [              │
        │     {                              │
        │       activo: {...},              │
        │       area: {...},                │
        │       equipo: {...},              │
        │       analisis_por_fecha: {       │
        │         fecha1: AnalisisObj,      │
        │         fecha2: AnalisisObj,      │
        │         fecha3: None,             │
        │       }                           │
        │     }                             │
        │   ],                              │
        │   fechas: [fecha1, fecha2, ...]   │
        │ }                                  │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │ Template HTML                      │
        │ vibraciones/historico.html         │
        │ o                                  │
        │ termografias/historico.html        │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │ TABLA HISTÓRICA (Al Navegador)     │
        │ ┌────────────────────────────────┐ │
        │ │ # │ Área │ Equipo │ Activo │... │ │
        │ ├────────────────────────────────┤ │
        │ │ 1 │ Aserr│ Motor1 │ Rotor  │...│ │
        │ │ 2 │ Aserr│ Motor1 │ Volante│...│ │
        │ └────────────────────────────────┘ │
        └────────────┬───────────────────────┘
                     │
                     ▼
              ┌─────────────┐
              │   USUARIO   │
              │ (Ve tabla)  │
              └─────────────┘
```

---

## Estructura de Modelos

```python
# DATOS BASE (Compartidos - No cambian)
Cliente
  ├── Sucursal
  │   ├── Area
  │   │   └── Equipo
  │   │       └── Activo (El equipamiento)
  │   │           ├── foto_termica
  │   │           └── estado (Sin Medición, Bueno, etc.)
  │   │
  │   └── ... más áreas


# ANÁLISIS HISTÓRICOS (Independientes - Se acumulan)
Activo (ForeignKey)
├── TermografiaAnalisis (1:N)
│   ├── fecha_muestreo
│   ├── temperatura_maxima
│   ├── resultado (NORMAL, ALERTA, CRITICO)
│   └── ... + 15 campos más
│
└── VibracionesAnalisis (1:N)
    ├── fecha_muestreo
    ├── velocidad_rms
    ├── resultado (NORMAL, ALERTA, CRITICO)
    └── ... + 10 campos más
```

---

## Flujo de Consulta SQL

### Para obtener histórico de vibraciones:

```sql
-- 1. Obtener todos los activos de la sucursal
SELECT * FROM core_activo
  WHERE equipo_id IN (
    SELECT id FROM core_equipo
      WHERE area_id IN (
        SELECT id FROM core_area
          WHERE sucursal_id = ?
      )
  )
  AND activo = TRUE;

-- 2. Obtener todas las fechas únicas
SELECT DISTINCT fecha_muestreo FROM core_vibracionesanalisis
  WHERE activo_id IN (...)
  ORDER BY fecha_muestreo DESC;

-- 3. Para cada activo y cada fecha, obtener el análisis
SELECT * FROM core_vibracionesanalisis
  WHERE activo_id = ? AND fecha_muestreo = ?;
```

### Complejidad:
- **Activos:** O(n) donde n = activos en sucursal (~73 en Longavís)
- **Fechas:** O(m) donde m = fechas únicas (~30 si es mensual)
- **Análisis:** O(n×m) = 73 × 30 = 2,190 queries (optimizado con diccionario Python)

---

## Archivos Modificados / Creados

### ✅ Creados
```
1. backend/core/migrations/0020_termografiaanalisis_vibracionesanalisis.py
   - Define los nuevos modelos en BD

2. backend/core/templates/core/vibraciones/historico.html
   - Template para histórico de vibraciones

3. backend/core/templates/core/termografias/historico.html
   - Template para histórico de termografías

4. IMPLEMENTACION_HISTORICO.md (este documento)
5. EJEMPLO_HISTORICO.md (ejemplo de tabla)
```

### ✏️ Modificados
```
1. backend/core/models.py
   - Agregados TermografiaAnalisis
   - Agregados VibracionesAnalisis

2. backend/core/views.py
   - Agregado import de nuevos modelos
   - Agregada historico_vibraciones()
   - Agregada historico_termografias()

3. backend/core/urls.py
   - Agregadas rutas para histórico vibraciones
   - Agregadas rutas para histórico termografías

4. backend/core/templates/core/equipos_totales.html
   - Agregado botón "Ver Histórico"

5. backend/core/templates/core/activos_totales.html
   - Agregado botón "Ver Histórico"
```

---

## Índices de BD

Los modelos incluyen índices para optimizar consultas:

```python
class Meta:
    indexes = [
        models.Index(fields=['-fecha_muestreo']),
        models.Index(fields=['activo', '-fecha_muestreo']),
    ]
```

**Beneficio:** Las consultas por activo + fecha son rápidas

---

## Seguridad

### Validaciones incluidas:
✅ `@login_required` - Solo usuarios autenticados
✅ `get_object_or_404` - Verifica que cliente/sucursal pertenezcan al mismo árbol
✅ Filtrado `activo=True` - Solo muestra activos no eliminados
✅ Separación por módulo - Templates nunca se mezclan

---

## Escalabilidad

### Estimaciones de rendimiento:

```
Sucursal con 73 activos
- Histórico con 30 fechas únicas
- Tabla con 2,190 celdas

Tiempo de carga estimado:
- Consultas BD:        ~50ms (con índices)
- Procesamiento Python: ~10ms
- Renderizado Template: ~20ms
- Transferencia HTTP:   ~30ms
─────────────────────────────
Total estimado:         ~110ms (acceptable)
```

### Optimizaciones futuras:
1. Caché de histórico (Redis)
2. Pagination (50 activos/página)
3. Lazy loading de análisis
4. GraphQL en lugar de REST

---

## Consideraciones de Base de Datos

### Tamaño de datos esperado (por año):

```
Análisis por activo por año:
- 73 activos
- 365 análisis/año (1 por día)
─────────────────────────────
Total registros/año: 26,645

Termografías:
- Tamaño imagen: ~2MB
- 26,645 × 2MB = ~53GB/año

Vibraciones:
- Solo datos (sin imagen)
- 26,645 × 0.5KB = ~13MB/año
```

### Recomendaciones:
- Archivar datos de >2 años
- Comprimir imágenes térmicas
- Usar CDN para servir imágenes

---

## Testing

### Casos de prueba recomendados:

```python
def test_historico_vibraciones_sin_datos():
    # Cuando no hay análisis registrados
    # Debe mostrar mensaje "Sin registros"
    pass

def test_historico_con_activos_sin_analisis():
    # Cuando hay activos pero sin análisis
    # Debe mostrar filas vacías (—)
    pass

def test_historico_con_multiples_fechas():
    # Con 30+ fechas de análisis
    # Debe mostrar tabla completa sin truncar
    pass

def test_permisos_usuario():
    # Usuario de cliente A no ve datos de cliente B
    pass

def test_modulos_separados():
    # Vibraciones nunca muestra datos de termografías
    # Termografías nunca muestra datos de vibraciones
    pass
```

---

## Roadmap Futuro

### Fase 2 (Próximo sprint):
- [ ] Exportar histórico a PDF/CSV
- [ ] Gráficos de tendencias (Chart.js)
- [ ] Filtros por rango de fechas
- [ ] Comparativa entre activos

### Fase 3:
- [ ] Machine Learning para predicción de fallas
- [ ] Alertas automáticas por tendencias
- [ ] Reportes automáticos por correo
- [ ] Dashboard ejecutivo con KPIs

---

**Arquitectura completa implementada**: ✅
**Listo para conectar datos reales**: ✅
**Documentación técnica**: ✅
