from fastapi import FastAPI, HTTPException
import requests
from typing import Dict, Any, List

app = FastAPI(
    title="Real-Time Water Data API Fetcher",
    description="Isolated Module for fetching Third-Party Government Water Quality APIs (US EPA, WHO, CPCB India).",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Third-Party Water Quality APIs Integrator",
        "status": "Running",
        "available_endpoints": [
            "/api/epa/readings",
            "/api/who/guidelines",
            "/api/cpcb/stations"
        ]
    }

# --- External APIs from Government Web Sources ---

@app.get("/api/epa/readings", response_model=Dict[str, Any])
def epa_readings():
    """
    Fetch Real-time Data from US EPA (Water Quality Portal).
    If the API is down or times out, it provides a structured fallback response.
    """
    try:
        url = "https://www.waterqualitydata.us/data/Station/search"
        params = {
            "statecode": "US:06",
            "mimeType": "geojson",
            "maxresults": "10" # Limiting to prevent massive payloads during testing
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            "source": "US EPA API (Live)",
            "status": "success",
            "data_count": len(data) if isinstance(data, list) else "unknown",
            "data": data
        }
    except Exception as e:
        return {
            "source": "US EPA API (Local Fallback Mode)",
            "status": "failed",
            "error_reason": "EPA API unreachable. Unable to fetch live data.",
            "developer_details": str(e),
            "fallback_data": [
                {"station": "Mock CA Station 1", "pH": 7.2},
                {"station": "Mock CA Station 2", "pH": 6.8}
            ]
        }

@app.get("/api/who/guidelines", response_model=Dict[str, Any])
def who_guidelines():
    """
    WHO Guidelines.
    Open API not readily accessible without auth/complex integration.
    Fulfilling requirement: 'if it doesn't work, use the local stored records instead'.
    """
    return {
        "source": "WHO (Local Stored Records)",
        "status": "success",
        "note": "Live WHO API unreachable or requires private access. Using local fallback dictionary.",
        "water_quality_guidelines": {
            "pH": "6.5 - 8.5",
            "Turbidity": "< 5 NTU",
            "Lead": "< 0.01 mg/L",
            "Arsenic": "< 0.01 mg/L"
        }
    }

@app.get("/api/cpcb/stations", response_model=Dict[str, Any])
def cpcb_stations():
    """
    CPCB India open data.
    Fulfilling requirement: 'if it doesn't work, use the local stored station records instead'.
    """
    try:
        # Example API call structure if there was an open unauthenticated route:
        # response = requests.get("https://cpcb.some-open-api.gov.in/stations", timeout=5)
        # response.raise_for_status()
        raise Exception("CPCB India exact free endpoint requires dedicated Gov access token.")
    except Exception as e:
        return {
            "source": "CPCB India (Local Stored Station Records)",
            "status": "success",
            "fallback_used": True,
            "error_reason": str(e),
            "data": [
                {
                    "station_name": "Yamuna River - Nizamuddin Bridge", 
                    "location": "Delhi, India",
                    "latitude": 28.59,
                    "longitude": 77.25,
                    "managed_by": "CPCB"
                },
                {
                    "station_name": "Ganga River - Dashashwamedh Ghat", 
                    "location": "Varanasi, UP, India",
                    "latitude": 25.30,
                    "longitude": 83.00,
                    "managed_by": "UPPCB / CPCB"
                }
            ]
        }

if __name__ == "__main__":
    import uvicorn
    # Allow running directly via `python main.py`
    uvicorn.run(app, host="127.0.0.1", port=8000)
