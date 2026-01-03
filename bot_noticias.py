import time
from gnews import GNews
from textblob import TextBlob

# --- CONFIGURACIÓN ---
# Lista de países que queremos monitorear
# Puedes agregar los que quieras, Google News soporta casi todos.
PAISES_OBJETIVO = {
    "Colombia": "CO",
    "Argentina": "AR",
    "Mexico": "MX",
    "Estados Unidos": "US",
    "España": "ES",
    "Venezuela": "VE",
    "Brasil": "BR",
    "Japon": "JP",
    "Rusia": "RU",
    "Israel": "IL",
    "Francia": "FR",
    "China": "CN"
}

def analizar_pais(nombre_pais, codigo_pais):
    try:
        # Configuramos Google News:
        # language='en': Pedimos noticias en inglés para que el análisis de sentimiento sea preciso.
        # country=codigo_pais: Filtramos por lo que pasa en ese país.
        google_news = GNews(language='en', country=codigo_pais, max_results=10)
        
        # Obtenemos las noticias
        noticias = google_news.get_news(nombre_pais) # Buscamos noticias sobre el país
        
        if not noticias:
            return None

        total = len(noticias)
        polaridad_acumulada = 0
        positivas = 0
        negativas = 0
        
        # Analizar sentimiento
        for noticia in noticias:
            titulo = noticia['title']
            analisis = TextBlob(titulo)
            score = analisis.sentiment.polarity
            polaridad_acumulada += score
            
            if score > 0.05: positivas += 1
            elif score < -0.05: negativas += 1

        promedio = polaridad_acumulada / total
        
        return {
            "pais": nombre_pais,
            "total": total,
            "score": promedio,
            "pos": positivas,
            "neg": negativas
        }

    except Exception as e:
        print(f"⚠️ Error en {nombre_pais}: {e}")
        return None

def ejecutar_scan_mundial():
    print("==========================================")
    print("🌍 INICIANDO MONITOR GLOBAL (vía Google News)")
    print("==========================================")
    
    resultados = []
    total_paises = len(PAISES_OBJETIVO)
    
    for i, (nombre, codigo) in enumerate(PAISES_OBJETIVO.items()):
        print(f"📡 ({i+1}/{total_paises}) Escaneando: {nombre}...", end="\r")
        
        stats = analizar_pais(nombre, codigo)
        
        if stats:
            resultados.append(stats)
        
        # Pausa de seguridad para que Google no nos bloquee por ir muy rápido
        time.sleep(1) 

    print("\n\n✅ ¡ANÁLISIS COMPLETADO!\n")

    # Ordenar: Los más positivos arriba
    resultados_ordenados = sorted(resultados, key=lambda x: x['score'], reverse=True)

    # --- IMPRIMIR TABLA FINAL ---
    print(f"{'RANGO':<6} {'PAÍS':<15} {'SCORE':<10} {'POS/NEG':<10} {'ESTADO'}")
    print("-" * 65)

    for i, dato in enumerate(resultados_ordenados):
        score = dato['score']
        ratio = f"{dato['pos']}/{dato['neg']}"
        
        if score > 0.05:
            estado = "🟢 Bueno"
        elif score < -0.05:
            estado = "🔴 Malo/Tenso"
        else:
            estado = "⚪ Neutral"
            
        print(f"{i+1:<6} {dato['pais']:<15} {score:<10.3f} {ratio:<10} {estado}")

    print("-" * 65)

# Ejecutar
if __name__ == "__main__":
    ejecutar_scan_mundial()