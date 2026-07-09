from difflib import SequenceMatcher


def normalize_text(value: object) -> str:
    if value is None:
        return ""

    return str(value).strip().lower()


def text_similarity(left: object, right: object) -> float:
    left_text = normalize_text(left)
    right_text = normalize_text(right)

    if not left_text or not right_text:
        return 0.0

    return SequenceMatcher(None, left_text, right_text).ratio()


def age_similarity(search_age: object, record_age: object) -> float:
    try:
        search_value = int(search_age)
        record_value = int(record_age)
    except (TypeError, ValueError):
        return 0.0

    difference = abs(search_value - record_value)

    if difference == 0:
        return 1.0

    if difference <= 2:
        return 0.85

    if difference <= 5:
        return 0.6

    if difference <= 10:
        return 0.3

    return 0.0


def category_matches(search_data: dict, record: dict) -> bool:
    search_category = normalize_text(search_data.get("category"))

    record_subject_type = normalize_text(
        record.get("subject_type")
        or record.get("category")
        or "human"
    )

    if search_category == "person":
        return record_subject_type in ["human", "person"]

    if search_category == "animal":
        return record_subject_type == "animal"

    return False


def calculate_person_score(search_data: dict, record: dict) -> tuple[int, list[str], list[str]]:
    score = 0
    matches = []
    warnings = []

    name_score = text_similarity(
        search_data.get("reported_name"),
        record.get("reported_name"),
    )

    if name_score >= 0.85:
        score += 35
        matches.append("Nombre muy similar.")
    elif name_score >= 0.6:
        score += 22
        matches.append("Nombre parcialmente similar.")
    else:
        warnings.append("El nombre no coincide claramente.")

    age_score = age_similarity(
        search_data.get("estimated_age"),
        record.get("estimated_age"),
    )

    if age_score >= 0.85:
        score += 20
        matches.append("Edad estimada compatible.")
    elif age_score >= 0.3:
        score += 10
        matches.append("Edad parcialmente compatible.")
    else:
        warnings.append("La edad estimada no coincide claramente.")

    location_score = text_similarity(
        search_data.get("location"),
        record.get("reported_location"),
    )

    if location_score >= 0.6:
        score += 25
        matches.append("Ubicación compatible.")
    elif location_score >= 0.35:
        score += 12
        matches.append("Ubicación parcialmente compatible.")
    else:
        warnings.append("La ubicación no coincide claramente.")

    features_score = text_similarity(
        search_data.get("recognition_features"),
        record.get("recognition_features"),
    )

    if features_score >= 0.5:
        score += 20
        matches.append("Características de identificación compatibles.")
    elif features_score >= 0.25:
        score += 8
        matches.append("Algunas características son parcialmente compatibles.")
    else:
        warnings.append("Hay pocas características compatibles.")

    return min(score, 100), matches, warnings


def calculate_animal_score(search_data: dict, record: dict) -> tuple[int, list[str], list[str]]:
    score = 0
    matches = []
    warnings = []

    species_score = text_similarity(
        search_data.get("species"),
        record.get("animal_species"),
    )

    if species_score >= 0.9:
        score += 20
        matches.append("Especie compatible.")
    else:
        warnings.append("La especie no coincide claramente.")

    name_score = text_similarity(
        search_data.get("animal_name"),
        record.get("reported_name"),
    )

    if name_score >= 0.85:
        score += 25
        matches.append("Nombre del animal muy similar.")
    elif name_score >= 0.6:
        score += 15
        matches.append("Nombre del animal parcialmente similar.")
    else:
        warnings.append("El nombre del animal no coincide claramente.")

    size_score = text_similarity(
        search_data.get("size"),
        record.get("animal_size"),
    )

    if size_score >= 0.9:
        score += 15
        matches.append("Tamaño compatible.")
    else:
        warnings.append("El tamaño no coincide claramente.")

    breed_score = text_similarity(
        search_data.get("breed_or_type"),
        record.get("animal_breed"),
    )

    if breed_score >= 0.7:
        score += 15
        matches.append("Raza, tipo o especie específica compatible.")
    elif breed_score >= 0.4:
        score += 8
        matches.append("Raza, tipo o especie parcialmente compatible.")
    else:
        warnings.append("La raza, tipo o especie no coincide claramente.")

    location_score = text_similarity(
        search_data.get("location"),
        record.get("reported_location"),
    )

    if location_score >= 0.6:
        score += 15
        matches.append("Ubicación compatible.")
    elif location_score >= 0.35:
        score += 8
        matches.append("Ubicación parcialmente compatible.")
    else:
        warnings.append("La ubicación no coincide claramente.")

    features_score = text_similarity(
        search_data.get("recognition_features"),
        record.get("recognition_features"),
    )

    if features_score >= 0.5:
        score += 10
        matches.append("Características de identificación compatibles.")
    elif features_score >= 0.25:
        score += 5
        matches.append("Algunas características son parcialmente compatibles.")
    else:
        warnings.append("Hay pocas características compatibles.")

    return min(score, 100), matches, warnings


def build_candidate(
    record: dict,
    probability: int,
    matches: list[str],
    warnings: list[str],
) -> dict:
    return {
        "candidate_id": record.get("id") or record.get("record_id") or "unknown",
        "probability": probability,
        "record": record,
        "matches": matches,
        "warnings": warnings,
    }


def correlate_records(
    search_data: dict,
    records: list[dict],
    limit: int = 3,
    min_probability: int = 20,
) -> list[dict]:
    candidates = []

    for record in records:
        if not category_matches(search_data, record):
            continue

        category = normalize_text(search_data.get("category"))

        if category == "animal":
            probability, matches, warnings = calculate_animal_score(
                search_data,
                record,
            )
        else:
            probability, matches, warnings = calculate_person_score(
                search_data,
                record,
            )

        if probability >= min_probability:
            candidates.append(
                build_candidate(
                    record=record,
                    probability=probability,
                    matches=matches,
                    warnings=warnings,
                )
            )

    candidates.sort(
        key=lambda candidate: candidate["probability"],
        reverse=True,
    )

    return candidates[:limit]
