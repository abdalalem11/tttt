import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد التسجيل للأخطاء
logging.basicConfig(level=logging.INFO)

# قراءة التوكن من متغيرات البيئة
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN غير موجود! أضفه في متغيرات البيئة.")

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك في بوت التواصل!\n\n"
        "أرسل أي رسالة وسأرد عليك فوراً."
    )

# الرد على أي رسالة نصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    user_name = update.message.from_user.first_name
    
    # هنا تقدر تضيف منطق الرد (مثلاً: ذكاء اصطناعي، ردود مبرمجة، إلخ)
    reply = f"📩 استقبلت رسالتك: \n\n\"{user_msg}\"\n\nشكراً لك {user_name}! 😊"
    
    await update.message.reply_text(reply)

# أمر /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 الأوامر المتاحة:\n"
        "/start - بدء البوت\n"
        "/help - عرض المساعدة\n\n"
        "💬 أو أرسل أي رسالة للتواصل."
    )

# التشغيل الرئيسي
def main():
    print("🚀 تشغيل البوت...")
    
    # إنشاء التطبيق
    app = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # تشغيل البوت (Polling)
    print("✅ البوت يعمل الآن...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
