USE smartlab;

SELECT id, device, topic, value, unit, ts_utc
FROM telemetry
ORDER BY id DESC
LIMIT 10;

SELECT id, device, topic, payload, ts_utc
FROM events
ORDER BY id DESC
LIMIT 10;
