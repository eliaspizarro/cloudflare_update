# Cludflare DDNS Update for zabbix alert script
# Descripción: Este programa cambia la IP de cloudflare mediante api y token.
# Autor: Elias Pizarro
# Fecha: 21 de julio de 2023 

# Uso: ./cloudflare_wan_update.py TU_API_KEY subdominio.dominio.tld 203.0.113.1
# Resultado: Cambia el registro A del fqdn subdominio.dominio.tld con valor 203.0.113.1

import sys
import logging
import requests

ruta_log = "/var/log/zabbix/zabbix_scripts.log"

def get_zone_id(api_key, site_name):
    api_url = "https://api.cloudflare.com/client/v4/zones"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"name": site_name}
    response = requests.get(api_url, headers=headers, params=params)
    result = response.json()["result"]
    return result[0]["id"] if result else None

def update_cloudflare_a_record(api_key, fqdn, ip_address):
    zone_id = get_zone_id(api_key, fqdn.split('.')[-2])
    if not zone_id:
        logger.error(f"No se encontró ninguna zona para el sitio {fqdn.split('.')[-2]}.")
        sys.exit(1)

    api_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    params = {"type": "A", "name": fqdn}
    response = requests.get(api_url, headers=headers, params=params)
    record_id = response.json()["result"][0]["id"]
    data = {"type": "A", "name": fqdn, "content": ip_address, "proxied": True}
    update_response = requests.put(f"{api_url}/{record_id}", headers=headers, json=data)
    logger.info(f"Registro A para {fqdn} actualizado correctamente.") if update_response.status_code == 200 else logger.error("Error al actualizar el registro A:", update_response.json())

if __name__ == "__main__":
    if len(sys.argv) != 4: sys.exit("Uso: python actualizador_cloudflare.py API_KEY FQDN IP_ADDRESS")
    logging.basicConfig(ruta_log, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger()
    api_key, fqdn, ip_address = sys.argv[1:]
    update_cloudflare_a_record(api_key, fqdn, ip_address)
