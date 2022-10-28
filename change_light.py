from asyncio import run
from dohome import DoHomeLight

async def main():
    light = DoHomeLight('7b5b', '192.168.31.225')
    await light.connect()
    # print(await light.get_color())
    # await light.turn_off()
    await light.set_rgb(0, 255, 0)

if __name__ == '__main__':
    run(main())