# 🚀 Troubleshooting: Deploy en Vercel

## ✅ Cambios Realizados

### 1. `vercel.json`
- **buildCommand**: Removido (Vercel lo hace automáticamente)
- **runtime**: Especificado como `python3.9`
- **Resultado**: Vercel sabe que debe usar Python 3.9

### 2. `api/requirements.txt`
- Duplicado desde la raíz
- **Resultado**: Vercel encuentra las dependencias en la función serverless

### 3. `.python-version`
- Especifica Python 3.9.19
- **Resultado**: Vercel usa la versión correcta de Python

---

## 🔍 Verificar Status

Ve a: **https://vercel.com/dashboard**

1. Click en tu proyecto: `HCI_Metafora`
2. Mira la sección **Deployments**
3. El último deployment debería decir:
   - ✅ **Production**: Todo OK
   - ⚠️ **Building**: Esperando...
   - ❌ **Failed**: Hay un error (ver logs)

---

## 📊 Si ves "Failed":

### Paso 1: Ver Logs
1. Haz click en el deployment fallido
2. Ve a **Function Logs** o **Build Logs**
3. Busca el error

### Paso 2: Errores Comunes

**Error: "No such file or directory: 'requirements.txt'"**
→ Solución: Ya está en `api/requirements.txt` ✅

**Error: "ModuleNotFoundError: No module named 'flask'"**
→ Solución: Las dependencias no se instalaron. Ver Logs.

**Error: "GEMINI_API_KEY not found"**
→ Solución: Agregar en Vercel Dashboard → Environment Variables

---

## 🎯 Próximos Pasos

1. **Espera el nuevo deployment** (5-10 minutos)
2. **Ve a:** https://hci-metafora.vercel.app/
3. **Debería estar funcionando** ✅

---

## 🆘 Si aún no funciona

**Opción 1: Redeploy Manual**
```
Dashboard → Deployments → Click (…) → Redeploy
```

**Opción 2: Revisar Vercel Status**
- ¿Vercel está down? https://www.vercel-status.com/

**Opción 3: Alternative (recomendado si Vercel falla)**
```
Cambia a Railway.app:
1. Crea cuenta en railway.app
2. Conecta tu GitHub
3. Selecciona rama master
4. Listo (sin limites de memoria)
```

---

## 📝 Resumen de Archivos

| Archivo | Propósito |
|---------|-----------|
| `vercel.json` | Configuración (ahora sin buildCommand) |
| `api/index.py` | Función principal Flask |
| `api/requirements.txt` | Dependencias para la función |
| `.python-version` | Versión de Python |
| `.vercelignore` | Archivos a ignorar |
| `public/` | Frontend estático |

---

**Estado:** ✅ Optimizado y listo para deploy

Vercel debería desplegar automáticamente en los próximos minutos.
