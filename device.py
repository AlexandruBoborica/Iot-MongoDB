from bson import ObjectId
from datetime import datetime, timezone

def create_device(
    db,
    name,
    company_id,
    device_type_id,
    manufacturer_id,
    location_id,
    status="active",
    last_reading=None
):
    device = {
        "name": name,
        "companyId": ObjectId(company_id),
        "deviceTypeId": ObjectId(device_type_id),
        "manufacturerId": ObjectId(manufacturer_id),
        "locationId": ObjectId(location_id),
        "status": status,
        "installedAt": datetime.now(timezone.utc),
        "createdAt": datetime.now(timezone.utc)
    }

    if last_reading:
        device["lastReading"] = last_reading

    result = db.devices.insert_one(device)
    print(f"Inserted device with _id: {result.inserted_id}")
    return result.inserted_id


def read_devices(db, filter={}):
    return list(db.devices.find(filter))


def update_device(db, device_id, update_fields):
    result = db.devices.update_one(
        {"_id": ObjectId(device_id)},
        {"$set": update_fields}
    )
    print(f"Matched {result.matched_count}, Modified {result.modified_count}")


def delete_device(db, device_id):
    result = db.devices.delete_one(
        {"_id": ObjectId(device_id)}
    )
    print(f"Deleted {result.deleted_count} device(s)")
