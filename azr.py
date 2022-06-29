import os
import asyncio
import json
import smbus
from time import sleep
from azure.iot.device.aio import IoTHubDeviceClient

data = {
  "message" : "hello",
  "value" : 123.0
  }

bus = smbus.SMBus(1)

async def main():
    print(json.dumps(data))
    # Fetch the connection string from an environment variable
    conn_str = os.getenv("IOTHUB")

    # Create instance of the device client using the connection string
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str, websockets=True)

    # Connect the device client.
    await device_client.connect()

    while True:
       block = bus.read_i2c_block_data(0x2d, 0x00,1)
    # Send a single message
       print("Sending message...")

       data['value'] = block[0]
       await device_client.send_message(json.dumps(data))
       print("Message successfully sent!")
       sleep(5)

    # Finally, shut down the client
    await device_client.shutdown()

if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
