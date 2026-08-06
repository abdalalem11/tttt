import os
import logging
import random
import requests
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)

# التوكن من متغيرات البيئة
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN غير موجود!")

# ========== قوائم المحتوى ==========

# نكت
JOKES = [
    "😂 مرة واحد دخل مطعم، قال للجرسون: أعطيني أكل بدون ملح. قال الجرسون: مستحيل! قال: ليش؟ قال: لأن الأكل كله بدون ملح ما يمديني!",
    "😄 واحد سأل صاحبه: ليش السمك ما يطير؟ قال: لأن الجناحين حقته صغار!",
    "🤣 مرة واحد نام في المقبرة، صحى لقى نفسه ميت!",
    "😅 واحد راح للدكتور قال: دكتور أنا عندي مشكلة! قال: وش هي؟ قال: كل ما أنام أحلم أني أكتب اختبار!",
    "😂 مرة واحد سأل أخوه: ليش الكلب يلهث؟ قال: لأنه ما يقدر يفتح الشباك!",
]

# نصائح
TIPS = [
    "💡 نصيحة: ابتسم فأنت جميل بأخلاقك قبل ملامحك.",
    "💡 نصيحة: النوم المبكر يحسن صحتك ومزاجك.",
    "💡 نصيحة: اقضِ 10 دقائق يومياً في القراءة، ستغير حياتك.",
    "💡 نصيحة: تواصل مع أهلك، فالوقت لا يعود.",
    "💡 نصيحة: تعلم شيئاً جديداً كل يوم.",
    "💡 نصيحة: الصدق يريح القلب ويجلب الاحترام.",
    "💡 نصيحة: المشي لمدة 30 دقيقة يومياً يقوي صحتك.",
]

# اقتباسات دينية
RELIGIOUS = [
    "🕌 {ربنا لا تزغ قلوبنا بعد إذ هديتنا وهب لنا من لدنك رحمة إنك أنت الوهاب} [آل عمران: 8]",
    "🕌 {وأن ليس للإنسان إلا ما سعى} [النجم: 39]",
    "🕌 {إن مع العسر يسراً} [الشرح: 6]",
    "🕌 {فإن مع العسر يسراً} [الشرح: 5]",
    "🕌 {إن الله مع الصابرين} [البقرة: 153]",
    "🕌 {وَلَا تَهِنُوا وَلَا تَحْزَنُوا وَأَنتُمُ الْأَعْلَوْنَ إِن كُنتُم مُّؤْمِنِينَ} [آل عمران: 139]",
    "🕌 {وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا} [الطلاق: 2]",
]

# رسائل حب
LOVE = [
    "❤️ أنت أجمل ما في حياتي، كل لحظة معك هي حلم تحقق.",
    "❤️ أحبك ليس لأنك جميل، بل لأن روحك تشبه القمر في ظلمة الليل.",
    "❤️ لو كان الحب كلمات، لكنت كتبت عنك ألف كتاب.",
    "❤️ ابتسامتك هي سبب سعادتي، وهي نور عيني.",
    "❤️ عندما أراك، أنسى كل همومي وتصبح الدنيا أجمل.",
    "❤️ كل يوم يمر وأنا أشكر الله على وجودك في حياتي.",
    "❤️ أنت الحب الذي لم أكن أعرف أنني بحاجة إليه.",
]

# نبذات عن تليجرام
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
    """
    يحاكي الذكاء الاصطناعي بردود ذكية
    يمكنك استبداله بـ Gemini API أو OpenAI
    """
    user_message = user_message.lower()
    
    # ردود مبرمجة ذكية
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
    
    # رد عام ذكي
    return f"🤔 فكرت في رسالتك: \"{user_message}\"\n\n" \
           f"ما رأيك تجرب الأزرار الجميلة بالأسفل؟ 😊\n" \
           f"أو اسألني عن شيء آخر!"

# ========== دوال البوت ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إنشاء الأزرار المرتبة
    keyboard = [
        [
            InlineKeyboardButton("🤖 ذكاء اصطناعي", callback_data="ai"),
            InlineKeyboardButton("😂 نكتة", callback_data="joke"),
        ],
        [
            InlineKeyboardButton("🕌 ديني", callback_data="religious"),
            InlineKeyboardButton("💡 نصيحة", callback_data="tip"),
        ],
        [
            InlineKeyboardButton("❤️ حب", callback_data="love"),
            InlineKeyboardButton("📱 تليجرام", callback_data="telegram"),
        ],
        [
            InlineKeyboardButton("📝 تواصل مع المطور", url="https://t.me/u_t_r"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌟 **مرحباً بك في بوت التواصل الذكي!** 🌟\n\n"
        "أنا هنا لخدمتك، اختر من الأزرار الفخمة أدناه:\n"
        "🔹 للرد التلقائي الذكي\n"
        "🔹 للنكت والفكاهة\n"
        "🔹 للنصائح والإرشادات\n"
        "🔹 للاقتباسات الدينية\n"
        "🔹 لرسائل الحب\n"
        "🔹 لمعلومات عن تليجرام\n\n"
        "✨ أو أرسل أي رسالة وسأرد عليك بذكاء!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_name = query.from_user.first_name
    
    if data == "ai":
        await query.edit_message_text(
            "🤖 **مرحباً! أنا الذكاء الاصطناعي هنا.**\n\n"
            "أرسل لي أي سؤال أو رسالة وسأرد عليك بأفضل شكل. 🌟\n\n"
            "💡 جرب تسألني: من أنت؟ أو كيف الحال؟",
            parse_mode="Markdown"
        )
    
    elif data == "joke":
        joke = random.choice(JOKES)
        await query.edit_message_text(
            f"😂 **نكتة اليوم** 😂\n\n{joke}\n\n"
            f"اضغط الزر مرة ثانية لنكتة جديدة!",
            parse_mode="Markdown"
        )
    
    elif data == "religious":
        quote = random.choice(RELIGIOUS)
        await query.edit_message_text(
            f"🕌 **اقتباس ديني** 🕌\n\n{quote}\n\n"
            f"نسأل الله التوفيق والهداية للجميع. آمين.",
            parse_mode="Markdown"
        )
    
    elif data == "tip":
        tip = random.choice(TIPS)
        await query.edit_message_text(
            f"💡 **نصيحة اليوم** 💡\n\n{tip}\n\n"
            f"تمنى تفيدك وتنفعك!",
            parse_mode="Markdown"
        )
    
    elif data == "love":
        love_msg = random.choice(LOVE)
        await query.edit_message_text(
            f"❤️ **رسالة حب** ❤️\n\n{love_msg}\n\n"
            f"لك {user_name} 💫",
            parse_mode="Markdown"
        )
    
    elif data == "telegram":
        fact = random.choice(TELEGRAM_FACTS)
        await query.edit_message_text(
            f"📱 **معلومة عن تليجرام** 📱\n\n{fact}\n\n"
            f"تليجرام منصة رائعة للتواصل! 🚀",
            parse_mode="Markdown"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    
    # استخدام الذكاء الاصطناعي المبرمج
    ai_reply = get_ai_response(user_msg)
    
    # الأزرار بعد الرد
    keyboard = [
        [
            InlineKeyboardButton("🤖 ذكاء", callback_data="ai"),
            InlineKeyboardButton("😂 نكتة", callback_data="joke"),
        ],
        [
            InlineKeyboardButton("💡 نصيحة", callback_data="tip"),
            InlineKeyboardButton("❤️ حب", callback_data="love"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{ai_reply}\n\n"
        f"🔽 **اختر زراً للمزيد:**",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **الأوامر المتاحة:**\n\n"
        "/start - عرض الأزرار والبدء\n"
        "/help - عرض هذه المساعدة\n"
        "/dev - معلومات المطور\n\n"
        "💬 أو استخدم الأزرار الجميلة للتفاعل!",
        parse_mode="Markdown"
    )

async def dev_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👨‍💻 **المطور**\n\n"
        "هذا البوت من تصميم وتطوير:\n"
        "✨ @u_t_r ✨\n\n"
        "📌 للاستفسارات والتواصل:\n"
        "[اضغط هنا للتواصل](https://t.me/u_t_r)\n\n"
        "شكراً لاستخدامك البوت! ❤️",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# ========== التشغيل الرئيسي ==========

async def main():
    print("🚀 تشغيل بوت التواصل الذكي...")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("dev", dev_command))
    
    # معالج الأزرار
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # معالج الرسائل
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ البوت يعمل الآن...")
    
    # تشغيل البوت
    await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    # إنشاء حلقة أحداث جديدة وتشغيلها
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    finally:
        asyncio.run(main())
