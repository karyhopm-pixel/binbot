import aiohttp

async def get_bin_info(bin_number):
    url = f"https://lookup.binlist.net/{bin_number}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "scheme": data.get("scheme"),
                        "bank": data.get("bank", {}).get("name"),
                        "country": data.get("country", {}).get("name"),
                        "country_emoji": data.get("country", {}).get("emoji")
                    }
    except:
        pass

    return {
        "scheme": "Unknown",
        "bank": "Unknown",
        "country": "Unknown",
        "country_emoji": ""
    }
