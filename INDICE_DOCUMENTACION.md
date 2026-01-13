# 📚 Índice de Documentación - Sistemas de Ecuaciones Diferenciales

## 🎯 Rápido y Directo

**¿Quieres empezar YA?** → Lee [GUIA_PRUEBA.md](GUIA_PRUEBA.md)

**¿Quieres entender qué cambió?** → Lee [RESUMEN_VISUAL.md](RESUMEN_VISUAL.md)

**¿Quieres detalles técnicos?** → Lee [MAPA_CAMBIOS.md](MAPA_CAMBIOS.md)

---

## 📖 Documentación Completa

### Nivel 1: Introducción (Para cualquiera)

| Documento | Propósito | Duración |
|-----------|-----------|----------|
| **[RESUMEN_VISUAL.md](RESUMEN_VISUAL.md)** | Ver diagramas de cómo funciona | 5 min |
| **[GUIA_PRUEBA.md](GUIA_PRUEBA.md)** | Instrucciones paso a paso | 10 min |
| **[RESUMEN_IMPLEMENTACION.md](RESUMEN_IMPLEMENTACION.md)** | Descripción ejecutiva | 10 min |

### Nivel 2: Implementación (Para desarrolladores)

| Documento | Propósito | Duración |
|-----------|-----------|----------|
| **[MAPA_CAMBIOS.md](MAPA_CAMBIOS.md)** | Dónde está exactamente cada línea | 15 min |
| **[CAMBIOS_SISTEMAS_ODE.md](CAMBIOS_SISTEMAS_ODE.md)** | API y características nuevas | 20 min |
| Código directo | Ver el código real | Variable |

### Nivel 3: Pruebas (Para QA/Testing)

| Script | Propósito | Cómo ejecutar |
|--------|-----------|---------------|
| `test_sistema_odes.py` | Tests locales Python | `python test_sistema_odes.py` |
| `test_api.py` | Tests del endpoint | `python test_api.py` |
| `test_api_final.py` | Suite completa | `python test_api_final.py` |

---

## 🚀 Inicio Rápido (3 pasos)

### 1️⃣ Iniciar servidor
```bash
cd Proyecto_metodos_py
python app.py
```
Verás: `Running on http://127.0.0.1:5000`

### 2️⃣ Abrir navegador
```
http://127.0.0.1:5000
→ Menú → Ecuaciones Diferenciales
```

### 3️⃣ Probar sistema (ejemplo oscilador armónico)
```
Función 1: y2
Función 2: -y1
y1(0) = 1
y2(0) = 0
Calcular →
```

---

## 📋 ¿Qué Cambió?

### Antes
- ❌ Solo una ecuación: dy/dx = f(x,y)
- ❌ Un campo de entrada para función
- ❌ Salida: tabla con x, y

### Ahora
- ✅ Múltiples ecuaciones simultáneamente
- ✅ Campos dinámicos (agregar/quitar con botones)
- ✅ Salida: tabla con x, y1, y2, y3, ...
- ✅ **Completamente compatible hacia atrás**

---

## 🔧 Casos de Uso

### Ejemplo 1: Oscilador Armónico (Clásico)
```
dy₁/dx = y₂
dy₂/dx = -y₁

Condiciones iniciales: y₁(0)=1, y₂(0)=0
Solución: Oscilación periódica
```

### Ejemplo 2: Predador-Presa (Lotka-Volterra)
```
dP/dt = P - 0.1*P*Q     (presas)
dQ/dt = 0.075*P*Q - 1.5*Q  (depredadores)

Condiciones iniciales: P(0)=50, Q(0)=5
Solución: Ciclos de población predecibles
```

### Ejemplo 3: Reacciones Químicas
```
dA/dt = -y1 + y2
dB/dt = y1 - y2 - 2*y2
dC/dt = 2*y2

Condiciones iniciales: [1, 0, 0]
Solución: Evolución de concentraciones
```

---

## 🏗️ Arquitectura

```
┌─────────────────┐
│  HTML/CSS/JS    │  Interfaz web mejorada
│  (Dinámico)     │  Campos +/- para funciones
└────────┬────────┘
         ↓
┌─────────────────┐
│   API (Flask)   │  Detecta tipo automáticamente
│   app.py        │  Sistema vs Ecuación única
└────────┬────────┘
         ↓
┌─────────────────┐
│  Métodos Python │  euler_sistema()
│  metodos.py     │  runge_kutta_4_sistema()
└─────────────────┘
```

---

## 📊 Estructura de Datos

### Sistema 2x2
```python
# Input
{
  "y0": [1, 0],
  "functions": ["y2", "-y1"]
}

# Output
{
  "y_valores": [
    [1.0, 0.995, 0.98, ...],  # y1
    [0.0, -0.1, -0.198, ...]  # y2
  ]
}
```

### Ecuación Única (Original)
```python
# Input
{
  "y0": 1,
  "f_expr": "x + y"
}

# Output
{
  "y_valores": [[1.0, 1.105, 1.225, ...]]
}
```

---

## ✅ Verificación

Todos los tests pasan:
- ✅ `test_sistema_odes.py` - Métodos Python
- ✅ `test_api.py` - Endpoints API
- ✅ Compatibilidad hacia atrás - Verificada
- ✅ Tabla de resultados - Múltiples variables
- ✅ Validación de entrada - Funciones correctas

---

## 🐛 Solución de Problemas

| Problema | Solución |
|----------|----------|
| Funciones no se agregan | Recargar página (F5) |
| "Mismatch funciones/y0" | Asegurar cantidad igual de ambas |
| Error 400 en API | Ver consola navegador (F12) |
| Tabla vacía | Verificar que método es válido |
| Respuesta lenta | Reducir número de pasos (n) |

---

## 📁 Estructura de Archivos

```
Proyecto_metodos_py/
├── app.py                          # API principal (modificado)
├── metodos/
│   └── metodos.py                  # Métodos (+ 150 líneas nuevas)
├── templates/
│   └── ecuaciones_diferenciales.html # UI (+ 200 líneas nuevas)
├── static/
│   └── style.css                   # Estilos (sin cambios)
│
├── 📚 DOCUMENTACIÓN NUEVA:
├── RESUMEN_VISUAL.md               # Diagramas y flujos
├── MAPA_CAMBIOS.md                 # Ubicación exacta de cambios
├── CAMBIOS_SISTEMAS_ODE.md         # Detalles técnicos
├── RESUMEN_IMPLEMENTACION.md       # Resumen ejecutivo
├── GUIA_PRUEBA.md                  # Paso a paso
│
├── 🧪 PRUEBAS:
├── test_sistema_odes.py            # Tests Python
├── test_api.py                     # Tests API básicos
├── test_api_final.py               # Suite completa
└── run_production.py               # Ejecutor sin debug
```

---

## 🔗 Referencias Cruzadas

| Tema | Dónde Aprender |
|------|---|
| Cómo empezar | [GUIA_PRUEBA.md](GUIA_PRUEBA.md) |
| Arquitectura | [RESUMEN_VISUAL.md](RESUMEN_VISUAL.md) |
| Cambios exactos | [MAPA_CAMBIOS.md](MAPA_CAMBIOS.md) |
| API endpoints | [CAMBIOS_SISTEMAS_ODE.md](CAMBIOS_SISTEMAS_ODE.md) |
| Ejemplos | [GUIA_PRUEBA.md](GUIA_PRUEBA.md) (sección Ejemplos Adicionales) |

---

## ❓ FAQ

### ¿Es compatible con el código anterior?
**Sí**, 100% compatible. Ecuaciones únicas funcionan igual que antes.

### ¿Cuántas variables puedo usar?
**Ilimitadas** (en la práctica: 10-20+), limitado solo por rendimiento.

### ¿Qué métodos soportan sistemas?
- ✅ Euler
- ✅ Runge-Kutta 4
- ⏳ Otros métodos (Taylor, Adams, etc.) = planeado

### ¿Necesito cambiar algo en producción?
**No**, simplemente reemplaza los archivos y funciona igual.

### ¿Hay límite de funciones?
**Técnico:** No hay límite real.
**Práctico:** ~20 variables es razonable.
**Recomendado:** 2-5 variables para mejor visualización.

---

## 🎓 Recursos de Aprendizaje

**Sobre Sistemas de ODEs:**
- Ver diagramas en [RESUMEN_VISUAL.md](RESUMEN_VISUAL.md)
- Leer ejemplos en [GUIA_PRUEBA.md](GUIA_PRUEBA.md)
- Estudiar código en `metodos/metodos.py` líneas ~1728+

**Sobre la Implementación:**
- Flujo completo: [RESUMEN_VISUAL.md](RESUMEN_VISUAL.md)
- Cambios exactos: [MAPA_CAMBIOS.md](MAPA_CAMBIOS.md)
- Detalles técnicos: [CAMBIOS_SISTEMAS_ODE.md](CAMBIOS_SISTEMAS_ODE.md)

---

## 📞 Contacto / Soporte

Para preguntas sobre:
- **Uso web:** Ver [GUIA_PRUEBA.md](GUIA_PRUEBA.md)
- **Código:** Ver [MAPA_CAMBIOS.md](MAPA_CAMBIOS.md)
- **API:** Ver [CAMBIOS_SISTEMAS_ODE.md](CAMBIOS_SISTEMAS_ODE.md)
- **Errors:** Ver sección "Solución de Problemas" arriba

---

## 📈 Estadísticas

| Métrica | Valor |
|---------|-------|
| Líneas de código nuevas | ~450 |
| Archivos modificados | 3 |
| Métodos nuevos | 3 |
| Tests incluidos | 3 |
| Documentos | 7 |
| Compatibilidad hacia atrás | ✅ 100% |
| Estado | ✅ Producción |

---

## 🎯 Próximos Pasos

1. **Ahora:** Lee [GUIA_PRUEBA.md](GUIA_PRUEBA.md) y prueba la aplicación
2. **Luego:** Experimenta con diferentes sistemas
3. **Finalmente:** Integra en tus problemas matemáticos

---

## ✨ Conclusión

El sistema está **listo para uso educativo** con:
- ✅ Interfaz intuitiva
- ✅ API robusta  
- ✅ Documentación completa
- ✅ Tests exhaustivos
- ✅ Compatibilidad total

**¡Disfruta resolviendo sistemas de ecuaciones diferenciales!**

---

**Última actualización:** 12 de Enero, 2026
**Versión:** 1.0 (Sistemas)
**Estado:** ✅ Listo

*Para preguntas o mejoras, consulta la documentación o revisa el código.*
