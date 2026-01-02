from ml_modelo import modelo_entrenado, predecir

# IP sospechosa de prueba
ip_sospechosa = {
    "isTor": True,
    "usageType": "hosting",
    "totalReports": 50,
    "countryCode": "RU"
}

# IP normal de prueba
ip_normal = {
    "isTor": False,
    "usageType": "isp",
    "totalReports": 0,
    "countryCode": "ES"
}

print("=== IP Sospechosa ===")
print(predecir(modelo_entrenado, ip_sospechosa))

print("\n=== IP Normal ===")
print(predecir(modelo_entrenado, ip_normal))