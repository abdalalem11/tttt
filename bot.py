import os
import logging
import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)

# ========== التوكن الجديد ==========
BOT_TOKEN = "8760673859:AAF04DjMq2-mDSo33maG0cdUpa5TsiObddY"

# ========== إعدادات المطور ==========
DEVELOPER_USERNAME = "@u_t_r"
DEVELOPER_ID = 1170411845

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
    keyboard = [
        [InlineKeyboardButton("🤖 ذكاء اصطناعي", callback_data="ai"), InlineKeyboardButton("😂 نكتة", callback_data="joke")],
        [InlineKeyboardButton("🕌 ديني", callback_data="religious"), InlineKeyboardButton("💡 نصيحة", callback_data="tip")],
        [InlineKeyboardButton("❤️ حب", callback_data="love"), InlineKeyboardButton("📱 تليجرام", callback_data="telegram")],
        [InlineKeyboardButton("📩 تواصل مع المطور", callback_data="contact_dev")],
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
        "🔹 لمعلومات عن تليجرام\n"
        "🔹 للتواصل مع المطور\n\n"
        "✨ أو أرسل أي رسالة وسأرد عليك بذكاء!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_name = query.from_user.first_name
    user_id = query.from_user.id
    
    if data == "ai":
        await query.edit_message_text(
            "🤖 **مرحباً! أنا الذكاء الاصطناعي هنا.**\n\n"
            "أرسل لي أي سؤال أو رسالة وسأرد عليك بأفضل شكل. 🌟",
            parse_mode="Markdown"
        )
    
    elif data == "joke":
        await query.edit_message_text(
            f"😂 **نكتة اليوم** 😂\n\n{random.choice(JOKES)}",
            parse_mode="Markdown"
        )
    
    elif data == "religious":
        await query.edit_message_text(
            f"🕌 **اقتباس ديني** 🕌\n\n{random.choice(RELIGIOUS)}",
            parse_mode="Markdown"
        )
    
    elif data == "tip":
        await query.edit_message_text(
            f"💡 **نصيحة اليوم** 💡\n\n{random.choice(TIPS)}",
            parse_mode="Markdown"
        )
    
    elif data == "love":
        await query.edit_message_text(
            f"❤️ **رسالة حب** ❤️\n\n{random.choice(LOVE)}\n\nلك {user_name} 💫",
            parse_mode="Markdown"
        )
    
    elif data == "telegram":
        await query.edit_message_text(
            f"📱 **معلومة عن تليجرام** 📱\n\n{random.choice(TELEGRAM_FACTS)}",
            parse_mode="Markdown"
        )
    
    elif data == "contact_dev":
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
            f"👨‍💻 المطور: {DEVELOPER_USERNAME}\n\n"
            f"⚠️ **تنبيه:**\n"
            f"إذا أرسلت أي محتوى مخالف أو غير لائق، سيتم **حظرك فوراً** من قبل المطور.\n\n"
            f"اختر نوع الملف الذي تريد إرساله:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    elif data == "send_message":
        context.user_data['waiting_for'] = 'message_to_dev'
        await query.edit_message_text(
            f"📝 **أرسل رسالتك الآن**\n\n"
            f"اكتب الرسالة التي تريد إرسالها للمطور {DEVELOPER_USERNAME}\n\n"
            f"⚠️ تذكر: المحتوى المخالف يؤدي إلى الحظر الفوري.\n\n"
            f"⏳ انتظر... سأرسلها فور استلامها.",
            parse_mode="Markdown"
        )
    
    elif data == "send_photo":
        context.user_data['waiting_for'] = 'photo_to_dev'
        await query.edit_message_text(
            f"🖼️ **أرسل الصورة الآن**\n\n"
            f"أرسل الصورة التي تريد إرسالها للمطور {DEVELOPER_USERNAME}\n\n"
            f"⚠️ تذكر: المحتوى المخالف يؤدي إلى الحظر الفوري.\n\n"
            f"💬 يمكنك إضافة تعليق مع الصورة.",
            parse_mode="Markdown"
        )
    
    elif data == "send_video":
        context.user_data['waiting_for'] = 'video_to_dev'
        await query.edit_message_text(
            f"🎥 **أرسل الفيديو الآن**\n\n"
            f"أرسل الفيديو الذي تريد إرساله للمطور {DEVELOPER_USERNAME}\n\n"
            f"⚠️ تذكر: المحتوى المخالف يؤدي إلى الحظر الفوري.\n\n"
            f"💬 يمكنك إضافة تعليق مع الفيديو.",
            parse_mode="Markdown"
        )
    
    elif data == "send_audio":
        context.user_data['waiting_for'] = 'audio_to_dev'
        await query.edit_message_text(
            f"🎵 **أرسل الصوت الآن**\n\n"
            f"أرسل الملف الصوتي الذي تريد إرساله للمطور {DEVELOPER_USERNAME}\n\n"
            f"⚠️ تذكر: المحتوى المخالف يؤدي إلى الحظر الفوري.\n\n"
            f"💬 يمكنك إضافة تعليق مع الصوت.",
            parse_mode="Markdown"
        )
    
    elif data == "back_to_start":
        keyboard = [
            [InlineKeyboardButton("🤖 ذكاء اصطناعي", callback_data="ai"), InlineKeyboardButton("😂 نكتة", callback_data="joke")],
            [InlineKeyboardButton("🕌 ديني", callback_data="religious"), InlineKeyboardButton("💡 نصيحة", callback_data="tip")],
            [InlineKeyboardButton("❤️ حب", callback_data="love"), InlineKeyboardButton("📱 تليجرام", callback_data="telegram")],
            [InlineKeyboardButton("📩 تواصل مع المطور", callback_data="contact_dev")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🌟 **مرحباً بك في بوت التواصل الذكي!** 🌟\n\n"
            "أنا هنا لخدمتك، اختر من الأزرار الفخمة أدناه:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    username = update.message.from_user.username
    
    if context.user_data.get('waiting_for') == 'message_to_dev':
        try:
            await context.bot.send_message(
                chat_id=DEVELOPER_ID,
                text=f"📩 **رسالة جديدة من مستخدم**\n\n"
                     f"👤 الاسم: {user_name}\n"
                     f"🆔 المعرف: @{username if username else 'لا يوجد'}\n"
                     f"🆔 الآيدي: {user_id}\n\n"
                     f"📝 **الرسالة:**\n{user_message}"
            )
            
            await update.message.reply_text(
                f"✅ **تم إرسال رسالتك بنجاح!**\n\n"
                f"شكراً لك {user_name} على تواصلك مع المطور {DEVELOPER_USERNAME}\n"
                f"سيتم الرد عليك في أقرب وقت. 🙏",
                parse_mode="Markdown"
            )
            
            context.user_data['waiting_for'] = None
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ عذراً، حدث خطأ أثناء إرسال الرسالة.\n"
                f"الرجاء المحاولة مرة أخرى لاحقاً.",
                parse_mode="Markdown"
            )
            logging.error(f"Error sending message to developer: {e}")
        
        return
    
    ai_reply = get_ai_response(user_message)
    await update.message.reply_text(ai_reply, parse_mode="Markdown")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    username = update.message.from_user.username
    photo_file = update.message.photo[-1]
    caption = update.message.caption or "بدون تعليق"
    
    if context.user_data.get('waiting_for') == 'photo_to_dev':
        try:
            file = await context.bot.get_file(photo_file.file_id)
            file_path = f"photo_{user_id}_{photo_file.file_id}.jpg"
            await file.download_to_drive(file_path)
            
            await context.bot.send_photo(
                chat_id=DEVELOPER_ID,
                photo=open(file_path, 'rb'),
                caption=f"🖼️ **صورة جديدة من مستخدم**\n\n"
                        f"👤 الاسم: {user_name}\n"
                        f"🆔 المعرف: @{username if username else 'لا يوجد'}\n"
                        f"🆔 الآيدي: {user_id}\n\n"
                        f"📝 **التعليق:**\n{caption}"
            )
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            await update.message.reply_text(
                f"✅ **تم إرسال صورتك بنجاح!**\n\n"
                f"شكراً لك {user_name} على تواصلك مع المطور {DEVELOPER_USERNAME}\n"
                f"سيتم الرد عليك في أقرب وقت. 🙏",
                parse_mode="Markdown"
            )
            
            context.user_data['waiting_for'] = None
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ عذراً، حدث خطأ أثناء إرسال الصورة.\n"
                f"الرجاء المحاولة مرة أخرى لاحقاً.",
                parse_mode="Markdown"
            )
            logging.error(f"Error sending photo to developer: {e}")
        
        return
    
    await update.message.reply_text(
        "📸 صورة جميلة! لكن إذا كنت تريد إرسالها للمطور، استخدم زر '📩 تواصل مع المطور' أولاً.",
        parse_mode="Markdown"
    )

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    username = update.message.from_user.username
    video_file = update.message.video
    caption = update.message.caption or "بدون تعليق"
    
    if context.user_data.get('waiting_for') == 'video_to_dev':
        try:
            file = await context.bot.get_file(video_file.file_id)
            file_path = f"video_{user_id}_{video_file.file_id}.mp4"
            await file.download_to_drive(file_path)
            
            await context.bot.send_video(
                chat_id=DEVELOPER_ID,
                video=open(file_path, 'rb'),
                caption=f"🎥 **فيديو جديد من مستخدم**\n\n"
                        f"👤 الاسم: {user_name}\n"
                        f"🆔 المعرف: @{username if username else 'لا يوجد'}\n"
                        f"🆔 الآيدي: {user_id}\n\n"
                        f"📝 **التعليق:**\n{caption}"
            )
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            await update.message.reply_text(
                f"✅ **تم إرسال الفيديو بنجاح!**\n\n"
                f"شكراً لك {user_name} على تواصلك مع المطور {DEVELOPER_USERNAME}\n"
                f"سيتم الرد عليك في أقرب وقت. 🙏",
                parse_mode="Markdown"
            )
            
            context.user_data['waiting_for'] = None
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ عذراً، حدث خطأ أثناء إرسال الفيديو.\n"
                f"الرجاء المحاولة مرة أخرى لاحقاً.",
                parse_mode="Markdown"
            )
            logging.error(f"Error sending video to developer: {e}")
        
        return
    
    await update.message.reply_text(
        "🎥 فيديو رائع! لكن إذا كنت تريد إرساله للمطور، استخدم زر '📩 تواصل مع المطور' أولاً.",
        parse_mode="Markdown"
    )

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    username = update.message.from_user.username
    audio_file = update.message.audio
    caption = update.message.caption or "بدون تعليق"
    
    if context.user_data.get('waiting_for') == 'audio_to_dev':
        try:
            file = await context.bot.get_file(audio_file.file_id)
            file_path = f"audio_{user_id}_{audio_file.file_id}.mp3"
            await file.download_to_drive(file_path)
            
            await context.bot.send_audio(
                chat_id=DEVELOPER_ID,
                audio=open(file_path, 'rb'),
                caption=f"🎵 **ملف صوتي جديد من مستخدم**\n\n"
                        f"👤 الاسم: {user_name}\n"
                        f"🆔 المعرف: @{username if username else 'لا يوجد'}\n"
                        f"🆔 الآيدي: {user_id}\n\n"
                        f"📝 **التعليق:**\n{caption}"
            )
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            await update.message.reply_text(
                f"✅ **تم إرسال الملف الصوتي بنجاح!**\n\n"
                f"شكراً لك {user_name} على تواصلك مع المطور {DEVELOPER_USERNAME}\n"
                f"سيتم الرد عليك في أقرب وقت. 🙏",
                parse_mode="Markdown"
            )
            
            context.user_data['waiting_for'] = None
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ عذراً، حدث خطأ أثناء إرسال الملف الصوتي.\n"
                f"الرجاء المحاولة مرة أخرى لاحقاً.",
                parse_mode="Markdown"
            )
            logging.error(f"Error sending audio to developer: {e}")
        
        return
    
    await update.message.reply_text(
        "🎵 ملف صوتي جميل! لكن إذا كنت تريد إرساله للمطور، استخدم زر '📩 تواصل مع المطور' أولاً.",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **الأوامر المتاحة:**\n\n"
        "/start - عرض الأزرار والبدء\n"
        "/help - عرض هذه المساعدة\n"
        "/dev - معلومات المطور\n\n"
        "📩 للتواصل مع المطور استخدم الزر في القائمة الرئيسية.",
        parse_mode="Markdown"
    )

async def dev_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👨‍💻 **المطور**\n\n"
        f"هذا البوت من تصميم وتطوير:\n"
        f"✨ {DEVELOPER_USERNAME} ✨\n\n"
        f"📌 للتواصل مع المطور:\n"
        f"• استخدم زر 📩 تواصل مع المطور في /start\n"
        f"• أو أرسل رسالة مباشرة: {DEVELOPER_USERNAME}\n\n"
        f"شكراً لاستخدامك البوت! ❤️",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# ========== التشغيل الرئيسي ==========

def main():
    print("🚀 تشغيل بوت التواصل الذكي...")
    print(f"👨‍💻 المطور: {DEVELOPER_USERNAME}")
    print(f"🆔 ID المطور: {DEVELOPER_ID}")
    print(f"🤖 التوكن: {BOT_TOKEN[:10]}... (مخفي)")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("dev", dev_command))
    
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
