# Ahuntsic SmartLab — Mini-système IoT supervisé

## 1. Présentation du projet

Ce projet réalise un mini-système IoT supervisé avec Raspberry Pi.  
Le système permet de :

- mesurer la température et l’humidité avec un capteur DHT22
- publier les données via MQTT
- superviser les données sur une application mobile
- commander une DEL à distance via MQTT
- enregistrer les mesures et événements dans MariaDB

Le flux complet est :

Capteur DHT22 → Publisher MQTT → Broker Mosquitto → Dashboard mobile / Subscriber LED / Logger MariaDB

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
