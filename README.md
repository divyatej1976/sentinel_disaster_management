# Epidemic.Intel: AI-Powered Outbreak Prediction Dashboard

Epidemic.Intel is a sophisticated, multi-agent decision support system designed to forecast infectious disease outbreak risks. By leveraging the Google Gemini 2.0 Flash API and real-time environmental telemetry, it provides actionable insights for public health officials and researchers.

![Dashboard Preview](https://raw.githubusercontent.com/placeholder-path/screenshot.png) *(Replace with your actual screenshot after pushing)*

## 🚀 Key Features

- **Multi-Agent Consensus Engine**: Three independent AI expert personas (Epidemiologist, Environmental Scientist, and Public Health Strategist) evaluate telemetry data to produce a weighted risk probability and a quantifiable disagreement index.
- **Live Environmental Telemetry**: Real-time weather data (humidity, precipitation, visibility, etc.) is automatically fetched via the Open-Meteo API based on the user's browser geolocation.
- **Scenario Comparison Engine**: Save a "Baseline" simulation, adjust parameters (e.g., improving sanitation), and instantly see the percentage impact of potential interventions.
- **Explainable AI (XAI)**: Detailed factor breakdowns and ranked risk drivers help users understand *why* a specific risk level was reached.
- **High-Fidelity UI**: Interactive radar charts, probability gauges, and fluid animations built with Framer Motion and Recharts.

## 🛠️ Tech Stack

- **Frontend**: React 19, TypeScript, Tailwind CSS, Framer Motion, Recharts, Lucide Icons.
- **Backend**: Python FastAPI, Uvicorn.
- **AI/LLM**: Google Gemini 2.0 Flash (via `google-genai`).
- **Data APIs**: Open-Meteo (Weather), Nominatim/OpenStreetMap (Reverse Geocoding).
- **Build Tool**: Vite.

## 📦 Installation & Setup

### Prerequisites
- Node.js (v18+)
- Python (v3.11+)
- A Google Gemini API Key

### 1. Clone the repository
```bash
git clone https://github.com/your-username/epidemic-intel.git
cd epidemic-intel
```

### 2. Frontend Setup
```bash
npm install
```

### 3. Backend Setup
```bash
# Recommended: create a virtual environment
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Running the Application
**Start Backend:**
```bash
python -m uvicorn server.main:app --reload --port 8000
```

**Start Frontend:**
```bash
npm run dev
```
The app will be available at `http://localhost:3000`.

## 🧠 Theoretical Background

The core of Epidemic.Intel is its **weighted consensus algorithm**. Instead of relying on a single prompt, the system simulates a panel of experts. 
- **Dr. Aris (Epidemiologist)** focuses on pathogen transmission and case velocity.
- **Prof. Lyra (Environmental Scientist)** focuses on climate stress and infrastructure.
- **Gen. Vance (Public Health Strategist)** focuses on response capacity and mitigation priority.

The final "Outbreak Risk" score is calculated by combining these independent assessments, accounting for the relative confidence and agreement between agents.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built as a high-fidelity Decision Support System for Epidemiological Intelligence.*
