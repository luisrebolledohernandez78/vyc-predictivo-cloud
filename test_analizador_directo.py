"""
Test directo del analizador térmico sin Django
"""
import sys
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

# Importar el analizador
from core.analisis_termico import AnalizadorTermico

def test_analizador():
    print("🧪 Test del Analizador Térmico")
    print("=" * 50)
    
    # Crear analizador
    analizador = AnalizadorTermico()
    
    # Probar con imagen de prueba
    imagen_path = 'imagen_termica_prueba.jpg'
    
    print(f"\n📁 Analizando: {imagen_path}")
    resultado = analizador.analizar_imagen(imagen_path)
    
    if 'error' in resultado:
        print(f"❌ Error: {resultado['error']}")
        return False
    
    print("\n✅ Análisis completado exitosamente!")
    print("\n📊 Resultados:")
    print(f"   Estado: {resultado['estado'].upper()}")
    print(f"   Mensaje: {resultado['mensaje']}")
    print(f"\n   🌡️ Temperaturas:")
    print(f"      Promedio:  {resultado['temperatura_promedio']}°C")
    print(f"      Máxima:    {resultado['temperatura_maxima']}°C")
    print(f"      Mínima:    {resultado['temperatura_minima']}°C")
    print(f"\n   📈 Zonas detectadas:")
    print(f"      Zona Crítica: {resultado['porcentaje_zona_critica']}%")
    print(f"      Zona Alerta:  {resultado['porcentaje_zona_alerta']}%")
    print(f"      Zona Caliente (combinada): {resultado['porcentaje_zona_caliente']}%")
    
    return True

if __name__ == '__main__':
    try:
        success = test_analizador()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
