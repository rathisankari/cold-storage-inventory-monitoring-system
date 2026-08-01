# ColdGuard – Real-Time Cold Storage Inventory Monitoring System
### Enterprise Capstone Project Report

---

## 1. Introduction

Vaccines and temperature-sensitive medicines are among the most fragile products in any supply chain — their effectiveness depends entirely on being kept within a strict temperature range from the moment they are manufactured until the moment they are administered to a patient. This continuous chain of controlled-temperature handling is known as the **cold chain**.

**ColdGuard** is a full-stack, real-time monitoring platform built to address a specific, well-documented failure point in this chain: the **storage stage**, where medicines sit in refrigerators and freezers at warehouses and healthcare facilities before distribution. The system continuously tracks the temperature of every monitored storage unit, manages the medicine inventory held within them, alerts responsible staff the moment conditions become unsafe, and — as an AI-driven enhancement — predicts temperature failures before they happen.

This project is built as a Semester-5 Enterprise Capstone Project, following a 60-day full-stack development lifecycle, covering the complete Software Development Life Cycle from problem identification through design, development, testing, deployment, and enhancement. Deployment stack: React frontend on Vercel, FastAPI backend on Render, PostgreSQL on a managed cloud provider (Railway/Neon).

## 2. Problem Statement

Cold storage facilities responsible for vaccines and temperature-sensitive medicines lack a continuous, automated, and trustworthy way to monitor storage conditions — resulting in delayed detection of temperature failures, silent spoilage that cannot be identified visually, unreliable record-keeping, and no ability to predict a failure before it occurs.

Published cold-chain literature places annual vaccine spoilage due to undetected temperature excursions in a wide range — roughly 25-50% depending on region and source (see `Literature_Review.md` for the full citation trail and honest discussion of this range) — a loss that is invisible until lab testing occurs, or until a spoiled dose has already been administered to a patient who is then wrongly assumed to be protected.

## 3. Existing System

Today, most cold storage facilities rely on manual, periodic temperature checks:
- A staff member physically inspects and records the temperature reading of each unit, typically once every few hours.
- Records are often kept in handwritten logs or editable spreadsheets.
- Alerts, when they exist at all, depend entirely on a human noticing a problem during a scheduled inspection.
- There is no system-wide dashboard showing the live status of every storage unit at once.
- Compliance reporting, where required, is compiled manually from these same handwritten or spreadsheet records.

## 4. Problems in Existing System

**Problem 1 — Manual Temperature Monitoring**
Staff check storage temperature only once every few hours. If a refrigerator fails immediately after an inspection, the temperature can remain outside the safe range for hours before anyone notices — resulting in unusable vaccines, wasted expensive medicines, financial losses, and compromised patient safety.

**Problem 2 — Spoiled Medicines Cannot Be Identified Visually**
A vaccine exposed to unsafe temperatures looks completely normal. Healthcare staff cannot tell by inspection whether a dose is still effective, increasing the risk of administering an ineffective vaccine to a patient.

**Problem 3 — Lack of Continuous Monitoring**
Existing systems record only a handful of readings per day. Temporary temperature spikes go unnoticed, and organizations cannot determine exactly when a failure occurred.

**Problem 4 — No Reliable Audit Trail**
Handwritten logs and editable spreadsheets can be modified, deleted, or contain simple human error, and cannot always be trusted during regulatory inspection.

**Problem 5 — Delayed Alerts**
Staff only become aware of a problem at the next scheduled inspection — by which point medicines may already be spoiled and the damage is irreversible.

**Problem 6 — Lack of Predictive Monitoring**
Traditional systems only detect a failure after it has already happened. They cannot identify early warning signs, such as a gradually rising temperature, that would allow preventive action.

### Impact of the Existing Problems
- Vaccine spoilage and reduced vaccine effectiveness
- Direct financial losses and increased operational costs
- Regulatory compliance failures
- Loss of public trust
- Increased health risk to patients
- Poor inventory visibility and management

## 5. Proposed System

ColdGuard replaces manual inspection with continuous, automated monitoring. Temperature data is received through a simulated IoT sensor API during development, allowing future integration with physical IoT devices without architectural changes. Whenever a reading crosses a safe threshold, the system immediately notifies responsible personnel via email/SMS. Every reading and every alert is stored permanently and cannot be edited or deleted, creating a trustworthy audit trail for compliance purposes. The system is built in three phases: Phase 1 delivers real-time monitoring and alerting; Phase 2 adds inventory management and compliance reporting; Phase 3 (Day 41-60) adds AI-driven trend analysis to flag a unit drifting toward a breach before it happens — enabling preventive action instead of reactive damage control. AI prediction is explicitly a later-phase capability, not part of the initial working system.

The system also manages medicine inventory held within each storage unit — tracking batch numbers, quantities, and expiry dates — directly addressing the "Inventory" component of the system's own name and scope.

## 6. Objectives

1. Replace manual, periodic temperature checks with continuous, automated monitoring.
2. Detect and alert on unsafe storage conditions immediately, not at the next scheduled inspection.
3. Maintain a tamper-proof, permanent record of every temperature reading and alert for compliance purposes.
4. Provide visibility into medicine inventory held within each storage unit, including expiry tracking.
5. Predict temperature failures before they occur, using trend analysis of recent readings.
6. Provide role-based dashboards so operators and administrators each see the information relevant to their responsibilities.

## 7. Scope

**In Scope**
- Real-time temperature monitoring per storage unit, with configurable safe-range thresholds
- Medicine inventory management (batch, quantity, expiry) linked to storage units
- Automatic email/SMS alerting on threshold breach
- AI-based trend detection for early warning (Phase 3 enhancement)
- Tamper-proof logging of all temperature readings and alerts (insert-only, no edit/delete API)
- Compliance report generation and storage
- Role-based access for Administrator and Storage Operator
- Cloud deployment with a live, publicly accessible URL

**Out of Scope**
- Integration with actual physical IoT sensor hardware (a simulator is used to mimic realistic sensor behavior)
- Full multi-leg transport/route tracking across the entire supply chain (this system monitors storage, not transit)
- Payment or procurement functionality
- Native mobile application (web-responsive only)
- The Auditor role (explicitly deferred as a future enhancement, not built in this version)

## 8. User Roles

**8.1 Administrator**
Has complete control over the system.
- Create and manage user accounts
- Manage storage units and configure temperature thresholds
- Monitor all storage facilities and view system-wide dashboards
- Manage inventory
- Generate and view compliance reports
- View alert history and configure notification settings

**8.2 Storage Operator**
Responsible for day-to-day monitoring.
- View assigned storage units and live temperatures
- View inventory within assigned units
- Receive and acknowledge alerts
- Report issues and monitor system status

**8.3 Auditor (Future Role — not built in this version)**
Would be responsible for regulatory inspection: viewing audit logs, generating compliance reports, and verifying storage history. Deferred to a future enhancement.

## 9. Functional Requirements

- FR1: Users authenticate via secure, role-based login (JWT-based)
- FR2: Administrators can create, edit, and deactivate user accounts, assigning roles
- FR3: Administrators can add and configure storage units, including their safe temperature range
- FR4: The system records incoming temperature readings continuously via API
- FR5: The system evaluates every new reading against its unit's configured threshold and generates an alert on breach
- FR6: Alerts are delivered to responsible personnel via email (SMS as a bonus integration)
- FR7: Operators and Administrators can view live temperature status and historical trend charts per unit
- FR8: Administrators can manage inventory (add/update/remove medicine batches) linked to a storage unit, including expiry dates
- FR9: Administrators can generate and export compliance reports covering a unit's full temperature/alert history
- FR10: No API endpoint permits editing or deleting a temperature reading or alert record once created

## 10. Non-Functional Requirements

- NFR1 (Security): Role-based access control enforced server-side; passwords hashed (bcrypt); no secrets committed to source control
- NFR2 (Performance): Dashboard queries return in under 2 seconds for a facility with hundreds of storage units
- NFR3 (Reliability): A threshold breach triggers a visible alert and notification within 1 minute
- NFR4 (Data Integrity / Auditability): Temperature and alert records are immutable once written — enforced at both the API and database permission level
- NFR5 (Scalability): Data model supports multiple facilities and storage units without redesign
- NFR6 (Maintainability): Layered architecture (API / service / data) with the anomaly-detection logic isolated behind a service interface, allowing the rule-based v1 to be upgraded to a trained model without touching the rest of the system
- NFR7 (Availability): Deployed on a live public URL, accessible for evaluation at any time

## 11. Functional Modules

| Module | Purpose | Key Functions |
|---|---|---|
| 1. Authentication | Secure login for all users | Login, Logout, JWT Auth, Role-Based Access Control |
| 2. User Management | Manage system users | Add / Edit / Delete User, Assign Roles |
| 3. Storage Unit Management | Manage refrigerators/freezers | Add / Update Storage Unit, Configure Temperature Range, View Status |
| 4. Inventory Management | Maintain vaccine/medicine inventory | Add / Update / Remove Inventory, View Stock, Track Expiry |
| 5. Temperature Monitoring | Collect and store readings continuously | Receive Sensor Data, Record Temperature, View Live Temperature, View History |
| 6. Alert Management | Notify users during abnormal conditions | Detect Breach, Generate Alert, Send Email/SMS, Store Alert History |
| 7. Dashboard | Graphical system status | Current Temperature, Active Alerts, Inventory Status, Trend Charts |
| 8. Compliance Reporting | Generate regulatory reports | Temperature History, Alert Reports, Compliance Certificates |
| 9. AI Anomaly Detection *(Phase 3 enhancement)* | Predict future temperature failures | Analyze Trends, Predict Failures, Generate Early Warnings |

## 12. Database Entities

1. **User** — id, name, email, password_hash, phone_number, role, status, created_at
2. **StorageUnit** — id, name, facility_location, temperature_category, min_temp, max_temp, current_status, last_synced_at
3. **Inventory** — id, medicine_name, batch_number, quantity, expiry_date, storage_unit_id (FK)
4. **TemperatureLog** — id, storage_unit_id (FK), temperature, sensor_status, timestamp *(insert-only)*
5. **Alert** — id, storage_unit_id (FK), temperature, alert_type, alert_status, alert_time *(insert-only)*
6. **ComplianceReport** — id, report_type, generated_by (FK → User), file_location, generated_date
7. **AuditLog** — id, user_id (FK), action, entity_type, entity_id, created_at *(append-only, covers admin actions)*

**Key relationships:** StorageUnit → Inventory (1:N) · StorageUnit → TemperatureLog (1:N) · StorageUnit → Alert (1:N) · User → ComplianceReport (1:N) · User → AuditLog (1:N)

Full schema with constraints: `docs/diagrams/schema.sql`. Visual ERD source: `docs/diagrams/er-diagram.dbml`.

## 13. Expected Outcomes

- Reduced vaccine and medicine spoilage through continuous, automated monitoring
- Faster response to unsafe storage conditions — alerts within minutes, not at the next scheduled inspection
- A reliable, tamper-proof audit trail supporting regulatory compliance
- Improved inventory visibility, including proactive expiry tracking
- Early warning of temperature failures before they occur, enabling preventive rather than reactive action
- Reduced manual monitoring effort and operational cost
- Improved patient safety through higher confidence in vaccine/medicine integrity at the point of use
