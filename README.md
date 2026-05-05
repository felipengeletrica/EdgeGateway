# EdgeGateway

**EdgeGateway** é um gateway de telemetria em Python para coletar dados de dispositivos embarcados, sensores e interfaces de campo, padronizar as mensagens e encaminhar os dados para um broker MQTT ou para arquivos locais de log.

O projeto foi pensado para cenários de IoT, instrumentação, testes de firmware, telemetria industrial, coleta em campo e depuração de dispositivos conectados por **Serial**, **Bluetooth**, **BLE** e **MQTT**.

![Architecture diagram](./img/diagram.png)

---

## Visão geral

O EdgeGateway atua como uma camada intermediária entre dispositivos físicos e sistemas de supervisão, banco de dados, dashboards ou plataformas de IoT.

Ele permite que múltiplos dispositivos sejam configurados em um único arquivo `config.json`, criando uma instância independente para cada interface. Cada instância roda em thread separada, permitindo coleta paralela de dados de várias portas seriais, dispositivos BLE ou GPS Bluetooth.

Fluxo principal de telemetria:

```text
Sensor / MCU / Device
        |
        | Serial, BLE ou Bluetooth
        v
EdgeGateway
        |
        | JSON validado + metadados do gateway
        v
MQTT Broker / File Server / Plataforma IoT
        |
        v
Dashboards, banco de dados, alarmes e integrações
```

---

## Objetivo do projeto

O objetivo é simplificar a coleta de telemetria de dispositivos embarcados sem obrigar cada firmware a implementar toda a pilha de comunicação com nuvem.

Com o EdgeGateway é possível:

- Ler dados seriais de microcontroladores como ESP32, Arduino, STM32, Raspberry Pi Pico ou módulos industriais.
- Converter mensagens seriais em publicações MQTT.
- Receber telemetria BLE e publicar em MQTT.
- Registrar logs localmente em arquivos CSV.
- Coletar dados GPS via Bluetooth.
- Encaminhar comandos MQTT de volta para o dispositivo conectado.
- Adicionar metadados do gateway, como timestamp de recepção.
- Executar como serviço Linux em campo.

---

## Casos de uso

### Telemetria IoT

Coleta de dados ambientais, industriais ou de campo, como:

- Temperatura
- Umidade
- Pressão
- CO2
- VOC
- Pluviometria
- Pulsos de medidores
- GPS
- Status de dispositivos
- Dados de sensores customizados

### Gateway serial para MQTT

Um dispositivo envia JSON pela serial e o EdgeGateway publica automaticamente no broker MQTT.

Exemplo de entrada serial:

```json
{
  "serial": "123456789",
  "message": "SENSOR_DATA",
  "temperature": 24.6,
  "humidity": 71.2,
  "pressure": 101325
}
```

Exemplo publicado no MQTT:

```json
{
  "gateway_meta": {
    "timestamp": "2026-05-05 17:30:22.410120"
  },
  "data": {
    "serial": "123456789",
    "message": "SENSOR_DATA",
    "temperature": 24.6,
    "humidity": 71.2,
    "pressure": 101325
  }
}
```

### Gateway BLE para MQTT

Um dispositivo BLE envia notificações contendo JSON. O EdgeGateway valida a mensagem, adiciona metadados e publica no tópico MQTT configurado.

### Datalogger local

A interface `serial-to-file` salva os dados recebidos em arquivos CSV, organizados por dispositivo, permitindo testes de bancada e auditoria offline.

### Campo e operação contínua

O projeto pode ser instalado como serviço Linux usando `systemd`, permitindo operação contínua em Raspberry Pi, gateway industrial, mini PC ou servidor local.

---

## Interfaces suportadas

| Interface | Função | Direção | Status |
|---|---|---:|---|
| `serial-to-file` | Lê dados de uma porta serial e salva localmente em arquivo | Entrada | Implementado |
| `serial-to-mqtt` | Lê JSON da serial, adiciona metadados e publica em MQTT | Bidirecional | Implementado |
| `bluetooth-gps` | Lê dados NMEA de GPS Bluetooth e salva localmente | Entrada | Implementado |
| `bluetooth-BLE` | Lê notificações BLE e mostra os dados recebidos | Entrada | Implementado |
| `bluetooth-BLE-to-mqtt` | Lê JSON via BLE, adiciona metadados e publica em MQTT | Bidirecional | Implementado |

---

## Estrutura do projeto

```text
EdgeGateway-development/
├── README.md
├── requirements.txt
├── config.json
├── src/
│   ├── main.py
│   ├── power-fail.py
│   ├── Utils.py
│   ├── interface/
│   │   ├── SerialToFile.py
│   │   ├── SerialToMQTT.py
│   │   ├── BLEConnector.py
│   │   ├── BLEConnectorToMQTT.py
│   │   ├── BluetoothGpsAgrinavi.py
│   │   └── mqtt_manager.py
│   └── storage/
│       └── Dataanalysis.py
├── services/
│   ├── datalogger.service
│   ├── install.sh
│   └── uninstall.sh
├── examples/
└── diagram/
```

---

## Formato de telemetria

A aplicação espera que os dispositivos enviem mensagens em JSON quando o destino for MQTT.

A validação mínima feita pelo gateway verifica se a mensagem contém uma estrutura compatível com JSON. Depois disso, o payload original é encapsulado no campo `data` e os metadados do gateway são adicionados no campo `gateway_meta`.

Formato publicado:

```json
{
  "gateway_meta": {
    "timestamp": "YYYY-MM-DD HH:MM:SS"
  },
  "data": {
    "serial": "device_serial",
    "message": "message_type",
    "payload": {}
  }
}
```

Esse formato facilita o consumo posterior por:

- Node-RED
- Home Assistant
- Grafana
- Telegraf
- InfluxDB
- ClickHouse
- MongoDB
- APIs de telemetria
- Serviços de alarme
- Pipelines de IA ou analytics

---

## Exemplo de configuração

Crie um arquivo `config.json` na raiz do projeto.

```json
{
  "server_mqtt": {
    "username": "mqtt_user",
    "password": "mqtt_password",
    "server": "broker.example.com",
    "port": 1883,
    "subscribe-upstream": "telemetry/gateway/upstream",
    "subscribe-downstream": "telemetry/gateway/downstream"
  },
  "devices": [
    {
      "serialport": "/dev/serial/by-path/pci-0000:00:14.0-usb-0:2:1.0",
      "baudrate": 115200,
      "timeout": 5,
      "description": "ESP32 Environmental Station",
      "interface": "serial-to-mqtt"
    },
    {
      "serialport": "/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller-if00-port0",
      "baudrate": 115200,
      "timeout": 5,
      "description": "STM32 Pulse Counter",
      "interface": "serial-to-file"
    },
    {
      "address": "44:17:93:60:33:22",
      "samplingSeconds": 0.05,
      "description": "BLE Telemetry Node",
      "interface": "bluetooth-BLE-to-mqtt"
    },
    {
      "address": "54:43:B2:8A:11:26",
      "port": 1,
      "samplingSeconds": 1,
      "description": "Bluetooth GPS",
      "interface": "bluetooth-gps"
    }
  ]
}
```

---

## Configuração de porta serial estável no Linux

Evite usar diretamente `/dev/ttyUSB0` ou `/dev/ttyACM0`, pois esses nomes podem mudar após reconexão ou reboot.

Use:

```bash
ls /dev/serial/by-path
```

ou:

```bash
ls /dev/serial/by-id
```

Depois configure o caminho completo no campo `serialport` do `config.json`.

Exemplo:

```json
{
  "serialport": "/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller-if00-port0",
  "baudrate": 115200,
  "timeout": 5,
  "description": "Production Gateway",
  "interface": "serial-to-mqtt"
}
```

---

## Instalação

Crie um ambiente virtual:

```bash
python3 -m venv env
source env/bin/activate
```

No Windows:

```bash
env\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Dependências de Bluetooth no Linux:

```bash
sudo apt-get update
sudo apt-get install -y bluetooth libbluetooth-dev
```

---

## Execução

Execute a aplicação:

```bash
python src/main.py
```

A aplicação irá:

1. Carregar o arquivo `config.json`.
2. Inicializar cada dispositivo configurado.
3. Abrir as conexões Serial, Bluetooth ou BLE.
4. Publicar dados válidos no MQTT ou salvar em arquivo.
5. Manter o processo em execução com mensagens periódicas de keep alive.

---

## Instalação como serviço Linux

Para instalar como serviço `systemd`:

```bash
cd services
sudo chmod +x install.sh
sudo ./install.sh
```

Ver logs em tempo real:

```bash
journalctl -u datalogger.service -f
```

Ver últimas mensagens:

```bash
journalctl --unit=datalogger.service -n 100 --no-pager
```

Remover serviço:

```bash
cd services
sudo ./uninstall.sh
```

---

## Tópicos MQTT

O projeto usa dois tópicos principais:

| Campo | Descrição |
|---|---|
| `subscribe-upstream` | Tópico onde o gateway publica a telemetria recebida dos dispositivos |
| `subscribe-downstream` | Tópico onde o gateway escuta comandos vindos da plataforma |

Exemplo:

```json
{
  "subscribe-upstream": "telemetry/edgegateway/data",
  "subscribe-downstream": "telemetry/edgegateway/commands"
}
```

### Publicação de telemetria

```text
Device -> EdgeGateway -> MQTT upstream
```

### Envio de comandos

```text
Cloud / Node-RED / API -> MQTT downstream -> EdgeGateway -> Device
```

---

## Integração com dashboards e bancos de dados

O EdgeGateway pode ser usado como coletor de borda para alimentar pipelines como:

```text
EdgeGateway -> MQTT -> Node-RED -> InfluxDB -> Grafana
EdgeGateway -> MQTT -> Telegraf -> InfluxDB -> Grafana
EdgeGateway -> MQTT -> API Python -> ClickHouse -> Grafana
EdgeGateway -> MQTT -> MongoDB -> Analytics
EdgeGateway -> MQTT -> Home Assistant
```

Essa arquitetura permite separar a coleta física dos sensores da camada de armazenamento e visualização.

---

## Exemplo para telemetria de pulsos

Para dispositivos que enviam múltiplos canais de pulso, recomenda-se manter a identificação do canal no payload.

Exemplo:

```json
{
  "product": 1,
  "protocol": "0.4.2",
  "firmware": "1.0.8-dev",
  "serial": "123456789",
  "message": "PULSE_SENSOR",
  "Pulses": [
    { "Sensor": 1, "lsb": 10, "msb": 0 },
    { "Sensor": 2, "lsb": 25, "msb": 0 },
    { "Sensor": 3, "lsb": 4, "msb": 1 }
  ],
  "radio_rssi": -78,
  "radio_snr": 7.5
}
```

Nesse caso, cada item em `Pulses` representa um canal independente de medição. A aplicação que consome o MQTT pode gravar os dados usando uma chave composta, por exemplo:

```text
serial + sensor_channel + timestamp
```

Campos recomendados para banco de dados:

| Campo | Descrição |
|---|---|
| `serial` | Identificação do dispositivo |
| `sensor_channel` | Canal físico do contador de pulsos |
| `pulse_value` | Valor calculado a partir de `lsb` e `msb` |
| `radio_rssi` | Intensidade de sinal do dispositivo |
| `radio_snr` | Relação sinal-ruído |
| `firmware` | Versão do firmware |
| `protocol` | Versão do protocolo |
| `gateway_timestamp` | Timestamp de recebimento no gateway |

---

## Desenvolvimento

Instale o pre-commit:

```bash
pip install pre-commit
pre-commit install
```

Executar verificações:

```bash
pre-commit run --all-files
```

---

## Testes

O diretório `examples/` contém projetos de exemplo para envio de dados por serial e BLE.

Para testar com PlatformIO:

```bash
cd examples/arduino
pio run -t upload
```

Depois execute o gateway e monitore o broker MQTT:

```bash
mosquitto_sub -h broker.example.com -p 1883 -t "telemetry/#" -v
```

---

## Troubleshooting

### Permissão de porta serial

Adicione o usuário ao grupo `dialout`:

```bash
sudo usermod -a -G dialout $USER
```

Faça logout/login após o comando.

### Verificar dispositivos seriais

```bash
dmesg | grep tty
ls /dev/serial/by-id
ls /dev/serial/by-path
```

### Verificar Bluetooth

```bash
bluetoothctl
scan on
```

### Verificar serviço

```bash
systemctl status datalogger.service
journalctl -u datalogger.service -f
```

---

## Segurança

- Não versionar credenciais reais no `config.json`.
- Usar usuários MQTT com permissões limitadas por tópico.
- Preferir TLS em produção quando o broker estiver exposto na internet.
- Manter dependências atualizadas.
- Executar o serviço com usuário limitado, evitando permissões de root quando possível.

---

## Roadmap sugerido

- Normalização opcional de payloads de pulso em múltiplos canais.
- Suporte nativo a RSSI/SNR como metadados de telemetria.
- Reconexão BLE com backoff configurável.
- Configuração por variáveis de ambiente para Docker/Kubernetes.
- Exportador direto para InfluxDB ou ClickHouse.
- Métricas internas do gateway, como uptime, mensagens por minuto e falhas de conexão.
- Testes automatizados para parsers de telemetria.

---

## Licença

Consulte o arquivo [`LICENSE`](LICENSE).
