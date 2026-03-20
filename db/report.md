# Mini-rapport — 3 requêtes SQL utiles

## Requête 1 — Dernières mesures de température

```sql
SELECT ts_utc, value, unit
FROM telemetry
WHERE device='pi01'
AND topic LIKE '%/sensors/temperature'
ORDER BY ts_utc DESC
LIMIT 20;

SELECT ts_utc, payload
FROM events
WHERE device='pi01'
AND topic LIKE '%/actuators/led%'
ORDER BY ts_utc DESC
LIMIT 20;

SELECT COUNT(*) AS total_mesures
FROM telemetry
WHERE device='pi01';