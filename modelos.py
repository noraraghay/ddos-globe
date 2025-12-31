from pydantic import BaseModel

class Amenaza (BaseModel):
    ip: str
    pais: str
    tipo: str
    severidad: int
    latitud: float
    longitud: float