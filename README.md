# Port Scanner

## Funcionalidades

- Escaneamento de um host ou uma rede;
- Controle de range (intervalo) de portas a serem escaneadas;
- Well Known Ports: Especifica o número da porta e o nome do serviço associado;
- Detecção do estado das portas[^1];
- Opção de escaneamento UDP;
- Detecção do sistema operacional via banner grabbing;
- Suporte a IPv6;

## Instalação
### Clone o Repositório:

~~~bash
git clone https://github.com/seuusuario/portscanner.git
cd portscanner
~~~

## Uso
### Sintaxe Básica
~~~bash
python3 portscanner.py <alvo> [opções]
~~~

### Argumentos
| Argumento | Descrição |
|-----------|------------|
| `<alvo>`  | Endereço IP, rede (notação CIDR) ou nome do host a ser escaneado. |

### Opções
| Opção     | Descrição |
|-----------|------------|
| `-p, --ports` | Intervalo de portas (por exemplo, 1-1000) ou porta única (por exemplo, 80). Padrão: 1-1024. |
| `-u, --udp`   | Escaneia portas UDP em vez de TCP. |
| `-6, --ipv6`  | Habilita suporte a IPv6. |
| `-o, --os`    | Tenta detectar o sistema operacional do alvo. |

### Exemplos
1. **Escanear um Único Endereço IP (TCP)**
   Escaneia todas as portas bem conhecidas (1-1024) em `<alvo>`:
   ~~~bash
   python3 portscanner.py <alvo>
   ~~~

2. **Escanear uma Porta Específica**
   Escaneia apenas a porta 80 em `<alvo>`:
   ~~~bash
   python3 portscanner.py <alvo> -p 80
   ~~~

3. **Escanear um Intervalo de Portas**
   Escaneia as portas 1-1000 em `<alvo>`:
   ~~~bash
   python3 portscanner.py <alvo> -p 1-1000
   ~~~

4. **Escanear Portas UDP**
   Escaneia as portas UDP 1-1024 em `<alvo>`:
   ~~~bash
   python3 portscanner.py <alvo> -u
   ~~~

5. **Escanear uma Rede (Notação CIDR)**
   Escaneia todos os hosts na rede `<rede>` em busca de portas TCP abertas:
   ~~~bash
   python3 portscanner.py <rede>
   ~~~

6. **Detectar Sistema Operacional**
   Escaneia <alvo> e tenta detectar o sistema operacional:
   ~~~bash
   python3 portscanner.py <alvo> -o
   ~~~

7. **Escanear com Suporte a IPv6**
   Escaneia um endereço IPv6:
   ~~~bash
   python3 portscanner.py <IPv6> -6
   ~~~

### Explicação da Saída
A saída do port scanner inclui as seguintes informações para cada porta escaneada:

- **Número da Porta**: A porta que está sendo escaneada.
- **Status**: O estado da porta (Aberta, Fechada ou Filtrada).
- **Serviço**: O serviço associado à porta (se for uma porta bem conhecida).

Exemplo de saída:
~~~plaintext
Escaneando alvo: <alvo>
Intervalo de portas: 1-1024
Protocolo: TCP
========================================
Porta 22: Aberta - SSH
Porta 80: Aberta - HTTP
Porta 443: Aberta - HTTPS
~~~

Se a detecção do sistema operacional estiver habilitada (-o), a saída também incluirá:
~~~plaintext
Detectando sistema operacional...
Sistema operacional detectado: Linux/Unix (SSH)
~~~

### Portas Bem Conhecidas Suportadas
A ferramenta reconhece as seguintes portas bem conhecidas e seus serviços associados:

| Porta | Serviço       |
|-------|---------------|
| 20    | FTP (Dados)   |
| 21    | FTP (Controle)|
| 22    | SSH           |
| 23    | Telnet        |
| 25    | SMTP          |
| 53    | DNS           |
| 80    | HTTP          |
| 110   | POP3          |
| 143   | IMAP          |
| 443   | HTTPS         |
| 3306  | MySQL         |
| 3389  | RDP           |

[^1]: Caso escaneie em um intervalo, apenas as portas ABERTAS serão exibidas.
