import asyncio
import random
from telethon.sync import TelegramClient, errors

#api_id = '20631255'
#api_hash = 'c0ce0d24c3a6a653b1aaaad41df9928c'
sessionFilePath = 'teleTool/tethonss'
minDelay = 3
maxDelay = 6


### =====
async def init_client(id, hash) -> TelegramClient:
    client = TelegramClient(sessionFilePath, id, hash)
    await client.start()
    return client


### =====
async def send_message_to_group(client, grpName, msg, mediaPath = ''):
    # Get the group
    try:
        group_entity = await client.get_input_entity(grpName)
    except Exception as e:
        return str(e)
        
    msg = msg.replace('---', '\n')

    try:
        if mediaPath:
            await client.send_message(group_entity, message=msg, media=mediaPath)
        else:
            await client.send_message(group_entity, message=msg)
    except errors.FloodWaitError as e:
        await asyncio.sleep(e.seconds)
        return f'Flood wait, sleeping for {e.seconds} seconds'
    except Exception as e:
        return str(e)


# --------------- MAIN APP ---------------
#'testnhom21\ntestnhom20'
### =====
async def main():
    api_id = input("Nhập API ID: ")
    api_hash = input("Nhập API HASH: ")
    groupsStr = input("Nhập DS nhóm (tên nhóm cách nhau bằng dấu ---): ")
    message = input("Nhập nội dung tin nhắn: ")
    filePath = input("Nhập file đính kèm: ")

    if not groupsStr:
        print('Chưa nhập danh sách group spam.')
        return
    
    # Create a Telethon client instance
    client = await init_client(api_id, api_hash)
    if not client:
        print('Cannot login Telegram.')

    accPhone = (await client.get_me()).phone
    listGrp = groupsStr.split('---')

    while True:
        for grpId in listGrp:
            grpId = grpId.strip()
            if 't.me' in grpId:
                grpId = grpId[grpId.rindex('/') + 1:]

            errMsg = await send_message_to_group(client, grpId, message, filePath)
            if not errMsg:
                print(f" ✔ '{accPhone}' gửi tin nhắn đến '{grpId}' thành công!")
            else:
                print(f" ✖ '{accPhone}' gửi tin nhắn đến '{grpId}' thất bại: {errMsg}")

            # Delay between message sent
            delay = random.uniform(minDelay, maxDelay)
            await asyncio.sleep(delay)



# Call the main function
if __name__ == "__main__":
    asyncio.run(main())  