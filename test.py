import asyncio
async def A():
    print("A1")
    await asyncio.sleep(0)
    print("A2")

async def B():
    print("B1")
    await asyncio.sleep(0)
    print("B2")

async def main():
    t1 = asyncio.create_task(A())
    t2 = asyncio.create_task(B())

    print("Main")

    # await t1
    # print("hiii")
    # await t2
    
asyncio.run(main())
#main,