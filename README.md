# VYC Predictivo Cloud

Repositorio principal del sistema *VYC Predictivo Cloud*.
Este proyecto busca centralizar los datos de análisis de vibraciones y termografías de maquinaria para múltiples empresas atendidas por VyC.

## Objetivo

Plataforma web cloud para gestionar activos, almacenar mediciones de vibraciones y termografías, presentar históricos y análisis técnico.

## Características del Sistema

### 🔐 Autenticación y Seguridad
- Sistema de login con usuario/contraseña
- Gestión de sesiones con Django
- Dashboard protegido solo para usuarios autenticados
- Contraseña de administrador: `VyCingenieria`

### 👥 Gestión de Clientes
- **CRUD completo** para crear, editar, eliminar clientes
- Campos: nombre, email, teléfono, dirección, contacto principal, RUC/NIT, industria
- Disponible en ambos módulos: Vibraciones y Termografías
- Búsqueda y filtrado de clientes activos

### 🏭 Gestión de Sucursales
- Crear múltiples sucursales por cliente
- Información de contacto independiente por sucursal
- Las sucursales se despliegan de forma tabular con acciones de editar/eliminar
- Acceso directo: clic en nombre del cliente → ver sucursales
- Disponible en ambos módulos

### 📍 Gestión de Áreas
- **3 áreas predefinidas** por sucursal: Aserradero, Elaborado, Caldera
- Las áreas se **crean automáticamente** al crear una sucursal
- Edición y eliminación de áreas
- Descripción personalizable por área
- Interfaz tipo tarjetas con colores distintivos por tipo
- Acceso directo: clic en sucursal → ver áreas

### 📊 Módulos Principales

#### Análisis de Vibraciones
- Ruta: `/vibraciones/`
- Monitoreo de vibraciones de maquinaria
- Detección de desgaste, desalineamiento, desequilibrio
- Integrado con IA para predicción de mantenimiento

#### Termografía Infrarroja
- Ruta: `/termografias/`
- Detección de anomalías térmicas
- Identificación de sobrecalentamientos y pérdidas de energía
- Monitoreo continuo para prevención de fallos

### 🛠️ Administración

#### Panel de Control Django
- Acceso en `/admin/` (usuario: admin)
- Gestión de Clientes, Sucursales y Áreas
- Filtros por estado, fecha, ubicación
- Búsqueda avanzada

#### Management Commands
```bash
# Crear áreas faltantes en sucursales antiguas
python manage.py crear_areas_faltantes
```

## Arquitectura Técnica

### Stack Tecnológico
- **Backend**: Django 6.0, Python 3.12
- **Base de Datos**: MySQL 5.7+
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **ORM**: Django ORM

### Configuración Base de Datos
```
Host: 127.0.0.1
Puerto: 3306
Base de datos: vyc_predictivo
Usuario: root
Contraseña: VyCingenieria
```

### Estructura de Datos
```
Cliente
  ├── Sucursal
  │   └── Área (Aserradero, Elaborado, Caldera)
```

### URLs Principales
```
GET  /                              - Página de bienvenida
POST /login/                        - Autenticación
GET  /logout/                       - Cerrar sesión
GET  /dashboard/                    - Dashboard principal

VIBRACIONES:
GET  /vibraciones/                  - Listar clientes
POST /vibraciones/cliente/crear/    - Crear cliente
GET  /vibraciones/cliente/<id>/sucursales/          - Listar sucursales
POST /vibraciones/cliente/<id>/sucursal/crear/      - Crear sucursal
GET  /vibraciones/cliente/<id>/sucursal/<id>/areas/ - Listar áreas

TERMOGRAFÍAS:
GET  /termografias/                 - Listar clientes
POST /termografias/cliente/crear/   - Crear cliente
GET  /termografias/cliente/<id>/sucursales/         - Listar sucursales
POST /termografias/cliente/<id>/sucursal/crear/     - Crear sucursal
GET  /termografias/cliente/<id>/sucursal/<id>/areas/- Listar áreas
```

### Paleta de Colores Institucionales

**INSTRUCCIÓN CLAVE**: Los usuarios deben identificar elementos a simple vista (sin leer) guiándose únicamente por el color.

#### Áreas de Monitoreo

| Área | Color Primario | Descripción | Uso |
|------|---|---|---|
| **Aserradero** | `#27ae60` (Verde) | Área de aserrado - Madera verde 🌳 | Cards, badges, bordes de área |
| **Elaborado** | `#d4af37` (Dorado) | Área de elaboración - Madera procesada 🌲 | Cards, badges, bordes de área |
| **Caldera** | `#e53935` (Rojo) | Área de caldera - Calor/temperatura 🔥 | Cards, badges, bordes de área |

#### Variantes de Color Recomendadas
```css
/* ASERRADERO - Verde */
--area-aserradero-primary: #27ae60;
--area-aserradero-light: #d5f4e6;
--area-aserradero-lighter: #f0fdf4;
--area-aserradero-dark: #1e8449;

/* ELABORADO - Dorado */
--area-elaborado-primary: #d4af37;
--area-elaborado-light: #fef9e7;
--area-elaborado-lighter: #fff8dc;
--area-elaborado-dark: #b8860b;

/* CALDERA - Naranjo */
--area-caldera-primary: #e53935;
--area-caldera-light: #fdebd0;
--area-caldera-lighter: #fff5ee;
--area-caldera-dark: #c62828;
```

#### Colores Corporativos Generales
- **Primario**: `#667eea` (Azul - UI general)
- **Secundario**: `#764ba2` (Púrpura - Acentos)
- **Éxito**: `#27ae60` (Verde - Operaciones exitosas)
- **Error**: `#e74c3c` (Rojo - Errores)
- **Advertencia**: `#f39c12` (Naranja - Advertencias)

### Modelos de Datos
```
Cliente:
  - nombre (único)
  - email (único)
  - telefono, direccion, ciudad, pais
  - contacto_nombre, contacto_puesto, contacto_email, contacto_telefono
  - ruc_nit (único), industria, empleados
  - creado, actualizado, activo

Sucursal:
  - cliente (ForeignKey)
  - nombre
  - email, telefono, direccion, ciudad, pais
  - contacto_nombre, contacto_puesto, contacto_email, contacto_telefono
  - creado, actualizado, activo

Área:
  - sucursal (ForeignKey)
  - nombre (aserradero, elaborado, caldera)
  - descripcion
  - creado, actualizado, activo
```

## Estructura del repositorio

```
vyc-predictivo-cloud/
├── backend/                    # Código Django
│   ├── config/                 # Configuración
│   ├── core/                   # Aplicación principal
│   │   ├── models.py           # Modelos (Cliente, Sucursal, Área)
│   │   ├── views.py            # Vistas (CRUD de todos los módulos)
│   │   ├── forms.py            # Formularios
│   │   ├── urls.py             # Rutas
│   │   ├── admin.py            # Admin de Django
│   │   ├── templates/          # Plantillas HTML
│   │   │   ├── core/welcome.html
│   │   │   ├── core/login.html
│   │   │   ├── core/dashboard_home.html
│   │   │   ├── core/vibraciones.html
│   │   │   ├── core/termografias.html
│   │   │   ├── core/cliente_form.html
│   │   │   ├── core/sucursales.html
│   │   │   ├── core/sucursal_form.html
│   │   │   ├── core/areas.html
│   │   │   └── core/area_form.html
│   │   └── management/commands/
│   │       └── crear_areas_faltantes.py
│   ├── manage.py
│   ├── create_database.py
│   ├── create_superuser.py
│   ├── change_password.py
│   └── .env.example
├── docs/                       # Documentación
│   ├── 01_producto/
│   ├── 02_datos/
│   ├── 03_arquitectura/
│   └── 04_ui-ux/
└── README.md
```

## Guía Rápida de Inicio

### Requisitos
- Python 3.12+
- MySQL 5.7+
- pip

### Instalación
```bash
# Clonar repositorio
git clone <repo_url>
cd vyc-predictivo-cloud

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos
cd backend
python create_database.py

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario (admin)
python create_superuser.py

# Crear áreas en sucursales antiguas (si es necesario)
python manage.py crear_areas_faltantes

# Levantar servidor
python manage.py runserver
```

## Cambios Recientes (Enero 2026)

### UI/UX Refinement & Sidebar Unification
- **Sidebar centralizada**: Creada única template `sidebar.html` incluida en todos los templates
- **Estilos consolidados**: CSS de sidebar con estilos inline en la propia template para funcionar en desarrollo
- **Características centradas**: Texto e iconos alineados al centro en welcome.html
- **Consistencia visual**: Botón "Salir" y navegación uniforme en todos los módulos

### Instrucciones para la IA

1. **No comitear sin confirmación**: SIEMPRE pedir confirmación antes de realizar cualquier commit a la rama.

2. **Mantener estructura de carpetas**: Los nuevos archivos deben colocarse en su respectiva carpeta según su tipo (documentación, scripts, tests, etc). Respetar la jerarquía y organización existente. El directorio raíz debe mantenerse limpio:
   - Código backend → `/backend/`
   - Documentación → `/docs/` (01_producto, 02_datos, 03_arquitectura, 04_ui-ux)
   - README y archivos de configuración en raíz

3. **Mantener lógica de programación**: Seguir los patrones arquitectónicos y de código ya establecidos en el proyecto. Garantizar consistencia en toda la base de código.

4. **Mantener diseño visual consistente**: Respetar la apariencia y layout del proyecto, incluyendo la paleta de colores e identidad visual institucional.

## Autores y Responsables

- **Inicio**: Enero 2026
- **Última actualización**: Enero 5, 2026
