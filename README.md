# Temp_Humidity_Monitoring

A smart home solution for monitoring temperature and humidity using ESP32, DHT11 sensor, and a web dashboard.

## Features

- ESP32 reads temperature and humidity from a DHT11 sensor and sends the data directly to InfluxDB Cloud.
- The web app (Flask) retrieves and visualizes this data using an embedded Grafana dashboard.

## Project Structure


## Project Structure

```
.
├── app/                  # Flask web application
│   ├── __init__.py
│   ├── routes.py
│   └── templates/
│       └── dashboard.html
├── esp32/                # ESP32 MicroPython code
│   ├── boot.py
│   ├── Hygrothermograph.py
│   ├── I2C_LCD.py
│   └── LCD_API.py
├── requirements.txt      # Python dependencies for Flask app
├── docker-compose.yml    # Docker Compose for Flask and Grafana
└── README.md
```

## Getting Started

### Prerequisites

- Docker Compose
- ESP32 board with MicroPython firmware
- DHT11 sensor
- (Optional) Python 3.12+ and pip for local development

### Setup

#### 1. ESP32

- Flash MicroPython firmware to your ESP32.
- Upload files from `esp32/` to your ESP32.
- Edit WiFi credentials and InfluxDB settings in `Hygrothermograph.py`.

#### 2. Start the Web App and Grafana

```sh
docker-compose up --build
```

- Flask app: [http://localhost:5000](http://localhost:5000)
- Grafana: [http://localhost:3001](http://localhost:3001)

#### 3. Access the Dashboard

Visit [http://localhost:5000](http://localhost:5000) to view the embedded Grafana dashboard.

## Configuration

- Update InfluxDB URL and token in `esp32/Hygrothermograph.py`.
- Edit the Grafana iframe URL in [`dashboard.html`](app/templates/dashboard.html) if your dashboard or panel IDs change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.