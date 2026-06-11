-- ============================================================
--  BancoSemFilas — Script de criação da base de dados MySQL
--  Executar: mysql -u root -p < schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS bancosemfilas
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE bancosemfilas;

-- ────────────────────────────
-- TABELA: clientes
-- ────────────────────────────
CREATE TABLE IF NOT EXISTS clientes (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    nome       VARCHAR(150)        NOT NULL,
    email      VARCHAR(150) UNIQUE NOT NULL,
    senha_hash VARCHAR(255)        NOT NULL,
    criado_em  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ────────────────────────────
-- TABELA: funcionarios
-- ────────────────────────────
CREATE TABLE IF NOT EXISTS funcionarios (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    nome       VARCHAR(150)        NOT NULL,
    username   VARCHAR(50)  UNIQUE NOT NULL,
    senha_hash VARCHAR(255)        NOT NULL,
    criado_em  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ────────────────────────────
-- TABELA: marcacoes
-- ────────────────────────────
CREATE TABLE IF NOT EXISTS marcacoes (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    senha    VARCHAR(10)   NOT NULL,
    nome     VARCHAR(150)  NOT NULL,
    bi       VARCHAR(20)   NOT NULL,
    telefone VARCHAR(20)   NOT NULL,
    email    VARCHAR(150)  NOT NULL,
    banco    VARCHAR(80)   NOT NULL,
    agencia  VARCHAR(80)   NOT NULL,
    servico  VARCHAR(100)  NOT NULL,
    data     DATE          NOT NULL,
    horario  VARCHAR(5)    NOT NULL,
    estado   ENUM('Aguardar','Atendido','Cancelado') NOT NULL DEFAULT 'Aguardar',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_data    (data),
    INDEX idx_estado  (estado),
    INDEX idx_banco   (banco, agencia)
);

-- ============================================================
--  DADOS INICIAIS (seed)
-- ============================================================

-- Cliente de demonstração  (senha: 123456)
INSERT INTO clientes (nome, email, senha_hash) VALUES
('Cliente Demo',
 'cliente@email.com',
 '$2b$12$ZFPJaM3QOmLZuFHuyQSu3ux0bqjjjmLZrVSzH2V/aumrPBEpmLXl2')
ON DUPLICATE KEY UPDATE nome = nome;

-- Funcionário de demonstração  (senha: admin123)
INSERT INTO funcionarios (nome, username, senha_hash) VALUES
('Funcionário Demo',
 'func001',
 '$2b$12$KaEWaM.eJRyDRJSSA8PBOeGFaWDuz3bIJ1NzmqPa68gQJJsLyiqnS')
ON DUPLICATE KEY UPDATE nome = nome;

-- Marcações fictícias para demonstração
INSERT INTO marcacoes (senha, nome, bi, telefone, email, banco, agencia, servico, data, horario, estado)
SELECT * FROM (
    SELECT 'A001','Ana Luísa Ferreira',   '008665412LA048','923000001','ana@email.com',    'BAI',        'Talatona',    'Abertura de Conta',     CURDATE(),'08:00','Atendido'
    UNION ALL
    SELECT 'A002','Carlos Mendes Silva',  '009112233LA050','923000002','carlos@email.com', 'BFA',        'Maianga',     'Transferência',         CURDATE(),'08:00','Atendido'
    UNION ALL
    SELECT 'A003','Maria João Baptista',  '007445566LA049','923000003','maria@email.com',  'Atlântico',  'Mutamba',     'Pedido de Cartão',      CURDATE(),'09:00','Atendido'
    UNION ALL
    SELECT 'A004','Pedro Domingos Lopes', '006334455LA047','923000004','pedro@email.com',  'BPC',        'Kilamba',     'Crédito Bancário',      CURDATE(),'10:00','Aguardar'
    UNION ALL
    SELECT 'A005','Sofia Nunes Cardoso',  '005223344LA046','923000005','sofia@email.com',  'Banco Sol',  'Viana',       'Depósito',              CURDATE(),'10:00','Aguardar'
    UNION ALL
    SELECT 'A006','António Sebastião',    '004112233LA045','923000006','antonio@email.com','BAI',        'Cacuaco',     'Levantamento de Cartão',CURDATE(),'11:00','Aguardar'
    UNION ALL
    SELECT 'A007','Filomena Teixeira',    '003001122LA044','923000007','filo@email.com',   'BFA',        'Benfica',     'Abertura de Conta',     CURDATE(),'12:00','Cancelado'
    UNION ALL
    SELECT 'A008','Ricardo Caetano Lima', '002990011LA043','923000008','ricardo@email.com','Atlântico',  'Samba',       'Transferência',         CURDATE(),'14:00','Aguardar'
    UNION ALL
    SELECT 'A009','Esperança Mateus',     '001880000LA042','923000009','esperanca@email.com','Banco Keve','Ingombota',  'Pedido de Cartão',      CURDATE(),'15:00','Aguardar'
    UNION ALL
    SELECT 'A010','Domingos Vieira Paulo','000770099LA041','923000010','domingos@email.com','Banco Yetu','Rocha Pinto', 'Crédito Bancário',      CURDATE(),'16:00','Aguardar'
) AS dados
WHERE NOT EXISTS (SELECT 1 FROM marcacoes WHERE senha = 'A001');
