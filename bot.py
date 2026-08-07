# استبدل دالة start بهذه النسخة المبسطة

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
        
        # أزرار الإرسال فقط
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
