import argparse
import asyncio
import nats
import sys

async def start_publisher():
  """
    Publishes data continuously on a particular subject.
  """

  parser = argparse.ArgumentParser()
  parser.add_argument('subject', default='hello', nargs='?')
  parser.add_argument('-s' '--servers', dest='servers', default="")
  args, unknown = parser.parse_known_args()

  if len(unknown) > 0:
    data = unknown[0]

  async def error_cb(e):
    print("Error:", e)

  async def reconnected_cb():
    print(f"Reconnected to NATS server: {args.servers}")

  options = {
    "error_cb": error_cb,
    "reconnected_cb": reconnected_cb
  }
    
  nats_connection = None
  
  try:
    if len(args.servers) > 0:
      options['servers'] = args.servers
      
    nats_connection = await nats.connect(**options)
  except Exception as ex:
    print(f"Failed to connect to the NATS server: {ex}")
    sys.exit(1)

  for counter in range(1, 60):
    message = "".join(("Current counter is ", str(counter)))
    print(f"Published [{args.subject}] = {message}")
    await nats_connection.publish(args.subject, message.encode())
    await asyncio.sleep(1)
  
  # Requests feedback from the server to indicate the message was published and received by the NATS server
  await nats_connection.flush()
  
  # Publishes any remaining messages before connection closes
  await nats_connection.drain()
  
if __name__ == '__main__':
  
  loop = asyncio.new_event_loop()
  
  try:
    loop.run_until_complete(start_publisher())
  finally:
    loop.close()