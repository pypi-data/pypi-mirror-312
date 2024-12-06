# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script]
import asyncio
from fr24.json import find
import httpx

async def main() -> None:  # (1)!
    async with httpx.AsyncClient() as client:
        list_ = await find(client, "Toulouse")  # (2)!
        print(list_)

if __name__ == "__main__":
    asyncio.run(main())  # (3)!
# --8<-- [end:script]
# %%
# --8<-- [start:jupyter]
from fr24.json import find
import httpx

async def main() -> None: # (1)!
    async with httpx.AsyncClient() as client:
        list_ = await find(client, "Toulouse") # (2)!
        print(list_)

await main()
# --8<-- [end:jupyter]
# %%
# --8<-- [start:output]
{
    "results": [
        {
            "id": "TLS",
            "label": "Toulouse Blagnac Airport (TLS / LFBO)",
            "detail": {"lat": 43.628101, "lon": 1.367263, "size": 33922},
            "type": "airport",
            "match": "begins",
        },
        # ...
    ]
}
# --8<-- [end:output]
#%%
#%%
# --8<-- [start:login]
from fr24.core import FR24

async def main() -> None:
    async with FR24() as fr24:
        # anonymous now
        await fr24.login() # reads from environment or configuration file, or,
        await fr24.login(creds={"username": "...", "password": "..."}) # or,
        await fr24.login(creds={"subscriptionKey": "...", "token": "..."})
# --8<-- [end:login]
#%%
# --8<-- [start:client-sharing]
import httpx

from fr24.core import FR24

client = httpx.AsyncClient(http1=False, http2=True, transport=httpx.AsyncHTTPTransport(retries=5))

async def main() -> None:
    async with FR24(client) as fr24:
        ...
# --8<-- [end:client-sharing]
# %%
