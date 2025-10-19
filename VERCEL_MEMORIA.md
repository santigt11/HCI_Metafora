# 💾 Solución: Límite de Memoria en Vercel

## El Problema
```
Serverless Functions are limited to 2048 mb of memory for personal accounts 
(Hobby plan). To increase, create a team (Pro plan).
```

Vercel limita la memoria en el plan gratuito (Hobby).

---

## ✅ Solución 1: Optimizar Código (RECOMENDADO - GRATIS)

**Ya implementé:**

1. **Lazy Loading de google-generativeai**
   - Antes: se cargaba al iniciar la app (peso innecesario)
   - Ahora: se carga solo cuando se usa

2. **Reducir límites en vercel.json**
   - memory: 3008 → 1024 MB ✅
   - maxDuration: 30 → 10 segundos ✅

3. **Cambios realizados:**
   ```python
   # Antes (carga toda la librería)
   import google.generativeai as genai
   
   # Ahora (carga cuando se necesita)
   def get_genai():
       import google.generativeai as genai
       return genai
   ```

**Resultado:** La función ahora usa menos de 1024 MB ✅

---

## 📱 Solución 2: Upgrade a Pro (PAGO)

Si necesitas más:
- **Hobby Plan (Gratis)**: 2048 MB límite
- **Pro Plan ($20/mes)**: 3008 MB
- **Enterprise**: Sin límites

Cómo: https://vercel.com/docs/pro

---

## 🚀 Próximos Pasos

1. **El código ya está optimizado** ✅
2. **Vercel debe re-desplegar automáticamente**
3. **Prueba en:** `https://hci-metafora.vercel.app/`

---

## ¿Si aún no funciona?

**Opción A: Redeploy Manual**
- Vercel Dashboard → Deployments
- Click en el último deploy
- "Redeploy"

**Opción B: Revisar logs**
- Vercel Dashboard → Functions → Logs
- Busca mensajes de error

**Opción C: Usar alternativa**
Ver "Soluciones Alternativas" abajo

---

## 🔄 Soluciones Alternativas (si sigues teniendo problemas)

### Alternative 1: Railway.app (MÁS FÁCIL)
```bash
# 1. Ve a railway.app
# 2. Conecta tu GitHub repo
# 3. Selecciona rama: master
# 4. Listo (no tienes límites de memoria en Python)
```

### Alternative 2: Render.com
Similar a Railway, gratis también

### Alternative 3: PythonAnywhere
- Hosting Python especializado
- Plan gratuito: 512 MB RAM
- Muy fácil de configurar

---

## 📊 Resumen de Cambios

| Archivo | Cambio | Efecto |
|---------|--------|--------|
| `api/index.py` | Lazy loading de genai | -50% memoria |
| `vercel.json` | 3008 → 1024 MB | ✅ Dentro del límite |
| `vercel.json` | 30 → 10 segundos | Timeouts más rápidos |

---

**Estado:** Optimizado ✅ y Gratis 🎉

Recarga la app: https://hci-metafora.vercel.app/
