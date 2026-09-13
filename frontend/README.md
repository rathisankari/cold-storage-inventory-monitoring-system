# ColdGuard – Cold Storage Inventory Monitoring System

**Real-Time Cold Storage Monitoring & Inventory Management System**

**Author:** Rathi Sankari S
**Department:** Artificial Intelligence & Data Science (AI & DS)

---

## 1. Project Overview

ColdGuard is a full-stack HealthTech system designed to monitor pharmaceutical cold-storage units and manage temperature-sensitive vaccine and medicine inventory.

The system continuously records temperature and humidity readings from storage units, detects temperature excursions, generates alerts, and provides a dashboard for monitoring storage conditions.

The project currently uses a **simulated IoT sensor feed** for development. The architecture is designed so that physical IoT sensors can be integrated in the future without changing the core application structure.

The system also maintains inventory information such as vaccine name, vaccine code, lot number, quantity, and expiration date.

---

## 2. Problem Statement

Vaccines and temperature-sensitive medicines must be stored within specific temperature ranges throughout the cold-chain process.

For example, many routine vaccines are stored between **2°C and 8°C**, while other pharmaceutical products may require deep-frozen or ultra-cold storage conditions.

Traditional cold-storage monitoring may depend on manual and periodic temperature checks. This creates a risk because a temperature excursion can occur between two manual checks and remain undetected.

A temperature-damaged vaccine or medicine may not show visible physical changes. Therefore, relying only on manual inspection is insufficient for maintaining reliable monitoring and traceability.

The project addresses this problem by providing a centralized system that can:

- Continuously monitor storage conditions
- Record temperature and humidity readings
- Detect temperature excursions
- Generate alerts when unsafe conditions occur
- Display real-time storage status
- Visualize temperature history
- Manage temperature-sensitive inventory
- Maintain historical monitoring records
- Support future anomaly and trend detection

---

## 3. Proposed Solution

ColdGuard provides a web-based monitoring and inventory management platform for pharmaceutical cold-storage facilities.

The system receives simulated sensor readings through the backend API and associates each reading with a storage unit.

The monitoring workflow is:

```text
Simulated Sensor
       |
       v
Temperature / Humidity Reading
       |
       v
FastAPI Backend
       |
       v
Temperature Log
       |
       v
Threshold Comparison
       |
       +----------------------+
       |                      |
       v                      v
   Normal                 Excursion
       |                      |
       v                      v
Dashboard              Alert Generated
                              |
                              v
                         Alert Dashboard
```

The system also provides inventory management for vaccines and medicines stored inside the monitored storage units.

---

## 4. Project Objectives

- To continuously monitor cold-storage environmental conditions.
- To maintain historical temperature and humidity records.
- To automatically identify unsafe temperature conditions.
- To generate alerts when temperature thresholds are breached.
- To provide a dashboard for storage operators.
- To maintain inventory information for temperature-sensitive products.
- To provide temperature trend visualization.
- To create a foundation for future AI-based anomaly detection.
- To maintain reliable monitoring records for compliance and auditing.

---

## 5. Users

### Storage Operator
Responsible for monitoring assigned storage units.

Can: view storage-unit conditions, current temperature, humidity, allowed range, temperature history, active alerts; acknowledge alerts; view inventory information.

The operator should not be able to modify historical sensor readings.

### Compliance / Logistics Admin
Responsible for system-level management.

Planned responsibilities: manage storage units, configure temperature thresholds, manage users and access, view system-wide monitoring information, view alerts, generate compliance reports, view audit records.

---

## 6. Core Features

### 6.1 Temperature Monitoring
Displays the current environmental condition of a storage unit — name, current temperature, current humidity, allowed range, current status.

### 6.2 Temperature History
Every temperature reading is stored with its timestamp, feeding a trend graph so operators can see how conditions change over time.

### 6.3 Automatic Alerts
When a reading falls outside the configured safe range, the system logs a temperature excursion and generates an alert (storage unit, alert type, message, status, timestamp). Operators can acknowledge active alerts.

### 6.4 Inventory Management
Tracks vaccine/medicine batches per storage unit: name, code, lot number, quantity, expiration date, status. Historical inventory records should not be casually modified, since altering the status of an already-expired or compromised batch could produce incorrect inventory information.

---

## 7. System Architecture

```text
                    USER
                     |
                     v
              React Frontend
                     |
                     v
              FastAPI Backend
                     |
        +------------+------------+
        |            |            |
        v            v            v
   Monitoring     Inventory     Alerts
        |
        v
 Temperature Logs
        |
        v
    PostgreSQL
```

**Frontend** (React): dashboard, inventory interface, monitoring interface, alert display, temperature history visualization, API communication.

**Backend** (FastAPI): REST API endpoints, monitoring logic, inventory management, alert management, temperature-log management, database communication.

**Database** (PostgreSQL): storage units, inventory records, temperature logs, alerts, future user and audit information.

**Architecture Diagram:** `docs/diagrams/architecture-diagram.png` (editable source: `docs/diagrams/architecture-diagram.drawio`)

---

## 8. Entity Relationship Diagram

Core entities: `User`, `StorageUnit`, `Inventory`, `TemperatureLog`, `Alert`, `ComplianceReport`, `AuditLog`.

```text
User
 |
 | manages / monitors
 |
 v
StorageUnit
 |
 +--------------------+
 |                    |
 v                    v
Inventory        TemperatureLog
                      |
                      v
                    Alert

User
 |
 +---------> AuditLog
 |
 +---------> ComplianceReport
```

A storage unit can contain multiple inventory records and multiple temperature logs. Temperature logs are associated with a storage unit and are used for monitoring and alert generation.

**ER Diagram:** `docs/diagrams/er-diagram.png` (editable source: `docs/diagrams/er-diagram.dbml`)
**Database Schema:** `docs/diagrams/schema.sql`

---

## 9. Database Entities

- **User** — application users and roles (Storage Operator, Compliance/Logistics Admin)
- **StorageUnit** — a physical cold-storage unit: name, category, min/max temperature, monitoring status
- **Inventory** — a vaccine/medicine batch: ID, storage unit, name, code, lot number, quantity, expiration date, status
- **TemperatureLog** — individual readings (temperature, humidity, storage unit, timestamp) — append-only, never edited or deleted
- **Alert** — temperature-related monitoring events (storage unit, type, message, status, timestamp)
- **ComplianceReport** — generated compliance report records (planned for a later phase)
- **AuditLog** — records of important system actions (planned, for accountability and auditing)

---

## 10. User Roles and Permissions

| Feature | Storage Operator | Compliance / Logistics Admin |
|---|---|---|
| View assigned storage units | Yes | Yes |
| View temperature / humidity | Yes | Yes |
| View temperature history | Yes | Yes |
| View alerts | Yes | Yes |
| Acknowledge alerts | Yes | Yes |
| View inventory | Yes | Yes |
| Manage storage units | No | Yes |
| Configure thresholds | No | Yes |
| Manage users | No | Yes |
| Generate compliance reports | No | Yes |
| View audit records | No | Yes |

---

## 11. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React |
| Backend | FastAPI |
| Programming Language | Python |
| Database | PostgreSQL |
| API Communication | REST API |
| Frontend Build Tool | Vite |
| Data Visualization | Recharts |
| Sensor Input | Simulated IoT Sensor Feed |
| Version Control | Git / GitHub |

---

## 12. Project Structure (current, as actually committed)

```text
cold-storage-inventory-monitoring-system/
│
├── app/
│   ├── api/            (routers — not yet implemented beyond scaffolding)
│   ├── core/
│   │   └── config.py    (reads .env variables)
│   ├── models/          (SQLAlchemy models — not yet written)
│   ├── schemas/         (Pydantic schemas — not yet written)
│   ├── services/        (business logic — not yet written)
│   └── main.py           (FastAPI app, /health endpoint working)
│
├── tests/
├── tools/
│   └── simulator.py      (sensor simulator script)
│
├── frontend/              (not yet scaffolded)
│
├── docs/
│   ├── Project_Report.md
│   ├── Literature_Review.md
│   └── diagrams/
│       ├── architecture-diagram.drawio / .png
│       ├── er-diagram.dbml / .png
│       ├── class-module-diagram.md
│       └── schema.sql
│
├── Problem_Statement.md
├── requirements.txt
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── LICENSE
└── README.md
```

---

## 13. Current Implementation Status

**Phase 1 — Design & Planning: Complete**
Problem Statement, Literature Review, Project Report, Architecture Diagram, ER Diagram, Class/Module Diagram, and database schema are all finalized and committed.

**Phase 2 — Core Development: In Progress**
- ✅ FastAPI application scaffolded with the standard layered structure (`api/core/models/schemas/services`)
- ✅ `/health` endpoint working
- ⬜ SQLAlchemy models (not yet implemented)
- ⬜ Storage Unit / Inventory / Temperature Log / Alert APIs (not yet implemented)
- ⬜ Authentication (not yet implemented)
- ⬜ React frontend (not yet scaffolded)

This section will be updated as each module is completed — nothing is listed as done here unless it is actually working and demoable.

---

## 14. Monitoring Workflow

```text
Simulated Sensor Reading
          |
          v
      FastAPI API
          |
          v
    Temperature Log
          |
          v
   Threshold Checking
          |
       +--+--+
       |     |
     Normal  Breach
       |     |
       v     v
  Dashboard Alert
             |
             v
       Operator Action
```

This workflow provides the foundation for future automated anomaly detection.

---

## 15. Inventory Workflow

```text
Add Inventory
      |
      v
Validate Inventory Data
      |
      v
Store Batch Information
      |
      v
Display Inventory Record
```

Inventory represents real stored batches and should maintain reliable historical information. The system should avoid unrestricted modification or deletion of records required for traceability.

---

## 16. Future Enhancements

- **AI-Based Anomaly Detection** — analyze recent readings for rate of change, repeated fluctuations, and gradual drift to flag an excursion before it happens (Phase 3)
- **Notification System** — Email / SMS / other channels
- **Compliance Reporting** — historical monitoring reports (storage unit, temperature history, safe range, excursion events, alert history, monitoring duration)
- **Audit Logging** — append-only trail of important administrative actions
- **Physical IoT Integration** — the simulated sensor API can later be replaced or extended with real sensors without changing the core architecture

---

## 17. Success Criteria

- Dashboard updates within 5 seconds of a new sensor reading
- Temperature excursions generate visible alerts within 1 minute
- Operators can acknowledge active alerts
- Temperature history is preserved and never silently modified
- Inventory records are maintained accurately
- Historical monitoring data cannot be casually modified or deleted
- Architecture supports future AI anomaly detection and physical IoT integration without redesign

---

## 18. Project Scope

**In Scope:** cold-storage monitoring, temperature/humidity monitoring, temperature history, excursion detection, alert generation, inventory management, dashboard visualization, simulated IoT sensor integration, future AI anomaly detection.

**Out of Scope:** physical IoT hardware integration, full transportation route tracking, payment or procurement management, native mobile application, pharmaceutical manufacturing management.

---

## 19. Development Approach

```text
Database & Backend Foundation
            |
            v
Storage Unit Management
            |
            v
Inventory Management
            |
            v
Temperature Monitoring
            |
            v
Alert Management
            |
            v
Frontend Dashboard
            |
            v
Historical Monitoring
            |
            v
AI-Based Anomaly Detection
            |
            v
Compliance & Audit Features
```

Each phase is implemented and tested before moving to the next stage.

---

## 20. Conclusion

ColdGuard provides a foundation for reliable pharmaceutical cold-storage monitoring by combining environmental monitoring, inventory management, alerting, and historical traceability in a single web-based system.

The current system establishes the core project design and initial backend scaffolding using React, FastAPI, and PostgreSQL. Future phases will extend the system with AI-based anomaly detection, compliance reporting, audit logging, notifications, and physical IoT integration.

---

**Author:** Rathi Sankari S
B.Tech – Artificial Intelligence & Data Science (AI & DS)
**Project:** ColdGuard – Cold Storage Inventory Monitoring System