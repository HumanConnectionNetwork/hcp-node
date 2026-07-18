from __future__ import annotations

from datetime import datetime
from typing import Any


MAX_SUPPORTING_EVIDENCE = 4
MAX_CONFLICTING_EVIDENCE = 4
MAX_RELATED_RECORDS = 3


EVENT_TYPE_LABELS = {
    "missing": "Persona desaparecida",
    "hospitalized": "Persona hospitalizada",
    "sheltered": "Persona refugiada",
    "refugee": "Persona refugiada",
    "safe": "Persona localizada o a salvo",
    "found": "Persona localizada",
    "public_emergency": "Emergencia pública",
    "missing_animal": "Animal desaparecido",
    "found_animal": "Animal encontrado",
}


EVIDENCE_LEVEL_LABELS = {
    "very_low": "Muy bajo",
    "low": "Bajo",
    "medium": "Medio",
    "moderate": "Medio",
    "high": "Alto",
    "very_high": "Muy alto",
}


VERIFICATION_STATUS_LABELS = {
    "unverified": "⚪ No verificado",
    "under_review": "🟡 En revisión",
    "human_verified": "🟢 Verificado por una persona",
    "rejected": "🔴 Rechazado",
}


SOURCE_LABELS = {
    "family": "Familia",
    "hospital": "Hospital",
    "fire_department": "Bomberos",
    "volunteer": "Voluntario",
    "police": "Policía",
    "friend": "Amigo o conocido",
    "unknown": "Fuente no especificada",
    "swagger_manual_test": "Prueba manual del nodo",
}


EVIDENCE_TYPE_LABELS = {
    "subject_reported_label_match": (
        "El nombre reportado coincide"
    ),
    "subject_reported_label_partial_match": (
        "El nombre presenta similitud parcial"
    ),
    "subject_reported_label_conflict": (
        "El nombre reportado presenta diferencias"
    ),
    "subject_estimated_age_match": (
        "La edad estimada coincide"
    ),
    "subject_estimated_age_partial_match": (
        "La edad estimada es similar"
    ),
    "subject_estimated_age_conflict": (
        "La edad estimada no coincide"
    ),
    "subject_recognition_features_match": (
        "Las características para identificación coinciden"
    ),
    "subject_recognition_features_partial_match": (
        "Las características presentan similitud parcial"
    ),
    "subject_recognition_features_conflict": (
        "Las características tienen poca similitud"
    ),
    "observation_reported_location_match": (
        "La ubicación reportada coincide"
    ),
    "observation_reported_location_partial_match": (
        "La ubicación presenta similitud parcial"
    ),
    "observation_reported_location_conflict": (
        "La ubicación reportada no coincide"
    ),
    "observation_event_type_match": (
        "El tipo de situación coincide"
    ),
    "observation_event_type_conflict": (
        "El tipo de situación presenta diferencias"
    ),
}


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value

    return {}


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value

    return []


def _normalize_key(value: Any) -> str:
    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def _format_event_type(value: Any) -> str:
    key = _normalize_key(value)

    if not key:
        return "No especificado"

    return EVENT_TYPE_LABELS.get(
        key,
        key.replace("_", " ").capitalize(),
    )


def _format_evidence_level(value: Any) -> str:
    key = _normalize_key(value)

    if not key:
        return "No especificado"

    return EVIDENCE_LEVEL_LABELS.get(
        key,
        key.replace("_", " ").capitalize(),
    )


def _format_verification_status(value: Any) -> str:
    key = _normalize_key(value)

    if not key:
        return VERIFICATION_STATUS_LABELS["unverified"]

    return VERIFICATION_STATUS_LABELS.get(
        key,
        key.replace("_", " ").capitalize(),
    )


def _format_source(value: Any) -> str:
    key = _normalize_key(value)

    if not key:
        return "Fuente no especificada"

    return SOURCE_LABELS.get(
        key,
        key.replace("_", " ").capitalize(),
    )


def _format_percentage(value: Any) -> str:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return "No disponible"

    if 0.0 <= score <= 1.0:
        score *= 100.0

    return f"{score:.0f}%"


def _format_datetime(value: Any) -> str:
    if value is None:
        return "No especificada"

    text = str(value).strip()

    if not text:
        return "No especificada"

    try:
        parsed = datetime.fromisoformat(
            text.replace("Z", "+00:00")
        )

        return parsed.strftime(
            "%d/%m/%Y, %H:%M UTC"
        )

    except ValueError:
        return text


def _singular_or_plural(
    count: int,
    singular: str,
    plural: str,
) -> str:
    return singular if count == 1 else plural


def _extract_case(
    search_response: dict[str, Any],
) -> dict[str, Any]:
    humanitarian_case = search_response.get(
        "humanitarian_case"
    )

    if isinstance(humanitarian_case, dict):
        return humanitarian_case

    case = search_response.get("case")

    if isinstance(case, dict):
        return case

    return search_response


def _translate_evidence_type(value: Any) -> str:
    key = _normalize_key(value)

    if not key:
        return "Señal de correlación"

    known_label = EVIDENCE_TYPE_LABELS.get(key)

    if known_label:
        return known_label

    if "reported_label" in key:
        if "conflict" in key:
            return "El nombre reportado presenta diferencias"

        if "partial" in key:
            return "El nombre presenta similitud parcial"

        return "El nombre reportado coincide"

    if "estimated_age" in key:
        if "conflict" in key:
            return "La edad estimada no coincide"

        if "partial" in key:
            return "La edad estimada es similar"

        return "La edad estimada coincide"

    if "recognition_features" in key:
        if "conflict" in key:
            return "Las características tienen poca similitud"

        if "partial" in key:
            return (
                "Las características presentan similitud parcial"
            )

        return (
            "Las características para identificación coinciden"
        )

    if "reported_location" in key or "location" in key:
        if "conflict" in key:
            return "La ubicación reportada no coincide"

        if "partial" in key:
            return "La ubicación presenta similitud parcial"

        return "La ubicación reportada coincide"

    if "event_type" in key:
        if "conflict" in key:
            return (
                "El tipo de situación presenta diferencias"
            )

        return "El tipo de situación coincide"

    return key.replace("_", " ").capitalize()


def _extract_evidence_label(
    evidence: Any,
) -> str:
    if isinstance(evidence, str):
        return _translate_evidence_type(evidence)

    evidence_data = _as_dict(evidence)

    return _translate_evidence_type(
        evidence_data.get("type")
    )


def _deduplicate_evidence(
    evidence_items: list[Any],
) -> list[str]:
    unique_labels: list[str] = []
    seen_labels: set[str] = set()

    for evidence in evidence_items:
        label = _extract_evidence_label(evidence)
        normalized_label = label.casefold()

        if normalized_label in seen_labels:
            continue

        seen_labels.add(normalized_label)
        unique_labels.append(label)

    return unique_labels


def _build_evidence_section(
    title: str,
    evidence_items: list[Any],
    limit: int,
) -> str:
    labels = _deduplicate_evidence(
        evidence_items
    )

    if not labels:
        return ""

    visible_labels = labels[:limit]

    lines = [title]

    for label in visible_labels:
        lines.append(f"• {label}.")

    remaining = len(labels) - len(visible_labels)

    if remaining > 0:
        lines.append(
            f"• Hay {remaining} señal(es) adicional(es)."
        )

    return "\n".join(lines)


def _build_related_records_section(
    related_records: list[Any],
) -> str:
    valid_records = [
        record
        for record in related_records
        if isinstance(record, dict)
    ]

    if not valid_records:
        return ""

    lines = [
        "📄 Observaciones relacionadas",
    ]

    for index, record in enumerate(
        valid_records[:MAX_RELATED_RECORDS],
        start=1,
    ):
        event_type = _format_event_type(
            record.get("event_type")
        )

        observed_at = _format_datetime(
            record.get("observed_at")
        )

        source = _format_source(
            record.get("source")
        )

        lines.extend(
            [
                "",
                f"#{index} {event_type}",
                f"🕒 {observed_at}",
                f"🏷️ Fuente: {source}",
            ]
        )

    remaining = (
        len(valid_records)
        - MAX_RELATED_RECORDS
    )

    if remaining > 0:
        lines.extend(
            [
                "",
                (
                    f"Hay {remaining} "
                    f"{_singular_or_plural(
                        remaining,
                        'observación adicional',
                        'observaciones adicionales',
                    )}."
                ),
            ]
        )

    return "\n".join(lines)


def build_case_message(
    search_response: dict[str, Any],
) -> str:
    """
    Build a concise Spanish Telegram message from an HCP
    SearchResponse or HumanitarianCase.

    A Humanitarian Case is a probabilistic local interpretation.
    It must not be presented as identity confirmation.
    """
    if not isinstance(search_response, dict):
        raise TypeError(
            "search_response must be a dictionary"
        )

    case = _extract_case(
        search_response
    )

    if not case:
        return (
            "🔍 Resultado de la búsqueda\n\n"
            "No se encontraron observaciones relacionadas "
            "con los datos proporcionados.\n\n"
            "Intenta nuevamente modificando alguno de los "
            "datos de búsqueda."
        )

    current_situation = _as_dict(
        case.get("current_situation")
    )

    correlation = _as_dict(
        case.get("correlation")
    )

    verification = _as_dict(
        case.get("verification")
    )

    related_records = _as_list(
        case.get("related_records")
    )

    if not related_records:
        return (
            "🔍 Resultado de la búsqueda\n\n"
            "No se encontraron observaciones relacionadas "
            "con los datos proporcionados.\n\n"
            "Intenta nuevamente modificando alguno de los "
            "datos de búsqueda."
        )

    likely_event_type = current_situation.get(
        "likely_event_type"
    )

    reported_location = current_situation.get(
        "reported_location"
    )

    observed_at = current_situation.get(
        "observed_at"
    )

    score = correlation.get(
        "score"
    )

    evidence_level = correlation.get(
        "evidence_level"
    )

    supporting_evidence = _as_list(
        correlation.get("supporting_evidence")
    )

    conflicting_evidence = _as_list(
        correlation.get("conflicting_evidence")
    )

    verification_status = verification.get(
        "status",
        "unverified",
    )

    record_count = len(related_records)

    observation_word = _singular_or_plural(
        record_count,
        "observación relacionada",
        "observaciones relacionadas",
    )

    message_parts = [
        "🔍 Posible caso relacionado",
        (
            "HCP no confirma identidades.\n"
            "Relaciona observaciones que podrían "
            "corresponder a un mismo caso."
        ),
        (
            f"📊 Compatibilidad: "
            f"{_format_percentage(score)}\n"
            f"🧭 Nivel de evidencia: "
            f"{_format_evidence_level(evidence_level)}"
        ),
        (
            f"📍 Estado probable: "
            f"{_format_event_type(likely_event_type)}\n"
            f"📌 Ubicación: "
            f"{reported_location or 'No especificada'}\n"
            f"🕒 Observación más relevante: "
            f"{_format_datetime(observed_at)}"
        ),
        (
            f"Se encontraron {record_count} "
            f"{observation_word}."
        ),
    ]

    supporting_section = _build_evidence_section(
        title="✅ Coincidencias principales",
        evidence_items=supporting_evidence,
        limit=MAX_SUPPORTING_EVIDENCE,
    )

    if supporting_section:
        message_parts.append(
            supporting_section
        )

    conflicting_section = _build_evidence_section(
        title="⚠️ Diferencias importantes",
        evidence_items=conflicting_evidence,
        limit=MAX_CONFLICTING_EVIDENCE,
    )

    if conflicting_section:
        message_parts.append(
            conflicting_section
        )

    related_records_section = (
        _build_related_records_section(
            related_records
        )
    )

    if related_records_section:
        message_parts.append(
            related_records_section
        )

    message_parts.append(
        (
            "🛡️ Verificación\n"
            f"Estado: "
            f"{_format_verification_status(
                verification_status
            )}\n\n"
            "Este resultado necesita verificación humana. "
            "Revisa las observaciones y sus fuentes antes "
            "de tomar una decisión."
        )
    )

    return "\n\n──────────────\n\n".join(
        message_parts
    )
