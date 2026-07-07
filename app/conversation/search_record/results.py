from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


MOCK_RESULTS = [
    {
        "candidate_id": "candidate_1",
        "probability": 92,
        "event_type": "🚨 Persona desaparecida",
        "reported_name": "Luis Trapito",
        "estimated_age": "45",
        "reported_location": "La Guaira",
        "status": "Reportado",
        "source": "👤 Amigo / Conocido",
    },
    {
        "candidate_id": "candidate_2",
        "probability": 78,
        "event_type": "🏥 Persona hospitalizada",
        "reported_name": "Luis Trápito",
        "estimated_age": "Aproximadamente 45",
        "reported_location": "Hospital en Caracas",
        "status": "Reportado",
        "source": "🏥 Hospital",
    },
    {
        "candidate_id": "candidate_3",
        "probability": 61,
        "event_type": "🏠 Persona refugiada / en albergue",
        "reported_name": "Luis T.",
        "estimated_age": "Adulto",
        "reported_location": "Centro de refugio",
        "status": "Reportado",
        "source": "🤝 Voluntario",
    },
]


async def show_mock_search_results(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    search_name = context.user_data.get("search_reported_name", "Desconocido")
    search_age = context.user_data.get("search_estimated_age", "Desconocido")
    search_location = context.user_data.get(
        "search_reported_location",
        "Desconocido",
    )

    message = (
        "🔍 Resultados de búsqueda\n\n"
        "HCP no identifica personas.\n"
        "Relaciona observaciones humanitarias que podrían corresponder a un mismo caso.\n\n"
        "Datos consultados:\n"
        f"👤 Nombre: {search_name}\n"
        f"🎂 Edad aproximada: {search_age}\n"
        f"📍 Localización: {search_location}\n\n"
        "Se encontraron posibles casos relacionados:\n\n"
    )

    keyboard = []

    for index, result in enumerate(MOCK_RESULTS, start=1):
        message += (
            f"──────────────\n"
            f"📄 Posible caso #{index}\n\n"
            f"Probabilidad: {result['probability']}%\n"
            f"Tipo: {result['event_type']}\n"
            f"Nombre reportado: {result['reported_name']}\n"
            f"Edad estimada: {result['estimated_age']}\n"
            f"Localización: {result['reported_location']}\n"
            f"Estado: {result['status']}\n"
            f"Fuente: {result['source']}\n\n"
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"Ver explicación #{index}",
                    callback_data=f"explain_{result['candidate_id']}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "⬅️ Volver al menú principal",
                callback_data="back_to_start",
            )
        ]
    )

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
