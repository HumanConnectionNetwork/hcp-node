from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.config import settings
from app.conversation import states
from app.conversation.create_record import (
    ask_estimated_age,
    create_record_menu,
    handle_animal_breed,
    handle_animal_size,
    handle_animal_species,
    handle_edit_animal_breed,
    handle_edit_animal_size,
    handle_edit_animal_species,
    handle_edit_choice,
    handle_edit_source,
    handle_record_text,
    handle_reporter_source,
    select_subject_type,
    show_edit_menu,
    submit_record,
)
from app.conversation.search_record.explain import explain_search_result
from app.conversation.search_record.form import (
    receive_animal_breed_text,
    receive_animal_features,
    receive_animal_location,
    receive_animal_name,
    receive_animal_size,
    receive_animal_species,
    receive_person_age,
    receive_person_features,
    receive_person_location,
    receive_person_name,
    start_animal_search_form,
    start_person_search_form,
)
from app.conversation.search_record.menu import search_record_menu
from app.conversation.search_record.results import show_search_results
from app.conversation.start import start


async def _set_search_state(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    handler,
) -> None:
    next_state = await handler(update, context)

    if next_state:
        context.user_data["search_state"] = next_state


async def handle_search_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    search_state = context.user_data.get("search_state")

    if search_state == states.SEARCH_REPORTED_NAME:
        await _set_search_state(update, context, receive_person_name)
        return

    if search_state == states.SEARCH_ESTIMATED_AGE:
        await _set_search_state(update, context, receive_person_age)
        return

    if search_state == states.SEARCH_LOCATION:
        await _set_search_state(update, context, receive_person_location)
        return

    if search_state == states.SEARCH_RECOGNITION_FEATURES:
        await _set_search_state(update, context, receive_person_features)
        await show_search_results(update, context)
        context.user_data.pop("search_state", None)
        return

    if search_state == states.SEARCH_ANIMAL_NAME:
        await _set_search_state(update, context, receive_animal_name)
        return

    if search_state == states.SEARCH_ANIMAL_BREED_TEXT:
        await _set_search_state(update, context, receive_animal_breed_text)
        return

    if search_state == states.SEARCH_ANIMAL_LOCATION:
        await _set_search_state(update, context, receive_animal_location)
        return

    if search_state == states.SEARCH_ANIMAL_FEATURES:
        await _set_search_state(update, context, receive_animal_features)
        await show_search_results(update, context)
        context.user_data.pop("search_state", None)
        return

    await handle_record_text(update, context)


async def reset_to_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    context.user_data.pop("search_state", None)
    context.user_data.pop("search_record", None)

    await start(update, context)


def main() -> None:
    application = Application.builder().token(
        settings.telegram_bot_token
    ).build()

    application.add_handler(CommandHandler("start", start))

    # General navigation

    application.add_handler(
        CallbackQueryHandler(
            reset_to_start,
            pattern="^(cancel|back_to_start|review_cancel)$",
        )
    )

    # Main menu actions

    application.add_handler(
        CallbackQueryHandler(create_record_menu, pattern="^create_report$")
    )

    application.add_handler(
        CallbackQueryHandler(search_record_menu, pattern="^search_report$")
    )

    application.add_handler(
        CallbackQueryHandler(search_record_menu, pattern="^search_menu$")
    )

    # Search Record callbacks

    application.add_handler(
        CallbackQueryHandler(
            lambda update, context: _set_search_state(
                update,
                context,
                start_person_search_form,
            ),
            pattern="^search_person$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            lambda update, context: _set_search_state(
                update,
                context,
                start_animal_search_form,
            ),
            pattern="^search_animal$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            lambda update, context: _set_search_state(
                update,
                context,
                receive_animal_species,
            ),
            pattern="^search_animal_species_",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            lambda update, context: _set_search_state(
                update,
                context,
                receive_animal_size,
            ),
            pattern="^search_animal_size_",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            explain_search_result,
            pattern="^explain_",
        )
    )

    # Create Record callbacks

    application.add_handler(
        CallbackQueryHandler(select_subject_type, pattern="^subject_")
    )

    application.add_handler(
        CallbackQueryHandler(ask_estimated_age, pattern="^event_")
    )

    application.add_handler(
        CallbackQueryHandler(handle_animal_species, pattern="^animal_species_")
    )

    application.add_handler(
        CallbackQueryHandler(handle_animal_size, pattern="^animal_size_")
    )

    application.add_handler(
        CallbackQueryHandler(handle_animal_breed, pattern="^animal_breed_")
    )

    application.add_handler(
        CallbackQueryHandler(handle_reporter_source, pattern="^source_")
    )

    application.add_handler(
        CallbackQueryHandler(show_edit_menu, pattern="^review_edit$")
    )

    application.add_handler(
        CallbackQueryHandler(handle_edit_source, pattern="^edit_source_")
    )

    application.add_handler(
        CallbackQueryHandler(
            handle_edit_animal_species,
            pattern="^edit_animal_species_",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            handle_edit_animal_size,
            pattern="^edit_animal_size_",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            handle_edit_animal_breed,
            pattern="^edit_animal_breed_",
        )
    )

    application.add_handler(
        CallbackQueryHandler(handle_edit_choice, pattern="^edit_")
    )

    application.add_handler(
        CallbackQueryHandler(submit_record, pattern="^review_confirm$")
    )

    # Text messages

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_text)
    )

    print("HCP Telegram Client is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
