import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import requests

# Defina sua chave de API do Asaas e o URL
ASAAS_API_KEY = 'sua_chave_de_api_asaas'
ASAAS_URL = 'https://www.asaas.com/api/v3/customers'

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Lê os dados enviados no formulário
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        # Extraindo dados do formulário
        name = data.get('name', [None])[0]
        email = data.get('email', [None])[0]
        phone = data.get('phone', [None])[0]

        if not name or not email or not phone:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Campos faltando.")
            return

        # Chamando a API do Asaas para cadastrar o cliente
        payload = {
            'name': name,
            'email': email,
            'phone': phone
        }

        headers = {
            'Authorization': f'Bearer {ASAAS_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.post(ASAAS_URL, json=payload, headers=headers)

        if response.status_code == 201:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Cliente cadastrado com sucesso.")
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Falha ao cadastrar cliente.")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor na porta {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
