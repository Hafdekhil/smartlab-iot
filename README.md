# Ahuntsic SmartLab — Mini-système IoT supervisé

[Lien vers le dépôt GitHub](https://github.com/Hafdekhil/smartlab-iot01)

## 1. Présentation du projet

Ce projet réalise un mini-système IoT supervisé avec Raspberry Pi.  
Le système permet de :

- mesurer la température et l’humidité avec un capteur DHT22
- publier les données via MQTT
- superviser les données sur une application mobile
- commander une DEL à distance via MQTT
- enregistrer les mesures et événements dans MariaDB

Le flux complet est :

**Capteur DHT22** → **Publisher MQTT** → **Broker Mosquitto** → **Dashboard mobile / Subscriber LED / Logger MariaDB**

---

## 2. Architecture

### Schéma logique

```text
DHT22
  │
  ▼
publisher_sensor.py
  │
  ▼
Mosquitto MQTT Broker
  ├──► Application mobile IoT MQTT Panel
  ├──► subscriber_led.py
  └──► logger_mariadb.py
             │
             ▼
          MariaDB
```

---

## 3. Contrat MQTT

Cette section définit les règles de communication entre les différents composants du système via le broker MQTT.

### Liste complète des topics et rôles

Voici le tableau récapitulatif des publications (Publish) et des abonnements (Subscribe) pour chaque topic du projet :

| Topic MQTT | Publié par (Publisher) | Abonné par (Subscriber) | Description |
| :--- | :--- | :--- | :--- |
| `ahuntsic/aec-iot/b3/team01/pi01/status/online` | `publisher_sensor.py` | Application Mobile | État de connexion du Raspberry Pi (online/offline via LWT). |
| `ahuntsic/aec-iot/b3/team01/pi01/sensors/temperature` | `publisher_sensor.py` | `logger_mariadb.py`, App Mobile | Données complètes de température au format JSON. |
| `ahuntsic/aec-iot/b3/team01/pi01/sensors/temperature/value` | `publisher_sensor.py` | Application Mobile | Valeur brute de la température (float) pour affichage simple. |
| `ahuntsic/aec-iot/b3/team01/pi01/sensors/humidity` | `publisher_sensor.py` | `logger_mariadb.py`, App Mobile | Données complètes d'humidité au format JSON. |
| `ahuntsic/aec-iot/b3/team01/pi01/sensors/humidity/value` | `publisher_sensor.py` | Application Mobile | Valeur brute de l'humidité (float) pour affichage simple. |
| `ahuntsic/aec-iot/b3/team01/pi01/actuators/led/cmd` | Application Mobile | `subscriber_led.py` | Commande texte brute (`on` ou `off`) pour allumer ou éteindre la DEL. |
| `ahuntsic/aec-iot/b3/team01/pi01/actuators/led/state` | `subscriber_led.py` | `logger_mariadb.py`, App Mobile | État de confirmation de la DEL au format JSON après une commande. |

### Exemples de Payload JSON

Le système utilise des formats JSON standardisés pour l'enregistrement détaillé en base de données.

**1. Payload de capteur (Température / Humidité)**
Publié sur `.../sensors/temperature` ou `.../sensors/humidity` :
```json
{
  "device": "pi01",
  "sensor": "temperature",
  "value": 22.5,
  "unit": "C",
  "ts": "2026-03-20T20:24:34.123456+00:00"
}
```

**2. Payload d'état d'actionneur (DEL)**
Publié sur `.../actuators/led/state` après un changement d'état :
```json
{
  "device": "pi01",
  "actuator": "led",
  "state": "on",
  "ts": "2026-03-20T20:24:35.987654+00:00"
}
```

**3. Payload de commande brute (DEL)**
Publié sur `.../actuators/led/cmd` :
```text
on
```
