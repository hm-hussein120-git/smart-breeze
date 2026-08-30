from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "SMART BREEZE SERVER IS RUNNING"


@app.route("/energy", methods=["POST"])
def energy():

    print("\n========== SMART BREEZE ==========")

    print("Raw data:")
    print(request.data)

    try:
        data = request.get_json(force=True)

        print("Device:", data.get("device"))
        print("Voltage:", data.get("voltage"), "V")
        print("Current:", data.get("current"), "A")
        print("Power:", data.get("power"), "W")
        print("Energy:", data.get("energy"), "kWh")

        print("==================================")

        return jsonify({
            "status": "received",
            "data": data
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )