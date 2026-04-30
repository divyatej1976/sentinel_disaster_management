# AI Disease Outbreak Predictor: Epidemic.Intel

![Epidemic.Intel Dashboard](https://raw.githubusercontent.com/placeholder-path/screenshot.png) *(Replace with your actual screenshot)*

## 📖 Overview
**Epidemic.Intel** is a sophisticated, multi-agent decision support system designed to forecast infectious disease outbreak risks. It functions as an interactive dashboard where users can adjust environmental and epidemiological factors—either manually or via live satellite/weather telemetry—to observe their impact on outbreak probability in real-time.

Built as a high-fidelity tool for researchers and public health officials, this application demonstrates the power of **Multi-Agent AI Consensus**. Instead of a single model output, it simulates a council of experts (Epidemiologist, Environmental Scientist, and Strategist) to provide a nuanced, weighted risk assessment with a measurable disagreement index.

---

## ✨ Features

- **🤖 Multi-Agent Consensus Engine**: Utilizes three independent AI expert personas to analyze telemetry data and reach a weighted consensus on risk, confidence, and drivers.
- **🎛️ Interactive Simulation Controls**: Manually adjust critical risk factors like weather patterns, population density, sanitation infrastructure, and recent case velocity.
- **🌐 Live Telemetry Integration**: Features an "Auto-fill from My Location" button that uses browser GPS and the **Open-Meteo API** to fetch real-time humidity, precipitation, visibility, and cloud cover.
- **📊 Rich Data Visualization**:
  - **Dynamic Probability Ring**: A high-fidelity visual representation of the final risk score.
  - **Radar Profile**: Visualizes the distribution of risk factors (Weather, Density, Sanitation, Cases).
  - **Expert Cards**: Staggered cards showing individual agent opinions, weightings, and recommendations.
- **🧠 Scenario Comparison (The "Delta" View)**: Save a baseline state, modify parameters, and quantify the exact impact of interventions (e.g., how much a 20% sanitation improvement reduces risk).
- **📱 Responsive Mission-Control UI**: A sleek, dark-themed "tactical" interface built with Tailwind CSS and Framer Motion for premium interactions.

---

## 🛠️ Tech Stack

- **Frontend**: React 19, TypeScript, Vite
- **Backend**: Python FastAPI, Uvicorn
- **AI/LLM**: Google Gemini 2.0 Flash
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Visualization**: Recharts
- **Live Data**: Open-Meteo API, Nominatim Geocoding

---

## 🚀 Getting Started

To run Epidemic.Intel locally, follow these steps.

### Prerequisites
- Node.js (v18+)
- Python (v3.11+)
- A **Google Gemini API Key** (Get one at [Google AI Studio](https://aistudio.google.com/))

### 1. Clone the repository
```bash
git clone https://github.com/your-username/epidemic-intel.git
cd epidemic-intel
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

### 3. Install Dependencies
```bash
# Install Frontend
npm install

# Install Backend
pip install -r requirements.txt
```

### 4. Run the Application
You will need two terminals running:

**Terminal 1 (Backend):**
```bash
python -m uvicorn server.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
npm run dev
```
Open your browser and navigate to `http://localhost:3000`.

---

## 📂 Project Structure
```text
.
├── components/          # React UI Components
│   ├── ui/              # Generic UI (TiltCard, AnimatedChat)
│   ├── AnalysisPanel.tsx # Expert opinion cards & drivers
│   ├── ControlsPanel.tsx # Simulation & Live Weather inputs
│   ├── ComparisonPanel.tsx # Scenario Delta Analysis
│   └── PredictionPanel.tsx # Charts & Probability Gauges
├── server/              # FastAPI Backend
│   └── main.py          # Multi-agent consensus logic
├── services/            # API interaction logic
│   ├── geminiService.ts # Frontend-to-Backend API calls
│   └── weatherService.ts # Open-Meteo & Geocoding logic
├── App.tsx              # Main application orchestrator
├── types.ts             # TypeScript type definitions
└── README.md            # This file
```

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
*Developed with a focus on explainable AI and precision epidemiology.*
