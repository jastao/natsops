import argparse
import asyncio
import logging
import nats
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pub.log"),
        logging.StreamHandler()
    ]
)

async def start_publisher():
  """
    Publishes data continuously on a particular subject.
  """

  parser = argparse.ArgumentParser()
  parser.add_argument('subject', default='hello', nargs='?')
  parser.add_argument('-s' '--servers', dest='servers', default="")
  args, unknown = parser.parse_known_args()

  logging.info("Starting publisher...")

  if len(unknown) > 0:
    data = unknown[0]

  async def error_cb(e):
    logging.error("Error:", e)

  async def reconnected_cb():
    logging.info(f"Reconnected to NATS server: {args.servers}")

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
    logging.error(f"Failed to connect to the NATS server: {ex}")
    sys.exit(1)

  for counter in range(1, 60):
    message = "".join(["[", str(time.perf_counter()), "]", " Current counter is ", str(counter)])
    logging.info(f"Published [{args.subject}] = {message}")
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