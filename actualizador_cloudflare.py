# Cludflare DDNS Update for zabbix alert script
# Descripción: Este programa cambia la IP de cloudflare mediante api y token.
# Autor: Elias Pizarro
# Fecha: 21 de julio de 2023 

# Uso: ./actualizador_cloudflare.py TU_API_KEY TU_ZONE_ID camaras 203.0.113.1
# Resultado: Cambia el registro A del fqdn subdominio.dominio.tld con valor 203.0.113.1

import sys
import logging
import requests

ruta_log = "/ruta/al/archivo/de/log.log"

def update_cloudflare_a_record(api_key, zone_id, subdomain, ip_address):
    fqdn = f"{subdomain}.{zone_id}"
    api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    params = {"type": "A", "name": fqdn}
    response = requests.get(api_url, headers=headers, params=params)
    record_id = response.json()["result"][0]["id"]
    data = {"type": "A", "name": fqdn, "content": ip_address, "proxied": True}
    update_response = requests.put(f"{api_url}/{record_id}", headers=headers, json=data)
    logger.info(f"Registro A para {fqdn} actualizado correctamente.") if update_response.status_code == 200 else logger.error("Error al actualizar el registro A:", update_response.json())

if __name__ == "__main__":
    if len(sys.argv) != 5: sys.exit("Uso: python actualizador_cloudflare.py API_KEY ZONE_ID SUBDOMAIN IP_ADDRESS")
    logging.basicConfig(ruta_log, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger()
    update_cloudflare_a_record(*sys.argv[1:])
