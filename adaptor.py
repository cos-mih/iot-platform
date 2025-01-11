import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json
import datetime

subscribed_topic = '#'
broker = 'broker'

db_name = 'io_data'
db_client = InfluxDBClient(host='db', port=8086, database=db_name)

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(subscribed_topic)

def on_message(client, userdata, msg):
    global db_client
    location = msg.topic.split('/')[0]
    station = msg.topic.split('/')[1]
    json_data = json.loads(msg.payload)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_ts = 'NOW'
    if 'timestamp' in json_data:
        iso_timestamp = datetime.datetime.fromisoformat(json_data['timestamp'])
        timestamp = iso_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        log_ts = json_data['timestamp']

    print(f'\n{timestamp} Received a message by topic [{msg.topic}]')
    print(f'{timestamp} Data timestamp is: {log_ts}')

    for parameter, value in json_data.items():
        if isinstance(value, (int, float)):
            series = '.'.join([location, station, parameter])
            json_body = [
                {
                    'measurement': series,
                    'tags': {
                        'location': location,
                        'station': station,
                        'parameter': parameter
                    },
                    'fields': {
                        'value': value
                    },
                    'time': timestamp
                }
            ]
            db_client.write_points(json_body)

            print(f'{timestamp} {series} {value}')



if __name__=='__main__':
    db_client.create_database(db_name)
    db_client.create_retention_policy(name='forever_policy', database=db_name, duration='INF', default=True, replication=2)

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(broker, 1883, 60)
    mqttc.loop_forever()
