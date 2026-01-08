
from flask import Flask, request, render_template, redirect, url_for
from db import get_db
from locations import read_locations, create_location
from deviceTypes import read_device_types, create_device_type
from device import read_devices, create_device
from readings import read_readings, create_reading
from flask import Flask, request, render_template, redirect, url_for
from db import get_db
from companies import read_companies, create_company
from manufacturers import read_manufacturers, create_manufacturer
from bson import ObjectId
from analytics import devices_per_location_aggregation, avg_readings_per_device_aggregation,avg_readings_per_device_type_aggregation
from indexes import create_indexes
from performance import run_performance_test



app = Flask(__name__)
my_database = get_db()

create_indexes(my_database)

@app.route("/", methods=["GET"])
def index():
    analytics = request.args.get("analytics")

    results = []
    analytics_title = None

    if analytics == "devices_per_location":
        analytics_title = "Devices per Location"
        results = devices_per_location_aggregation(my_database)

    elif analytics == "avg_readings_per_device":
        analytics_title = "Average Readings per Device"
        results = avg_readings_per_device_aggregation(my_database)

    elif analytics == "avg_readings_per_device_type":
        analytics_title = "Average Readings per Device Type"
        results = avg_readings_per_device_type_aggregation(my_database)

    return render_template(
        "index.html",
        analytics_type=analytics,
        analytics_title=analytics_title,
        results=results
    )


print("Starting Flask app...")


@app.route("/companies", methods=["GET", "POST"])
def companies_page():
    if request.method == "POST":
        name = request.form["name"]
        industry = request.form["industry"]
        create_company(my_database, name, industry)
        return redirect(url_for("companies_page"))

    companies = read_companies(my_database)
    return render_template("companies.html", companies=companies)


@app.route("/companies/delete/<company_id>", methods=["POST"])
def delete_company(company_id):
    my_database.companies.delete_one({"_id": ObjectId(company_id)})
    return redirect(url_for("companies_page"))



@app.route("/companies/edit/<company_id>", methods=["GET", "POST"])
def edit_company(company_id):
    company = my_database.companies.find_one({"_id": ObjectId(company_id)})

    if request.method == "POST":
        name = request.form["name"]
        industry = request.form["industry"]

        my_database.companies.update_one(
            {"_id": ObjectId(company_id)},
            {"$set": {"name": name, "industry": industry}}
        )
        return redirect(url_for("companies_page"))

    return render_template("company_edit.html", company=company)



@app.route("/locations", methods=["GET", "POST"])
def locations_page():
    companies = read_companies(my_database)

    if request.method == "POST":
        company_id = request.form["company_id"]
        city = request.form["city"]
        street = request.form["street"]
        building = request.form["building"]
        floor = int(request.form["floor"])

        create_location(
            my_database,
            company_id,
            city,
            street,
            building,
            floor
        )
        return redirect(url_for("locations_page"))

    locations = read_locations(my_database)
    return render_template(
        "locations.html",
        locations=locations,
        companies=companies
    )

@app.route("/locations/edit/<location_id>", methods=["GET", "POST"])
def edit_location(location_id):
    location = my_database.locations.find_one(
        {"_id": ObjectId(location_id)}
    )

    if not location:
        return "Location not found", 404

    companies = read_companies(my_database)

    if request.method == "POST":
        company_id = request.form["company_id"]
        city = request.form["city"]
        street = request.form["street"]
        building = request.form["building"]
        floor = int(request.form["floor"])

        my_database.locations.update_one(
            {"_id": ObjectId(location_id)},
            {"$set": {
                "companyId": ObjectId(company_id),
                "address.city": city,
                "address.street": street,
                "address.building": building,
                "address.floor": floor
            }}
        )

        return redirect(url_for("locations_page"))

    return render_template(
        "location_edit.html",
        location=location,
        companies=companies
    )


@app.route("/locations/delete/<location_id>", methods=["POST"])
def delete_location(location_id):
    my_database.locations.delete_one(
        {"_id": ObjectId(location_id)}
    )
    return redirect(url_for("locations_page"))


@app.route("/devices", methods=["GET", "POST"])
def devices_page():
    companies = read_companies(my_database)
    device_types = read_device_types(my_database)
    manufacturers = read_manufacturers(my_database)
    locations = read_locations(my_database)

    if request.method == "POST":
        name = request.form["name"]
        company_id = request.form["company_id"]
        device_type_id = request.form["device_type_id"]
        manufacturer_id = request.form["manufacturer_id"]
        location_id = request.form.get("location_id")

        if not location_id:
            return "Error: Please select a location.", 400

        create_device(
            my_database,
            name,
            company_id,
            device_type_id,
            manufacturer_id,
            location_id,
            status=request.form.get("status", "active")
        )
        return redirect(url_for("devices_page"))

    # Prepare devices list
    devices_raw = read_devices(my_database)
    devices = []
    for d in devices_raw:
        company_doc = my_database.companies.find_one({"_id": d["companyId"]})
        device_type_doc = my_database.deviceTypes.find_one({"_id": d["deviceTypeId"]})
        manufacturer_doc = my_database.manufacturers.find_one({"_id": d["manufacturerId"]})
        location_doc = my_database.locations.find_one({"_id": d["locationId"]})

        devices.append({
            "id": str(d["_id"]),
            "name": d.get("name", "Unnamed"),
            "company": company_doc["name"] if company_doc else "Unknown Company",
            "device_type": device_type_doc["name"] if device_type_doc else "Unknown Type",
            "manufacturer": manufacturer_doc["name"] if manufacturer_doc else "Unknown Manufacturer",
            "location": f"{location_doc['address']['city']}, {location_doc['address']['street']}, {location_doc['address']['building']}" if location_doc else "Unknown Location",
            "status": d.get("status", "active")
        })

    return render_template(
        "devices.html",
        devices=devices,
        companies=companies,
        device_types=device_types,
        manufacturers=manufacturers,
        locations=locations
    )

@app.route("/devices/edit/<device_id>", methods=["GET", "POST"])
def edit_device(device_id):
    device_doc = my_database.devices.find_one({"_id": ObjectId(device_id)})
    if not device_doc:
        return "Device not found", 404

    companies = read_companies(my_database)
    device_types = read_device_types(my_database)
    manufacturers = read_manufacturers(my_database)
    locations = read_locations(my_database)

    if request.method == "POST":
        name = request.form["name"]
        company_id = request.form["company_id"]
        device_type_id = request.form["device_type_id"]
        manufacturer_id = request.form["manufacturer_id"]
        location_id = request.form["location_id"]
        status = request.form.get("status", "active")

        if not location_id:
            return "Error: Please select a location.", 400

        my_database.devices.update_one(
            {"_id": ObjectId(device_id)},
            {"$set": {
                "name": name,
                "companyId": ObjectId(company_id),
                "deviceTypeId": ObjectId(device_type_id),
                "manufacturerId": ObjectId(manufacturer_id),
                "locationId": ObjectId(location_id),
                "status": status
            }}
        )
        return redirect(url_for("devices_page"))

    return render_template(
        "device_edit.html",
        device=device_doc,
        companies=companies,
        device_types=device_types,
        manufacturers=manufacturers,
        locations=locations
    )

@app.route("/devices/delete/<device_id>", methods=["POST"])
def delete_device(device_id):
    my_database.devices.delete_one({"_id": ObjectId(device_id)})
    return redirect(url_for("devices_page"))



@app.route("/readings", methods=["GET", "POST"])
def readings_page():
    devices_list = read_devices(my_database)

    if request.method == "POST":
        device_id = request.form["device_id"]
        values_raw = request.form["values"]  # e.g. "temperature:23,humidity:50"
        values = {}
        for pair in values_raw.split(","):
            if ":" in pair:
                key, val = pair.split(":")
                try:
                    values[key.strip()] = float(val.strip())
                except ValueError:
                    values[key.strip()] = val.strip()
        create_reading(my_database, device_id, values)
        return redirect(url_for("readings_page"))

    readings_raw = read_readings(my_database)
    readings = []
    for r in readings_raw:
        device_doc = my_database.devices.find_one({"_id": r.get("deviceId")})
        device_name = device_doc["name"] if device_doc else "Unknown Device"

        values = r.get("values", {})
        if not isinstance(values, dict):
            values = {}

        readings.append({
            "id": str(r["_id"]),
            "device": device_name,
            "read_values": values,
            "timestamp": r.get("timestamp"),
            "deviceId": r.get("deviceId"),
            "values": values
        })

    return render_template("readings.html", readings=readings, devices=devices_list)


@app.route("/readings/edit/<reading_id>", methods=["GET", "POST"])
def edit_reading(reading_id):
    reading_doc = my_database.readings.find_one({"_id": ObjectId(reading_id)})
    if not reading_doc:
        return "Reading not found", 404

    devices_list = read_devices(my_database)

    # Ensure 'values' is a dictionary
    values_dict = reading_doc.get("values", {})
    if not isinstance(values_dict, dict):
        values_dict = {}

    if request.method == "POST":
        device_id = request.form["device_id"]
        values_raw = request.form["values"]
        values = {}
        for pair in values_raw.split(","):
            if ":" in pair:
                key, val = pair.split(":")
                try:
                    values[key.strip()] = float(val.strip())
                except ValueError:
                    values[key.strip()] = val.strip()
        my_database.readings.update_one(
            {"_id": ObjectId(reading_id)},
            {"$set": {"deviceId": ObjectId(device_id), "values": values}}
        )
        return redirect(url_for("readings_page"))

    return render_template(
        "reading_edit.html",
        reading=reading_doc,
        devices=devices_list,
        values_dict=values_dict   # pass the dictionary explicitly
    )



@app.route("/readings/delete/<reading_id>", methods=["POST"])
def delete_reading(reading_id):
    my_database.readings.delete_one({"_id": ObjectId(reading_id)})
    return redirect(url_for("readings_page"))



@app.route("/device-types", methods=["GET", "POST"])
def device_types_page():
    manufacturers = read_manufacturers(my_database)

    if request.method == "POST":
        name = request.form["name"]
        manufacturer_id = request.form["manufacturer_id"]
        metrics_raw = request.form["metrics"]
        metrics = [m.strip() for m in metrics_raw.split(",")]

        create_device_type(my_database, name, manufacturer_id, metrics)
        return redirect(url_for("device_types_page"))

    device_types = read_device_types(my_database)
    return render_template("device_types.html",
                           device_types=device_types,
                           manufacturers=manufacturers)


@app.route("/device-types/edit/<device_type_id>", methods=["GET", "POST"])
def edit_device_type(device_type_id):
    device_type = my_database.deviceTypes.find_one(
        {"_id": ObjectId(device_type_id)}
    )

    if not device_type:
        return "Device type not found", 404

    manufacturers = read_manufacturers(my_database)

    if request.method == "POST":
        name = request.form["name"]
        manufacturer_id = request.form["manufacturer_id"]
        metrics_raw = request.form["metrics"]

        # Convert "temp, humidity, pressure" → ["temp", "humidity", "pressure"]
        metrics = [m.strip() for m in metrics_raw.split(",") if m.strip()]

        my_database.deviceTypes.update_one(
            {"_id": ObjectId(device_type_id)},
            {"$set": {
                "name": name,
                "manufacturerId": ObjectId(manufacturer_id),
                "metrics": metrics
            }}
        )

        return redirect(url_for("device_types_page"))

    return render_template(
        "device_type_edit.html",
        device_type=device_type,
        manufacturers=manufacturers
    )

@app.route("/device-types/delete/<device_type_id>", methods=["POST"])
def delete_device_type(device_type_id):
    my_database.deviceTypes.delete_one(
        {"_id": ObjectId(device_type_id)}
    )
    return redirect(url_for("device_types_page"))



@app.route("/manufacturers", methods=["GET", "POST"])
def manufacturers_page():
    if request.method == "POST":
        name = request.form["name"]
        country = request.form["country"]
        create_manufacturer(my_database, name, country)
        return redirect(url_for("manufacturers_page"))

    manufacturers = read_manufacturers(my_database)
    return render_template("manufacturers.html", manufacturers=manufacturers)



from bson import ObjectId

@app.route("/manufacturers/edit/<manufacturer_id>", methods=["GET", "POST"])
def edit_manufacturer(manufacturer_id):
    manufacturer = my_database.manufacturers.find_one(
        {"_id": ObjectId(manufacturer_id)}
    )

    if not manufacturer:
        return "Manufacturer not found", 404

    if request.method == "POST":
        name = request.form["name"]
        country = request.form["country"]

        my_database.manufacturers.update_one(
            {"_id": ObjectId(manufacturer_id)},
            {"$set": {
                "name": name,
                "country": country
            }}
        )

        return redirect(url_for("manufacturers_page"))

    return render_template(
        "manufacturer_edit.html",
        manufacturer=manufacturer
    )


@app.route("/performance")
def performance_page():
    results = run_performance_test(my_database)

    return render_template(
        "performance.html",
        results=results
    )


# =======================
# MAIN
# =======================
if __name__ == "__main__":
    app.run(debug=True)
