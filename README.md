# IoT Fleet Management with MongoDB

**Authors:** Boborica Mihai-Alexandru, Boca Bogdan Nicolae  

This repository contains the code and documentation for an **IoT Fleet Management System** implemented using **MongoDB** and **Python Flask**. The system manages devices, device types, manufacturers, locations, and readings in a scalable and flexible way.

---

## Overview

The project demonstrates:

- **Database schema design** using MongoDB collections and references.
- **CRUD operations** for all entities (Create, Read, Update, Delete) via Flask web interface.
- **Aggregation pipelines** for analytics, such as average readings, devices per location, and device distribution.
- **Indexing** to optimize query performance.
- **Scaling strategies**, including replication and sharding simulations.
- **NoSQL vs SQL discussion** and trade-offs for IoT workloads.

---

## Tech Stack

- **Backend:** Python 3.11, Flask  
- **Database:** MongoDB  
  - MongoDB Shell & Compass for testing and visualization  
  - PyMongo for Python integration  
- **Frontend:** HTML, CSS (simple dashboard UI)  
- **Other tools:**  
  - ChatGPT (for documentation drafting and code support)  
  - Optional: Postman for API testing  

---

## Features

- **Manage entities:** Companies, Manufacturers, Locations, Device Types, Devices, Readings  
- **Analytics:**  
  - Devices per Location  
  - Average Readings per Device  
  - Average Readings per Device Type  
  - Devices per Manufacturer  
  - Metrics across fleet  
- **Performance testing:** Evaluate queries with and without indexing  
- **Scaling demonstration:** Replication (replica sets) and Sharding simulations  

---

