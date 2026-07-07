from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.conversation import states
from app.conversation.create_record.review import review_record


ANIMAL_SPECIES = "animal_species"
ANIMAL_SIZE = "animal_size"
ANIMAL_BREED = "animal_breed"


async def ask_estimated_age(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    event_type = query.data.replace("event_", "")
    context.user_data["event_type"] = event_type

    subject_type = context.user_data.get("subject_type", "human")

    if subject_type == "animal":
        context.user_data["record_step"] = ANIMAL_SPECIES
        await query.edit_message_text(
            text=(
                "🐾 ¿Qué animal es?\n\n"
                "Ejemplos:\n"
                "Perro\n"
                "Gato\n"
                "Caballo\n"
                "Ave\n"
                "Otro"
            )
        )
        return

    context.user_data["record_step"] = states.ESTIMATED_AGE

    await query.edit_message_text(
        text=(
            "🎂 ¿Cuál es la edad estimada de la persona?\n\n"
            "Escribe solo números.\n\n"
            "Ejemplo:\n"
            "45"
        )
    )


async def ask_animal_size(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    keyboard = [
        [InlineKeyboardButton("🐕 Grande", callback_data="animal_size_large")],
        [InlineKeyboardButton("🐕 Mediano", callback_data="animal_size_medium")],
        [InlineKeyboardButton("🐕 Pequeño", callback_data="animal_size_small")],
        [InlineKeyboardButton("❓ Desconocido", callback_data="animal_size_unknown")],
    ]

    await update.message.reply_text(
        "📏 ¿Cuál es el tamaño aproximado del animal?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_animal_size(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    size = query.data.replace("animal_size_", "")
    context.user_data["animal_size"] = size
    context.user_data["record_step"] = ANIMAL_BREED

    await query.edit_message_text(
        text=(
            "🐾 ¿Qué raza parece ser?\n\n"
            "Ejemplos:\n"
            "Pastor Alemán\n"
            "Golden Retriever\n"
            "Criollo\n"
            "Sin raza\n"
            "Desconocida"
        )
    )


async def ask_reporter_source(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not update.message:
        return

    keyboard = [
        [InlineKeyboardButton("👨‍👩‍👧 Familia", callback_data="source_family")],
        [InlineKeyboardButton("🏥 Hospital", callback_data="source_hospital")],
        [InlineKeyboardButton("🚒 Bomberos", callback_data="source_fire_department")],
        [InlineKeyboardButton("🤝 Voluntario", callback_data="source_volunteer")],
        [InlineKeyboardButton("👮 Policía", callback_data="source_police")],
        [InlineKeyboardButton("👤 Amigo / Conocido", callback_data="source_friend")],
        [InlineKeyboardButton("❓ Desconocido", callback_data="source_unknown")],
    ]

    await update.message.reply_text(
        "📣 ¿Quién está reportando este evento?\n\n"
        "Selecciona la opción que mejor describa la fuente del reporte.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_reporter_source(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    source = query.data.replace("source_", "")

    context.user_data["source"] = source
    context.user_data["record_step"] = states.DESCRIPTION

    await query.edit_message_text(
        text=(
            "📝 Describe brevemente la situación.\n\n"
            "Escribe únicamente información útil y relevante."
        )
    )


async def handle_record_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not update.message:
        return

    text = update.message.text.strip()
    step = context.user_data.get("record_step")
    subject_type = context.user_data.get("subject_type", "human")

    if step == ANIMAL_SPECIES:
        context.user_data["animal_species"] = text
        context.user_data["record_step"] = ANIMAL_SIZE

        await ask_animal_size(update, context)
        return

    if step == ANIMAL_BREED:
        context.user_data["animal_breed"] = text
        context.user_data["record_step"] = states.REPORTED_NAME

        await update.message.reply_text(
            "👤 ¿Sabes el nombre del animal?\n\n"
            "Si lo sabes, escribe el nombre reportado.\n\n"
            "Si no lo sabes, escribe:\n"
            "Desconocido"
        )
        return

    if step == states.ESTIMATED_AGE:
        if not text.isdigit():
            await update.message.reply_text(
                "⚠️ La edad debe ser un número.\n\n"
                "Ejemplo:\n"
                "45"
            )
            return

        context.user_data["estimated_age"] = text
        context.user_data["record_step"] = states.REPORTED_NAME

        await update.message.reply_text(
            "👤 ¿Sabes el nombre de la persona?\n\n"
            "Si lo sabes, escribe el nombre reportado.\n\n"
            "Si no lo sabes, escribe:\n"
            "Desconocido"
        )
        return

    if step == states.REPORTED_NAME:
        context.user_data["reported_name"] = text
        context.user_data["record_step"] = states.REPORTED_LOCATION

        if subject_type == "animal":
            await update.message.reply_text(
                "📍 ¿Dónde se encuentra o fue visto el animal?\n\n"
                "Puedes escribir ciudad, barrio, refugio, clínica veterinaria o punto de referencia."
            )
        else:
            await update.message.reply_text(
                "📍 ¿En qué localización está esa persona?\n\n"
                "Puedes escribir:\n"
                "• Ciudad\n"
                "• Barrio\n"
                "• Hospital\n"
                "• Refugio\n"
                "• Punto de referencia"
            )
        return

    if step == states.REPORTED_LOCATION:
        context.user_data["reported_location"] = text
        context.user_data["record_step"] = states.SOURCE

        await ask_reporter_source(update, context)
        return

    if step == states.DESCRIPTION:
        if subject_type == "animal":
            extra = (
                f"Especie: {context.user_data.get('animal_species', 'Desconocida')}\n"
                f"Tamaño: {context.user_data.get('animal_size', 'Desconocido')}\n"
                f"Raza aproximada: {context.user_data.get('animal_breed', 'Desconocida')}\n\n"
            )
            context.user_data["description"] = extra + text
        else:
            context.user_data["description"] = text

        context.user_data["record_step"] = states.REVIEW

        await review_record(update, context)
        return
