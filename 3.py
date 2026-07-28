#!/usr/bin/env python3
# ===================================================================
# 🔥 ARIYAN WORLD CHAT BOT - EXTREME HANG (FREEZE) EDITION 🔥
# DEVELOPER : ARYAN
# AUTHORIZED USE ONLY
# ===================================================================

import requests, os, json, binascii, time, urllib3, base64, datetime, re, socket, ssl, asyncio, aiohttp, random, traceback
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from protobuf_decoder.protobuf_decoder import Parser
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2
import google.protobuf.json_format as json_format

LEVEL_UP = "ARYAN"

# ─────────────────────────────────────────
#          GUEST DATA FILE LOADER
# ─────────────────────────────────────────
def load_guest_credentials():
    """guest100067.dat ফাইল থেকে UID এবং Password অটো লোড করার ফাংশন"""
    target_file = None
    if os.path.exists("guest100067.dat"):
        target_file = "guest100067.dat"
    else:
        for file in os.listdir("."):
            if file.endswith("guest100067.dat"):
                target_file = file
                break
    
    if not target_file:
        print("❌ [ERROR] guest100067.dat ফাইলটি পাওয়া যায়নি! দয়া করে ফাইলটি বটের ফোল্ডারে রাখুন।")
        return None, None

    try:
        with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
        
        guest_info = data.get("guest_account_info", {})
        uid = guest_info.get("com.garena.msdk.guest_uid")
        password = guest_info.get("com.garena.msdk.guest_password")

        if uid and password:
            print(f"📂 [SUCCESS] '{target_file}' থেকে সফলভাবে অ্যাকাউন্ট তথ্য লোড করা হয়েছে।")
            return str(uid), str(password)
        else:
            print(f"❌ [ERROR] '{target_file}' ফাইলে UID বা Password পাওয়া যায়নি!")
            return None, None
    except Exception as e:
        print(f"❌ [ERROR] '{target_file}' রিড করতে সমস্যা হয়েছে: {e}")
        return None, None

# ─────────────────────────────────────────
#           SERVER CONFIG (HARDCODED)
# ─────────────────────────────────────────
CONFIG = {
    "client_url": {
        "etc": "https://clientbp.ggpolarbear.com/",
        "ind": "https://client.ind.freefiremobile.com/",
        "us":  "https://client.us.freefiremobile.com/"
    },
    "current_version":        "1.126.7",
    "host":                   "loginbp.ggpolarbear.com",
    "latest_release_version": "OB54",
    "next_update":            "July 04, 2026",
    "play_version":           "1.123.1",
    "server_url":             "https://loginbp.ggpolarbear.com/"
}

login_url = CONFIG["server_url"]
ob        = CONFIG["latest_release_version"]
version   = CONFIG["current_version"]

def get_client_url(region: str) -> str:
    r = region.lower()
    if r in ("ind", "in"):
        return CONFIG["client_url"]["ind"]
    elif r in ("us",):
        return CONFIG["client_url"]["us"]
    else:
        return CONFIG["client_url"]["etc"]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─────────────────────────────────────────
#           CRYPTO HELPERS
# ─────────────────────────────────────────
async def EnC_Vr(N):
    if N<0: return b''
    H = []
    while True:
        RedZed = N & 0x7F
        N >>= 7
        if N: RedZed |= 0x80
        H.append(RedZed)
        if not N: break
    return bytes(H)

async def CrEaTe_VarianT(fn, val):
    return await EnC_Vr((fn<<3)|0) + await EnC_Vr(val)

async def CrEaTe_LenGTh(fn, val):
    ev = val.encode() if isinstance(val,str) else val
    return await EnC_Vr((fn<<3)|2) + await EnC_Vr(len(ev)) + ev

async def CrEaTe_ProTo(fields):
    packet = bytearray()
    for f,v in fields.items():
        if isinstance(v,dict):
            nested = await CrEaTe_ProTo(v)
            packet.extend(await CrEaTe_LenGTh(f, nested))
        elif isinstance(v,int):
            packet.extend(await CrEaTe_VarianT(f,v))
        elif isinstance(v,(str,bytes)):
            packet.extend(await CrEaTe_LenGTh(f,v))
    return bytes(packet)

async def DecodE_HeX(H):
    F = str(hex(H))[2:]
    return "0"+F if len(F)==1 else F

async def EnC_PacKeT(HeX, K, V):
    cipher = AES.new(K, AES.MODE_CBC, V)
    return cipher.encrypt(pad(bytes.fromhex(HeX),16)).hex()

async def GeneRaTePk(Pk, N, K, V):
    PkEnc = await EnC_PacKeT(Pk, K, V)
    _ = await DecodE_HeX(len(PkEnc)//2)
    HeadEr = N+"000000" if len(_)==2 else N+"00000" if len(_)==3 else N+"0000" if len(_)==4 else N+"000"
    return bytes.fromhex(HeadEr+_+PkEnc)

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def EnC_Uid(H , Tp):
    e , H = [] , int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0)) ; H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None

# ─────────────────────────────────────────
#           UAA HEADER
# ─────────────────────────────────────────
async def Ua():
    versions = ['5.0.1B2','5.1.0P1','5.2.0B1']
    models = ['SM-A125F','Redmi 9A','POCO M3']
    android = random.choice(['11','12','13'])
    return f"GarenaMSDK/{random.choice(versions)}({random.choice(models)};Android {android};en-US;USA;)"

def Uaa():
    versions = ['5.0.1B2','5.1.0P1','5.2.0B1']
    models = ['SM-A125F','Redmi 9A','POCO M3']
    android = random.choice(['11','12','13'])
    return f"GarenaMSDK/{random.choice(versions)}({random.choice(models)};Android {android};en-US;USA;)"

Hr = {
    'User-Agent': Uaa(),
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': ob
}

# ─────────────────────────────────────────
#           SEND PACKET
# ─────────────────────────────────────────
async def SEndPacKeT(ChaT, OnLinE, TypE, PacKeT):
    if TypE == 'ChaT' and ChaT:
        ChaT.write(PacKeT)
        await ChaT.drain()
    elif TypE == 'OnLine' and OnLinE:
        OnLinE.write(PacKeT)
        await OnLinE.drain()

# ─────────────────────────────────────────
#           LOGIN & AUTH
# ─────────────────────────────────────────
async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": await Ua(),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("open_id"), data.get("access_token")
            return None, None

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 2
    major_login.client_version = "1.126.7"
    major_login.client_version_code = "2024010012"
    major_login.system_software = "Android OS 11 / API-30 (RQ3A.210805.001)"
    major_login.system_hardware = "Handheld"    
    major_login.device_type = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1080
    major_login.screen_height = 2400
    major_login.screen_dpi = "440"
    major_login.processor_details = "ARMv8"
    major_login.memory = 6144
    major_login.gpu_renderer = "Adreno (TM) 650"
    major_login.gpu_version = "OpenGL ES 3.2 V@1.50"
    major_login.graphics_api = "OpenGLES3"
    major_login.supported_astc_bitset = 16383
    major_login.unique_device_id = f"Google|{random.randint(10000000,99999999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(100000000000,999999999999)}"
    major_login.client_ip = ""
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    
    major_login.memory_available.version = 55
    major_login.memory_available.hidden_value = 81
    
    major_login.access_token = access_token
    major_login.platform_sdk_id = 2
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = random.randint(120000, 130000)
    major_login.external_storage_available = random.randint(38000, 52000)
    major_login.internal_storage_total = random.randint(100000, 120000)
    major_login.internal_storage_available = random.randint(18000, 32000)
    major_login.game_disk_storage_available = random.randint(18000, 28080)
    major_login.external_sdcard_avail_storage = random.randint(28080, 60000)
    major_login.external_sdcard_total_storage = random.randint(110000, 130000)
    major_login.login_by = 3
    major_login.library_path = "/data/app/~~random/base.apk"
    major_login.reg_avatar = 1
    major_login.library_token = "hash|base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.login_open_id_type = 4
    major_login.loading_time = random.randint(9000, 18000)
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTy3KUhvha/qugOBot9Bf7gcwqrf2btWC5rnrKZxrHIxEFfgxmPVkTxN+2dHiSprlxvm2Kl6o8EEgBJy7FzLLpbARlcqc2f/GQz+6UsLSMGXd"
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 0
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    
    string = major_login.SerializeToString()
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(string, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def MajorLogin(payload):
    url = f"{login_url}MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def DecRypTMajoRLoGin(data):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(data)
    return proto

async def DecRypTLoGinDaTa(data):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(data)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9:
        headers = '0000000'
    elif uid_length == 8:
        headers = '00000000'
    elif uid_length == 10:
        headers = '000000'
    elif uid_length == 7:
        headers = '000000000'
    else:
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

# ─────────────────────────────────────────
#           PACKET BUILDERS
# ─────────────────────────────────────────
async def AuthClan(ClanID, ClanAuth, K, V):
    fields = {1: 3, 2: {1: int(ClanID), 2: 1, 4: str(ClanAuth)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1215', K, V)

async def join_teamcode_packet(team_code, key, iv, region):
    fields = {
        1: 4,
        2: {
            4: bytes.fromhex("01090a0b121920"),
            5: str(team_code),
            6: 6,
            8: 1,
            9: {2: 800, 6: 11, 8: version, 9: 5, 10: 1}
        }
    }
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def start_auto_packet(key, iv, region):
    fields = {
        1: 9,
        2: {
            1: 12480598706,
            2: 1,
            3: int(time.time())
        }
    }
    p_type = '0514' if region.lower()=="ind" else ('0519' if region.lower()=="bd" else '0515')
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), p_type, key, iv)

async def leave_squad_packet(key, iv, region):
    fields = {1: 7, 2: {1: 12480598706}}
    p_type = '0514' if region.lower()=="ind" else ('0519' if region.lower()=="bd" else '0515')
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), p_type, key, iv)

# ─────────────────────────────────────────
#           SEND MESSAGE
# ─────────────────────────────────────────
async def xBunnEr():
    bN = [902000306, 902000305, 902000003, 902000016, 902000017, 902000019, 902031010, 902043025, 902043024, 902000020]
    return random.choice(bN)

async def SEndMsG(chat_type, message, target_uid, chat_id, key, iv, region):
    fields = {
        1: 1,
        2: {
            1: target_uid,
            2: chat_id,
            4: message,
            5: str(int(time.time())),
            9: {
                1: "Fun1w5a2",
                2: await xBunnEr(),
                3: 909000024,
                4: 330,
                5: 909000024,
                10: 1,
                11: 1,
                7: 2,
                13: {1: 2},
                14: {1: target_uid, 2: 8, 3: b""}
            },
            10: "fr",
            13: {2: 1, 3: 1},
            14: {}
        }
    }
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1215', key, iv)

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, region, max_retries=2):
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return True
        except Exception:
            if attempt < max_retries - 1:
                await asyncio.sleep(0.3)
    return False

# ─────────────────────────────────────────
#           GLOBALS
# ─────────────────────────────────────────
online_writer = None
whisper_writer = None
CURRENT_BOT_UID = None
region = 'BD'
auto_start_running = False
stop_auto = False
auto_start_task = None

# ─────────────────────────────────────────
#   AUTO START LOOP - 27 SECONDS TOTAL
# ─────────────────────────────────────────
async def auto_start_loop(team_code, key, iv, region):
    global auto_start_running, stop_auto
    count = 0

    print(f"\n🚀 [AUTO-LW] লুপ শুরু হয়েছে! টিম কোড: {team_code}")

    while not stop_auto:
        try:
            count += 1
            
            # ──── STEP 1: JOIN TEAM (2 sec) ────
            join_pkt = await join_teamcode_packet(team_code, key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_pkt)
            await asyncio.sleep(2)

            # ──── STEP 2: SEND 5 START REQUESTS IN 1 SECOND (1 sec) ────
            start_pkt = await start_auto_packet(key, iv, region)
            for i in range(5):
                if stop_auto:
                    break
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', start_pkt)
                await asyncio.sleep(0.2)

            if stop_auto:
                break

            # ──── STEP 3: WAIT 22 SECONDS ────
            waited = 0
            while waited < 22 and not stop_auto:
                await asyncio.sleep(1)
                waited += 1

            if stop_auto:
                break

            # ──── STEP 4: LEAVE SQUAD (2 sec) ────
            leave_pkt = await leave_squad_packet(key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_pkt)
            await asyncio.sleep(2)

        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"❌ [AUTO-LW ERROR]: {e}")
            await asyncio.sleep(2)
            continue

    auto_start_running = False
    stop_auto = False
    print(f"🛑 [AUTO-LW] লুপ বন্ধ করা হয়েছে! মোট রাউন্ড: {count}")

async def stop_auto_loop():
    global auto_start_running, stop_auto, auto_start_task
    stop_auto = True
    if auto_start_task and not auto_start_task.done():
        auto_start_task.cancel()
        try:
            await auto_start_task
        except asyncio.CancelledError:
            pass
    auto_start_running = False

# ─────────────────────────────────────────
#           TCP CONNECTIONS
# ─────────────────────────────────────────
async def TcPOnLine(ip, port, jwt_token, bot_uid, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            writer.write(bytes.fromhex(AutHToKen))
            await writer.drain()
            while True:
                data = await reader.read(9999)
                if not data:
                    break
            online_writer.close()
            await online_writer.wait_closed()
            online_writer = None
        except Exception as e:
            if online_writer:
                online_writer.close()
                await online_writer.wait_closed()
                online_writer = None
        await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region, reconnect_delay=0.5):
    global whisper_writer, online_writer, auto_start_running, auto_start_task, stop_auto, CURRENT_BOT_UID
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            writer.write(bytes.fromhex(AutHToKen))
            await writer.drain()
            ready_event.set()

            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                pK = await AuthClan(clan_id, clan_compiled_data, key, iv)
                if whisper_writer:
                    writer.write(pK)
                    await writer.drain()

            while True:
                data = await reader.read(9999)
                if not data:
                    break

                if data.hex().startswith("120000"):
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        inPuTMsG = response.Data.msg.strip().lower()

                        # ── ১. /lw <team_code> (শুধু সঠিক থাকলে শুরু হবে এবং গেমের ভেতরে ছোট উত্তর দেবে) ──
                        if inPuTMsG.startswith('/lw '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) >= 2:
                                team_code = parts[1]
                                if team_code.isdigit():
                                    if not auto_start_running:
                                        stop_auto = False
                                        auto_start_running = True
                                        auto_start_task = asyncio.create_task(
                                            auto_start_loop(team_code, key, iv, region)
                                        )
                                    # গেমের ভেতরে ছোট উত্তর
                                    await safe_send_message(
                                        response.Data.chat_type,
                                        "Join Successful",
                                        uid, chat_id, key, iv, region
                                    )

                        # ── ২. /stop অথবা /stop_lw (শুধু বন্ধ করবে এবং গেমের ভেতরে ছোট উত্তর দেবে) ──
                        elif inPuTMsG in ('/stop', '/stop_lw'):
                            if auto_start_running:
                                await stop_auto_loop()
                            # গেমের ভেতরে ছোট উত্তর
                            await safe_send_message(
                                response.Data.chat_type,
                                "Stopped",
                                uid, chat_id, key, iv, region
                            )

                        # অন্য যেকোনো কম্যান্ড বা কথা সম্পূর্ণ ইগনোর করা হবে (কোনো রিপ্লাই দেওয়া হবে না)

                    except Exception as e:
                        print(f"Decode error: {e}")

            whisper_writer.close()
            await whisper_writer.wait_closed()
            whisper_writer = None
        except Exception as e:
            if whisper_writer:
                whisper_writer.close()
                await whisper_writer.wait_closed()
                whisper_writer = None
        await asyncio.sleep(reconnect_delay)

# ─────────────────────────────────────────
#           MAIN FUNCTION
# ─────────────────────────────────────────
async def MaiiiinE():
    global CURRENT_BOT_UID, region, online_writer, whisper_writer
    
    # guest100067.dat থেকে লোড
    uid, password = load_guest_credentials()
    if not uid or not password:
        return None

    print(f"📱 Logging in with Guest UID: {uid}")

    open_id, access_token = await GeNeRaTeAccEss(uid, password)
    if not open_id:
        print("❌ Failed to get open_id/access_token")
        return None

    payload = await EncRypTMajoRLoGin(open_id, access_token)
    login_resp = await MajorLogin(payload)
    if not login_resp:
        print("❌ MajorLogin failed")
        return None
    auth = await DecRypTMajoRLoGin(login_resp)
    token = auth.token
    if not token:
        print("❌ No token")
        return None

    token_data = {
        "token": token,
        "saved_at": time.time(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "bot_uid": str(auth.account_uid),
        "region": getattr(auth, 'region', 'BD'),
        "version": version,
        "ob": ob
    }
    with open("token.json", "w") as f:
        json.dump(token_data, f, indent=2)

    url = auth.url
    region = getattr(auth, 'region', 'BD')
    bot_uid = auth.account_uid
    CURRENT_BOT_UID = str(bot_uid)
    key = auth.key
    iv = auth.iv
    timestamp = auth.timestamp

    login_data = await GetLoginData(url, payload, token)
    if not login_data:
        print("❌ GetLoginData failed")
        return None
    ports = await DecRypTLoGinDaTa(login_data)
    online_ip, online_port = ports.Online_IP_Port.split(":")
    chat_ip, chat_port = ports.AccountIP_Port.split(":")

    auth_token = await xAuThSTarTuP(int(bot_uid), token, int(timestamp), key, iv)

    ready = asyncio.Event()
    task1 = asyncio.create_task(TcPChaT(chat_ip, chat_port, auth_token, key, iv, ports, ready, region))
    task2 = asyncio.create_task(TcPOnLine(online_ip, online_port, token, bot_uid, key, iv, auth_token))

    print(f"🟢 [ONLINE] Bot UID: {CURRENT_BOT_UID} | Region: {region} | Version: {version} ({ob})")
    print("💬 In-Game Commands Active: '/lw <team_code>' & '/stop'")
    await asyncio.gather(task1, task2)

async def StarTinG():
    while True:
        try:
            await MaiiiinE()
        except Exception as e:
            print(f"Restarting due to error: {e}")
            traceback.print_exc()
            await asyncio.sleep(5)

if __name__ == '__main__':
    # 🌟 নতুন বড় ও আকর্ষণীয় কনসোল লোগো ব্যানার 🌟
    banner = f"""
 ╔══════════════════════════════════════════════════════════════════════════╗
 ║                                                                          ║
 ║  ██████╗ ██████╗ ██╗██╗   ██╗██████╗ ███╗   ██╗    ██████╗  ██████╗ ████████╗  ║
 ║  ██╔══██╗██╔══██╗██║╚██╗ ██╔╝██╔══██╗████╗  ██║    ██╔══██╗██╔═══██╗╚══██╔══╝  ║
 ║  ██████╔╝██████╔╝██║ ╚████╔╝ ██████╔╝██╔██╗ ██║    ██████╔╝██║   ██║   ██║     ║
 ║  ██╔══██╗██╔══██╗██║  ╚██╔╝  ██╔══██╗██║╚██╗██║    ██╔══██╗██║   ██║   ██║     ║
 ║  ██║  ██║██║  ██║██║   ██║   ██║  ██║██║ ╚████║    ██████╔╝╚██████╔╝   ██║     ║
 ║  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═════╝  ╚═════╝    ╚═╝     ║
 ║                                                                          ║
 ║   🔥 ARIYAN WORLD CHAT BOT - EXTREME HANG (FREEZE) EDITION 🔥            ║
 ║                                                                          ║
 ║   📌 Version  : {version} - {ob}                                              ║
 ║   👑 Developer: ARYAN                                                    ║
 ║   🔐 Mode     : In-Game Direct Commands Only                             ║
 ║                                                                          ║
 ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    asyncio.run(StarTinG())