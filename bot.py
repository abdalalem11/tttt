import os
import logging
import random
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

# ========== قوائم المحتوى ==========
JOKES = [
    "😂 مرة واحد دخل مطعم، قال للجرسون: أعطيني أكل بدون ملح. قال الجرسون: مستحيل! قال: ليش؟ قال: لأن الأكل كله بدون ملح ما يمديني!",
    "😄 واحد سأل صاحبه: ليش السمك ما يطير؟ قال: لأن الجناحين حقته صغار!",
    "🤣 مرة واحد نام في المقبرة، صحى لقى نفسه ميت!",
    "😅 واحد راح للدكتور قال: دكتور أنا عندي مشكلة! قال: وش هي؟ قال: كل ما أنام أحلم أني أكتب اختبار!",
    "😂 مرة واحد سأل أخوه: ليش الكلب يلهث؟ قال: لأنه ما يقدر يفتح الشباك!",
]

TIPS = [
    "💡 نصيحة: ابتسم فأنت جميل بأخلاقك قبل ملامحك.",
    "💡 نصيحة: النوم المبكر يحسن صحتك ومزاجك.",
    "💡 نصيحة: اقضِ 10 دقائق يومياً في القراءة، ستغير حياتك.",
    "💡 نصيحة: تواصل مع أهلك، فالوقت لا يعود.",
    "💡 نصيحة: تعلم شيئاً جديداً كل يوم.",
    "💡 نصيحة: الصدق يريح القلب ويجلب الاحترام.",
    "💡 نصيحة: المشي لمدة 30 دقيقة يومياً يقوي صحتك.",
]

RELIGIOUS = [
    "🕌 {ربنا لا تزغ قلوبنا بعد إذ هديتنا وهب لنا من لدنك رحمة إنك أنت الوهاب} [آل عمران: 8]",
    "🕌 {وأن ليس للإنسان إلا ما سعى} [النجم: 39]",
    "🕌 {إن مع العسر يسراً} [الشرح: 6]",
    "🕌 {فإن مع العسر يسراً} [الشرح: 5]",
    "🕌 {إن الله مع الصابرين} [البقرة: 153]",
    "🕌 {وَلَا تَهِنُوا وَلَا تَحْزَنُوا وَأَنتُمُ الْأَعْلَوْنَ إِن كُنتُم مُّؤْمِنِينَ} [آل عمران: 139]",
    "🕌 {وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا} [الطلاق: 2]",
]

LOVE = [
    "❤️ أنت أجمل ما في حياتي، كل لحظة معك هي حلم تحقق.",
    "❤️ أحبك ليس لأنك جميل، بل لأن روحك تشبه القمر في ظلمة الليل.",
    "❤️ لو كان الحب كلمات، لكنت كتبت عنك ألف كتاب.",
    "❤️ ابتسامتك هي سبب سعادتي، وهي نور عيني.",
    "❤️ عندما أراك، أنسى كل همومي وتصبح الدنيا أجمل.",
    "❤️ كل يوم يمر وأنا أشكر الله على وجودك في حياتي.",
    "❤️ أنت الحب الذي لم أكن أعرف أنني بحاجة إليه.",
]

TELEGRAM_FACTS = [
    "📱 تأسس تليجرام في عام 2013 على يد الأخوين دواروف.",
    "📱 تليجرام يدعم البوتات التي تسهل الحياة اليومية.",
    "📱 يمكنك إنشاء قنوات غير محدودة الأعضاء على تليجرام.",
    "📱 تليجرام يوفر تشفيراً كاملاً للمحادثات السرية.",
    "📱 يمكنك إرسال ملفات بحجم يصل إلى 2 جيجابايت على تليجرام.",
    "📱 تليجرام يعمل على جميع الأجهزة والأنظمة.",
    "📱 تليجرام لديه أكثر من 700 مليون مستخدم نشط حول العالم.",
]

# ========== دوال الذكاء الاصطناعي ==========
def get_ai_response(user_message):
    user_message = user_message.lower()
    
    if "مرحبا" in user_message or "السلام" in user_message:
        return "👋 وعليكم السلام! كيف يمكنني مساعدتك اليوم؟"
    
    if "كيف حالك" in user_message:
        return "🙂 أنا بخير والحمد لله! شكراً لسؤالك، وأنت كيف حالك؟"
    
    if "شكرا" in user_message or "مشكور" in user_message:
        return "🤍 الشكر لله، ولو! أنا هنا لخدمتك دائماً."
    
    if "ما اسمك" in user_message:
        return "🤖 أنا بوت التواصل الذكي، صممته لأقدم لك المساعدة والمتعة!"
    
    if "من انت" in user_message:
        return "🌟 أنا بوت ذكي، تم تطويره لتقديم النصائح، النكت، والردود المفيدة."
    
    if "باي" in user_message or "مع السلامة" in user_message:
        return "👋 مع السلامة! أتمنى لك يوماً سعيداً، عد متى شئت."
    
    if "الحب" in user_message:
        return random.choice(LOVE)
    
    if "نصيحة" in user_message:
        return random.choice(TIPS)
    
    if "نكتة" in user_message:
        return random.choice(JOKES)
    
    return f"🤔 فكرت في رسالتك: \"{user_message}\"\n\nما رأيك تجرب الأزرار في /start 😊"

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
        
        keyboard = [
            [InlineKeyboardButton("🤖 ذكاء", callback_data="ai"), InlineKeyboardButton("😂 نكتة", callback_data="joke")],
            [InlineKeyboardButton("🕌 ديني", callback_data="religious"), InlineKeyboardButton("💡 نصيحة", callback_data="tip")],
            [InlineKeyboardButton("❤️ حب", callback_data="love"), InlineKeyboardButton("📱 تليجرام", callback_data="telegram")],
            [InlineKeyboardButton("📩 المطور", callback_data="contact_dev")],
        ]
        
        # إضافة زر لوحة التحكم للمطور فقط
        if user_id == DEVELOPER_ID:
            keyboard.append([InlineKeyboardButton("⚙️ التحكم", callback_data="admin_panel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"👑 **بوت التواصل الذكي** 👑\n\n"
            f"✧ مطوري: @SSSTlF ✧\n\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🤖 ذكاء  •  😂 نكتة\n"
            f"🕌 ديني  •  💡 نصيحة\n"
            f"❤️ حب  •  📱 تليجرام\n"
            f"📩 تواصل مع المطور\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            f"✨ أرسل وسأرد بذكاء",
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
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    status = "🟢 مفعل" if data["bot_active"] else "🔴 معطل"
    await update.message.reply_text(
        f"⚙️ **لوحة التحكم**\n\n"
        f"👨‍💻 المطور: @SSSTlF\n"
        f"📊 المستخدمين: {data['total_users']}\n"
        f"🚫 المحظورين: {len(data['banned_users'])}\n"
        f"📌 الحالة: {status}\n\n"
        f"اختر الإجراء:",
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
        
        if data_callback == "ai":
            await query.edit_message_text(
                "🤖 **مرحباً! أنا الذكاء الاصطناعي هنا.**\n\n"
                "أرسل لي أي سؤال أو رسالة وسأرد عليك بأفضل شكل. 🌟",
                parse_mode="Markdown"
            )
        
        elif data_callback == "joke":
            await query.edit_message_text(
                f"😂 **نكتة اليوم** 😂\n\n{random.choice(JOKES)}",
                parse_mode="Markdown"
            )
        
        elif data_callback == "religious":
            await query.edit_message_text(
                f"🕌 **اقتباس ديني** 🕌\n\n{random.choice(RELIGIOUS)}",
                parse_mode="Markdown"
            )
        
        elif data_callback == "tip":
            await query.edit_message_text(
                f"💡 **نصيحة اليوم** 💡\n\n{random.choice(TIPS)}",
                parse_mode="Markdown"
            )
        
        elif data_callback == "love":
            await query.edit_message_text(
                f"❤️ **رسالة حب** ❤️\n\n{random.choice(LOVE)}\n\nلك {user_name} 💫",
                parse_mode="Markdown"
            )
        
        elif data_callback == "telegram":
            await query.edit_message_text(
                f"📱 **معلومة عن تليجرام** 📱\n\n{random.choice(TELEGRAM_FACTS)}",
                parse_mode="Markdown"
            )
        
        elif data_callback == "contact_dev":
            keyboard = [
                [InlineKeyboardButton("📝 رسالة", callback_data="send_message")],
                [InlineKeyboardButton("🖼️ صورة", callback_data="send_photo")],
                [InlineKeyboardButton("🎥 فيديو", callback_data="send_video")],
                [InlineKeyboardButton("🎵 صوت", callback_data="send_audio")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"📩 **التواصل مع المطور**\n\n"
                f"👨‍💻 المطور: @SSSTlF\n\n"
                f"⚠️ **تنبيه:**\n"
                f"المحتوى المخالف يؤدي إلى الحظر الفوري.\n\n"
                f"اختر نوع الملف:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif data_callback == "send_message":
            context.user_data['waiting_for'] = 'message_to_dev'
            await query.edit_message_text(
                f"📝 **أرسل رسالتك الآن**\n\n"
                f"للمطور @SSSTlF\n\n"
                f"⚠️ المحتوى المخالف = حظر فوري\n\n"
                f"⏳ انتظر... سأرسلها فوراً.",
                parse_mode="Markdown"
            )
        
        elif data_callback == "send_photo":
            context.user_data['waiting_for'] = 'photo_to_dev'
            await query.edit_message_text(
                f"🖼️ **أرسل الصورة الآن**\n\n"
                f"للمطور @SSSTlF\n\n"
                f"⚠️ المحتوى المخالف = حظر فوري\n\n"
                f"💬 يمكنك إضافة تعليق.",
                parse_mode="Markdown"
            )
        
        elif data_callback == "send_video":
            context.user_data['waiting_for'] = 'video_to_dev'
            await query.edit_message_text(
                f"🎥 **أرسل الفيديو الآن**\n\n"
                f"للمطور @SSSTlF\n\n"
                f"⚠️ المحتوى المخالف = حظر فوري\n\n"
                f"💬 يمكنك إضافة تعليق.",
                parse_mode="Markdown"
            )
        
        elif data_callback == "send_audio":
            context.user_data['waiting_for'] = 'audio_to_dev'
            await query.edit_message_text(
                f"🎵 **أرسل الصوت الآن**\n\n"
                f"للمطور @SSSTlF\n\n"
                f"⚠️ المحتوى المخالف = حظر فوري\n\n"
                f"💬 يمكنك إضافة تعليق.",
                parse_mode="Markdown"
            )
        
        elif data_callback == "back_to_start":
            keyboard = [
                [InlineKeyboardButton("🤖 ذكاء", callback_data="ai"), InlineKeyboardButton("😂 نكتة", callback_data="joke")],
                [InlineKeyboardButton("🕌 ديني", callback_data="religious"), InlineKeyboardButton("💡 نصيحة", callback_data="tip")],
                [InlineKeyboardButton("❤️ حب", callback_data="love"), InlineKeyboardButton("📱 تليجرام", callback_data="telegram")],
                [InlineKeyboardButton("📩 المطور", callback_data="contact_dev")],
            ]
            if user_id == DEVELOPER_ID:
                keyboard.append([InlineKeyboardButton("⚙️ التحكم", callback_data="admin_panel")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"👑 **بوت التواصل الذكي** 👑\n\n"
                f"✧ مطوري: @SSSTlF ✧\n\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"🤖 ذكاء  •  😂 نكتة\n"
                f"🕌 ديني  •  💡 نصيحة\n"
                f"❤️ حب  •  📱 تليجرام\n"
                f"📩 تواصل مع المطور\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
                f"✨ أرسل وسأرد بذكاء",
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
                [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            status = "🟢 مفعل" if data["bot_active"] else "🔴 معطل"
            await query.edit_message_text(
                f"⚙️ **لوحة التحكم**\n\n"
                f"👨‍💻 المطور: @SSSTlF\n"
                f"📊 المستخدمين: {data['total_users']}\n"
                f"🚫 المحظورين: {len(data['banned_users'])}\n"
                f"📌 الحالة: {status}\n\n"
                f"اختر الإجراء:",
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
                # إرسال للمطور مع جميع المعلومات
                await context.bot.send_message(
                    chat_id=DEVELOPER_ID,
                    text=f"📩 **رسالة جديدة**\n\n"
                         f"━━━━━━━━━━━━━━━━━━━\n"
                         f"👤 {user_name}\n"
                         f"🆔 @{username if username else 'لا يوجد'}\n"
                         f"🔢 `{user_id}`\n"
                         f"━━━━━━━━━━━━━━━━━━━\n\n"
                         f"📝 {user_message}\n\n"
                         f"━━━━━━━━━━━━━━━━━━━\n"
                         f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    parse_mode="Markdown"
                )
                
                # تأكيد للمستخدم
                await update.message.reply_text(
                    f"✅ **تم الإرسال بنجاح!**\n\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 {user_name}\n"
                    f"🆔 @{username if username else 'لا يوجد'}\n"
                    f"🔢 `{user_id}`\n"
                    f"━━━━━━━━━━━━━━━━━━━\n\n"
                    f"📝 {user_message}\n\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"شكراً لتواصلك مع @SSSTlF 🙏",
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
        
        ai_reply = get_ai_response(user_message)
        await update.message.reply_text(ai_reply, parse_mode="Markdown")
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
                    caption=f"🖼️ **صورة جديدة**\n\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"👤 {user_name}\n"
                            f"🆔 @{username if username else 'لا يوجد'}\n"
                            f"🔢 `{user_id}`\n"
                            f"━━━━━━━━━━━━━━━━━━━\n\n"
                            f"📝 {caption}\n\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
            "📸 صورة جميلة! استخدم زر '📩 المطور' لإرسالها.",
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
                    caption=f"🎥 **فيديو جديد**\n\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"👤 {user_name}\n"
                            f"🆔 @{username if username else 'لا يوجد'}\n"
                            f"🔢 `{user_id}`\n"
                            f"━━━━━━━━━━━━━━━━━━━\n\n"
                            f"📝 {caption}\n\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
            "🎥 فيديو رائع! استخدم زر '📩 المطور' لإرساله.",
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
                    caption=f"🎵 **ملف صوتي جديد**\n\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"👤 {user_name}\n"
                            f"🆔 @{username if username else 'لا يوجد'}\n"
                            f"🔢 `{user_id}`\n"
                            f"━━━━━━━━━━━━━━━━━━━\n\n"
                            f"📝 {caption}\n\n"
                            f"━━━━━━━━━━━━━━━━━━━\n"
                            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
            "🎵 ملف صوتي جميل! استخدم زر '📩 المطور' لإرساله.",
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Error in handle_audio: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **الأوامر:**\n\n"
        "/start - القائمة الرئيسية\n"
        "/help - هذه المساعدة\n"
        "/dev - المطور\n"
        "/panel - لوحة التحكم\n"
        "/cancel - إلغاء العملية\n\n"
        "📩 للتواصل مع المطور استخدم الزر.",
        parse_mode="Markdown"
    )

async def dev_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👨‍💻 **المطور**\n\n"
        f"البوت من تصميم:\n"
        f"✨ @SSSTlF ✨\n\n"
        f"📌 للتواصل: @SSSTlF\n\n"
        f"شكراً لاستخدامك! ❤️",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['waiting_for'] = None
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
    
    # إنشاء ملف البيانات إذا لم يكن موجوداً
    if not os.path.exists(DATA_FILE):
        save_data({"users": [], "banned_users": [], "bot_active": True, "total_users": 0})
    
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
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
