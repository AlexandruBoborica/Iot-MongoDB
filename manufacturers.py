from bson import ObjectId
from datetime import datetime, timezone


def create_manufacturer(db, name, country):
    manufacturer = {
        "name": name,
        "country": country,
        "createdAt": datetime.now(timezone.utc)
    }
    result = db.manufacturers.insert_one(manufacturer)
    print(f"Inserted manufacturer with _id: {result.inserted_id}")
    return result.inserted_id


def read_manufacturers(db, filter={}):
    return list(db.manufacturers.find(filter))


def update_manufacturer(db, manufacturer_id, update_fields):
    result = db.manufacturers.update_one(
        {"_id": ObjectId(manufacturer_id)},
        {"$set": update_fields}
    )
    print(f"Matched {result.matched_count}, Modified {result.modified_count}")


def delete_manufacturer(db, manufacturer_id):
    result = db.manufacturers.delete_one(
        {"_id": ObjectId(manufacturer_id)}
    )
    print(f"Deleted {result.deleted_count} manufacturer")
