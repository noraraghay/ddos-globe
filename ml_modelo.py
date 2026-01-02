"""
Clasificador de amenazas simple (sin dependencias externas)
Implementa la lógica de un árbol de decisión manualmente
"""

# Países de alto riesgo según estadísticas globales de ciberataques
PAISES_RIESGO_ALTO = ["CN", "RU", "IR", "KP"]
PAISES_RIESGO_MEDIO = ["BR", "IN", "VN", "ID", "UA", "TR"]


def crear_features(ip_data: dict) -> dict:
    """
    Extrae características relevantes de una IP
    """
    usage_type = ip_data.get("usageType", "").lower()
    
    return {
        "es_tor": ip_data.get("isTor", False),
        "es_proxy": "proxy" in usage_type,
        "es_hosting": "hosting" in usage_type or "data center" in usage_type,
        "reportes": ip_data.get("totalReports", 0),
        "pais": ip_data.get("countryCode", ""),
        "es_pais_alto_riesgo": ip_data.get("countryCode", "") in PAISES_RIESGO_ALTO,
        "es_pais_medio_riesgo": ip_data.get("countryCode", "") in PAISES_RIESGO_MEDIO,
    }


def calcular_score_riesgo(features: dict) -> int:
    """
    Calcula un score de riesgo (0-100) basado en las features.
    Este es nuestro "modelo" - una serie de reglas aprendidas de datos.
    """
    score = 0
    
    # Factor 1: Tor (+30 puntos)
    if features["es_tor"]:
        score += 30
    
    # Factor 2: Proxy (+20 puntos)
    if features["es_proxy"]:
        score += 20
    
    # Factor 3: Hosting/Datacenter (+15 puntos)
    if features["es_hosting"]:
        score += 15
    
    # Factor 4: País de alto riesgo (+20 puntos)
    if features["es_pais_alto_riesgo"]:
        score += 20
    elif features["es_pais_medio_riesgo"]:
        score += 10
    
    # Factor 5: Reportes previos (hasta +30 puntos)
    reportes = features["reportes"]
    if reportes > 100:
        score += 30
    elif reportes > 50:
        score += 20
    elif reportes > 10:
        score += 10
    elif reportes > 0:
        score += 5
    
    return min(score, 100)  # Máximo 100


def clasificar_severidad(score: int) -> str:
    """
    Convierte score numérico en categoría
    """
    if score >= 70:
        return "critica"
    elif score >= 45:
        return "alta"
    elif score >= 20:
        return "media"
    return "baja"


def predecir(ip_data: dict) -> dict:
    """
    Predice la severidad de una IP
    """
    features = crear_features(ip_data)
    score = calcular_score_riesgo(features)
    severidad = clasificar_severidad(score)
    
    # Calcular "confianza" basada en cuántos factores de riesgo tiene
    factores_activos = sum([
        features["es_tor"],
        features["es_proxy"],
        features["es_hosting"],
        features["es_pais_alto_riesgo"],
        features["reportes"] > 10
    ])
    confianza = 60 + (factores_activos * 8)  # 60-100%
    
    return {
        "score_riesgo": score,
        "severidad_predicha": severidad,
        "confianza": min(confianza, 100),
        "factores": {
            "tor": features["es_tor"],
            "proxy": features["es_proxy"],
            "hosting": features["es_hosting"],
            "pais_riesgo": features["es_pais_alto_riesgo"] or features["es_pais_medio_riesgo"],
            "reportes_previos": features["reportes"] > 0
        }
    }


# Prueba rápida al ejecutar directamente
if __name__ == "__main__":
    print("=== Probando clasificador ===\n")
    
    ip_peligrosa = {
        "isTor": True,
        "usageType": "Data Center/Web Hosting",
        "totalReports": 150,
        "countryCode": "RU"
    }
    
    ip_normal = {
        "isTor": False,
        "usageType": "ISP",
        "totalReports": 0,
        "countryCode": "ES"
    }
    
    print("IP Peligrosa (Tor + Hosting + Rusia + 150 reportes):")
    print(predecir(ip_peligrosa))
    
    print("\nIP Normal (ISP España, sin reportes):")
    print(predecir(ip_normal))