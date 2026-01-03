# 🌍 DDoS Globe

Real-time DDoS attack visualization on an interactive 3D globe with cyberpunk aesthetics.

![Status](https://img.shields.io/badge/status-active-00ff88)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![Docker](https://img.shields.io/badge/docker-ready-2496ED)

## 🎯 Overview

DDoS Globe is a cybersecurity visualization tool that displays real-time threat data on an interactive 3D globe. It fetches malicious IP data from AbuseIPDB, processes it through a custom ML classifier, and renders animated attack paths using WebSocket streaming.

## ✨ Features

- **Real-time threat visualization** - Live attack data via WebSocket
- **3D interactive globe** - Built with Globe.gl
- **ML threat classification** - Custom classifier predicting threat severity
- **AbuseIPDB integration** - Real malicious IP data
- **Animated attack arcs** - Comet-style traveling animations
- **Statistics dashboard** - Live threat counters and country tracking
- **Dockerized** - One command to run everything

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI, WebSocket |
| Frontend | HTML5, CSS3, JavaScript, Globe.gl |
| ML | Custom rule-based classifier |
| Data Source | AbuseIPDB API |
| DevOps | Docker, Docker Compose |

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- AbuseIPDB API key ([get free key](https://www.abuseipdb.com/register))

### Run with Docker

1. Clone the repository:
```bash
git clone https://github.com/noraraghay/ddos-globe.git
cd ddos-globe
```

2. Create `.env` file:
```bash
ABUSEIPDB_KEY=your_api_key_here
```

3. Start the application:
```bash
docker compose up --build
```

4. Open in browser:
   - **Globe**: http://localhost:3000
   - **API Docs**: http://localhost:8000/docs

### Run without Docker

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with your API key

4. Start the server:
```bash
uvicorn main:app --reload
```

5. Open `frontend/index.html` in your browser

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌──────────┐    WebSocket     ┌──────────┐               │
│   │ Frontend │◄────────────────►│ Backend  │               │
│   │ Globe.gl │   Real-time      │ FastAPI  │               │
│   └──────────┘                  └────┬─────┘               │
│                                      │                      │
│                          ┌───────────┼───────────┐         │
│                          ▼           ▼           ▼         │
│                    ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│                    │AbuseIPDB │ │    ML    │ │   Geo    │  │
│                    │   API    │ │Classifier│ │ Location │  │
│                    └──────────┘ └──────────┘ └──────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🤖 ML Classifier

The custom threat classifier analyzes multiple risk factors:

| Factor | Weight |
|--------|--------|
| Tor exit node | +30 |
| Proxy server | +20 |
| Hosting/Datacenter | +15 |
| High-risk country | +20 |
| Previous reports | +5 to +30 |

**Severity levels:**
- 🔴 **Critical** (70-100)
- 🟠 **High** (45-69)
- 🔵 **Medium** (20-44)
- 🟢 **Low** (0-19)

## 📁 Project Structure
```
ddos-globe/
├── main.py              # FastAPI application
├── servicios.py         # AbuseIPDB integration
├── ml_modelo.py         # ML threat classifier
├── modelos.py           # Pydantic data models
├── coordenadas.py       # Country geolocation data
├── frontend/
│   └── index.html       # 3D globe interface
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Multi-container setup
├── requirements.txt     # Python dependencies
└── README.md
```

## 📸 Screenshots

*Add screenshots of your running application here*

## 🔮 Future Improvements

- [ ] Historical attack data storage
- [ ] Multiple target locations
- [ ] Attack pattern detection
- [ ] Real-time notifications
- [ ] Mobile responsive design

## 👩‍💻 Author

**Nora Raghay**

- GitHub: [@noraraghay](https://github.com/noraraghay)

## 📝 License

This project is open source and available under the [MIT License](LICENSE).