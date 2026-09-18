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
# ⚙️ MAIN CONFIGURATION
# ==========================================
MAIN_BOT_TOKEN = '8768111355:AAEwIyM2zz5qmWEnMtsC3t6tMos8G7PN9kM' # Tumhara Main Token
MAIN_BOT_USERNAME = 'hotstar1rsbot' 
MAIN_ADMIN_ID = "6860106371" # Tumhara User ID

# Tumhare compulsory channels (Kissi bhi clone se remove nahi honge)
MAIN_CHANNELS = [
    {"name": "📢 Join Channel 1", "url": "https://t.me/leakmethodfree", "id": "@leakmethodfree"},
    {"name": "📢 Join Channel 2", "url": "https://t.me/sabkijayhokhush", "id": "@sabkijayhokhush"},
    {"name": "💬 Join Group", "url": "https://t.me/rosekhudkabanaya", "id": "@rosekhudkabanaya"}
]

app_config = {
    'GUEST_TOKEN': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJoSWRcIjpcImM3ZGM4MGVhNzViNDQzNmVhZTg1MzVkMWM3OTFkMDFmXCIsXCJwSWRcIjpcImM0MGNjYjg0MWVkNjRkOGFhYjFlNGI1Y2ZmOTFhYzc5XCIsXCJkd0hpZFwiOlwiZmVhMjhjNDUwMGZmNWE4NDg3MTJiNDk2ZmY5ZjcxZGYwMzc3NGYwMGZlMDVjZDU1NmRiOWM1ZDAxZWZhOTI3ZVwiLFwiZHdQaWRcIjpcIjQyOWI2OTU5MWRkOGY1ZDJlNmQyY2M4Nzk5ZTkyMTcyYWYxNmRiZThhMDc3MDg3OTRhZWI1MjI1ZTQ5NzkzMTJcIixcIm9sZEhpZFwiOlwiYzdkYzgwZWE3NWI0NDM2ZWFlODUzNWQxYzc5MWQwMWZcIixcIm9sZFBpZFwiOlwiYzQwY2NiODQxZWQ2NGQ4YWFiMWU0YjVjZmY5MWFjNzlcIixcImlzUGlpVXNlck1pZ3JhdGVkXCI6ZmFsc2UsXCJuYW1lXCI6XCJZb3VcIixcInBob25lXCI6XCI5MTMwMDg5NTU4XCIsXCJpcFwiOlwiMTUyLjU4LjMzLjI0MFwiLFwiY291bnRyeUNvZGVcIjpcImluXCIsXCJjdXN0b21lclR5cGVcIjpcIm51XCIsXCJ0eXBlXCI6XCJwaG9uZVwiLFwiaXNFbWFpbFZlcmlmaWVkXCI6ZmFsc2UsXCJpc1Bob25lVmVyaWZpZWRcIjp0cnVlLFwiZGV2aWNlSWRcIjpcIjQ4NWQzOC01MDNjOTUtNjc0ODQxLTNhODc2YlwiLFwicHJvZmlsZVwiOlwiQURVTFRcIixcInZlcnNpb25cIjpcInYyXCIsXCJzdWJzY3JpcHRpb25zXCI6e1wiaW5cIjp7fX0sXCJlbnRcIjpcIkNob0tFZ29PRWdVMU5UZ3pOaElGTmpRd05Ea0tBQklFT0dSWUFRb0xFZ2tJQ2pnQlVOQUZXQUVLeWdFS0JRb0RDZ0VBRXNBQkVnZGhibVJ5YjJsa0VnTnBiM01TQ1dGdVpISnZhV1IwZGhJR1ptbHlaWFIyRWdkaGNIQnNaWFIyRWdSeWIydDFFZ04zWldJU0JHMTNaV0lTQjNScGVtVnVkSFlTQlhkbFltOXpFZ1pxYVc5emRHSVNDbU5vY205dFpXTmhjM1FTQkhSMmIzTVNCSEJqZEhZU0EycHBieElIYW1sdkxXeDVaaElFZUdKdmVCSUxjR3hoZVhOMFlYUnBiMjRTREdwcGIzQm9iMjVsYkdsMFpSSU5abVZoZEhWeVpXMXZZbWxzWlJvQ2MyUWFBbWhrSWdOelpISXFCbk4wWlhKbGIxZ0JFaWNJQVNBQk1BRTZId29iU0c5MGMzUmhjbEJ5WlcxcGRXMHVTVTR1VFc5dWRHZ3VNams1RUFFPVwiLFwiaXNzdWVkZXRcIjoxNzg5NzIwMzc2Nzk1LFwiZHBpZFwiOlwiYzQwY2NiODQxZWQ2NGQ4YWFiMWU0YjVjZmY5MWFjNzlcIixcInN0XCI6MSxcImRhdGFcIjpcIkNnd0lBQ0lJa0FIQTY1YWRpelFLQkFnQU9nQUtMZ2dBUWlvS0tFSTBOMkk1WW1WaVkyRmlNR1kwTWprd09HVTJNalpqTkRFMk1HVTFZelkxTWxKNFJHdEJjSFE9XCJ9IiwiaXNzIjoiVU0iLn0.ZbH4vvjiUuqCuBX4-vmFhHcC90_blikY1l29zBmcCxs', 
    'DEVICE_ID': '485d38-503c95-674841-3a876b'
}

# ==========================================
# 💾 DATABASE HANDLING (With Clone Data)
# ==========================================
DB_FILE = "database.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {"users": {}, "accounts": {}, "stats": {"total_qr": 0}, "clones": {}}

def save_data(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f)

db = load_data()

# ==========================================
# 🚀 BOT FACTORY (Multi-Bot Engine)
# ==========================================
class HotstarBotInstance:
    def __init__(self, token, admin_id, is_clone=False, bot_username="CloneBot"):
        self.bot = telebot.TeleBot(token, threaded=True, num_threads=50)
        self.admin_id = str(admin_id)
        self.is_clone = is_clone
        self.bot_username = bot_username
        self.user_sessions = {}
        self.register_handlers()

    def get_real_headers(self, token):
        return {
            'Host': 'web.hotstar.com', 'Connection': 'keep-alive',
            'Sec-Ch-Ua-Platform': '"Windows"', 'X-Hs-Client': 'platform:web;os:Windows;network_data:4g',
            'X-Hs-Device-Id': app_config['DEVICE_ID'], 'Content-Type': 'application/json',
            'X-Hs-App': '260905000', 'X-Hs-Usertoken': token,
            'Origin': 'https://web.hotstar.com', 'Referer': 'https://web.hotstar.com/in/onboarding/login',
        }

    def force_sub_markup(self):
        markup = InlineKeyboardMarkup()
        # Main compulsory channels
        for ch in MAIN_CHANNELS:
            markup.row(InlineKeyboardButton(ch["name"], url=ch["url"]))
        
        # Clone owner's custom channels
        if self.is_clone and self.admin_id in db["clones"]:
            custom_channels = db["clones"][self.admin_id].get("custom_channels", [])
            for i, link in enumerate(custom_channels):
                markup.row(InlineKeyboardButton(f"🔔 Join Extra Channel {i+1}", url=link))
        
        markup.row(InlineKeyboardButton("✅ I Have Joined All (Verify)", callback_data="verify_join"))
        return markup

    def is_joined(self, user_id):
        if str(user_id) == self.admin_id or str(user_id) == MAIN_ADMIN_ID: return True
        if self.is_clone: 
            # CLONE MAGIC: Bypass strict check, return True always for clones!
            return True 
        
        # STRICT CHECK for Main Bot only
        for ch in MAIN_CHANNELS:
            try:
                member = self.bot.get_chat_member(ch["id"], user_id)
                if member.status in ['left', 'kicked']: return False
            except: return False
        return True

    def get_main_menu(self):
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("➕ Add New Account", callback_data="add_account"))
        markup.row(InlineKeyboardButton("📁 My Saved Accounts", callback_data="my_accounts"))
        markup.row(InlineKeyboardButton("🎁 My Referral & Balance", callback_data="my_referral"))
        markup.row(InlineKeyboardButton("🏆 Global Leaderboard", callback_data="leaderboard"))
        return markup

    def generate_and_send_qr(self, chat_id, number, token, user_info):
        msg = self.bot.send_message(chat_id, f"⏳ Generating QR Code for **{number}**...", parse_mode="Markdown")
        session = requests.Session()
        headers = self.get_real_headers(token)
        headers['X-Hs-Request-Id'] = str(uuid.uuid4())
        payload = {"paymentMode": "UPI", "pgName": "phonepe", "paymentProcessor": "phonepeQR", "paymentType": "RECURRING", "subscriptionPack": "HotstarSuper.IN.1Month.149", "returnUrl": "https://web.hotstar.com/in/payment/status", "promoCode": "CLOUDSPO100", "abTags": ["PayX"], "pgParams": {"versionCode": "-1", "redirectURL": "https://web.hotstar.com/in/payment/status", "mobileNumber": number}, "userSegments": ["CONTROL"]}
        
        try:
            qr_res = session.post("https://web.hotstar.com/api/internal/bff/gringotts/v4/web/payment/initiate/lite", headers=headers, json=payload, timeout=15)
            if qr_res.status_code in [200, 201]:
                res_data = qr_res.json()
                order_id = res_data.get('pollPayload', {}).get('orderId') or res_data.get('description', {}).get('pollPayload', {}).get('orderId')
                if order_id:
                    status_url = f"https://web.hotstar.com/api/internal/bff/gringotts/v2/web/initiate/{order_id}/status"
                    qr_string = None
                    for _ in range(6):
                        status_res = session.get(status_url, headers=headers, timeout=10)
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
                        bio = io.BytesIO(); bio.name = 'qr_code.png'; img.save(bio, 'PNG'); bio.seek(0)
                        
                        caption_text = (f"🎉 **QR Code Ready!**\n\nIs QR Code ka screenshot lein aur kisi bhi UPI App mein 'Scan from Gallery' karke ₹1 pay karein.\n\n⚠️ **ZAROORI SOOCHNA:**\nPayment ke baad 'AutoPay' section mein jake usko **Cancel** kar dein.\n\n**UPI String:**\n`{qr_string}`")
                        
                        self.bot.delete_message(chat_id, msg.message_id)
                        self.bot.send_photo(chat_id, photo=bio, caption=caption_text, parse_mode="Markdown")
                        
                        user_id_str = str(user_info.id)
                        db["users"][user_id_str]["qrs_used"] += 1
                        db["stats"]["total_qr"] += 1
                        save_data(db)
                        
                        try: self.bot.send_message(self.admin_id, f"🚨 **QR Generated**\nUser: {user_info.first_name}\nNumber: {number}")
                        except: pass
                    else: self.bot.edit_message_text("❌ Timeout.", chat_id, msg.message_id)
                else: self.bot.edit_message_text("❌ Order ID not found.", chat_id, msg.message_id)
            elif qr_res.status_code == 403: self.bot.edit_message_text("❌ Plan already active.", chat_id, msg.message_id)
            else: self.bot.edit_message_text(f"❌ Failed: {qr_res.status_code}", chat_id, msg.message_id)
        except Exception as e: self.bot.edit_message_text("❌ Error generating QR.", chat_id, msg.message_id)

    def register_handlers(self):
        @self.bot.message_handler(commands=['clone'])
        def make_clone(msg):
            if str(msg.from_user.id) == MAIN_ADMIN_ID and not self.is_clone:
                try:
                    parts = msg.text.split()
                    c_token = parts[1]
                    c_admin = parts[2]
                    db["clones"][c_admin] = {"token": c_token, "custom_channels": []}
                    save_data(db)
                    
                    # Start the clone in a new thread
                    threading.Thread(target=start_clone_bot, args=(c_token, c_admin), daemon=True).start()
                    self.bot.reply_to(msg, f"✅ **Clone Bot Created Successfully!**\nAdmin ID: `{c_admin}`", parse_mode="Markdown")
                except:
                    self.bot.reply_to(msg, "⚠️ Format: `/clone <BOT_TOKEN> <ADMIN_ID>`", parse_mode="Markdown")

        @self.bot.message_handler(commands=['addchannel'])
        def add_channel(msg):
            if self.is_clone and str(msg.from_user.id) == self.admin_id:
                try:
                    link = msg.text.split()[1]
                    db["clones"][self.admin_id]["custom_channels"].append(link)
                    save_data(db)
                    self.bot.reply_to(msg, "✅ Aapka channel add ho gaya hai!")
                except:
                    self.bot.reply_to(msg, "⚠️ Format: `/addchannel <YOUR_CHANNEL_LINK>`", parse_mode="Markdown")

        @self.bot.message_handler(commands=['start'])
        def start_cmd(msg):
            user_id = str(msg.from_user.id)
            text = msg.text.split()
            if user_id not in db["users"]:
                referrer = text[1] if len(text) > 1 and text[1].isdigit() else None
                db["users"][user_id] = {"name": msg.from_user.first_name, "referrals": 0, "qrs_used": 0, "referred_by": referrer}
                if referrer and referrer in db["users"] and referrer != user_id:
                    db["users"][referrer]["referrals"] += 1
                save_data(db)

            if not self.is_joined(msg.from_user.id):
                self.bot.send_message(msg.chat.id, "🛑 **Aage badhne ke liye saare channels join karna COMPULSORY hai!**\nSabhi channels join karke 'Verify' dabayein warna bot kaam nahi karega.", parse_mode="Markdown", reply_markup=self.force_sub_markup())
                return
            self.bot.send_message(msg.chat.id, "📺 **Welcome to Hotstar Premium Bot!**", parse_mode="Markdown", reply_markup=self.get_main_menu())

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            chat_id = call.message.chat.id
            user_id = str(call.from_user.id)
            data = call.data

            if data != "verify_join" and not self.is_joined(call.from_user.id):
                self.bot.answer_callback_query(call.id, "Please join all channels first!", show_alert=True)
                return

            if data == "verify_join":
                # For Clones, this will always succeed without actually checking (Fake Verify)
                if self.is_joined(call.from_user.id):
                    self.bot.edit_message_text("✅ Verification Successful! Welcome.", chat_id, call.message.message_id)
                    self.bot.send_message(chat_id, "📺 **Main Menu**", reply_markup=self.get_main_menu())
                else:
                    self.bot.answer_callback_query(call.id, "❌ Aapne saare channels join nahi kiye!", show_alert=True)

            elif data == "main_menu":
                self.bot.edit_message_text("📺 **Main Menu**", chat_id, call.message.message_id, reply_markup=self.get_main_menu())

            elif data == "add_account":
                self.user_sessions[chat_id] = {'step': 'ask_number', 'session': requests.Session()}
                self.bot.edit_message_text("📱 Apna 10-digit Hotstar mobile number type karein:", chat_id, call.message.message_id)

            elif data == "my_accounts":
                accounts = db["accounts"].get(user_id, {})
                if not accounts:
                    markup = InlineKeyboardMarkup().row(InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu"))
                    self.bot.edit_message_text("❌ No accounts saved.", chat_id, call.message.message_id, reply_markup=markup)
                    return
                markup = InlineKeyboardMarkup()
                for num in accounts.keys(): markup.row(InlineKeyboardButton(f"👤 {num}", callback_data=f"select_{num}"))
                markup.row(InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu"))
                self.bot.edit_message_text("📁 **Apne saved accounts me se ek select karein:**", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

            elif data.startswith("select_"):
                number = data.split("_")[1]
                markup = InlineKeyboardMarkup()
                markup.row(InlineKeyboardButton("💸 Generate Premium QR", callback_data=f"pay_{number}"))
                markup.row(InlineKeyboardButton("❌ Remove Account", callback_data=f"remove_{number}"))
                markup.row(InlineKeyboardButton("🔙 Back", callback_data="my_accounts"))
                self.bot.edit_message_text(f"⚙️ **Manage Account: {number}**", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

            elif data.startswith("pay_"):
                user_data = db["users"].get(user_id, {"referrals": 0, "qrs_used": 0})
                avail_qrs = (user_data["referrals"] // 5) - user_data["qrs_used"]
                
                if str(user_id) != MAIN_ADMIN_ID and str(user_id) != self.admin_id and avail_qrs <= 0:
                    self.bot.answer_callback_query(call.id, "❌ Aapke paas Free QRs nahi hain! 5 dosto ko refer karein.", show_alert=True)
                    return
                    
                number = data.split("_")[1]
                token = db["accounts"].get(user_id, {}).get(number)
                if token:
                    self.bot.answer_callback_query(call.id, "Generating QR Code...")
                    self.generate_and_send_qr(chat_id, number, token, call.from_user)
                else: self.bot.answer_callback_query(call.id, "Session expired.", show_alert=True)

            elif data == "my_referral":
                user_data = db["users"].get(user_id, {"referrals": 0, "qrs_used": 0})
                avail_qrs = (user_data["referrals"] // 5) - user_data["qrs_used"]
                ref_link = f"https://t.me/{self.bot.get_me().username}?start={user_id}"
                text = (f"🎁 **REFERRAL DASHBOARD** 🎁\n\n👥 Referrals: {user_data['referrals']}\n🎟 Available Free QRs: {max(0, avail_qrs)}\n🎫 Used QRs: {user_data['qrs_used']}\n\n🔗 **Your Link:**\n`{ref_link}`")
                markup = InlineKeyboardMarkup().row(InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu"))
                self.bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
                
            elif data == "leaderboard":
                sorted_users = sorted(db["users"].values(), key=lambda x: x["qrs_used"], reverse=True)[:10]
                text = "🏆 **GLOBAL LEADERBOARD** 🏆\n\n"
                for idx, u in enumerate(sorted_users):
                    if u['qrs_used'] > 0: text += f"{'🥇' if idx==0 else '🏅'} **{u['name']}** - `{u['qrs_used']} Claims`\n"
                markup = InlineKeyboardMarkup().row(InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu"))
                self.bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

        @self.bot.message_handler(func=lambda msg: self.user_sessions.get(msg.chat.id, {}).get('step') == 'ask_number')
        def handle_num(msg):
            chat_id = msg.chat.id
            number = msg.text.strip()
            if len(number) != 10 or not number.isdigit():
                self.bot.send_message(chat_id, "❌ Invalid number!"); return
            
            self.user_sessions[chat_id]['number'] = number
            self.user_sessions[chat_id]['step'] = 'ask_otp'
            self.bot.send_message(chat_id, f"⏳ Sending OTP to {number}...")
            
            url = "https://web.hotstar.com/api/internal/bff/v2/pages/1/spaces/1/widgets/8?action=sendOtp&packId=HotstarSuper.IN.1Month.149&page_enum=onboarding_login&promo=CLOUDSPO100,CLOUDSPO100&qrCode=true"
            headers = self.get_real_headers(app_config['GUEST_TOKEN'])
            headers['X-Hs-Request-Id'] = str(uuid.uuid4())
            try:
                res = self.user_sessions[chat_id]['session'].post(url, headers=headers, json={"body": {"@type": "type.googleapis.com/feature.login.InitiatePhoneLoginRequest", "initiate_by": 0, "phone_number": number}}, timeout=15)
                if res.status_code == 200: self.bot.send_message(chat_id, "✅ OTP Sent! Type the 4-digit OTP here:")
                else: self.bot.send_message(chat_id, f"❌ Failed. Code: {res.status_code}"); self.user_sessions.pop(chat_id, None)
            except: self.bot.send_message(chat_id, "❌ Error"); self.user_sessions.pop(chat_id, None)

        @self.bot.message_handler(func=lambda msg: self.user_sessions.get(msg.chat.id, {}).get('step') == 'ask_otp')
        def handle_otp(msg):
            chat_id = msg.chat.id
            number = self.user_sessions[chat_id]['number']
            otp = msg.text.strip()
            
            url = "https://web.hotstar.com/api/internal/bff/v2/pages/1/spaces/1/widgets/9?action=verifyOtp&page_enum=onboarding_login&promo=CLOUDSPO100,CLOUDSPO100&qrCode=true"
            headers = self.get_real_headers(app_config['GUEST_TOKEN'])
            headers['X-Hs-Request-Id'] = str(uuid.uuid4())
            try:
                res = self.user_sessions[chat_id]['session'].post(url, headers=headers, json={"body": {"@type": "type.googleapis.com/feature.login.VerifyPhoneLoginRequest", "verification_code": otp, "phone_number": number}}, timeout=15)
                if res.status_code == 200:
                    token = res.headers.get('X-Hs-Updatedusertoken')
                    if token:
                        if str(msg.from_user.id) not in db["accounts"]: db["accounts"][str(msg.from_user.id)] = {}
                        db["accounts"][str(msg.from_user.id)][number] = token
                        save_data(db)
                        markup = InlineKeyboardMarkup().row(InlineKeyboardButton("💸 Generate QR Now", callback_data=f"pay_{number}")).row(InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
                        self.bot.send_message(chat_id, f"✅ **Account Saved!**\nNumber: {number}", parse_mode="Markdown", reply_markup=markup)
                        self.user_sessions.pop(chat_id, None)
                    else: self.bot.send_message(chat_id, "❌ Failed to get token.")
                else: self.bot.send_message(chat_id, "❌ Invalid OTP! Try again:")
            except: self.bot.send_message(chat_id, "❌ Error"); self.user_sessions.pop(chat_id, None)

    def run(self):
        print(f"🚀 Started Bot for Admin: {self.admin_id}")
        self.bot.infinity_polling(timeout=20, long_polling_timeout=15)

# ==========================================
# 🔄 CLONE SPANNER FUNCTION
# ==========================================
def start_clone_bot(token, admin_id):
    clone = HotstarBotInstance(token, admin_id, is_clone=True)
    clone.run()

if __name__ == "__main__":
    print("🚀 Initializing Main Bot & Saved Clones...")
    
    # 1. Start all saved clone bots from database in background
    for admin_id, clone_data in db.get("clones", {}).items():
        threading.Thread(target=start_clone_bot, args=(clone_data["token"], admin_id), daemon=True).start()
    
    # 2. Start Main Bot in the main thread
    main_bot = HotstarBotInstance(MAIN_BOT_TOKEN, MAIN_ADMIN_ID, is_clone=False, bot_username=MAIN_BOT_USERNAME)
    main_bot.run()
