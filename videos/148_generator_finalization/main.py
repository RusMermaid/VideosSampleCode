import asyncio
import contextlib


class Resource:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"cleanup: {self.name}")


async def gen():
    with Resource("database/lock/file/etc"):
        for x in range(3):
            print(f"yield {x}")
            try:
                yield x
            except BaseException as exc:
                print("got exc: ", type(exc).__name__)
                raise


async def main():
    with Resource("outer resource"):
        async with contextlib.aclosing(gen()) as g:
            async for x in g:
                print(f"got {x}")
                if x == 1:
                    break
        print("after loop")


class AsyncGenerator:
    async def __aiterclose__(self):
        await self.aclose()


class Generator:
    def __iterclose__(self):
        self.close()


def breaking_change():
    with my_open("test.txt") as lines:
        # process header lines
        for f in lines:
            ...
            if True:  # header done
                break

        # process the rest
        for f in lines:
            ...


if __name__ == "__main__":
    asyncio.run(main())
