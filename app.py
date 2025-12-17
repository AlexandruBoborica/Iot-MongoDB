from pymongo import MongoClient
from companies import create_company
from datetime import datetime, timezone

def get_db():
    client = MongoClient("mongodb://localhost:27017")
    db = client["Iot_Fleat"]
    return db

def main():
    db = get_db()
    print(f"Successfully connected to database: {db.name}")
    print(db.list_collection_names())

    company_id = create_company(db, "XtempSens", "Manufacturing")
    print("Inserted company ID:", company_id)

    #all companies
    print("Companies in DB:")
    for doc in db.companies.find():
        print(doc)

if __name__ == "__main__":
    main()
