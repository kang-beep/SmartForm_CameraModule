import serv_mqtt_handler

serv_mqtt_send = serv_mqtt_handler.mqtt_send(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc1")
serv_mqtt_send.send_message("camera_start")