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
        [
            InlineKeyboardButton(
                t("event.missing", user_language),
                callback_data="event_missing",
            )
        ],
        [
            InlineKeyboardButton(
                t("event.hospitalized", user_language),
                callback_data="event_hospitalized",
            )
        ],
        [
            InlineKeyboardButton(
                t("event.sheltered", user_language),
                callback_data="event_sheltered",
            )
        ],
        [
            InlineKeyboardButton(
                t("event.safe", user_language),
                callback_data="event_safe",
            )
        ],
        [
            InlineKeyboardButton(
                t("event.public_emergency", user_language),
                callback_data="event_public_emergency",
            )
        ],
        [
            InlineKeyboardButton(
                t("common.cancel", user_language),
                callback_data="cancel",
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        f"{t('record.title', user_language)}\n\n"
        f"{t('record.question', user_language)}"
    )

    if query:
        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
        )
