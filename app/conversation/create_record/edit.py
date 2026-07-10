from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.conversation import states
from app.conversation.create_record.review import review_record


EDIT_FIELD_KEY = "edit_field"

MAX_NAME_LENGTH = 80
MAX_LOCATION_LENGTH = 120
MAX_RECOGNITION_FEATURES_LENGTH = 300
MAX_PUBLIC_CONTACT_LENGTH = 160
MAX_BREED_LENGTH = 40


ANIMAL_ICONS = {
    "dog": "🐕",
    "cat": "🐈",
    "horse": "🐎",
    "bird": "🦜",
    "unknown": "🐾",
}


ANIMAL_BREED_EXAMPLES = {
    "dog": "Rottweiler, Pastor Alemán, Golden Retriever, mestizo",
    "cat": "Siamés, Angora, Persa, mestizo",
    "horse": "Pura sangre, Criollo, Cuarto de milla",
    "bird": "Loro, Guacamaya, Periquito, Canario",
    "unknown": "Escribe la raza, tipo o especie aproximada",
}


def _clear_edit_state(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    context.user_data.pop(EDIT_FIELD_KEY, None)
    context.user_data["record_step"] = states.REVIEW


async def show_edit_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    subject_type = context.user_data.get("subject_type", "human")

    if subject_type == "animal":
        keyboard = [
            [
                InlineKeyboardButton(
                    "🐾 Especie",
                    callback_data="edit_animal_species",
                )
            ],
            [
                InlineKeyboardButton(
                    "📏 Tamaño",
                    callback_data="edit_animal_size",
                )
            ],
            [
                InlineKeyboardButton(
                    "🧬 Raza / tipo",
                    callback_data="edit_animal_breed",
                )
            ],
            [
                InlineKeyboardButton(
                    "🏷️ Nombre",
                    callback_data="edit_reported_name",
                )
            ],
            [
                InlineKeyboardButton(
                    "📍 Ubicación",
                    callback_data="edit_reported_location",
                )
            ],
            [
                InlineKeyboardButton(
                    "📣 Fuente",
                    callback_data="edit_source",
                )
            ],
            [
                InlineKeyboardButton(
                    "🧩 Características para identificación",
                    callback_data="edit_recognition_features",
                )
            ],
            [
                InlineKeyboardButton(
                    "📞 Medio de contacto",
                    callback_data="edit_public_contact",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Volver al resumen",
                    callback_data="edit_back_to_review",
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ Cancelar",
                    callback_data="review_cancel",
                )
            ],
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(
                    "👤 Nombre",
                    callback_data="edit_reported_name",
                )
            ],
            [
                InlineKeyboardButton(
                    "🎂 Edad",
                    callback_data="edit_estimated_age",
                )
            ],
            [
                InlineKeyboardButton(
                    "📍 Ubicación",
                    callback_data="edit_reported_location",
                )
            ],
            [
                InlineKeyboardButton(
                    "📣 Fuente",
                    callback_data="edit_source",
                )
            ],
            [
                InlineKeyboardButton(
                    "🧩 Características para identificación",
                    callback_data="edit_recognition_features",
                )
            ],
            [
                InlineKeyboardButton(
                    "📞 Medio de contacto",
                    callback_data="edit_public_contact",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Volver al resumen",
                    callback_data="edit_back_to_review",
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ Cancelar",
                    callback_data="review_cancel",
                )
            ],
        ]

    await query.edit_message_text(
        text="✏️ ¿Qué información deseas editar?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_edit_choice(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    choice = query.data.replace("edit_", "")

    if choice == "back_to_review":
        context.user_data.pop(EDIT_FIELD_KEY, None)
        await review_record(update, context)
        return

    context.user_data[EDIT_FIELD_KEY] = choice

    if choice == "estimated_age":
        context.user_data["record_step"] = states.EDIT_TEXT

        await query.edit_message_text(
            text=(
                "🎂 Escribe la nueva edad estimada.\n\n"
                "Debe contener solo números.\n\n"
                "Ejemplo:\n"
                "45"
            )
        )
        return

    if choice == "reported_name":
        context.user_data["record_step"] = states.EDIT_TEXT

        subject_type = context.user_data.get("subject_type", "human")
        subject_label = "animal" if subject_type == "animal" else "persona"

        await query.edit_message_text(
            text=(
                f"🏷️ Escribe el nuevo nombre reportado del {subject_label}.\n\n"
                "Si no se conoce, escribe:\n"
                "Desconocido"
            )
        )
        return

    if choice == "reported_location":
        context.user_data["record_step"] = states.EDIT_TEXT

        await query.edit_message_text(
            text=(
                "📍 Escribe la nueva ubicación.\n\n"
                "Puedes indicar ciudad, barrio, hospital, refugio, "
                "clínica veterinaria o punto de referencia.\n\n"
                "Máximo 120 caracteres."
            )
        )
        return

    if choice == "recognition_features":
        context.user_data["record_step"] = states.EDIT_TEXT
        subject_type = context.user_data.get("subject_type", "human")

        if subject_type == "animal":
            message = (
                "🧩 Características para identificación\n\n"
                "Describe cualquier detalle visible que facilite reconocer "
                "al animal.\n\n"
                "Puedes incluir información como:\n\n"
                "🎨 Color del pelaje\n"
                "⚪ Manchas\n"
                "🦺 Collar o arnés\n"
                "🏷️ Placa identificadora\n"
                "🩹 Cicatrices\n"
                "🐾 Forma de caminar\n"
                "👁️ Color de los ojos\n\n"
                "Máximo 300 caracteres."
            )
        else:
            message = (
                "🧩 Características para identificación\n\n"
                "Describe cualquier detalle visible que facilite reconocer "
                "a la persona.\n\n"
                "Puedes incluir información como:\n\n"
                "👕 Vestimenta\n"
                "🎨 Colores\n"
                "👓 Lentes\n"
                "🎒 Mochila\n"
                "🖋️ Tatuajes\n"
                "🩹 Cicatrices\n"
                "💇 Cabello\n\n"
                "Máximo 300 caracteres."
            )

        await query.edit_message_text(text=message)
        return

    if choice == "public_contact":
        context.user_data["record_step"] = states.EDIT_TEXT

        await query.edit_message_text(
            text=(
                "📞 Medio de contacto\n\n"
                "Escribe el nuevo medio de contacto que deseas compartir.\n\n"
                "Puede ser, por ejemplo:\n\n"
                "📱 Número de teléfono\n"
                "💬 Usuario de Telegram\n"
                "📧 Correo electrónico\n\n"
                "Este dato no se utilizará para buscar ni correlacionar "
                "personas o animales.\n\n"
                "Máximo 160 caracteres."
            )
        )
        return

    if choice == "source":
        await show_edit_source_options(update, context)
        return

    if choice == "animal_species":
        await show_edit_animal_species_options(update, context)
        return

    if choice == "animal_size":
        await show_edit_animal_size_options(update, context)
        return

    if choice == "animal_breed":
        await show_edit_animal_breed_options(update, context)
        return


async def show_edit_source_options(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "👨‍👩‍👧 Familia",
                callback_data="edit_source_family",
            )
        ],
        [
            InlineKeyboardButton(
                "🏥 Hospital",
                callback_data="edit_source_hospital",
            )
        ],
        [
            InlineKeyboardButton(
                "🚒 Bomberos",
                callback_data="edit_source_fire_department",
            )
        ],
        [
            InlineKeyboardButton(
                "🤝 Voluntario",
                callback_data="edit_source_volunteer",
            )
        ],
        [
            InlineKeyboardButton(
                "👮 Policía",
                callback_data="edit_source_police",
            )
        ],
        [
            InlineKeyboardButton(
                "👤 Amigo / Conocido",
                callback_data="edit_source_friend",
            )
        ],
        [
            InlineKeyboardButton(
                "❓ Desconocido",
                callback_data="edit_source_unknown",
            )
        ],
    ]

    await query.edit_message_text(
        text="📣 Selecciona la nueva fuente del reporte.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_edit_source(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    source = query.data.replace("edit_source_", "")
    context.user_data["source"] = source

    _clear_edit_state(context)
    await review_record(update, context)


async def show_edit_animal_species_options(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "🐕 Perro",
                callback_data="edit_animal_species_dog",
            )
        ],
        [
            InlineKeyboardButton(
                "🐈 Gato",
                callback_data="edit_animal_species_cat",
            )
        ],
        [
            InlineKeyboardButton(
                "🐎 Caballo",
                callback_data="edit_animal_species_horse",
            )
        ],
        [
            InlineKeyboardButton(
                "🦜 Ave",
                callback_data="edit_animal_species_bird",
            )
        ],
        [
            InlineKeyboardButton(
                "🐾 Otro / No sé",
                callback_data="edit_animal_species_unknown",
            )
        ],
    ]

    await query.edit_message_text(
        text="🐾 Selecciona la nueva especie.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_edit_animal_species(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    species = query.data.replace("edit_animal_species_", "")
    context.user_data["animal_species"] = species

    _clear_edit_state(context)
    await review_record(update, context)


async def show_edit_animal_size_options(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    species = context.user_data.get("animal_species", "unknown")
    icon = ANIMAL_ICONS.get(species, "🐾")

    keyboard = [
        [
            InlineKeyboardButton(
                f"{icon} Grande",
                callback_data="edit_animal_size_large",
            )
        ],
        [
            InlineKeyboardButton(
                f"{icon} Mediano",
                callback_data="edit_animal_size_medium",
            )
        ],
        [
            InlineKeyboardButton(
                f"{icon} Pequeño",
                callback_data="edit_animal_size_small",
            )
        ],
        [
            InlineKeyboardButton(
                "❓ Desconocido",
                callback_data="edit_animal_size_unknown",
            )
        ],
    ]

    await query.edit_message_text(
        text=f"{icon} Selecciona el nuevo tamaño aproximado.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_edit_animal_size(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    size = query.data.replace("edit_animal_size_", "")
    context.user_data["animal_size"] = size

    _clear_edit_state(context)
    await review_record(update, context)


async def show_edit_animal_breed_options(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    species = context.user_data.get("animal_species", "unknown")
    icon = ANIMAL_ICONS.get(species, "🐾")

    keyboard = [
        [
            InlineKeyboardButton(
                f"{icon} Raza / especie conocida",
                callback_data="edit_animal_breed_known",
            )
        ],
        [
            InlineKeyboardButton(
                f"{icon} Mestizo / Criollo",
                callback_data="edit_animal_breed_mixed",
            )
        ],
        [
            InlineKeyboardButton(
                "❓ Desconocida",
                callback_data="edit_animal_breed_unknown",
            )
        ],
    ]

    await query.edit_message_text(
        text=f"{icon} Selecciona la nueva raza, tipo o especie.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_edit_animal_breed(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if not query:
        return

    await query.answer()

    breed = query.data.replace("edit_animal_breed_", "")

    if breed == "known":
        context.user_data[EDIT_FIELD_KEY] = "animal_breed"
        context.user_data["record_step"] = states.ANIMAL_BREED_TEXT

        species = context.user_data.get("animal_species", "unknown")
        icon = ANIMAL_ICONS.get(species, "🐾")
        examples = ANIMAL_BREED_EXAMPLES.get(
            species,
            ANIMAL_BREED_EXAMPLES["unknown"],
        )

        label = (
            "especie aproximada"
            if species == "bird"
            else "raza o tipo aproximado"
        )

        await query.edit_message_text(
            text=(
                f"{icon} Escribe la nueva {label}.\n\n"
                f"Ejemplos:\n{examples}\n\n"
                "Máximo 40 caracteres."
            )
        )
        return

    context.user_data["animal_breed"] = breed

    _clear_edit_state(context)
    await review_record(update, context)


async def handle_edit_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> bool:
    if not update.message:
        return False

    step = context.user_data.get("record_step")

    if step == states.ANIMAL_BREED_TEXT:
        if context.user_data.get(EDIT_FIELD_KEY) != "animal_breed":
            return False
    elif step != states.EDIT_TEXT:
        return False

    text = update.message.text.strip()
    field = context.user_data.get(EDIT_FIELD_KEY)

    if step == states.ANIMAL_BREED_TEXT:
        if len(text) > MAX_BREED_LENGTH:
            await update.message.reply_text(
                "⚠️ La raza, tipo o especie debe tener máximo "
                "40 caracteres.\n\n"
                "Intenta escribir una versión más corta."
            )
            return True

        context.user_data["animal_breed"] = text

        _clear_edit_state(context)
        await review_record(update, context)
        return True

    if field == "estimated_age":
        if not text.isdigit():
            await update.message.reply_text(
                "⚠️ La edad debe ser un número.\n\n"
                "Ejemplo:\n"
                "45"
            )
            return True

        context.user_data["estimated_age"] = text

    elif field == "reported_name":
        if len(text) > MAX_NAME_LENGTH:
            await update.message.reply_text(
                "⚠️ El nombre debe tener máximo 80 caracteres."
            )
            return True

        context.user_data["reported_name"] = text

    elif field == "reported_location":
        if len(text) > MAX_LOCATION_LENGTH:
            await update.message.reply_text(
                "⚠️ La ubicación debe tener máximo 120 caracteres."
            )
            return True

        context.user_data["reported_location"] = text

    elif field == "recognition_features":
        if len(text) > MAX_RECOGNITION_FEATURES_LENGTH:
            await update.message.reply_text(
                "⚠️ Las características para identificación deben tener "
                "máximo 300 caracteres."
            )
            return True

        context.user_data["recognition_features"] = text

    elif field == "public_contact":
        if len(text) > MAX_PUBLIC_CONTACT_LENGTH:
            await update.message.reply_text(
                "⚠️ El medio de contacto debe tener máximo "
                "160 caracteres."
            )
            return True

        context.user_data["public_contact"] = text

    else:
        return False

    _clear_edit_state(context)
    await review_record(update, context)

    return True
