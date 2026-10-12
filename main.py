import os, requests, io, urllib.parse, threading, http.server
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = http.server.HTTPServer(('0.0.0.0', port), http.server.SimpleHTTPRequestHandler)
    print(f"Servidor web de simulación corriendo en el puerto {port}")
    server.serve_forever()

async def crear(u: Update, c: ContextTypes.DEFAULT_TYPE):
    texto = u.message.text.strip()
    await u.message.reply_text("🎨 Dibujando tu idea desde cero, por favor espera...")
    try:
        # RUTA ABSOLUTA: Pieza blindada en una sola linea limpia para el motor de IA
        link = "https://pollinations.ai" + urllib.parse.quote(texto)
        r = requests.get(link, timeout=30)
        if r.status_code == 200:
            img = io.BytesIO(r.content)
            img.name = 'dibujo.jpg'
            await u.message.reply_photo(img)
    except Exception as e:
        print(f"Error en la red: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    app = ApplicationBuilder().token("8659010720:AAFdJ75nXacdYULTLAvy9AjGdci31z0AQ34").build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, crear))
    app.run_polling()

