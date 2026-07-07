from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.messages import t


async def search_record_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Displays the Search Report menu.
    """

    query = update.callback_query

    if not query:
        return

    await query.answer()

    user_language = "es"

    keyboard = [
        [
            InlineKeyboardButton(
                t("event.missing", user_language),
                callback_data="search_missing",
            )
        ],
        [
            InlineKeyboardButton(
                t("event.hospitalized", user_language),
                callback_data="search_hospitalized",
            )
        ],
        [
            InlineKeyboardButton(
                t("event.sheltered", user_language),
                callback_data="search_sheltered",
            )
        ],
        [
            InlineKeyboardButton(
                t("event.safe", user_language),
                callback_data="search_safe",
            )
        ],
        [
            InlineKeyboardButton(
                t("common.cancel", user_language),
                callback_data="cancel",
            )
        ],
    ]

    message = (
        "🔍 Buscar Caso Reportado\n\n"
        "HCP no busca personas por su identidad.\n\n"
        "Busca observaciones humanitarias que puedan estar relacionadas con la información disponible.\n\n"
        "¿Qué tipo de caso deseas buscar?"
    )

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
