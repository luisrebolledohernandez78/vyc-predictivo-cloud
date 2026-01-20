# 📖 GUÍA DE USO - SISTEMA DE HISTÓRICO

## Para el Usuario Final

### ¿Cómo acceder al Histórico de Vibraciones?

#### Paso 1: Ingresa al módulo de Vibraciones
```
Dashboard → Click en "Análisis de Vibraciones"
```

#### Paso 2: Selecciona el Cliente
```
Página de Clientes → Click en el cliente deseado
Ej: "Forestal Santa Blanca"
```

#### Paso 3: Selecciona la Sucursal
```
Página de Sucursales → Click en la sucursal
Ej: "Planta Longavís"
```

#### Paso 4: Visualiza Áreas
```
Página de Áreas → Verás: Aserradero, Elaborado, Caldera
Click en "Ver Equipos Totales" (arriba)
```

#### Paso 5: Accede al Histórico
```
Página de Equipos Totales → 
Click en botón AZUL "📊 Ver Histórico"
```

#### Paso 6: Visualiza la Tabla
```
¡Eres! Ahora ves:
┌────┬─────────────┬──────────────┬────────────┬─────────────┐
│ #  │ Área        │ Equipo       │ Activo     │ Fechas...   │
├────┼─────────────┼──────────────┼────────────┼─────────────┤
│ 1  │ Aserradero  │ Motor 1      │ Rotor      │ NORMAL|ALERTA│
│ 2  │ Aserradero  │ Motor 1      │ Volante    │ ...         │
└────┴─────────────┴──────────────┴────────────┴─────────────┘
```

---

### ¿Cómo acceder al Histórico de Termografías?

#### Paso 1: Ingresa al módulo de Termografías
```
Dashboard → Click en "Termografía Infrarroja"
```

#### Paso 2: Selecciona el Cliente
```
Página de Clientes → Click en el cliente
```

#### Paso 3: Selecciona la Sucursal
```
Página de Sucursales → Click en la sucursal
```

#### Paso 4: Visualiza Áreas
```
Página de Áreas → Click en "Ver Activos Totales"
```

#### Paso 5: Accede al Histórico
```
Página de Activos Totales → 
Click en botón ROJO "🌡️  Ver Histórico"
```

#### Paso 6: Visualiza la Tabla
```
Ves la tabla con temperaturas máximas en lugar de RMS
```

---

## Cómo Interpretar la Tabla

### Estados de Salud

```
🟢 NORMAL   - Todo está bien, equipo operando correctamente
🟡 ALERTA   - Se requiere inspección en breve (próxima semana)
🔴 CRITICO  - ⚠️ Intervención urgente (hoy o mañana)
⚪ —         - Sin datos registrados en esa fecha
```

### Valores Mostrados

**Vibraciones (Análisis de Vibraciones):**
```
┌─────────┐
│ NORMAL  │  ← Estado
│ 2.3 mm/s│  ← Velocidad RMS (al pasar mouse vés más datos)
└─────────┘
```

**Termografías (Análisis de Temperaturas):**
```
┌─────────┐
│ ALERTA  │  ← Estado
│ 92.3°C  │  ← Temperatura Máxima
└─────────┘
```

### Tooltip (Información al Pasar el Mouse)

**Vibraciones:**
```
Al pasar mouse sobre una celda:
"RMS: 2.3 mm/s | Aceleración: 0.8 g"
```

**Termografías:**
```
Al pasar mouse sobre una celda:
"T°Max: 92.3°C | T°Min: 65.1°C"
```

---

## Cómo Analizar Tendencias

### Ejemplo 1: Tendencia Normal
```
Rotor del Motor 1:
15/12 → NORMAL (2.1) → 20/12 → NORMAL (2.3) → 25/12 → NORMAL (2.0)

Análisis: ✅ Equipo estable, sin cambios significativos
Acción: Continuar con mantenimiento normal
```

### Ejemplo 2: Tendencia Creciente (⚠️ ALERTA)
```
Volante del Motor 1:
15/12 → NORMAL (1.9) → 20/12 → ALERTA (3.5) → 25/12 → ALERTA (4.2)

Análisis: ⬆️ Los valores están aumentando
Acción: Inspeccionar urgentemente, posible desgaste
```

### Ejemplo 3: Cambio Repentino (🔴 CRÍTICO)
```
Cabezal del Quemador:
15/12 → ALERTA (92.1) → 20/12 → ALERTA (105.3) → 25/12 → CRITICO (118.7)

Análisis: Escalada rápida, fallo inminente
Acción: PARADA INMEDIATA - Mantenimiento crítico
```

---

## Decisiones Según Estados

### Si ves NORMAL
```
✅ No hay acción urgente
✅ Continúa con mantenimiento preventivo regular
✅ Monitorea en la próxima fecha de muestreo
```

### Si ves ALERTA
```
⚠️  Inspecciona en los próximos 3-5 días
⚠️  Verifica con técnico especializado
⚠️  Aumenta frecuencia de muestreo
⚠️  Prepara repuestos para reparación
```

### Si ves CRITICO
```
🔴 DETÉN la máquina inmediatamente
🔴 Llama al técnico urgentemente
🔴 Prepara equipo de repuesto
🔴 Evalúa si es reparable o necesita reemplazo
```

---

## Casos de Uso Reales

### Caso 1: Planificar Mantenimiento
```
Usuario: Gerente de Planta
Necesidad: "¿Cuándo debo hacer mantenimiento?"

Solución:
1. Abre Histórico de Vibraciones
2. Busca activos con tendencia ALERTA creciente
3. Identifica que Motor 2 está en 3.5 mm/s (ALERTA)
4. Programa mantenimiento para la próxima semana
5. Avisa a equipo de logística para tener repuestos
```

### Caso 2: Investigar Falla Repentina
```
Usuario: Técnico de Mantenimiento
Necesidad: "¿Por qué el Motor 1 falló?"

Solución:
1. Abre Histórico de Termografías
2. Ve que Cabezal pasó de NORMAL (85°C) a CRITICO (120°C)
3. Observa que cambio ocurrió en solo 5 días
4. Deduce: acumulación de depósitos o sello defectuoso
5. Planifica limpieza y reemplazo de sello
```

### Caso 3: Comparar Equipos
```
Usuario: Ingeniero de Procesos
Necesidad: "¿Cuál motor está en mejor condición?"

Solución:
1. Abre Histórico de Vibraciones
2. Compara Motor 1 vs Motor 2:
   - Motor 1: NORMAL → ALERTA → CRITICO (tendencia mala)
   - Motor 2: NORMAL → NORMAL → NORMAL (tendencia buena)
3. Decide reemplazar Motor 1 primero
4. Mantiene Motor 2 en operación normal
```

---

## Preguntas Frecuentes (FAQ)

### P: ¿Por qué no veo datos de ayer?
**R:** El histórico se actualiza cuando se registran nuevos análisis. 
Si no hay datos, es que no se ha realizado un análisis para esa fecha.

### P: ¿Puedo ver datos de años anteriores?
**R:** Sí, la tabla muestra todas las fechas de análisis registradas.
(En el futuro, agregaremos filtros de rango de fechas)

### P: ¿Qué significa el signo "—"?
**R:** Significa que no hay análisis para ese activo en esa fecha.
Es normal si aún no se ha realizado el muestreo.

### P: ¿Cómo agrego más activos al histórico?
**R:** Primero crea el activo en el módulo correspondiente (Equipos/Activos),
luego realiza un análisis (sube foto térmica o mida vibraciones),
y aparecerá automáticamente en el histórico.

### P: ¿Puedo exportar la tabla?
**R:** Por ahora solo puedes captura de pantalla (Print Screen).
En la próxima versión agregaremos botón de exportar PDF/CSV.

### P: ¿Hay límite de fechas en el histórico?
**R:** No, puedes tener ilimitadas fechas. El sistema es escalable.
(Recomendamos mantener últimos 2 años en BD y archivar el resto)

---

## Navegar de Vuelta

### Para volver a Equipos Totales (desde Histórico)
```
Click en botón "⬅ Volver"
```

### Para volver a Áreas (desde Equipos Totales)
```
Click en botón "⬅ Volver"
```

### Para volver a Sucursal (desde Áreas)
```
Click en botón "⬅ Volver" o en el breadcrumb
```

---

## Tips y Trucos

### Tip 1: Analizar Patrones
```
✨ Mira el histórico cada semana para detectar patrones
✨ Los aumentos graduales son más predecibles que cambios repentinos
✨ Documenta cambios en operación que coincidan con cambios en datos
```

### Tip 2: Comparar Entre Sucursales
```
✨ Compara el mismo modelo de motor en diferentes sucursales
✨ Si uno está en NORMAL y otro en CRÍTICO, investiga la diferencia
✨ Pueden ser diferencias en carga, temperatura ambiente, mantenimiento
```

### Tip 3: Establecer Umbrales
```
✨ Define alertas personalizadas basadas en tu experiencia:
   - Para tu tipo de motor: ¿a qué RMS consideras ALERTA?
   - Para tu caldera: ¿a qué temperatura consideras CRÍTICO?
✨ El sistema aprenderá automáticamente (futuro)
```

### Tip 4: Documentar Cambios
```
✨ Cuando ves un cambio anormal, documenta:
   - Qué cambió exactamente
   - Cuándo ocurrió
   - Qué se hizo para solucionarlo
✨ Esto te ayudará a identificar patrones en el futuro
```

---

## Contacto y Soporte

- **Sistema:** VYC Predictivo Cloud v1.0
- **Módulo:** Sistema de Histórico de Análisis
- **Versión:** 1.0
- **Soporte:** contact@vycpredictivo.com

---

**Última actualización:** 20 de Enero de 2026
**Documentado por:** Equipo de Desarrollo VYC
