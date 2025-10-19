# 🚀 SOLUCIÓN: Deploy a Vercel - Estructura Corregida

## El Problema
La aplicación no cargaba preguntas en Vercel aunque el HTML se veía. Esto ocurría porque:

1. **Estructura Incorrecta**: Vercel necesita que las funciones Python estén en `api/index.py`, no en `app.py` en la raíz
2. **Archivos Estáticos**: No estaban en la carpeta correcta `public/`
3. **API Hardcodeada**: El frontend hacía fetch a `http://localhost:5000/api`, que no existe en producción
4. **Configuración de Vercel**: El `vercel.json` no estaba correctamente configurado

## La Solución Implementada

### 1. **Estructura de Carpetas Corregida** ✅
```
.
├── api/
│   └── index.py          ← Función principal de Vercel
├── public/
│   ├── index.html        ← Frontend estático
│   ├── styles.css        ← Estilos
│   └── animations.js     ← Animaciones
├── vercel.json           ← Configuración de Vercel
└── requirements.txt      ← Dependencias
```

### 2. **api/index.py** ✅
- Contiene toda la lógica de Flask
- Vercel ejecuta este archivo como función serverless
- Lee la clave API desde variables de entorno (`GEMINI_API_KEY`)

### 3. **public/index.html** ✅
- Frontend con detección automática de entorno:
  ```javascript
  const isProduction = window.location.hostname !== 'localhost';
  const API_BASE = isProduction ? '/api' : 'http://localhost:5000/api';
  ```
- En producción: usa rutas relativas `/api`
- En desarrollo: usa `http://localhost:5000/api`

### 4. **vercel.json** ✅
```json
{
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.py" },
    { "src": "/(.*)", "dest": "/public/index.html" }
  ]
}
```

## ¿Qué Debes Hacer Ahora?

### 1. Verifica que Vercel tiene tu GEMINI_API_KEY
Ve a: **vercel.com/dashboard → Tu Proyecto → Settings → Environment Variables**

Debe estar configurada:
- **Nombre:** `GEMINI_API_KEY`
- **Valor:** Tu clave de Gemini

### 2. Verifica que el Deploy Pasó
El push a GitHub debería haber disparado un deploy automático. Verifica:
- Dashboard de Vercel → tu proyecto
- ¿Dice "Production"? ✅
- ¿O dice "Failed"? ❌

### 3. Prueba la Aplicación
Ve a: `https://hci-metafora.vercel.app/`

Debería:
- ✅ Cargar el HTML
- ✅ Mostrar preguntas
- ✅ Permitir responder
- ✅ Dar pistas con IA

## Si Sigue Sin Funcionar

**Paso 1:** Ve a Vercel Dashboard → Logs → Function Logs
- Busca errores como: `ModuleNotFoundError` o `NameError`

**Paso 2:** Verifica el archivo `.env` local tiene correcto valor de `GEMINI_API_KEY`

**Paso 3:** Re-deploy manualmente:
- Dashboard de Vercel → Tu Proyecto → Deployments
- Click en los "3 puntos" del deployment más reciente
- "Redeploy"

## Archivos Modificados

| Archivo | Cambio |
|---------|--------|
| `api/index.py` | ✨ NUEVO - Función principal |
| `public/index.html` | ✨ NUEVO - Frontend con detección de entorno |
| `public/styles.css` | ✨ NUEVO - Estilos |
| `public/animations.js` | ✨ NUEVO - Animaciones |
| `vercel.json` | 🔧 Actualizado - Rutas correctas |
| `app.py` | 📝 Modificado - Lee GEMINI_API_KEY desde env |

## Desarrollo Local

Para probar localmente:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Correr el servidor
python app.py

# Abre: http://localhost:5000
```

¡Debería funcionar normalmente!

---

**Nota:** El deploy ahora es automático. Cuando hagas push a GitHub, Vercel se redeploy automáticamente.
