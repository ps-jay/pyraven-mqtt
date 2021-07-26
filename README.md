# RFA RAVEn -> MQTT

## Build

```
export DOCKER_BUILDKIT=1
docker build -t pyrmqtt .
```

## Run

```
docker run \
    --detach \
    --tty \
    --restart=always \
    --name=pyrmqtt \
    --device="$(readlink -f /dev/serial/by-id/usb-Rainforest_RFA-Z106-RA-PC_RAVEn_v2.3.21-if00-port0):/serial" \
    pyrmqtt \
        --host "${MQTT_BROKER}" \
        --device /serial
```
