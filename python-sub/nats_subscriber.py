import argparse
import asyncio
import signal
import nats
import sys

async def start_subscriber():
  """
    Subscribes data from a particular subject.
  """

  parser = argparse.ArgumentParser()
  parser.add_argument('subject', default='hello', nargs='?')
  parser.add_argument('-s' '--servers', dest='servers', default="")
  parser.add_argument('-q', '--queue', default="")
  args = parser.parse_args()
  
  async def error_cb(e):
    print("Error:", e)

  async def closed_cb():
      # Wait for tasks to stop otherwise get a warning.
      await asyncio.sleep(0.2)
      loop.stop()

  async def reconnected_cb():
    print(f"Reconnected to NATS server: {args.servers}")
    
  async def subscribe_handler(message):

      subject = message.subject
      reply   = message.reply
      data    = message.data.decode()
      
      print(
          "Received a message on '{subject} {reply}': {data}".format(
              subject=subject, reply=reply, data=data
          )
      )
  options = {
      "error_cb": error_cb,
      "closed_cb": closed_cb,
      "reconnected_cb": reconnected_cb
  }
    
  nats_connection = None
  
  try:
      if len(args.servers) > 0:
          options['servers'] = args.servers
      
      nats_connection = await nats.connect(**options)
  except Exception as ex:
    print(f"Failed to connect to the NATS server: {ex}")
    loop.close()
  
  print(f"Listening on [{args.subject}]")
  
  def raise_graceful_exit():
    loop.stop()
    sys.exit(1)
  
  def signal_handler():
      if nats_connection.is_closed:
          return
      asyncio.create_task(nats_connection.drain())
    
      signal.signal(signal.SIGINT, raise_graceful_exit)
      signal.signal(signal.SIGTERM, raise_graceful_exit)
      
  await nats_connection.subscribe(args.subject, args.queue, subscribe_handler)
    
if __name__ == '__main__':
  
  loop = asyncio.new_event_loop()
  loop.run_until_complete(start_subscriber())
  
  try:
    loop.run_forever()
  finally:
    loop.close()