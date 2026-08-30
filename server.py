from flask import Flask, request, jsonify

app = Flask(__name__)

# Store the latest energy reading
latest_data = {
    "device": None,
    "voltage": None,
    "current": None,
    "power": None,
    "energy": None
}


@app.route("/")
def home():
    return "SMART BREEZE SERVER IS RUNNING"


# ESP32 sends data here
@app.route("/energy", methods=["POST"])
def energy():

    global latest_data

    print("\n========== SMART BREEZE ==========")
    print("Raw data:")
    print(request.data)

    try:
        data = request.get_json(force=True)

        latest_data = {
            "device": data.get("device"),
            "voltage": data.get("voltage"),
            "current": data.get("current"),
            "power": data.get("power"),
            "energy": data.get("energy")
        }

        print("Device:", latest_data["device"])
        print("Voltage:", latest_data["voltage"], "V")
        print("Current:", latest_data["current"], "A")
        print("Power:", latest_data["power"], "W")
        print("Energy:", latest_data["energy"], "kWh")
        print("==================================")

        return jsonify({
            "status": "received",
            "data": latest_data
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


# Get the latest energy data
@app.route("/energy", methods=["GET"])
def get_energy():

    return jsonify({
        "status": "success",
        "data": latest_data
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
