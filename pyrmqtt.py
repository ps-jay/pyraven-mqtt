"""
Transfers data from a Rainforest Automation RAVEn USB stick to an MQTT topic
"""

import argparse
import json
import time

import paho.mqtt.client as mqtt  # pip install paho-mqtt
import raven  # pip install pyraven

BACKOFF=60

def main():
    """
    main(): does all the things: parse args, connect to the RAVEn, connect to MQTT, and transfer data
    """

    parser = argparse.ArgumentParser(prog="pyrmqtt",)

    parser.add_argument('--device', '-d',
                        help="Device path (serial port) of the USB stick [%(default)s]",
                        default='/dev/ttyUSB0')

    parser.add_argument('--host', '-H', required=True,
                        help='Hostname of the MQTT broker to publish to')

    parser.add_argument('--port', '-P',
                        help="Port number of the MQTT broker to publish to [%(default)s]",
                        default='1883')

    parser.add_argument('--username', '-u',
                        help="MQTT Username")

    parser.add_argument('--password', '-p',
                        help="MQTT Password")

    parser.add_argument('--topic', '-T',
                        help="Topic name to publish to [%(default)s]",
                        default='raven')

    args = parser.parse_args()

    # connect to the USB device
    raven_usb = raven.raven.Raven(args.device)

    # init a MQTT client
    client = mqtt.Client()
    connected = False

    client.username_pw_set(username=args.username,password=args.password)

    while True:
        payload = json.dumps(raven_usb.long_poll_result())

        if not connected:
            try:
                client.connect(args.host, int(args.port))
                connected = True
            except Exception as err:  # pylint: disable=broad-except
                print(f"Connection failed: error={err}; backoff={BACKOFF}")
                time.sleep(BACKOFF)

        code, mid = client.publish(args.topic, payload)
        if code == 0:
            print(f"Published: message_id={mid}; payload={payload}")
        else:
            print(f"Failed: code={code}; message_id={mid}")
            connected = False

if __name__ == "__main__":
    main()
