import time

name = "test"

async def run(client, message, args):
    start_time = time.perf_counter()
    await message.channel.send("supe,r,... creek,.,. ")
    end_time = time.perf_counter()
    ping = (end_time - start_time) * 1000
    await message.channel.send(f"Latency: {int(ping)}ms")
