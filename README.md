# RFA RAVEn -> MQTT

## Build

```shell
export DOCKER_BUILDKIT=1
docker build -t pyrmqtt .
```

## Run

```shell
docker run \
    --detach \
    --tty \
    --restart=always \
    --name=pyrmqtt \
    --username=username \
    --password=password \
    --device="$(readlink -f /dev/serial/by-id/usb-Rainforest_RFA-Z106-RA-PC_RAVEn_v2.3.21-if00-port0):/serial" \
    pyrmqtt \
        --host "${MQTT_BROKER}" \
        --device /serial
```
## Docker-compose

Please see docker-compose.yaml


## Ingest into Home Assistant

Add a sensor to `configuration.yaml`:

```yaml
sensor Meter:
  - platform: mqtt
    state_topic: "raven"
    name: "Current Demand"
    unit_of_measurement: 'kW'
    icon: mdi:flash
    value_template: >-
      {% if "demand" in value_json %}
        {{ value_json.demand }}
      {% else %}
        {% if states('sensor.current_demand') != "unknown" %}
            {{ states('sensor.current_demand') }}
          {% else %}
             0
          {% endif %}
      {% endif %}
  - platform: mqtt
    state_topic: "raven"
    name: "Total Import"
    unit_of_measurement: 'kWh'
    icon: mdi:flash
    value_template: >-
      {% if "summation_delivered" in value_json %}
        {{ value_json.summation_delivered }}
      {% else %}
        {% if states('sensor.total_import') != "unknown" %}
            {{ states('sensor.total_import') }}
          {% else %}
             0
          {% endif %}
      {% endif %}
  - platform: mqtt
    state_topic: "raven"
    name: "Total Export"
    unit_of_measurement: 'kWh'
    icon: mdi:flash
    value_template: >-
      {% if "summation_received" in value_json %}
        {{ value_json.summation_received }}
      {% else %}
        {% if states('sensor.total_export') != "unknown" %}
            {{ states('sensor.total_export') }}
          {% else %}
             0
          {% endif %}
      {% endif %}
```
