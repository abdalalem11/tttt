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
        
        # تحميل البيانات
        data = load_data()
        
        # التحقق من الحظر
        if str(user_id) in data["banned_users"]:
            await update.message.reply_text(
                "🚫 **أنت محظور من استخدام هذا البوت.**\n"
                "للتواصل مع المطور: @SSSTlF",
                parse_mode="Markdown"
            )
            return
        
        # إضافة المستخدم إذا كان جديداً
        if str(user_id) not in data["users"]:
            data["users"].append(str(user_id))
            data["total_users"] = len(data["users"])
            save_data(data)
            
            # إرسال إشعار للمطور
            try:
                await context.bot.send_message(
                    chat_id=DEVELOPER_ID,
                    text=f"🆕 **مستخدم جديد دخل البوت!**\n\n"
                         f"━━━━━━━━━━━━━━━━━━━\n"
                         f"👤 **الاسم:** {user_name}\n"
                         f"🆔 **اليوزر:** @{username if username else 'لا يوجد'}\n"
                         f"🔢 **الايدي:** `{user_id}`\n"
                         f"━━━━━━━━━━━━━━━━━━━\n\n"
                         f"📊 إجمالي المستخدمين: {data['total_users']}\n"
                         f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    parse_mode="Markdown"
                )
            except:
                pass
        
        # تصميم فخم للرسالة
        keyboard = [
            [InlineKeyboardButton("📩 إرسال رسالة", callback_data="send_message")],
            [InlineKeyboardButton("🖼️ إرسال صورة", callback_data="send_photo")],
            [InlineKeyboardButton("🎥 إرسال فيديو", callback_data="send_video")],
            [InlineKeyboardButton("🎵 إرسال صوت", callback_data="send_audio")],
        ]
        
        # إضافة زر لوحة التحكم للمطور فقط
        if user_id == DEVELOPER_ID:
            keyboard.append([InlineKeyboardButton("⚙️ لوحة التحكم", callback_data="admin_panel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"╔══════════════════════════╗\n"
            f"║   🤖 بوت التواصل الذكي   ║\n"
            f"╚══════════════════════════╝\n\n"
            f"✨ **مرحباً بك {user_name}** ✨\n\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"📌 **هذا البوت مخصص للتواصل**\n"
            f"📌 **مع المطور @SSSTlF**\n\n"
            f"💫 **يمكنك إرسال:**\n"
            f"• رسالة نصية 📝\n"
            f"• صورة 🖼️\n"
            f"• فيديو 🎥\n"
            f"• ملف صوتي 🎵\n\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"⚡ **اختر نوع الملف المراد إرساله:**\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            f"🔹 **للاستفسارات والشكاوى**\n"
            f"🔹 **للمقترحات والتطوير**\n"
            f"🔹 **للتواصل المباشر**\n\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"👨‍💻 **المطور:** @SSSTlF\n"
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
        f"╔══════════════════════════╗\n"
        f"║    ⚙️ لوحة التحكم        ║\n"
        f"╚══════════════════════════╝\n\n"
        f"👨‍💻 **المطور:** @SSSTlF\n"
        f"📊 **المستخدمين:** {data['total_users']}\n"
        f"🚫 **المحظورين:** {len(data['banned_users'])}\n"
        f"📌 **الحالة:** {status}\n\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"اختر الإجراء المناسب:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        
        data = load_data()
        user_id = query.from_user.id
        
        # التحقق من الحظر
        if str(user_id) in data["banned_users"] and user_id != DEVELOPER_ID:
            await query.edit_message_text(
                "🚫 **أنت محظور من استخدام هذا البوت.**",
                parse_mode="Markdown"
            )
            return
        
        # التحقق من تفعيل البوت
        if not data["bot_active"] and user_id != DEVELOPER_ID:
            await query.edit_message_text(
                "⏸️ **البوت معطل حالياً.** يرجى المحاولة لاحقاً.",
                parse_mode="Markdown"
            )
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
            
            # إرسال الرد للمستخدم
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"╔══════════════════════════╗\n"
                         f"║   📩 رد من المطور        ║\n"
                         f"╚══════════════════════════╝\n\n"
                         f"{reply_text}\n\n"
                         f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                         f"✧ للرد على المطور: /start ✧",
                    parse_mode="Markdown"
                )
                
                # تأكيد للمطور
                await query.edit_message_text(
                    f"✅ **تم إرسال الرد السريع بنجاح!**\n\n"
                    f"👤 المستخدم: `{target_user_id}`\n"
                    f"📝 الرد: {reply_text}",
                    parse_mode="Markdown"
                )
            except Exception as e:
                await query.edit_message_text(
                    f"❌ **خطأ:** لم يتمكن البوت من إرسال الرد.\n"
                    f"تأكد من أن المستخدم بدأ البوت أولاً.",
                    parse_mode="Markdown"
                )
                logging.error(f"Error sending quick reply: {e}")
            return
        
        # ========== أزرار الرد المخصص ==========
        elif data_callback.startswith("custom_reply_"):
            target_user_id = int(data_callback.split('_')[2])
            
            # حفظ في السياق بأن المطور يريد الرد على هذا المستخدم
            context.user_data['replying_to'] = target_user_id
            context.user_data['waiting_for'] = 'custom_reply'
            
            await query.edit_message_text(
                f"✏️ **أرسل ردك المخصص الآن**\n\n"
                f"👤 المستخدم: `{target_user_id}`\n\n"
                f"📝 اكتب رسالتك وسأرسلها فوراً.\n\n"
                f"لإلغاء: /cancel",
                parse_mode="Markdown"
            )
            return
        
        # ========== عرض جميع الرسائل ==========
        elif data_callback == "show_all_messages":
            if user_id != DEVELOPER_ID:
                return
            
            replies = load_replies()
            
            if not replies:
                await query.edit_message_text(
                    "📭 **لا توجد رسائل حالياً.**",
                    parse_mode="Markdown"
                )
                return
            
            # عرض آخر 10 رسائل
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
                f"📋 **آخر الرسائل ({len(replies)} رسالة)**\n\n"
                f"{messages_text}\n\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"💡 للرد: استخدم زر الرد السريع",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            return
        
        # ========== أزرار الإرسال ==========
        if data_callback == "send_message":
            context.user_data['waiting_for'] = 'message_to_dev'
            await query.edit_message_text(
                f"╔══════════════════════════╗\n"
                f"║    📝 إرسال رسالة        ║\n"
                f"╚══════════════════════════╝\n\n"
                f"✍️ **أرسل رسالتك الآن**\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"📌 سيتم إرسالها للمطور @SSSTlF\n"
                f"⚠️ المحتوى المخالف = حظر فوري\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
                f"⏳ انتظر... سأرسلها فوراً.",
                parse_mode="Markdown"
            )
        
        elif data_callback == "send_photo":
            context.user_data['waiting_for'] = 'photo_to_dev'
            await query.edit_message_text(
                f"╔══════════════════════════╗\n"
                f"║    🖼️ إرسال صورة        ║\n"
                f"╚══════════════════════════╝\n\n"
                f"🖼️ **أرسل الصورة الآن**\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"📌 سيتم إرسالها للمطور @SSSTlF\n"
                f"⚠️ المحتوى المخالف = حظر فوري\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
                f"💬 يمكنك إضافة تعليق مع الصورة.",
                parse_mode="Markdown"
            )
        
        elif data_callback == "send_video":
            context.user_data['waiting_for'] = 'video_to_dev'
            await query.edit_message_text(
                f"╔══════════════════════════╗\n"
                f"║    🎥 إرسال فيديو        ║\n"
                f"╚══════════════════════════╝\n\n"
                f"🎥 **أرسل الفيديو الآن**\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"📌 سيتم إرساله للمطور @SSSTlF\n"
                f"⚠️ المحتوى المخالف = حظر فوري\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
                f"💬 يمكنك إضافة تعليق مع الفيديو.",
                parse_mode="Markdown"
            )
        
        elif data_callback == "send_audio":
            context.user_data['waiting_for'] = 'audio_to_dev'
            await query.edit_message_text(
                f"╔══════════════════════════╗\n"
                f"║    🎵 إرسال صوت         ║\n"
                f"╚══════════════════════════╝\n\n"
                f"🎵 **أرسل الملف الصوتي الآن**\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"📌 سيتم إرساله للمطور @SSSTlF\n"
                f"⚠️ المحتوى المخالف = حظر فوري\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
                f"💬 يمكنك إضافة تعليق مع الملف الصوتي.",
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
                f"╔══════════════════════════╗\n"
                f"║   🤖 بوت التواصل الذكي   ║\n"
                f"╚══════════════════════════╝\n\n"
                f"✨ **مرحباً بك {user_name}** ✨\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"📌 **هذا البوت مخصص للتواصل**\n"
                f"📌 **مع المطور @SSSTlF**\n\n"
                f"💫 **يمكنك إرسال:**\n"
                f"• رسالة نصية 📝\n"
                f"• صورة 🖼️\n"
                f"• فيديو 🎥\n"
                f"• ملف صوتي 🎵\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"⚡ **اختر نوع الملف المراد إرساله:**\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
                f"🔹 **للاستفسارات والشكاوى**\n"
                f"🔹 **للمقترحات والتطوير**\n"
                f"🔹 **للتواصل المباشر**\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"👨‍💻 **المطور:** @SSSTlF\n"
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
                f"╔══════════════════════════╗\n"
                f"║    ⚙️ لوحة التحكم        ║\n"
                f"╚══════════════════════════╝\n\n"
                f"👨‍💻 **المطور:** @SSSTlF\n"
                f"📊 **المستخدمين:** {data['total_users']}\n"
                f"🚫 **المحظورين:** {len(data['banned_users'])}\n"
                f"📌 **الحالة:** {status}\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"اختر الإجراء المناسب:",
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
            
            keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "⏸️ **تم تعطيل البوت بنجاح!**",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif data_callback == "admin_enable" and user_id == DEVELOPER_ID:
            data["bot_active"] = True
            save_data(data)
            
            keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "▶️ **تم تفعيل البوت بنجاح!**",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif data_callback == "admin_ban" and user_id == DEVELOPER_ID:
            context.user_data['waiting_for'] = 'ban_user'
            await query.edit_message_text(
                "🚫 **حظر مستخدم**\n\n"
                "أرسل **آيدي المستخدم**.\n"
                "مثال: `123456789`\n\n"
                "لإلغاء: /cancel",
                parse_mode="Markdown"
            )
        
        elif data_callback == "admin_unban" and user_id == DEVELOPER_ID:
            context.user_data['waiting_for'] = 'unban_user'
            await query.edit_message_text(
                "✅ **الغاء حظر**\n\n"
                "أرسل **آيدي المستخدم**.\n"
                "مثال: `123456789`\n\n"
                "لإلغاء: /cancel",
                parse_mode="Markdown"
            )
        
        elif data_callback == "admin_banned_list" and user_id == DEVELOPER_ID:
            keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if data["banned_users"]:
                banned_list = "\n".join([f"🚫 `{uid}`" for uid in data["banned_users"]])
                await query.edit_message_text(
                    f"📋 **المحظورين**\n\n"
                    f"{banned_list}\n\n"
                    f"العدد: {len(data['banned_users'])}",
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
        
        # التحقق من إلغاء الأمر
        if user_message and user_message.lower() == "/cancel":
            context.user_data['waiting_for'] = None
            context.user_data['replying_to'] = None
            await update.message.reply_text(
                "❌ **تم إلغاء العملية.**",
                parse_mode="Markdown"
            )
            return
        
        data = load_data()
        
        # التحقق من الحظر
        if str(user_id) in data["banned_users"] and user_id != DEVELOPER_ID:
            await update.message.reply_text(
                "🚫 **أنت محظور من استخدام هذا البوت.**\n"
                "للتواصل مع المطور: @SSSTlF",
                parse_mode="Markdown"
            )
            return
        
        # التحقق من تفعيل البوت
        if not data["bot_active"] and user_id != DEVELOPER_ID:
            await update.message.reply_text(
                "⏸️ **البوت معطل حالياً.** يرجى المحاولة لاحقاً.",
                parse_mode="Markdown"
            )
            return
        
        # ========== معالج الرد المخصص من المطور ==========
        if user_id == DEVELOPER_ID and context.user_data.get('waiting_for') == 'custom_reply':
            target_user_id = context.user_data.get('replying_to')
            reply_text = user_message
            
            if not target_user_id:
                await update.message.reply_text(
                    "❌ حدث خطأ: لا يوجد مستهدف للرد.",
                    parse_mode="Markdown"
                )
                context.user_data['waiting_for'] = None
                return
            
            # إرسال الرد للمستخدم
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"╔══════════════════════════╗\n"
                         f"║   📩 رد من المطور        ║\n"
                         f"╚══════════════════════════╝\n\n"
                         f"{reply_text}\n\n"
                         f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                         f"✧ للرد على المطور: /start ✧",
                    parse_mode="Markdown"
                )
                
                await update.message.reply_text(
                    f"✅ **تم إرسال الرد المخصص بنجاح!**\n\n"
                    f"👤 المستخدم: `{target_user_id}`\n"
                    f"📝 الرد:\n{reply_text}",
                    parse_mode="Markdown"
                )
            except Exception as e:
                await update.message.reply_text(
                    f"❌ **خطأ:** لم يتمكن البوت من إرسال الرد.\n"
                    f"تأكد من أن المستخدم بدأ البوت أولاً.",
                    parse_mode="Markdown"
                )
                logging.error(f"Error sending custom reply: {e}")
            
            # مسح البيانات
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
                        await update.message.reply_text(
                            f"✅ **تم حظر المستخدم بنجاح!**\n\n"
                            f"🆔 الآيدي: `{target_id}`",
                            parse_mode="Markdown"
                        )
                    else:
                        await update.message.reply_text(
                            "⚠️ **هذا المستخدم محظور بالفعل.**",
                            parse_mode="Markdown"
                        )
                    context.user_data['waiting_for'] = None
                except ValueError:
                    await update.message.reply_text(
                        "❌ **خطأ:** يرجى إرسال آيدي صحيح (أرقام فقط).",
                        parse_mode="Markdown"
                    )
                return
            
            elif context.user_data.get('waiting_for') == 'unban_user':
                try:
                    target_id = int(user_message.strip())
                    if str(target_id) in data["banned_users"]:
                        data["banned_users"].remove(str(target_id))
                        save_data(data)
                        await update.message.reply_text(
                            f"✅ **تم الغاء حظر المستخدم بنجاح!**\n\n"
                            f"🆔 الآيدي: `{target_id}`",
                            parse_mode="Markdown"
                        )
                    else:
                        await update.message.reply_text(
                            "⚠️ **هذا المستخدم غير محظور.**",
                            parse_mode="Markdown"
                        )
                    context.user_data['waiting_for'] = None
                except ValueError:
                    await update.message.reply_text(
                        "❌ **خطأ:** يرجى إرسال آيدي صحيح (أرقام فقط).",
                        parse_mode="Markdown"
                    )
                return
        
        # ========== إرسال رسالة للمطور ==========
        if context.user_data.get('waiting_for') == 'message_to_dev':
            try:
                # حفظ معلومات المستخدم للرد عليه لاحقاً
                replies = load_replies()
                replies[str(user_id)] = {
                    "name": user_name,
                    "username": username,
                    "message": user_message,
                    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "user_id": user_id
                }
                save_replies(replies)
                
                # إنشاء أزرار ردود سريعة للمطور
                quick_buttons = []
                for i, reply in enumerate(QUICK_REPLIES):
                    quick_buttons.append([
                        InlineKeyboardButton(
                            f"{reply[0][:20]}...", 
                            callback_data=f"quick_reply_{i}_{user_id}"
                        )
                    ])
                
                # أزرار إضافية
                quick_buttons.append([
                    InlineKeyboardButton("✏️ رد مخصص", callback_data=f"custom_reply_{user_id}"),
                    InlineKeyboardButton("📋 عرض جميع الرسائل", callback_data="show_all_messages")
                ])
                quick_buttons.append([
                    InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")
                ])
                
                reply_markup = InlineKeyboardMarkup(quick_buttons)
                
                # إرسال للمطور مع الأزرار
                await context.bot.send_message(
                    chat_id=DEVELOPER_ID,
                    text=f"╔══════════════════════════╗\n"
                         f"║   📩 رسالة جديدة         ║\n"
                         f"╚══════════════════════════╝\n\n"
                         f"👤 **الاسم:** {user_name}\n"
                         f"🆔 **اليوزر:** @{username if username else 'لا يوجد'}\n"
                         f"🔢 **الايدي:** `{user_id}`\n\n"
                         f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                         f"📝 **الرسالة:**\n"
                         f"{user_message}\n\n"
                         f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                         f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                         f"💡 اختر رداً سريعاً أو اكتب رداً مخصصاً:",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
                
                # تأكيد للمستخدم
                await update.message.reply_text(
                    f"╔══════════════════════════╗\n"
                    f"║    ✅ تم الإرسال بنجاح    ║\n"
                    f"╚══════════════════════════╝\n\n"
                    f"📨 **تم إرسال رسالتك بنجاح!**\n\n"
                    f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                    f"👤 **المرسل:** {user_name}\n"
                    f"🆔 **اليوزر:** @{username if username else 'لا يوجد'}\n"
                    f"🔢 **الايدي:** `{user_id}`\n"
                    f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
                    f"📝 **رسالتك:**\n{user_message}\n\n"
                    f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                    f"📨 سيتم الرد عليك قريباً من المطور @SSSTlF\n"
                    f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
                    parse_mode="Markdown"
                )
                
                context.user_data['waiting_for'] = None
                
            except Exception as e:
                await update.message.reply_text(
                    f"❌ عذراً، حدث خطأ أثناء إرسال الرسالة.",
                    parse_mode="Markdown"
                )
                logging.error(f"Error sending message to developer: {e}")
            
            return
        
        # ========== ردود البوت العادية ==========
        await update.message.reply_text(
            f"╔══════════════════════════╗\n"
            f"║   🤖 بوت التواصل الذكي   ║\n"
            f"╚══════════════════════════╝\n\n"
            f"📌 **هذا البوت مخصص للتواصل مع المطور**\n\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"💡 **لإرسال رسالة استخدم الأمر:**\n"
            f"📩 /start\n\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"👨‍💻 **المطور:** @SSSTlF\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
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
            await update.message.reply_text("🚫 أنت محظور.")
            return
        
        if context.user_data.get('waiting_for') == 'photo_to_dev':
            try:
                file = await context.bot.get_file(photo_file.file_id)
                file_path = f"photo_{user_id}_{photo_file.file_id}.jpg"
                await file.download_to_drive(file_path)
                
                await context.bot.send_photo(
                    chat_id=DEVELOPER_ID,
                    photo=open(file_path, 'rb'),
                    caption=f"╔══════════════════════════╗\n"
                            f"║   🖼️ صورة جديدة          ║\n"
                            f"╚══════════════════════════╝\n\n"
                            f"👤 {user_name}\n"
                            f"🆔 @{username if username else 'لا يوجد'}\n"
                            f"🔢 `{user_id}`\n\n"
                            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                            f"📝 {caption}\n\n"
                            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                            f"💡 للرد: استخدم /panel ثم اختر الرد المناسب"
                )
                
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                await update.message.reply_text(
                    f"✅ **تم إرسال الصورة بنجاح!**\n\n"
                    f"شكراً لتواصلك مع @SSSTlF 🙏",
                    parse_mode="Markdown"
                )
                
                context.user_data['waiting_for'] = None
                
            except Exception as e:
                await update.message.reply_text(
                    f"❌ عذراً، حدث خطأ أثناء إرسال الصورة.",
                    parse_mode="Markdown"
                )
                logging.error(f"Error sending photo: {e}")
            
            return
        
        await update.message.reply_text(
            "📸 صورة جميلة! استخدم /start لإرسالها للمطور.",
            parse_mode="Markdown"
        )
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
            await update.message.reply_text("🚫 أنت محظور.")
            return
        
        if context.user_data.get('waiting_for') == 'video_to_dev':
            try:
                file = await context.bot.get_file(video_file.file_id)
                file_path = f"video_{user_id}_{video_file.file_id}.mp4"
                await file.download_to_drive(file_path)
                
                await context.bot.send_video(
                    chat_id=DEVELOPER_ID,
                    video=open(file_path, 'rb'),
                    caption=f"╔══════════════════════════╗\n"
                            f"║   🎥 فيديو جديد          ║\n"
                            f"╚══════════════════════════╝\n\n"
                            f"👤 {user_name}\n"
                            f"🆔 @{username if username else 'لا يوجد'}\n"
                            f"🔢 `{user_id}`\n\n"
                            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                            f"📝 {caption}\n\n"
                            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                            f"💡 للرد: استخدم /panel ثم اختر الرد المناسب"
                )
                
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                await update.message.reply_text(
                    f"✅ **تم إرسال الفيديو بنجاح!**\n\n"
                    f"شكراً لتواصلك مع @SSSTlF 🙏",
                    parse_mode="Markdown"
                )
                
                context.user_data['waiting_for'] = None
                
            except Exception as e:
                await update.message.reply_text(
                    f"❌ عذراً، حدث خطأ أثناء إرسال الفيديو.",
                    parse_mode="Markdown"
                )
                logging.error(f"Error sending video: {e}")
            
            return
        
        await update.message.reply_text(
            "🎥 فيديو رائع! استخدم /start لإرساله للمطور.",
            parse_mode="Markdown"
        )
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
            await update.message.reply_text("🚫 أنت محظور.")
            return
        
        if context.user_data.get('waiting_for') == 'audio_to_dev':
            try:
                file = await context.bot.get_file(audio_file.file_id)
                file_path = f"audio_{user_id}_{audio_file.file_id}.mp3"
                await file.download_to_drive(file_path)
                
                await context.bot.send_audio(
                    chat_id=DEVELOPER_ID,
                    audio=open(file_path, 'rb'),
                    caption=f"╔══════════════════════════╗\n"
                            f"║   🎵 ملف صوتي جديد       ║\n"
                            f"╚══════════════════════════╝\n\n"
                            f"👤 {user_name}\n"
                            f"🆔 @{username if username else 'لا يوجد'}\n"
                            f"🔢 `{user_id}`\n\n"
                            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                            f"📝 {caption}\n\n"
                            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                            f"💡 للرد: استخدم /panel ثم اختر الرد المناسب"
                )
                
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                await update.message.reply_text(
                    f"✅ **تم إرسال الملف الصوتي بنجاح!**\n\n"
                    f"شكراً لتواصلك مع @SSSTlF 🙏",
                    parse_mode="Markdown"
                )
                
                context.user_data['waiting_for'] = None
                
            except Exception as e:
                await update.message.reply_text(
                    f"❌ عذراً، حدث خطأ أثناء إرسال الملف الصوتي.",
                    parse_mode="Markdown"
                )
                logging.error(f"Error sending audio: {e}")
            
            return
        
        await update.message.reply_text(
            "🎵 ملف صوتي جميل! استخدم /start لإرساله للمطور.",
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Error in handle_audio: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"╔══════════════════════════╗\n"
        f"║    📖 المساعدة           ║\n"
        f"╚══════════════════════════╝\n\n"
        f"📌 **الأوامر المتاحة:**\n\n"
        f"/start - القائمة الرئيسية\n"
        f"/help - عرض هذه المساعدة\n"
        f"/dev - معلومات المطور\n"
        f"/panel - لوحة التحكم (للمطور فقط)\n"
        f"/cancel - إلغاء العملية\n\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"📩 للتواصل مع المطور استخدم /start\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"👨‍💻 **المطور:** @SSSTlF\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        parse_mode="Markdown"
    )

async def dev_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"╔══════════════════════════╗\n"
        f"║    👨‍💻 المطور            ║\n"
        f"╚══════════════════════════╝\n\n"
        f"✨ **البوت من تصميم:**\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"👑 **@SSSTlF**\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
        f"📌 **للتواصل:** @SSSTlF\n\n"
        f"❤️ شكراً لاستخدامك البوت!\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['waiting_for'] = None
    context.user_data['replying_to'] = None
    await update.message.reply_text(
        "❌ **تم إلغاء العملية.**",
        parse_mode="Markdown"
    )

# ========== التشغيل الرئيسي ==========

def main():
    print("🚀 تشغيل بوت التواصل الذكي...")
    print(f"👨‍💻 المطور: @SSSTlF")
    print(f"🆔 ID المطور: {DEVELOPER_ID}")
    print(f"🤖 التوكن: {BOT_TOKEN[:10]}... (مخفي)")
    
    # إنشاء ملفات البيانات إذا لم تكن موجودة
    if not os.path.exists(DATA_FILE):
        save_data({"users": [], "banned_users": [], "bot_active": True, "total_users": 0})
    
    if not os.path.exists(REPLIES_FILE):
        save_replies({})
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("dev", dev_command))
    app.add_handler(CommandHandler("panel", panel_command))
    app.add_handler(CommandHandler("cancel", cancel_command))
    
    # معالج الأزرار
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # معالج الرسائل
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # معالج الصور
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # معالج الفيديو
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    
    # معالج الصوت
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    
    print("✅ البوت يعمل الآن...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
