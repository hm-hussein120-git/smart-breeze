from flask import Flask, request, jsonify, render_template
import os
import psycopg

app = Flask(__name__)


def get_db_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise Exception("DATABASE_URL is not configured")

    return psycopg.connect(database_url)


def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS energy_data (
                    id SERIAL PRIMARY KEY,
                    device VARCHAR(100),
                    voltage DOUBLE PRECISION,
                    current DOUBLE PRECISION,
                    power DOUBLE PRECISION,
                    energy DOUBLE PRECISION,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()


@app.route("/")
def home():
    return "SMART BREEZE SERVER IS RUNNING"


@app.route("/energy", methods=["POST"])
def energy():

    print("\n========== SMART BREEZE ==========")

    try:
        data = request.get_json(force=True)

        device = data.get("device")
        voltage = data.get("voltage")
        current = data.get("current")
        power = data.get("power")
        energy = data.get("energy")

        print("Device:", device)
        print("Voltage:", voltage, "V")
        print("Current:", current, "A")
        print("Power:", power, "W")
        print("Energy:", energy, "kWh")

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO energy_data
                    (device, voltage, current, power, energy)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    device,
                    voltage,
                    current,
                    power,
                    energy
                ))
            conn.commit()

        print("Data saved to PostgreSQL")
        print("==================================")

        return jsonify({
            "status": "received",
            "message": "Data saved to database",
            "data": data
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


@app.route("/energy", methods=["GET"])
def get_energy():

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        id,
                        device,
                        voltage,
                        current,
                        power,
                        energy,
                        created_at
                    FROM energy_data
                    ORDER BY id DESC
                    LIMIT 50
                """)

                rows = cur.fetchall()

        data = []

        for row in rows:
            data.append({
                "id": row[0],
                "device": row[1],
                "voltage": row[2],
                "current": row[3],
                "power": row[4],
                "energy": row[5],
                "created_at": row[6].isoformat()
            })

        return jsonify({
            "status": "success",
            "count": len(data),
            "data": data
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Create database table when the server starts
try:
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print("Database initialization error:", e)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
