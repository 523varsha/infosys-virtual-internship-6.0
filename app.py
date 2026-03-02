from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Water Quality Third Party APIs",
        "status": "Server Running"
    })



@app.route("/api/epa/readings")
def epa_readings():
    try:
        url = "https://www.waterqualitydata.us/data/Result/search"
        params = {
            "statecode": "US:CA",
            "mimeType": "json"
        }

        response = requests.get(url, params=params, timeout=5)

        if response.status_code == 200:
            return jsonify({
                "source": "US EPA",
                "result": "success",
                "data": response.json()
            })
        else:
            return jsonify({
                "source": "US EPA",
                "result": "failed",
                "message": "Could not fetch data"
            })

    except Exception as e:
        return jsonify({
            "source": "US EPA",
            "result": "error",
            "message": str(e)
        })



@app.route("/api/who/guidelines")
def who_guidelines():
    return jsonify({
        "source": "WHO",
        "water_quality_guidelines": {
            "pH": "6.5 - 8.5",
            "Turbidity": "< 5 NTU",
            "Lead": "< 0.01 mg/L",
            "Arsenic": "< 0.01 mg/L"
        }
    })



@app.route("/api/cpcb/stations")
def cpcb_stations():
    return jsonify({
        "source": "CPCB India",
        "stations": [
            {
                "station_name": "Yamuna River",
                "location": "Delhi",
                "water_quality": "Poor"
            },
            {
                "station_name": "Ganga River",
                "location": "Varanasi",
                "water_quality": "Moderate"
            }
        ]
    })



if __name__ == "__main__":
    app.run(debug=True)