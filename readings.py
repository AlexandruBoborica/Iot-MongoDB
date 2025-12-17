from bson import ObjectId
from datetime import datetime, timezone


def create_reading(db, device_id, values, timestamp=None):
    reading = {
        "deviceId": ObjectId(device_id),
        "values": values,
        "timestamp": timestamp or datetime.now(timezone.utc)
    }

    result = db.readings.insert_one(reading)
    print(f"Inserted reading with _id: {result.inserted_id}")
    return result.inserted_id


def read_readings(db, filter={}):
    return list(db.readings.find(filter))


def update_reading(db, reading_id, update_fields):
    result = db.readings.update_one(
        {"_id": ObjectId(reading_id)},
        {"$set": update_fields}
    )
    print(f"Matched {result.matched_count}, Modified {result.modified_count}")


def delete_reading(db, reading_id):
    result = db.readings.delete_one(
        {"_id": ObjectId(reading_id)}
    )
    print(f"Deleted {result.deleted_count} reading(s)")
