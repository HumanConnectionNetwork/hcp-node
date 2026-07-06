from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.messages import t


async def create_record_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if query:
        await query.answer()

    user_language = "es"

    keyboard = [
        [InlineKeyboardButton(t("event.missing", user_language), callback_data="event_missing")],
        [InlineKeyboardButton(t("event.hospitalized", user_language), callback_data="event_hospitalized")],
        [InlineKeyboardButton(t("event.sheltered", user_language), callback_data="event_sheltered")],
        [InlineKeyboardButton(t("event.safe", user_language), callback_data="event_safe")],
        [InlineKeyboardButton(t("event.public_emergency", user_language), callback_data="event_public_emergency")],
        [InlineKeyboardButton(t("common.cancel", user_language), callback_data="cancel")],
    ]

    message = (
        f"{t('record.title', user_language)}\n\n"
        f"{t('record.question', user_language)}"
    )

    if query:
        await query.edit_message_text(
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


async def ask_reported_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if query:
        await query.answer()

        event_type = query.data.replace("event_", "")
        context.user_data["event_type"] = event_type
        context.user_data["record_step"] = "reported_name"

        print(f"Selected event_type: {event_type}")

        await query.edit_message_text(
            text=(
                "👤 ¿Cómo fue reportada la persona?\n\n"
                "Ejemplos:\n"
                "María Pérez\n"
                "José González\n"
                "Desconocido"
            )
        )


async def handle_record_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not update.message:
        return

    text = update.message.text.strip()
    current_step = context.user_data.get("record_step")

    if current_step == "reported_name":
        context.user_data["reported_name"] = text
        context.user_data["record_step"] = "estimated_age"

        print(f"Reported name: {text}")

        await update.message.reply_text(
            "🎂 ¿Cuál es la edad aproximada?\n\n"
            "Puedes escribir un número o una aproximación.\n\n"
            "Ejemplos:\n"
            "34\n"
            "Alrededor de 50\n"
            "Niño\n"
            "Adulto\n"
            "Desconocido"
        )
        return

    if current_step == "estimated_age":
        context.user_data["estimated_age"] = text
        context.user_data["record_step"] = "reported_location"

        print(f"Estimated age: {text}")

        await update.message.reply_text(
            "📍 ¿Dónde fue reportado el caso?\n\n"
            "Puedes escribir ciudad, barrio, hospital, refugio o punto de referencia."
        )
        return
