# Colores Institucionales - VYC Predictivo Cloud

## Paleta de Colores Corporativa

Este documento establece los colores institucionales del sistema VYC Predictivo Cloud. **Estos colores deben usarse consistentemente en toda la aplicación** para mantener una identidad visual clara y permitir a los usuarios identificar elementos a simple vista sin necesidad de leer etiquetas.

### Áreas de Monitoreo - Códigos por Color

| Área | Color Primario | Color Claro | Color Oscuro | Descripción | Símbolo |
|------|---|---|---|---|---|
| **Aserradero** | `#27ae60` | `#d5f4e6` / `#f0fdf4` | `#1e8449` | Verde suave para el área de aserradero (árbol/madera verde) | 🌳 |
| **Elaborado** | `#d4af37` | `#fef9e7` / `#fff8dc` | `#b8860b` | Dorado para el área de elaboración (madera procesada) | 🌲 |
| **Caldera** | `#e53935` | `#ffebee` / `#ffcdd2` | `#c62828` | Rojo para el área de caldera (calor/temperatura) | 🔥 |

## Uso en Interfaces

### Tarjetas/Cards de Áreas

```html
<!-- Aserradero -->
<div class="area-card aserradero">
    <!-- Fondo: #f0fdf4 - #dbeafe (gradiente suave) -->
    <!-- Borde izquierdo: #27ae60 -->
</div>

<!-- Elaborado -->
<div class="area-card elaborado">
    <!-- Fondo: #fef9e7 - #fff8dc (gradiente suave) -->
    <!-- Borde izquierdo: #d4af37 -->
</div>

<!-- Caldera -->
<div class="area-card caldera">
    <!-- Fondo: #fff5ee - #ffe4c4 (gradiente suave) -->
    <!-- Borde izquierdo: #e53935 -->
</div>
```

### Badges/Etiquetas

```html
<!-- Aserradero -->
<span class="badge bg-success">Aserradero</span>
<!-- O con estilo personalizado: background-color: #27ae60 -->

<!-- Elaborado -->
<span class="badge" style="background-color: #d4af37; color: #333;">Elaborado</span>

<!-- Caldera -->
<span class="badge bg-warning text-dark">Caldera</span>
```

### Preview de Importación

En el accordion y resumen de datos durante carga de Excel:

```html
<!-- Aserradero -->
<span class="badge bg-success">Aserradero</span>

<!-- Elaborado -->
<span class="badge" style="background-color: #d4af37; color: #333;">Elaborado</span>

<!-- Caldera -->
<span class="badge bg-warning text-dark">Caldera</span>
```

## Principios de Diseño

### 1. **Diferenciación Visual por Color**
   - Los usuarios deben poder identificar un área únicamente por su color, sin leer el nombre
   - Aplicar colores de forma consistente: siempre verde para Aserradero, dorado para Elaborado, naranjo para Caldera

### 2. **Jerarquía Visual**
   - Color primario: Borde izquierdo de cards, badges principales
   - Color claro: Fondo de cards y backgrounds de elementos secundarios
   - Color oscuro: Texto sobre fondos claros, acentos

### 3. **Accesibilidad**
   - Mantener suficiente contraste entre texto y fondo
   - Usar tanto color como iconos/símbolos para no depender únicamente del color
   - Para Elaborado (dorado), usar texto oscuro (#333) para garantizar legibilidad

## Aplicaciones en el Proyecto

### ✅ Implementado
- Cards de áreas en `areas.html`
- Badges en preview de importación `upload_equipos_preview.html`
- Resumen de datos por área en vista previa

### 📋 Por Implementar
- [ ] Botones de acción por área (Ver Equipos, Editar, etc.)
- [ ] Estados/indicadores en tabla de equipos
- [ ] Gráficos y visualizaciones de datos
- [ ] Indicadores en dashboard
- [ ] Reportes y exportaciones

## Variables CSS Recomendadas

```css
:root {
    --area-aserradero-primary: #27ae60;
    --area-aserradero-light: #d5f4e6;
    --area-aserradero-lighter: #f0fdf4;
    --area-aserradero-dark: #1e8449;
    
    --area-elaborado-primary: #d4af37;
    --area-elaborado-light: #fef9e7;
    --area-elaborado-lighter: #fff8dc;
    --area-elaborado-dark: #b8860b;
    
    --area-caldera-primary: #e53935;
    --area-caldera-light: #fdebd0;
    --area-caldera-lighter: #fff5ee;
    --area-caldera-dark: #c62828;
}
```

## Historiales de Cambios

- **2026-01-06**: Establecimiento inicial de paleta de colores institucionales
  - Definición de 3 colores para las áreas (Aserradero, Elaborado, Caldera)
  - Implementación en areas.html y upload_equipos_preview.html
  - Creación de esta documentación

