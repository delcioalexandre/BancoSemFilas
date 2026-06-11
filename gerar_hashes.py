"""
Gera os hashes bcrypt correctos para os utilizadores de demonstração.
Executar: python gerar_hashes.py
Depois copiar os hashes gerados para o schema.sql se necessário.
"""
import bcrypt

senhas = {
    "cliente@email.com (senha: 123456)": "123456",
    "func001 (senha: admin123)":         "admin123",
}

for label, senha in senhas.items():
    h = bcrypt.hashpw(senha.encode(), bcrypt.gensalt(12)).decode()
    print(f"{label}\n  → {h}\n")
