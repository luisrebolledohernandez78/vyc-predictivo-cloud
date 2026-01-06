"""
Parser para archivos Excel de Equipos y Activos
Estructura esperada:
- Columna A: Área (Aserradero, Elaborado, Caldera)
- Columna B: Nombre Equipo
- Columna C: Nombre Activo
- Columna D: Observaciones
"""
import openpyxl
from .models import Area, Equipo, Activo


class ExcelEquiposParser:
    def __init__(self, archivo, sucursal):
        self.archivo = archivo
        self.sucursal = sucursal
        self.errores = []
        self.advertencias = []
        self.datos_parseados = []
    
    def parsear(self):
        """Parsea el archivo Excel y retorna estructura jerárquica"""
        try:
            wb = openpyxl.load_workbook(self.archivo)
            ws = wb.active
            
            datos = []
            area_actual = None
            equipo_actual = None
            
            # Saltar encabezados (filas 1-8, datos comienzan en fila 9)
            for row in ws.iter_rows(min_row=9, values_only=True):
                if all(cell is None for cell in row[:4]):
                    continue
                
                area_nombre = row[0]
                equipo_nombre = row[1]
                activo_nombre = row[2]
                observaciones = row[3] if len(row) > 3 else None
                
                # Nueva área detectada
                if area_nombre:
                    area_actual = self._normalizar_area(area_nombre)
                    if not area_actual:
                        self.errores.append(f"Área no válida: {area_nombre}")
                        continue
                    equipo_actual = None  # Reset equipo cuando cambia área
                
                # Nuevo equipo detectado
                if equipo_nombre and area_actual:
                    equipo_actual = equipo_nombre.strip()
                
                # Nuevo activo detectado
                if activo_nombre and equipo_actual and area_actual:
                    datos.append({
                        'area': area_actual,
                        'equipo': equipo_actual,
                        'activo': activo_nombre.strip(),
                        'observaciones': observaciones.strip() if observaciones else None
                    })
            
            self.datos_parseados = datos
            return datos
        
        except Exception as e:
            self.errores.append(f"Error al parsear archivo: {str(e)}")
            return []
    
    def _normalizar_area(self, area_nombre):
        """Normaliza el nombre del área a su valor en choices"""
        if not area_nombre:
            return None
        
        area_lower = str(area_nombre).strip().lower()
        
        mapeo = {
            'aserradero': 'aserradero',
            'elaborado': 'elaborado',
            'caldera': 'caldera',
        }
        
        return mapeo.get(area_lower)
    
    def obtener_preview(self):
        """Retorna un preview de los datos que serán importados con detalle de activos"""
        if not self.datos_parseados:
            return {
                'total_filas': 0,
                'por_area': {},
                'errores': self.errores
            }
        
        preview = {
            'total_filas': len(self.datos_parseados),
            'por_area': {},
            'errores': self.errores,
            'advertencias': self.advertencias
        }
        
        for dato in self.datos_parseados:
            area = dato['area']
            if area not in preview['por_area']:
                preview['por_area'][area] = {
                    'equipos': {},
                    'total_activos': 0
                }
            
            equipo = dato['equipo']
            if equipo not in preview['por_area'][area]['equipos']:
                preview['por_area'][area]['equipos'][equipo] = {
                    'activos': [],
                    'cantidad': 0
                }
            
            # Agregar detalle del activo
            preview['por_area'][area]['equipos'][equipo]['activos'].append({
                'nombre': dato['activo'],
                'observaciones': dato['observaciones']
            })
            preview['por_area'][area]['equipos'][equipo]['cantidad'] += 1
            preview['por_area'][area]['total_activos'] += 1
        
        return preview
    
    def importar(self, accion='merge'):
        """
        Importa los datos a la BD
        
        Acciones:
        - 'reemplazar': Elimina todos los equipos/activos existentes en la sucursal
        - 'merge': Agrega nuevos, mantiene existentes (evita duplicados)
        - 'upsert': Actualiza existentes, agrega nuevos
        """
        if not self.datos_parseados:
            self.errores.append("No hay datos para importar")
            return {'exito': False, 'errores': self.errores}
        
        try:
            resultados = {
                'equipos_creados': 0,
                'equipos_actualizados': 0,
                'activos_creados': 0,
                'activos_actualizados': 0,
                'errores': []
            }
            
            # Si es reemplazar, elimina primero
            if accion == 'reemplazar':
                Equipo.objects.filter(area__sucursal=self.sucursal).delete()
                resultados['nota'] = 'Equipos y activos anteriores eliminados'
            
            # Procesar datos
            for dato in self.datos_parseados:
                try:
                    # Obtener o crear área
                    area = Area.objects.get(
                        sucursal=self.sucursal,
                        nombre=dato['area']
                    )
                    
                    # Obtener o crear equipo
                    if accion == 'upsert':
                        equipo, creado = Equipo.objects.update_or_create(
                            area=area,
                            nombre=dato['equipo'],
                            defaults={'observaciones': dato['observaciones'] or ''}
                        )
                        if creado:
                            resultados['equipos_creados'] += 1
                        else:
                            resultados['equipos_actualizados'] += 1
                    else:  # merge
                        equipo, creado = Equipo.objects.get_or_create(
                            area=area,
                            nombre=dato['equipo'],
                            defaults={'observaciones': dato['observaciones'] or ''}
                        )
                        if creado:
                            resultados['equipos_creados'] += 1
                    
                    # Obtener o crear activo
                    if accion == 'upsert':
                        activo, creado = Activo.objects.update_or_create(
                            equipo=equipo,
                            nombre=dato['activo'],
                            defaults={'observaciones': dato['observaciones'] or ''}
                        )
                        if creado:
                            resultados['activos_creados'] += 1
                        else:
                            resultados['activos_actualizados'] += 1
                    else:  # merge
                        activo, creado = Activo.objects.get_or_create(
                            equipo=equipo,
                            nombre=dato['activo'],
                            defaults={'observaciones': dato['observaciones'] or ''}
                        )
                        if creado:
                            resultados['activos_creados'] += 1
                
                except Area.DoesNotExist:
                    resultados['errores'].append(
                        f"Área '{dato['area']}' no existe en la sucursal"
                    )
                except Exception as e:
                    resultados['errores'].append(
                        f"Error al importar equipo '{dato['equipo']}': {str(e)}"
                    )
            
            resultados['exito'] = True
            return resultados
        
        except Exception as e:
            return {
                'exito': False,
                'errores': [f"Error general en importación: {str(e)}"]
            }
