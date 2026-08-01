# Literature Review — ColdGuard – Real-Time Cold Storage Inventory Monitoring System

## Purpose

This review establishes the evidence base for the requirements in this project's SRS (`Project_Report.md`). Every requirement tracing back to a real-world problem should be traceable to a cited source here, not to an unverified claim.

## 1. Vaccine Temperature Requirements

The 2–8°C storage range used throughout this project is not an assumption — it is the standard maintained across regulatory and public health bodies. The CDC's Vaccine Storage and Handling guidance states that vaccines licensed for refrigerator storage must be kept at 2°C–8°C (36°F–46°F), and that liquid vaccines containing an aluminum adjuvant permanently lose potency if they freeze — meaning a *below*-range excursion can be just as damaging as an *above*-range one, not only overheating. A peer-reviewed review of cold chain management technology confirms the same FDA-approved 2–8°C range for viral vaccines, while noting some vaccine types (e.g., certain live-attenuated and mRNA formulations) require deep-frozen ranges as low as −90°C to −60°C.

**Software requirement this supports:** per-storage-unit configurable temperature categories (not a single hardcoded safe range) — directly reflected in `StorageUnit.temperature_category`, `min_temp`, `max_temp` in the schema.

## 2. Vaccine Wastage Due to Cold Chain Failures

Industry cold-chain guidance citing WHO data places global vaccine wastage from inadequate cold chain logistics as high as 50%, while other industry summaries put temperature-mishandling-related spoilage specifically closer to 35%. These figures come from secondary industry sources rather than a single WHO publication I was able to verify directly, so the honest position for this project is: **wastage estimates in published sources range roughly from 25% to 50% depending on region and methodology** — a wide but consistently large figure, not a single precise statistic. This project's documentation should state the range, not overclaim precision with one exact number.

**Software requirement this supports:** the entire premise of continuous monitoring over periodic manual checks — even the low end of this range represents a large, addressable loss.

## 3. Continuous Monitoring vs. Manual Checks

Multiple sources converge on the same operational finding: WHO guidance calls for continuous temperature monitoring at every level of the supply chain, and industry cold-chain literature notes that manual, periodic checks create dangerous monitoring gaps — an equipment failure or power outage between two scheduled checks can compromise an entire vaccine stock without anyone noticing until the next inspection. Digital data loggers with automated alerting are specifically recommended as the fix, providing the continuous, tamper-resistant records that manual logs cannot.

**Software requirement this supports:** this is the direct justification for FR4/FR5/FR10 in the SRS — continuous ingestion, automatic threshold evaluation, and immutable (insert-only) logging.

## 4. Sea Freight as an Emerging Cold Chain Innovation

UNICEF's own Supply Division reports that shipping vaccines by sea, rather than the traditionally-used air freight, can reduce shipping costs by roughly 50% on average and cut greenhouse gas emissions by up to 90%, depending on origin, destination, and volume. UNICEF carried out its first maritime vaccine shipment in 2025 — pneumococcal conjugate vaccines traveling from Belgium to Côte d'Ivoire, departing June 4 and arriving July 10, 2025, carrying over 500,000 doses. This confirms and slightly refines earlier informal research used in this project: the pilot did occur in June–July 2025 as understood, with UNICEF's own figures matching the 50% cost / 90% emissions reduction previously cited.

**Relevance to this project:** this finding is informative context for the *transport* leg of the cold chain, which is explicitly **out of scope** for ColdGuard (this system monitors storage, not transit) — included here for completeness and to correctly attribute the statistic, not because it drives a software requirement in this version.

## 5. Research Gap and Positioning of This Project

The reviewed literature is strong on *why* cold chain failures happen (manual monitoring, lack of continuous tracking, no predictive capability) but focuses mainly on hardware/logistics improvements (better refrigeration units, sea freight, data loggers). It is comparatively thin on **integrated software platforms that combine continuous monitoring, inventory tracking, and predictive trend analysis in one system with a tamper-proof audit trail** — which is precisely the gap ColdGuard is built to address at the storage-unit level.

## Sources

1. CDC — *Storage and Handling of Immunobiologics*, cdc.gov (primary)
2. UNICEF Supply Division — *Shipping vaccines by sea*, unicef.org (primary)
3. UNICEF Supply Division — *What is a cold chain?*, unicef.org (primary)
4. UNICEF USA — *Sustainable Solutions: UNICEF Pioneers Vaccine Delivery by Sea* (primary/affiliate)
5. Peer-reviewed review — *Vaccine cold chain management and cold storage technology to address the challenges of vaccination programs*, PMC (peer-reviewed)
6. Scoping review — *How the use of vaccines outside the cold chain or in controlled temperature chain contributes to improving immunization coverage in LMICs*, PMC (peer-reviewed)
7. Industry cold-chain guidance summarizing WHO/CDC storage standards (secondary — used only for corroboration, not as sole source of any figure)

## Note on citation discipline going forward

Per the project's evidence standard: any new statistic added to future documentation should be traced to a primary source (WHO, CDC, UNICEF, peer-reviewed literature) before being written into the SRS or Project Report. Where only secondary/industry sources are available, the documentation should state a range and flag the uncertainty explicitly, as done in Section 2 above, rather than presenting a single number as precise fact.
