# ========== دوال البوت ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        username = update.message.from_user.username
        
        data = load_data()
        
        if str(user_id) in data["banned_users"]:
            await update.message.reply_text("🚫 **أنت محظور من استخدام هذا البوت.**\nللتواصل: @SSSTlF", parse_mode="Markdown")
            return
        
        if str(user_id) not in data["users"]:
            data["users"].append(str(user_id))
            data["total_users"] = len(data["users"])
            save_data(data)
            
            try:
                await context.bot.send_message(
                    chat_id=DEVELOPER_ID,
                    text=f"🆕 **مستخدم جديد!**\n\n👤 {user_name}\n🆔 @{username if username else 'لا يوجد'}\n🔢 `{user_id}`\n📊 الإجمالي: {data['total_users']}",
                    parse_mode="Markdown"
                )
            except:
                pass
        
        # ✅ أزرار فخمة مرتبة بالعرض
        keyboard = [
            [
                InlineKeyboardButton("📩 رسالة", callback_data="send_message"),
                InlineKeyboardButton("🖼️ صورة", callback_data="send_photo"),
            ],
            [
                InlineKeyboardButton("🎥 فيديو", callback_data="send_video"),
                InlineKeyboardButton("🎵 صوت", callback_data="send_audio"),
            ],
            [
                InlineKeyboardButton("📎 ملف", callback_data="send_document"),
                InlineKeyboardButton("🏷️ ملصق", callback_data="send_sticker"),
            ],
        ]
        
        if user_id == DEVELOPER_ID:
            keyboard.append([InlineKeyboardButton("⚙️ لوحة التحكم", callback_data="admin_panel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"📩 **بوت التواصل مع المطور**\n\n"
            f"👨‍💻 **المطور:** @SSSTlF\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"📌 **اختر ما تريد إرساله:**\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Error in start: {e}")

# ========== معالج الأزرار (الجزء المعدل) ==========

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

        # ========== ردود المطور ==========
        # رد بصورة
        if data_callback.startswith("reply_photo_"):
            target_id = int(data_callback.split('_')[2])
            context.user_data['replying_to_photo'] = target_id
            context.user_data['waiting_for'] = 'reply_photo'
            await query.edit_message_text(f"🖼️ **أرسل الصورة التي تريد الرد بها**\n👤 للمستخدم: `{target_id}`\nلإلغاء: /cancel", parse_mode="Markdown")
            return

        # رد بفيديو
        elif data_callback.startswith("reply_video_"):
            target_id = int(data_callback.split('_')[2])
            context.user_data['replying_to_video'] = target_id
            context.user_data['waiting_for'] = 'reply_video'
            await query.edit_message_text(f"🎥 **أرسل الفيديو الذي تريد الرد به**\n👤 للمستخدم: `{target_id}`\nلإلغاء: /cancel", parse_mode="Markdown")
            return

        # رد بصوت
        elif data_callback.startswith("reply_audio_"):
            target_id = int(data_callback.split('_')[2])
            context.user_data['replying_to_audio'] = target_id
            context.user_data['waiting_for'] = 'reply_audio'
            await query.edit_message_text(f"🎵 **أرسل الصوت الذي تريد الرد به**\n👤 للمستخدم: `{target_id}`\nلإلغاء: /cancel", parse_mode="Markdown")
            return

        # ✅ رد بملصق (جديد)
        elif data_callback.startswith("reply_sticker_"):
            target_id = int(data_callback.split('_')[2])
            context.user_data['replying_to_sticker'] = target_id
            context.user_data['waiting_for'] = 'reply_sticker'
            await query.edit_message_text(f"🏷️ **أرسل الملصق الذي تريد الرد به**\n👤 للمستخدم: `{target_id}`\nلإلغاء: /cancel", parse_mode="Markdown")
            return

        # رد بملف (جديد)
        elif data_callback.startswith("reply_document_"):
            target_id = int(data_callback.split('_')[2])
            context.user_data['replying_to_document'] = target_id
            context.user_data['waiting_for'] = 'reply_document'
            await query.edit_message_text(f"📎 **أرسل الملف الذي تريد الرد به**\n👤 للمستخدم: `{target_id}`\nلإلغاء: /cancel", parse_mode="Markdown")
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
        elif data_callback == "send_message":
            context.user_data['waiting_for'] = 'message_to_dev'
            await query.edit_message_text("📝 **أرسل رسالتك الآن**\nللمطور @SSSTlF\n⚠️ المحتوى المخالف = حظر فوري", parse_mode="Markdown")
        
        elif data_callback == "send_photo":
            context.user_data['waiting_for'] = 'photo_to_dev'
            await query.edit_message_text("🖼️ **أرسل الصورة الآن**\nللمطور @SSSTlF", parse_mode="Markdown")
        
        elif data_callback == "send_video":
            context.user_data['waiting_for'] = 'video_to_dev'
            await query.edit_message_text("🎥 **أرسل الفيديو الآن**\nللمطور @SSSTlF", parse_mode="Markdown")
        
        elif data_callback == "send_audio":
            context.user_data['waiting_for'] = 'audio_to_dev'
            await query.edit_message_text("🎵 **أرسل الصوت الآن**\nللمطور @SSSTlF", parse_mode="Markdown")
        
        elif data_callback == "send_document":
            context.user_data['waiting_for'] = 'document_to_dev'
            await query.edit_message_text("📎 **أرسل الملف الآن**\nللمطور @SSSTlF", parse_mode="Markdown")
        
        # ✅ زر إرسال ملصق للمطور (جديد)
        elif data_callback == "send_sticker":
            context.user_data['waiting_for'] = 'sticker_to_dev'
            await query.edit_message_text("🏷️ **أرسل الملصق الآن**\nللمطور @SSSTlF", parse_mode="Markdown")

        elif data_callback == "back_to_start":
            keyboard = [
                [
                    InlineKeyboardButton("📩 رسالة", callback_data="send_message"),
                    InlineKeyboardButton("🖼️ صورة", callback_data="send_photo"),
                ],
                [
                    InlineKeyboardButton("🎥 فيديو", callback_data="send_video"),
                    InlineKeyboardButton("🎵 صوت", callback_data="send_audio"),
                ],
                [
                    InlineKeyboardButton("📎 ملف", callback_data="send_document"),
                    InlineKeyboardButton("🏷️ ملصق", callback_data="send_sticker"),
                ],
            ]
            if user_id == DEVELOPER_ID:
                keyboard.append([InlineKeyboardButton("⚙️ لوحة التحكم", callback_data="admin_panel")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"📩 **بوت التواصل مع المطور**\n\n👨‍💻 **المطور:** @SSSTlF\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n📌 **اختر ما تريد إرساله:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
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
                f"⚙️ **لوحة التحكم**\n\n👨‍💻 المطور: @SSSTlF\n📊 المستخدمين: {data['total_users']}\n🚫 المحظورين: {len(data['banned_users'])}\n📌 الحالة: {status}",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        elif data_callback == "admin_stats" and user_id == DEVELOPER_ID:
            keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"📊 **الإحصائيات**\n\n👥 المستخدمين: {data['total_users']}\n🚫 المحظورين: {len(data['banned_users'])}\n📌 الحالة: {'🟢 مفعل' if data['bot_active'] else '🔴 معطل'}\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
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
            await query.edit_message_text("🚫 **حظر مستخدم**\n\nأرسل الآيدي:\nمثال: `123456789`\nلإلغاء: /cancel", parse_mode="Markdown")
        
        elif data_callback == "admin_unban" and user_id == DEVELOPER_ID:
            context.user_data['waiting_for'] = 'unban_user'
            await query.edit_message_text("✅ **الغاء حظر**\n\nأرسل الآيدي:\nمثال: `123456789`\nلإلغاء: /cancel", parse_mode="Markdown")
        
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
                await query.edit_message_text("✅ **لا يوجد محظورين.**", reply_markup=reply_markup, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error in button_handler: {e}")

# ========== معالج الملصقات (معدل لدعم الرد) ==========

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        username = update.message.from_user.username
        sticker_file = update.message.sticker
        
        data = load_data()
        if str(user_id) in data["banned_users"] and user_id != DEVELOPER_ID:
            await update.message.reply_text("🚫 محظور.", parse_mode="Markdown")
            return

        # ✅ رد المطور بملصق
        if user_id == DEVELOPER_ID and context.user_data.get('waiting_for') == 'reply_sticker':
            target_id = context.user_data.get('replying_to_sticker')
            if target_id:
                try:
                    await context.bot.send_sticker(chat_id=target_id, sticker=sticker_file.file_id)
                    await update.message.reply_text(f"✅ **تم الرد بالملصق** 👤 `{target_id}`", parse_mode="Markdown")
                except Exception as e:
                    await update.message.reply_text("❌ فشل الإرسال.", parse_mode="Markdown")
                context.user_data.clear()
            return

        # ✅ إرسال ملصق للمطور
        if context.user_data.get('waiting_for') == 'sticker_to_dev':
            try:
                await context.bot.send_sticker(
                    chat_id=DEVELOPER_ID,
                    sticker=sticker_file.file_id
                )
                
                await context.bot.send_message(
                    chat_id=DEVELOPER_ID,
                    text=f"🏷️ **ملصق جديد**\n\n👤 {user_name}\n🆔 @{username if username else 'لا يوجد'}\n🔢 `{user_id}`\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                # ✅ أزرار للرد على الملصق
                keyboard = [
                    [InlineKeyboardButton("🏷️ رد بملصق", callback_data=f"reply_sticker_{user_id}")],
                    [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")],
                ]
                await context.bot.send_message(
                    chat_id=DEVELOPER_ID,
                    text=f"📌 للرد على هذا الملصق:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                
                await update.message.reply_text("✅ **تم الإرسال!**", parse_mode="Markdown")
                context.user_data['waiting_for'] = None
            except Exception as e:
                await update.message.reply_text("❌ حدث خطأ.", parse_mode="Markdown")
                logging.error(f"Error: {e}")
            return
        
        await update.message.reply_text("🏷️ استخدم /start للإرسال.", parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error in handle_sticker: {e}")

# ========== معالج الملفات (مع دعم الرد) ==========

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        username = update.message.from_user.username
        document_file = update.message.document
        caption = update.message.caption or "بدون تعليق"
        
        data = load_data()
        if str(user_id) in data["banned_users"] and user_id != DEVELOPER_ID:
            await update.message.reply_text("🚫 محظور.", parse_mode="Markdown")
            return

        # ✅ رد المطور بملف
        if user_id == DEVELOPER_ID and context.user_data.get('waiting_for') == 'reply_document':
            target_id = context.user_data.get('replying_to_document')
            if target_id:
                try:
                    await context.bot.send_document(chat_id=target_id, document=document_file.file_id)
                    await update.message.reply_text(f"✅ **تم الرد بالملف** 👤 `{target_id}`", parse_mode="Markdown")
                except Exception as e:
                    await update.message.reply_text("❌ فشل الإرسال.", parse_mode="Markdown")
                context.user_data.clear()
            return

        if context.user_data.get('waiting_for') == 'document_to_dev':
            try:
                await context.bot.send_document(
                    chat_id=DEVELOPER_ID,
                    document=document_file.file_id,
                    caption=f"📎 **ملف جديد**\n\n👤 {user_name}\n🆔 @{username if username else 'لا يوجد'}\n🔢 `{user_id}`\n📝 {caption}\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                keyboard = [
                    [InlineKeyboardButton("📎 رد بملف", callback_data=f"reply_document_{user_id}")],
                    [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_start")],
                ]
                await context.bot.send_message(
                    chat_id=DEVELOPER_ID,
                    text=f"📌 للرد على هذا الملف:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                
                await update.message.reply_text("✅ **تم الإرسال!**", parse_mode="Markdown")
                context.user_data['waiting_for'] = None
            except Exception as e:
                await update.message.reply_text("❌ حدث خطأ.", parse_mode="Markdown")
                logging.error(f"Error: {e}")
            return
        
        await update.message.reply_text("📎 استخدم /start للإرسال.", parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error in handle_document: {e}")

# ========== بقية الكود كما هو ==========
