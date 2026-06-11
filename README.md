# BancoSemFilas — Backend Flask + MySQL

Sistema de pré-atendimento bancário com backend Python/Flask ligado a base de dados MySQL.

---

## Estrutura do Projecto

```
bancosemfilas/
├── app.py                  ← Servidor Flask (API REST)
├── schema.sql              ← Script de criação da BD e dados iniciais
├── requirements.txt        ← Dependências Python
├── .env.example            ← Modelo de configuração (copiar para .env)
├── gerar_hashes.py         ← Utilitário para gerar hashes bcrypt
├── templates/              ← Páginas HTML (servidas pelo Flask)
│   ├── index.html
│   ├── login.html
│   ├── marcação.html
│   └── dashboard.html
└── static/
    └── style.css           ← Folha de estilos
```

---

## Instalação Passo-a-Passo

### 1. Pré-requisitos
- Python 3.10+
- MySQL 8.0+ em execução
- pip

### 2. Instalar dependências Python
```bash
pip install -r requirements.txt
```

### 3. Configurar a base de dados

#### 3a. Criar a BD e as tabelas
```bash
mysql -u root -p < schema.sql
```
Isto cria a base de dados `bancosemfilas`, todas as tabelas e insere dados de demonstração.

#### 3b. Configurar credenciais
```bash
cp .env.example .env
# Editar .env com o editor preferido
nano .env
```

Preencher `.env`:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=SUA_SENHA_MYSQL
DB_NAME=bancosemfilas
```

### 4. Arrancar o servidor
```bash
python app.py
```
O servidor inicia em **http://localhost:5000**

---

## Credenciais de Demonstração

| Tipo         | Campo    | Valor              |
|--------------|----------|--------------------|
| Cliente      | Email    | cliente@email.com  |
| Cliente      | Senha    | 123456             |
| Funcionário  | ID       | func001            |
| Funcionário  | Senha    | admin123           |

---

## API Endpoints

| Método | Rota                       | Descrição                          |
|--------|----------------------------|------------------------------------|
| POST   | `/api/login`               | Autenticação (cliente/funcionário) |
| POST   | `/api/marcacoes`           | Criar nova marcação                |
| GET    | `/api/marcacoes`           | Listar marcações (com filtros)     |
| PATCH  | `/api/marcacoes/<id>`      | Atualizar estado da marcação       |
| GET    | `/api/estatisticas`        | Estatísticas do dia (dashboard)    |

### Exemplos de chamadas

**Login funcionário:**
```json
POST /api/login
{ "tipo": "funcionario", "username": "func001", "senha": "admin123" }
```

**Criar marcação:**
```json
POST /api/marcacoes
{
  "nome": "João Silva", "bi": "008665412LA048",
  "telefone": "923000001", "email": "joao@email.com",
  "banco": "BAI", "agencia": "Talatona",
  "servico": "Depósito", "data": "2026-06-15", "horario": "10:00"
}
```

**Atualizar estado:**
```json
PATCH /api/marcacoes/5
{ "estado": "Atendido" }
```

**Listar com filtros:**
```
GET /api/marcacoes?data=2026-06-15&estado=Aguardar&q=João
```

---

## Produção (opcional)

Para produção use **Gunicorn** em vez do servidor de desenvolvimento:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
