# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
#%%
# --8<-- [start:script0]
from fr24.core import FR24

async def my_list() -> None:
    async with FR24() as fr24:
        response = await fr24.flight_list.fetch(reg="B-HPB")
        data = response.to_arrow()
        print(data.df)
        data.save()

await my_list()
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:df0]
   flight_id  number callsign   icao24 registration typecode origin destination        status                STOD ETOD                ATOD                STOA ETOA                ATOA  
0  882269295   CX982   CPA982  7901768        B-HPB     A21N   None        None     Scheduled                 NaT  NaT                 NaT                 NaT  NaT                 NaT  
1  882279849   CX983   CPA983  7901768        B-HPB     A21N   ZGGG        VHHH  Landed 12:28 2024-04-01 02:15:00  NaT 2024-04-01 03:45:26 2024-04-01 03:45:00  NaT 2024-04-01 04:28:37  
2  882263077   CX982   CPA982  7901768        B-HPB     A21N   VHHH        ZGGG  Landed 10:02 2024-03-31 23:50:00  NaT 2024-04-01 01:30:05 2024-04-01 00:55:00  NaT 2024-04-01 02:02:58  
3  882098982   CX439   CPA439  7901768        B-HPB     A21N   RKSI        VHHH  Landed 17:02 2024-03-31 04:35:00  NaT 2024-03-31 05:28:02 2024-03-31 08:25:00  NaT 2024-03-31 09:02:19  
4  882069433  CX2410  CPA2410  7901768        B-HPB     A21N   VHHH        RKSI  Landed 12:49 2024-03-30 23:55:00  NaT 2024-03-31 00:51:40 2024-03-31 03:35:00  NaT 2024-03-31 03:49:22  
5  881837333   CX976   CPA976  7901768        B-HPB     A21N   RPLL        VHHH  Landed 07:30 2024-03-29 21:45:00  NaT 2024-03-29 21:46:49 2024-03-30 00:05:00  NaT 2024-03-29 23:30:12  
6  881725491   CX913   CPA913  7901768        B-HPB     A21N   VHHH        RPLL  Landed 22:24 2024-03-29 12:20:00  NaT 2024-03-29 12:42:42 2024-03-29 14:35:00  NaT 2024-03-29 14:24:57  
7  881693238   CX674   CPA674  7901768        B-HPB     A21N   VTBS        VHHH  Landed 18:58 2024-03-29 08:05:00  NaT 2024-03-29 08:52:54 2024-03-29 10:55:00  NaT 2024-03-29 10:58:14  
8  881665708   CX653   CPA653  7901768        B-HPB     A21N   VHHH        VTBS  Landed 14:26 2024-03-29 04:00:00  NaT 2024-03-29 04:35:36 2024-03-29 07:05:00  NaT 2024-03-29 07:26:51  
9  881605496   CX976   CPA976  7901768        B-HPB     A21N   RPLL        VHHH  Landed 07:30 2024-03-28 21:45:00  NaT 2024-03-28 21:46:18 2024-03-29 00:05:00  NaT 2024-03-28 23:30:58  
# --8<-- [end:df0]
"""
# %%
# --8<-- [start:script1]
from fr24.core import FR24

async def my_full_list() -> None:
    async with FR24() as fr24:
        data = fr24.flight_list.load(reg="B-HPB")  # (1)!
        async for response in fr24.flight_list.fetch_all(reg="B-HPB"):
            data_new = response.to_arrow()
            data.concat(data_new, inplace=True)  # (2)!
            if input() == "x":
                break
            data.save()
        print(data.df)

await my_full_list()
# --8<-- [end:script1]
#%%
"""
# --8<-- [start:df1]
    flight_id  number callsign   icao24 registration typecode origin destination        status                STOD ETOD                ATOD                STOA ETOA                ATOA  
0   882269295   CX982   CPA982  7901768        B-HPB     A21N   None        None     Scheduled                 NaT  NaT                 NaT                 NaT  NaT                 NaT  
1   882279849   CX983   CPA983  7901768        B-HPB     A21N   ZGGG        VHHH  Landed 12:28 2024-04-01 02:15:00  NaT 2024-04-01 03:45:26 2024-04-01 03:45:00  NaT 2024-04-01 04:28:37  
2   882263077   CX982   CPA982  7901768        B-HPB     A21N   VHHH        ZGGG  Landed 10:02 2024-03-31 23:50:00  NaT 2024-04-01 01:30:05 2024-04-01 00:55:00  NaT 2024-04-01 02:02:58  
3   882098982   CX439   CPA439  7901768        B-HPB     A21N   RKSI        VHHH  Landed 17:02 2024-03-31 04:35:00  NaT 2024-03-31 05:28:02 2024-03-31 08:25:00  NaT 2024-03-31 09:02:19  
4   882069433  CX2410  CPA2410  7901768        B-HPB     A21N   VHHH        RKSI  Landed 12:49 2024-03-30 23:55:00  NaT 2024-03-31 00:51:40 2024-03-31 03:35:00  NaT 2024-03-31 03:49:22  
5   881837333   CX976   CPA976  7901768        B-HPB     A21N   RPLL        VHHH  Landed 07:30 2024-03-29 21:45:00  NaT 2024-03-29 21:46:49 2024-03-30 00:05:00  NaT 2024-03-29 23:30:12  
6   881725491   CX913   CPA913  7901768        B-HPB     A21N   VHHH        RPLL  Landed 22:24 2024-03-29 12:20:00  NaT 2024-03-29 12:42:42 2024-03-29 14:35:00  NaT 2024-03-29 14:24:57  
7   881693238   CX674   CPA674  7901768        B-HPB     A21N   VTBS        VHHH  Landed 18:58 2024-03-29 08:05:00  NaT 2024-03-29 08:52:54 2024-03-29 10:55:00  NaT 2024-03-29 10:58:14  
8   881665708   CX653   CPA653  7901768        B-HPB     A21N   VHHH        VTBS  Landed 14:26 2024-03-29 04:00:00  NaT 2024-03-29 04:35:36 2024-03-29 07:05:00  NaT 2024-03-29 07:26:51  
9   881605496   CX976   CPA976  7901768        B-HPB     A21N   RPLL        VHHH  Landed 07:30 2024-03-28 21:45:00  NaT 2024-03-28 21:46:18 2024-03-29 00:05:00  NaT 2024-03-28 23:30:58  
10  881497323   CX913   CPA913  7901768        B-HPB     A21N   VHHH        RPLL  Landed 22:24 2024-03-28 12:20:00  NaT 2024-03-28 12:49:47 2024-03-28 14:35:00  NaT 2024-03-28 14:24:36  
11  881467141   CX421   CPA421  7901768        B-HPB     A21N   RCTP        VHHH  Landed 18:45 2024-03-28 09:00:00  NaT 2024-03-28 09:11:26 2024-03-28 11:05:00  NaT 2024-03-28 10:45:36  
12  881447170   CX420   CPA420  7901768        B-HPB     A21N   VHHH        RCTP  Landed 15:33 2024-03-28 05:50:00  NaT 2024-03-28 06:11:32 2024-03-28 07:50:00  NaT 2024-03-28 07:33:47  
13  881399852   CX449   CPA449  7901768        B-HPB     A21N   RCKH        VHHH  Landed 08:55 2024-03-27 23:45:00  NaT 2024-03-27 23:46:05 2024-03-28 01:15:00  NaT 2024-03-28 00:55:16  
14  881284852   CX448   CPA448  7901768        B-HPB     A21N   VHHH        RCKH  Landed 22:58 2024-03-27 13:45:00  NaT 2024-03-27 14:02:26 2024-03-27 15:15:00  NaT 2024-03-27 14:58:08  
15  881224769   CX357   CPA357  7901768        B-HPB     A21N   ZSNJ        VHHH  Landed 16:48 2024-03-27 06:15:00  NaT 2024-03-27 06:38:34 2024-03-27 09:05:00  NaT 2024-03-27 08:48:19  
16  881200477   CX356   CPA356  7901768        B-HPB     A21N   VHHH        ZSNJ  Landed 13:01 2024-03-27 02:25:00  NaT 2024-03-27 03:09:36 2024-03-27 05:00:00  NaT 2024-03-27 05:01:42  
17  881059983   CX742   CPA742  7901768        B-HPB     A21N   VVNB        VHHH  Landed 22:12 2024-03-26 12:20:00  NaT 2024-03-26 12:53:49 2024-03-26 14:15:00  NaT 2024-03-26 14:12:35  
18  881028286   CX743   CPA743  7901768        B-HPB     A21N   VHHH        VVNB  Landed 18:26 2024-03-26 09:15:00  NaT 2024-03-26 09:45:30 2024-03-26 11:20:00  NaT 2024-03-26 11:26:21  
19  880987691   CX906   CPA906  7901768        B-HPB     A21N   RPLL        VHHH  Landed 13:00 2024-03-26 02:50:00  NaT 2024-03-26 03:17:20 2024-03-26 05:30:00  NaT 2024-03-26 05:00:05  
20  880961197   CX907   CPA907  7901768        B-HPB     A21N   VHHH        RPLL  Landed 09:31 2024-03-25 23:30:00  NaT 2024-03-25 23:48:48 2024-03-26 01:40:00  NaT 2024-03-26 01:31:18  
21  880878019   CX989   CPA989  7901768        B-HPB     A21N   ZGGG        VHHH  Landed 00:08 2024-03-25 14:25:00  NaT 2024-03-25 15:32:32 2024-03-25 15:35:00  NaT 2024-03-25 16:08:08  
22  880853941   CX988   CPA988  7901768        B-HPB     A21N   VHHH        ZGGG  Landed 22:13 2024-03-25 12:05:00  NaT 2024-03-25 13:39:17 2024-03-25 13:10:00  NaT 2024-03-25 14:13:28  
23  880807848   CX674   CPA674  7901768        B-HPB     A21N   VTBS        VHHH  Landed 18:51 2024-03-25 08:05:00  NaT 2024-03-25 08:27:12 2024-03-25 10:55:00  NaT 2024-03-25 10:51:37  
24  880782639   CX653   CPA653  7901768        B-HPB     A21N   VHHH        VTBS  Landed 13:51 2024-03-25 04:00:00  NaT 2024-03-25 04:19:31 2024-03-25 07:05:00  NaT 2024-03-25 06:51:40  
...
# --8<-- [end:df1]
"""
