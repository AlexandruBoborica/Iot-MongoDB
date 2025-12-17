from bson import ObjectId
from datetime import datetime, timezone


def create_device_type(db, name, manufacturer_id, metrics):
    device_type = {
        "name": name,
        "manufacturerId": ObjectId(manufacturer_id),
        "metrics": metrics,  # list of strings
        "createdAt": datetime.now(timezone.utc)
    }
    result = db.deviceTypes.insert_one(device_type)
    print(f"Inserted device type with _id: {result.inserted_id}")
    return result.inserted_id


def read_device_types(db, filter={}):
    return list(db.deviceTypes.find(filter))


def update_device_type(db, device_type_id, update_fields):
    result = db.deviceTypes.update_one(
        {"_id": ObjectId(device_type_id)},
        {"$set": update_fields}
    )
    print(f"Matched {result.matched_count}, Modified {result.modified_count}")


def delete_device_type(db, device_type_id):
    result = db.deviceTypes.delete_one(
        {"_id": ObjectId(device_type_id)}
    )
    print(f"Deleted {result.deleted_count} device type(s)")
