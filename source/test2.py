import mqtt_handler
import time
def image_to_byte(image_path):
    with open(image_path, 'rb') as image_file:
        return image_file.read()

_mqtt_sender = mqtt_handler.mqtt_send(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc1")

byte_data = image_to_byte("/home/sks/Desktop/camera_module/image/raspi_module_pin_map.png")
print(_mqtt_sender.TOPIC)
for i in range(5) :
    print(f"발행 {i}")

    _mqtt_sender.client.loop_start()
    _mqtt_sender.client.publish(_mqtt_sender.TOPIC, byte_data)
    _mqtt_sender.client.loop_stop()
    time.sleep(5)
