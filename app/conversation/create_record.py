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
                t("report_missing_person", user_language),
                callback_data="report_missing_person",
            )
        ],
        [
            InlineKeyboardButton(
                t("report_hospitalized_person", user_language),
                callback_data="report_hospitalized_person",
            )
        ],
        [
            InlineKeyboardButton(
                t("report_sheltered_person", user_language),
                callback_data="report_sheltered_person",
            )
        ],
        [
            InlineKeyboardButton(
                t("report_safe_person", user_language),
                callback_data="report_safe_person",
            )
        ],
        [
            InlineKeyboardButton(
                t("report_public_emergency", user_language),
                callback_data="report_public_emergency",
            )
        ],
        [
            InlineKeyboardButton(
                t("cancel", user_language),
                callback_data="cancel",
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        f"{t('create_report_title', user_language)}\n\n"
        f"{t('create_report_question', user_language)}"
    )

    if query:
        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
        )
