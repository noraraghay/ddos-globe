import os
import httpx
from dotenv import load_dotenv
from coordenadas import obtener_coordenadas

load_dotenv()

API_KEY = os.getenv("ABUSEIPDB_KEY")


def transformar_a_amenaza(datos: dict):
    info = datos["data"]
    
    if info.get("isTor"):
        tipo = "Tor"
    elif "proxy" in info.get("usageType", "").lower():
        tipo = "Proxy"
    else:
        tipo = "Sospechoso"
    
    lat, lon = obtener_coordenadas(info["countryCode"])
    
    return {
        "ip": info["ipAddress"],
        "pais": info["countryCode"],
        "tipo": tipo,
        "severidad": info["abuseConfidenceScore"],
        "latitud": lat,
        "longitud": lon
    }


async def consultar_ip(ip: str):
    url = "https://api.abuseipdb.com/api/v2/check"
    
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }
    
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }
    
    async with httpx.AsyncClient() as cliente:
        respuesta = await cliente.get(url, headers=headers, params=params)
        datos = respuesta.json()
        amenaza = transformar_a_amenaza(datos)
        return amenaza


async def obtener_blacklist(limite: int = 50):
    """
    Obtiene las IPs más reportadas de AbuseIPDB
    """
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }
    
    params = {
        "confidenceMinimum": 50,
        "limit": limite
    }
    
    async with httpx.AsyncClient() as cliente:
        respuesta = await cliente.get(url, headers=headers, params=params)
        datos = respuesta.json()
        return datos.get("data", [])