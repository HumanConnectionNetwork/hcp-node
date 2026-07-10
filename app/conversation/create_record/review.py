from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.conversation import states


HUMAN_EVENT_LABELS = {
    "missing": "🚨 Persona desaparecida",
    "hospitalized": "🏥 Persona hospitalizada",
    "sheltered": "🏠 Persona refugiada / en albergue",
    "safe": "✅ Persona localizada / segura",
    "public_emergency": "🚨 Emergencia pública",
}


ANIMAL_EVENT_LABELS = {
    "missing": "desaparecido",
    "found": "encontrado",
}


ANIMAL_SPECIES_LABELS = {
    "dog": "Perro",
    "cat": "Gato",
    "horse": "Caballo",
    "bird": "Ave",
    "unknown": "Animal",
}


ANIMAL_SPECIES_ICONS = {
    "dog": "🐕",
    "cat": "🐈",
    "horse": "🐎",
    "bird": "🦜",
    "unknown": "🐾",
}


ANIMAL_SIZE_LABELS = {
    "large": "Grande",
    "medium": "Mediano",
    "small": "Pequeño",
    "unknown": "Desconocido",
}


ANIMAL_BREED_LABELS = {
    "mixed": "Mestizo / Criollo",
    "unknown": "Desconocida",
}


SOURCE_LABELS = {
    "family": "👨‍👩‍👧 Familia",
    "hospital": "🏥 Hospital",
    "fire_department": "🚒 Bomberos",
    "volunteer": "🤝 Voluntario",
    "police": "👮 Policía",
    "friend": "👤 Amigo / Conocido",
    "unknown": "❓ Desconocido",
}


def _display_value(
    value: object,
    fallback: str = "No especificado",
) -> str:
    """
    Returns a clean value for the review summary.
    """

    if value is None:
        return fallback

    text = str(value).strip()

    if not text:
        return fallback

    return text


def get_event_label(
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """
    Returns the human-readable event label shown to the user.
    """

    subject_type = context.user_data.get(
        "subject_type",
        "human",
    )
    event_type = context.user_data.get(
        "event_type",
        "unknown",
    )

    if subject_type == "animal":
        species = context.user_data.get(
            "animal_species",
            "unknown",
        )

        species_label = ANIMAL_SPECIES_LABELS.get(
            species,
            "Animal",
        )
        species_icon = ANIMAL_SPECIES_ICONS.get(
            species,
            "🐾",
        )
        event_label = ANIMAL_EVENT_LABELS.get(
            event_type,
            "reportado",
        )

        return (
            f"{species_icon} "
            f"{species_label} {event_label}"
        )

    return HUMAN_EVENT_LABELS.get(
        event_type,
        _display_value(event_type),
    )


def get_animal_breed_label(
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """
    Returns the selected animal breed or its predefined label.
    """

    breed = context.user_data.get(
        "animal_breed",
        "unknown",
    )

    return ANIMAL_BREED_LABELS.get(
        breed,
        _display_value(breed, "Desconocida"),
    )


def build_review_summary(
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """
    Builds the complete review message before the report is submitted.
    """

    subject_type = context.user_data.get(
        "subject_type",
        "human",
    )
    source = context.user_data.get(
        "source",
        "unknown",
    )

    reported_name = _display_value(
        context.user_data.get("reported_name"),
        "Desconocido",
    )
    reported_location = _display_value(
        context.user_data.get("reported_location"),
        "Desconocido",
    )
    recognition_features = _display_value(
        context.user_data.get("recognition_features"),
        "No especificadas",
    )
    public_contact = _display_value(
        context.user_data.get("public_contact"),
        "No especificado",
    )

    summary = (
        "📋 Revisa tu reporte antes de enviarlo\n\n"
        "Has completado la información disponible para este caso.\n\n"
        "Este reporte formará parte de un servicio humanitario abierto "
        "que ayuda a relacionar información durante situaciones de "
        "emergencia.\n\n"
        "Envía únicamente información que consideres verdadera o "
        "razonablemente confiable. Un reporte honesto puede ayudar a "
        "conectar información importante para otras personas.\n\n"
        "──────────────\n\n"
        f"Tipo de reporte: {get_event_label(context)}\n"
    )

    if subject_type == "animal":
        species = context.user_data.get(
            "animal_species",
            "unknown",
        )
        size = context.user_data.get(
            "animal_size",
            "unknown",
        )

        summary += (
            f"Especie: "
            f"{ANIMAL_SPECIES_LABELS.get(species, 'Animal')}\n"
            f"Tamaño: "
            f"{ANIMAL_SIZE_LABELS.get(size, 'Desconocido')}\n"
            f"Raza / tipo: {get_animal_breed_label(context)}\n"
            f"Nombre reportado: {reported_name}\n"
            f"Ubicación: {reported_location}\n"
            f"Reportado por: "
            f"{SOURCE_LABELS.get(source, _display_value(source))}\n"
            f"Características para identificación: "
            f"{recognition_features}\n"
            f"📞 Medio de contacto: {public_contact}\n\n"
        )
    else:
        estimated_age = _display_value(
            context.user_data.get("estimated_age"),
            "Desconocida",
        )

        summary += (
            f"Nombre reportado: {reported_name}\n"
            f"Edad estimada: {estimated_age}\n"
            f"Ubicación: {reported_location}\n"
            f"Reportado por: "
            f"{SOURCE_LABELS.get(source, _display_value(source))}\n"
            f"Características para identificación: "
            f"{recognition_features}\n"
            f"📞 Medio de contacto: {public_contact}\n\n"
        )

    summary += (
        "El medio de contacto se mostrará únicamente junto a este "
        "reporte y no participará en la correlación.\n\n"
        "¿Deseas registrar este reporte?"
    )

    return summary


async def review_record(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Displays the final review screen.
    """

    context.user_data["record_step"] = states.REVIEW

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Registrar reporte",
                callback_data="review_confirm",
            )
        ],
        [
            InlineKeyboardButton(
                "✏️ Editar información",
                callback_data="review_edit",
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Cancelar",
                callback_data="review_cancel",
            )
        ],
    ]

    summary = build_review_summary(context)
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            text=summary,
            reply_markup=reply_markup,
        )
        return

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=summary,
            reply_markup=reply_markup,
        )
