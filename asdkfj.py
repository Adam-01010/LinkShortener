import asyncio


async def boil_water():
    print("Ставим воду на плиту...")
    await asyncio.sleep(3)  # Имитация времени, необходимого для закипания воды
    print("Вода закипела!")
async def chop_vegetables():
    print("Режем овощи для салата...")
    await asyncio.sleep(2)  # Имитация времени на нарезку
    print("Овощи нарезаны!")

async def fry_chicken():
    print("Жарим курицу на сковороде...")
    await asyncio.sleep(4)  # Имитация времени на жарку
    print("Курица готова!")

async def main():
    await boil_water()
    await chop_vegetables()
    await fry_chicken()

asyncio.run(main())