import os
import logging
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)

# ========== التوكن ==========
BOT_TOKEN = "8760673859:AAF04DjMq2-mDSo33maG0cdUpa5TsiObddY"

# ========== إعدادات المطور ==========
DEVELOPER_USERNAME = "@SSSTlF"
DEVELOPER_ID = 1170411845

# ========== ملفات البيانات ==========
DATA_FILE = "bot_data.json"
REPLIES_FILE = "replies_data.json"

# ========== قوائم الردود السريعة ==========
QUICK_REPLIES = [
    ["👋 مرحباً! كيف يمكنني مساعدتك؟", "شكراً لتواصلك"],
    ["✅ تم استلام رسالتك، سأرد قريباً", "🙏 شكراً لك"],
    ["📌 أنا مشغول حالياً، سأرد لاحقاً", "⏳ انتظر قليلاً"],
    ["❌ عذراً، لا أستطيع مساعدتك في هذا", "🔍 وضح أكثر"],
    ["👍 تم، سأعمل على طلبك", "📋 جاري التنفيذ"],
    ["📞 تواصل معي الآن", "📨 أرسل تفاصيل أكثر"],
]

# ========== تحميل/حفظ البيانات ==========
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "users": [],
        "banned_users": [],
        "bot_active": True,
        "total_users": 0
    }

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_replies():
    if os.path.exists(REPLIES_FILE):
        with open(REPLIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_replies(replies):
    with open(REPLIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(replies, f, ensure_ascii=False, indent=4)

# ========== دوال البوت ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        username = update.message.from_user.username
        
        data = load_data()
        
        if str(user_id) in data["banned_users"]:
            await update.message.reply_text(
                "🚫 **أنت محظور من استخدام هذا البوت.**\n"
                "للتواصل مع المطور: @SSSTlF",
                parse_mode="Markdown"
            )
            return
        
        if str(user_id) not in data["users"]:
            data["users"].append(str(user_id))
            data["total_users"] = len(data["users"])
            save_data(data)
            
            try:
                await context.bot.send_message(
                    chat_id=DEVELOPER_ID,
                    text=f"🆕 **مستخدم جديد!**\n\n"
                         f"👤 {user_name}\n"
                         f"🆔 @{username if username else 'لا يوجد'}\n"
                         f"🔢 `{user_id}`\n"
                         f"📊 الإجمالي: {data['total_users']}",
                    parse_mode="Markdown"
                )
            except:
                pass
        
        keyboard = [
            [InlineKeyboardButton("📩 إرسال رسالة", callback_data="send_message")],
            [InlineKeyboardButton("🖼️ إرسال صورة", callback_data="send_photo")],
            [InlineKeyboardButton("🎥 إرسال فيديو", callback_data="send_video")],
            [InlineKeyboardButton("🎵 إرسال صوت", callback_data="send_audio")],
        ]
        
        if user_id == DEVELOPER_ID:
            keyboard.append([InlineKeyboardButton("⚙️ لوحة التحكم", callback_data="admin_panel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"📩 **بوت التواصل مع المطور**\n\n"
            f"👨‍💻 **المطور:** @SSSTlF\n\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"📌 **اختر نوع الملف المراد إرساله:**\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            f"📝 رسالة نصية\n"
            f"🖼️ صورة\n"
            f"🎥 فيديو\n"
            f"🎵 ملف صوتي\n\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Error in start: {e}")

async def panel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_id != DEVELOPER_ID:
        await update.message.reply_text(
            "🚫 **هذا الأمر مخصص للمطور فقط.**",
            parse_mode="Markdown"
        )
        return
    
    data = load_data()
    keyboard = [
        [InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")],
        [InlineKeyboardButton("⏸️ تعطيل البوت", callback_data="admin_disable")] if data["bot_active"] else [InlineKeyboardButton("▶️ تفعيل البوت", callback_data="admin_enable")],
        [InlineKeyboardButton("🚫 حظر مستخدم", callback_data="admin_ban")],
        [InlineKeyboardButton("✅ الغاء حظر", callback_data="admin_unban")],
        [InlineKeyboardButton("📋 المحظورين", callback_data="admin_banned_list")],
        [InlineKeyboardButton("📩 جميع الرسائل", callback_data="show_all_messages")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    status = "🟢 مفعل" if data["bot_active"] else "🔴 معطل"
    await update.message.reply_text(
        f"⚙️ **لوحة التحكم**\n\n"
        f"👨‍💻 المطور: @SSSTlF\n"
        f"📊 المستخدمين: {data['total_users']}\n"
        f"🚫 المحظورين: {len(data['banned_users'])}\n"
        f"📌 الحالة: {status}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        
        data = load_data()
        user_id = query.from_user.id
        
        if str(user_id) in data["banned_users"] and user_id != DEVELOPER_ID:
            await query.edit_message_text("🚫 **أنت محظور.**", parse_mode="Markdown")
            return
        
        if not data["bot_active"] and user_id != DEVELOPER_ID:
            await query.edit_message_text("⏸️ **البوت معطل.**", parse_mode="Markdown")
            return
        
        data_callback = query.data
        user_name = query.from_user.first_name
        username = query.from_user.username
        
        # ========== أزرار الردود السريعة ==========
        if data_callback.startswith("quick_reply_"):
            parts = data_callback.split('_')
            reply_index = int(parts[2])
            target_user_id = int(parts[3])
            
            reply_text = QUICK_REPLIES[reply_index][0]
            
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"📩 **رد من المطور @SSSTlF**\n\n{reply_text}",
                    parse_mode="Markdown"
                )
                
                await query.edit_message_text(
                    f"✅ **تم الإرسال!**\n👤 `{target_user_id}`\n📝 {reply_text}",
                    parse_mode="Markdown"
                )
            except Exception as e:
                await query.edit_message_text(
                    f"❌ **خطأ:** لم يتمكن البوت من إرسال الرد.",
                    parse_mode="Markdown"
                )
            return
        
        # ========== أزرار الرد المخصص ==========
        elif data_callback.startswith("custom_reply_"):
            target_user_id = int(data_callback.split('_')[2])
            context.user_data['replying_to'] = target_user_id
            context.user_data['waiting_for'] = 'custom_reply'
            
            await query.edit_message_text(
                f"✏️ **أرسل ردك المخصص**\n\n👤 المستخدم: `{target_user_id}`\n\nلإلغاء: /cancel",
                parse_mode="Markdown"
            )
            return
        
        # ========== عرض جميع الرسائل ==========
        elif data_callback == "show_all_messages":
            if user_id != DEVELOPER_ID:
                return
            
            replies = load_replies()
            
            if not replies:
                await query.edit_message_text("📭 **لا توجد رسائل.**", parse_mode="Markdown")
                return
            
            message_list = []
            for uid, msg_data in list(replies.items())[-10:]:
                message_list.append(
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 {msg_data['name']}\n"
                    f"🆔 `{uid}`\n"
                    f"📝 {msg_data['message'][:50]}...\n"
                    f"⏰ {msg_data['time']}"
                )
            
            messages_text = "\n".join(message_list)
            
            keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"📋 **آخر الرسائل ({len(replies)})**\n\n{messages_text}",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            return
        
        # ========== أزرار الإرسال ==========
        if data_callback == "send_message":
            context.user_data['waiting_for'] = 'message_to_dev'
            await query.edit_message_text(
                f"📝 **أرسل رسالتك الآن**\n\n"
                f"للمطور @SSSTlF\n"
                f"⚠️ المحتوى المخالف = حظر فوري",
                parse_mode="Markdown"
            )
        
        elif data_callback == "send_photo":
            context.user_data['waiting_for'] = 'photo_to_dev'
            await query.edit_message_text(
                f"🖼️ **أرسل الصورة الآن**\n\n"
                f"للمطور @SSSTlF\n"
                f"⚠️ المحتوى المخالف = حظر فوري",
                parse_mode="Markdown"
            )
        
        elif data_callback == "send_video":
            context.user_data['waiting_for'] = 'video_to_dev'
            await query.edit_message_text(
                f"🎥 **أرسل الفيديو الآن**\n\n"
                f"للمطور @SSSTlF\n"
                f"⚠️ المحتوى المخالف = حظر فوري",
                parse_mode="Markdown"
            )
        
        elif data_callback == "send_audio":
            context.user_data['waiting_for'] = 'audio_to_dev'
            await query.edit_message_text(
                f"🎵 **أرسل الصوت الآن**\n\n"
                f"للمطور @SSSTlF\n"
                f"⚠️ المحتوى المخالف = حظر فوري",
                parse_mode="Markdown"
            )
        
        elif data_callback == "back_to_start":
            keyboard = [
                [InlineKeyboardButton("📩 إرسال رسالة", callback_data="send_message")],
                [InlineKeyboardButton("🖼️ إرسال صورة", callback_data="send_photo")],
                [InlineKeyboardButton("🎥 إرسال فيديو", callback_data="send_video")],
                [InlineKeyboardButton("🎵 إرسال صوت", callback_data="send_audio")],
            ]
            if user_id == DEVELOPER_ID:
                keyboard.append([InlineKeyboardButton("⚙️ لوحة التحكم", callback_data="admin_panel")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"📩 **بوت التواصل مع المطور**\n\n"
                f"👨‍💻 **المطور:** @SSSTlF\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"📌 **اختر نوع الملف المراد إرساله:**\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
                f"📝 رسالة نصية\n"
                f"🖼️ صورة\n"
                f"🎥 فيديو\n"
                f"🎵 ملف صوتي\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        # ========== لوحة تحكم المطور ==========
        elif data_callback == "admin_panel" and user_id == DEVELOPER_ID:
            keyboard = [
                [InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")],
                [InlineKeyboardButton("⏸️ تعطيل البوت", callback_data="admin_disable")] if data["bot_active"] else [InlineKeyboardButton("▶️ تفعيل البوت", callback_data="admin_enable")],
                [InlineKeyboardButton("🚫 حظر مستخدم", callback_data="admin_ban")],
                [InlineKeyboardButton("✅ الغاء حظر", callback_data="admin_unban")],
                [InlineKeyboardButton("📋 المحظورين", callback_data="admin_banned_list")],
                [InlineKeyboardButton("📩 جميع الرسائل", callback_data="show_all_messages")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            status = "🟢 مفعل" if data["bot_active"] else "🔴 معطل"
            await query.edit_message_text(
                f"⚙️ **لوحة التحكم**\n\n"
                f"👨‍💻 المطور: @SSSTlF\n"
                f"📊 المستخدمين: {data['total_users']}\n"
                f"🚫 المحظورين: {len(data['banned_users'])}\n"
                f"📌 الحالة: {status}",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif data_callback == "admin_stats" and user_id == DEVELOPER_ID:
            keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"📊 **الإحصائيات**\n\n"
                f"👥 المستخدمين: {data['total_users']}\n"
                f"🚫 المحظورين: {len(data['banned_users'])}\n"
                f"📌 الحالة: {'🟢 مفعل' if data['bot_active'] else '🔴 معطل'}\n"
                f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif data_callback == "admin_disable" and user_id == DEVELOPER_ID:
            data["bot_active"] = False
            save_data(data)
            await query.edit_message_text("⏸️ **تم تعطيل البوت!**", parse_mode="Markdown")
        
        elif data_callback == "admin_enable" and user_id == DEVELOPER_ID:
            data["bot_active"] = True
            save_data(data)
            await query.edit_message_text("▶️ **تم تفعيل البوت!**", parse_mode="Markdown")
        
        elif data_callback == "admin_ban" and user_id == DEVELOPER_ID:
            context.user_data['waiting_for'] = 'ban_user'
            await query.edit_message_text(
                "🚫 **حظر مستخدم**\n\nأرسل الآيدي:\nمثال: `123456789`\nلإلغاء: /cancel",
                parse_mode="Markdown"
            )
        
        elif data_callback == "admin_unban" and user_id == DEVELOPER_ID:
            context.user_data['waiting_for'] = 'unban_user'
            await query.edit_message_text(
                "✅ **الغاء حظر**\n\nأرسل الآيدي:\nمثال: `123456789`\nلإلغاء: /cancel",
                parse_mode="Markdown"
            )
        
        elif data_callback == "admin_banned_list" and user_id == DEVELOPER_ID:
            keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if data["banned_users"]:
                banned_list = "\n".join([f"🚫 `{uid}`" for uid in data["banned_users"]])
                await query.edit_message_text(
                    f"📋 **المحظورين**\n\n{banned_list}\n\nالعدد: {len(data['banned_users'])}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            else:
                await query.edit_message_text(
                    "✅ **لا يوجد محظورين.**",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
    except Exception as e:
        logging.error(f"Error in button_handler: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        username = update.message.from_user.username
        user_message = update.message.text
        
        if user_message and user_message.lower() == "/cancel":
            context.user_data['waiting_for'] = None
            context.user_data['replying_to'] = None
            await update.message.reply_text("❌ **تم الإلغاء.**", parse_mode="Markdown")
            return
        
        data = load_data()
        
        if str(user_id) in data["banned_users"] and user_id != DEVELOPER_ID:
            await update.message.reply_text("🚫 **أنت محظور.**", parse_mode="Markdown")
            return
        
        if not data["bot_active"] and user_id != DEVELOPER_ID:
            await update.message.reply_text("⏸️ **البوت معطل.**", parse_mode="Markdown")
            return
        
        # ========== معالج الرد المخصص من المطور ==========
        if user_id == DEVELOPER_ID and context.user_data.get('waiting_for') == 'custom_reply':
            target_user_id = context.user_data.get('replying_to')
            reply_text = user_message
            
            if not target_user_id:
                await update.message.reply_text("❌ لا يوجد مستهدف.", parse_mode="Markdown")
                context.user_data['waiting_for'] = None
                return
            
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"📩 **رد من المطور @SSSTlF**\n\n{reply_text}",
                    parse_mode="Markdown"
                )
                
                await update.message.reply_text(
                    f"✅ **تم الإرسال!**\n👤 `{target_user_id}`\n📝 {reply_text}",
                    parse_mode="Markdown"
                )
            except Exception as e:
                await update.message.reply_text(
                    f"❌ **خطأ:** لم يتمكن البوت من إرسال الرد.",
                    parse_mode="Markdown"
                )
            
            context.user_data['waiting_for'] = None
            context.user_data['replying_to'] = None
            return
        
        # ========== أوامر المطور ==========
        if user_id == DEVELOPER_ID:
            if context.user_data.get('waiting_for') == 'ban_user':
                try:
                    target_id = int(user_message.strip())
                    if str(target_id) not in data["banned_users"]:
                        data["banned_users"].append(str(target_id))
                        save_data(data)
                        await update.message.reply_text(f"✅ **تم حظر `{target_id}`**", parse_mode="Markdown")
                    else:
                        await update.message.reply_text("⚠️ **محظور بالفعل.**", parse_mode="Markdown")
                    context.user_data['waiting_for'] = None
                except ValueError:
                    await update.message.reply_text("❌ **أرسل أرقام فقط.**", parse_mode="Markdown")
                return
            
            elif context.user_data.get('waiting_for') == 'unban_user':
                try:
                    target_id = int(user_message.strip())
                    if str(target_id) in data["banned_users"]:
                        data["banned_users"].remove(str(target_id))
                        save_data(data)
                        await update.message.reply_text(f"✅ **تم الغاء حظر `{target_id}`**", parse_mode="Markdown")
                    else:
                        await update.message.reply_text("⚠️ **غير محظور.**", parse_mode="Markdown")
                    context.user_data['waiting_for'] = None
                except ValueError:
                    await update.message.reply_text("❌ **أرسل أرقام فقط.**", parse_mode="Markdown")
                return
        
        # ========== إرسال رسالة للمطور ==========
        if context.user_data.get('waiting_for') == 'message_to_dev':
            try:
                replies = load_replies()
                replies[str(user_id)] = {
                    "name": user_name,
                    "username": username,
                    "message": user_message,
                    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "user_id": user_id
                }
                save_replies(replies)
                
                quick_buttons = []
                for i, reply in enumerate(QUICK_REPLIES):
                    quick_buttons.append([
                        InlineKeyboardButton(f"{reply[0][:20]}...", callback_data=f"quick_reply_{i}_{user_id}")
                    ])
                
                quick_buttons.append([
                    InlineKeyboardButton("✏️ رد مخصص", callback_data=f"custom_reply_{user_id}"),
                    InlineKeyboardButton("📋 جميع الرسائل", callback_data="show_all_messages")
                ])
                quick_buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")])
                
                reply_markup = InlineKeyboardMarkup(quick_buttons)
                
                await context.bot.send_message(
                    chat_id=DEVELOPER_ID,
                    text=f"📩 **رسالة جديدة**\n\n"
                         f"👤 {user_name}\n"
                         f"🆔 @{username if username else 'لا يوجد'}\n"
                         f"🔢 `{user_id}`\n\n"
                         f"📝 {user_message}\n\n"
                         f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
                
                await update.message.reply_text(
                    f"✅ **تم الإرسال!**\n\n📨 سيتم الرد عليك قريباً.",
                    parse_mode="Markdown"
                )
                
                context.user_data['waiting_for'] = None
                
            except Exception as e:
                await update.message.reply_text("❌ حدث خطأ.", parse_mode="Markdown")
                logging.error(f"Error: {e}")
            
            return
        
        # ========== ردود البوت ==========
        await update.message.reply_text(
            f"📩 **بوت التواصل مع المطور**\n\n"
            f"استخدم /start للتواصل مع @SSSTlF",
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Error in handle_message: {e}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        username = update.message.from_user.username
        photo_file = update.message.photo[-1]
        caption = update.message.caption or "بدون تعليق"
        
        data = load_data()
        
        if str(user_id) in data["banned_users"] and user_id != DEVELOPER_ID:
            await update.message.reply_text("🚫 محظور.", parse_mode="Markdown")
            return
        
        if context.user_data.get('waiting_for') == 'photo_to_dev':
            try:
                file = await context.bot.get_file(photo_file.file_id)
                file_path = f"photo_{user_id}_{photo_file.file_id}.jpg"
                await file.download_to_drive(file_path)
                
                await context.bot.send_photo(
                    chat_id=DEVELOPER_ID,
                    photo=open(file_path, 'rb'),
                    caption=f"🖼️ **صورة جديدة**\n\n"
                            f"👤 {user_name}\n"
                            f"🆔 @{username if username else 'لا يوجد'}\n"
                            f"🔢 `{user_id}`\n"
                            f"📝 {caption}\n"
                            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                await update.message.reply_text("✅ **تم الإرسال!**", parse_mode="Markdown")
                context.user_data['waiting_for'] = None
                
            except Exception as e:
                await update.message.reply_text("❌ حدث خطأ.", parse_mode="Markdown")
                logging.error(f"Error: {e}")
            
            return
        
        await update.message.reply_text("📸 استخدم /start للإرسال.", parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error in handle_photo: {e}")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        username = update.message.from_user.username
        video_file = update.message.video
        caption = update.message.caption or "بدون تعليق"
        
        data = load_data()
        
        if str(user_id) in data["banned_users"] and user_id != DEVELOPER_ID:
            await update.message.reply_text("🚫 محظور.", parse_mode="Markdown")
            return
        
        if context.user_data.get('waiting_for') == 'video_to_dev':
            try:
                file = await context.bot.get_file(video_file.file_id)
                file_path = f"video_{user_id}_{video_file.file_id}.mp4"
                await file.download_to_drive(file_path)
                
                await context.bot.send_video(
                    chat_id=DEVELOPER_ID,
                    video=open(file_path, 'rb'),
                    caption=f"🎥 **فيديو جديد**\n\n"
                            f"👤 {user_name}\n"
                            f"🆔 @{username if username else 'لا يوجد'}\n"
                            f"🔢 `{user_id}`\n"
                            f"📝 {caption}\n"
                            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                await update.message.reply_text("✅ **تم الإرسال!**", parse_mode="Markdown")
                context.user_data['waiting_for'] = None
                
            except Exception as e:
                await update.message.reply_text("❌ حدث خطأ.", parse_mode="Markdown")
                logging.error(f"Error: {e}")
            
            return
        
        await update.message.reply_text("🎥 استخدم /start للإرسال.", parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error in handle_video: {e}")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        username = update.message.from_user.username
        audio_file = update.message.audio
        caption = update.message.caption or "بدون تعليق"
        
        data = load_data()
        
        if str(user_id) in data["banned_users"] and user_id != DEVELOPER_ID:
            await update.message.reply_text("🚫 محظور.", parse_mode="Markdown")
            return
        
        if context.user_data.get('waiting_for') == 'audio_to_dev':
            try:
                file = await context.bot.get_file(audio_file.file_id)
                file_path = f"audio_{user_id}_{audio_file.file_id}.mp3"
                await file.download_to_drive(file_path)
                
                await context.bot.send_audio(
                    chat_id=DEVELOPER_ID,
                    audio=open(file_path, 'rb'),
                    caption=f"🎵 **ملف صوتي جديد**\n\n"
                            f"👤 {user_name}\n"
                            f"🆔 @{username if username else 'لا يوجد'}\n"
                            f"🔢 `{user_id}`\n"
                            f"📝 {caption}\n"
                            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                await update.message.reply_text("✅ **تم الإرسال!**", parse_mode="Markdown")
                context.user_data['waiting_for'] = None
                
            except Exception as e:
                await update.message.reply_text("❌ حدث خطأ.", parse_mode="Markdown")
                logging.error(f"Error: {e}")
            
            return
        
        await update.message.reply_text("🎵 استخدم /start للإرسال.", parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error in handle_audio: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📖 **المساعدة**\n\n"
        f"/start - القائمة الرئيسية\n"
        f"/help - هذه المساعدة\n"
        f"/dev - المطور\n"
        f"/panel - لوحة التحكم\n"
        f"/cancel - إلغاء العملية",
        parse_mode="Markdown"
    )

async def dev_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👨‍💻 **المطور**\n\n"
        f"البوت من تصميم:\n"
        f"✨ @SSSTlF ✨\n\n"
        f"📌 للتواصل: @SSSTlF",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['waiting_for'] = None
    context.user_data['replying_to'] = None
    await update.message.reply_text("❌ **تم الإلغاء.**", parse_mode="Markdown")

# ========== التشغيل الرئيسي ==========

def main():
    print("🚀 تشغيل بوت التواصل الذكي...")
    print(f"👨‍💻 المطور: @SSSTlF")
    
    if not os.path.exists(DATA_FILE):
        save_data({"users": [], "banned_users": [], "bot_active": True, "total_users": 0})
    
    if not os.path.exists(REPLIES_FILE):
        save_replies({})
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("dev", dev_command))
    app.add_handler(CommandHandler("panel", panel_command))
    app.add_handler(CommandHandler("cancel", cancel_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    
    print("✅ البوت يعمل الآن...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
