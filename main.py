from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from modelos import Amenaza
from servicios import consultar_ip, obtener_blacklist

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {"mensaje": "DDoS Globe API"}


@app.get("/consultar/{ip}")
async def consultar(ip: str):
    resultado = await consultar_ip(ip)
    return resultado


@app.websocket("/ws")
async def websocket_amenazas(websocket: WebSocket):
    await websocket.accept()
    print("Cliente conectado")
    
    import asyncio
    import random
    
    # Intentar obtener blacklist real
    blacklist = await obtener_blacklist(30)
    print(f"Obtenidas {len(blacklist)} IPs de la blacklist")
    
    # Si no hay blacklist, usar IPs conocidas
    if not blacklist:
        print("Usando IPs de ejemplo (blacklist requiere plan premium)")
        ips_ejemplo = [
            "185.220.101.34",
            "45.33.32.156", 
            "218.92.0.107",
            "89.248.167.131",
            "171.25.193.77",
            "195.54.160.149",
            "222.186.30.112",
            "61.177.172.136",
            "103.251.167.20",
            "141.98.11.95",
        ]
    
    while True:
        if blacklist:
            ip_data = random.choice(blacklist)
            ip = ip_data["ipAddress"]
        else:
            ip = random.choice(ips_ejemplo)
        
        amenaza = await consultar_ip(ip)
        await websocket.send_json(amenaza)
        
        await asyncio.sleep(5)