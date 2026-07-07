# SEARCH-RECORD-FLOW

Version: 0.2 (Draft)

Status: Draft

Category: Client UX Specification

Project: Human Connection Network

Repository: hcp-client-telegram

License: Apache-2.0

Depends On:

- HCP Client Role
- BOT-FLOW
- CLIENT-DESIGN-PRINCIPLES
- HCP-0001 Humanitarian Record

---

# 1. Purpose

This document defines the complete user experience for searching Humanitarian Records using an HCP Client.

Unlike traditional search systems, HCP does not attempt to identify people directly.

Instead, it searches for humanitarian observations that may correspond to the same real-world event.

---

# 2. Design Principles

The Search flow follows the same philosophy as Create Report.

- One question at a time.
- Simple language.
- Buttons whenever possible.
- Explainable results.
- Correlation instead of identity.

---

# 3. Search Flow

```text
/start

↓

🔍 Buscar Caso Reportado

↓

Seleccionar tipo de caso

↓

Edad aproximada

↓

Nombre reportado (opcional)

↓

Lugar reportado

↓

Consultar Nodo HCP

↓

Resultados correlacionados

↓

Explicación de la correlación
```

---

# 4. Event Selection

The user selects one option.

- 🚨 Persona desaparecida
- 🏥 Persona hospitalizada
- 🏠 Persona refugiada
- ✅ Persona localizada

Public Emergency is intentionally excluded.

Public emergencies represent institutional observations and will be handled by specialized HCP clients in future versions.

---

# 5. Search Form

## Step 1

🎂

**What is the estimated age?**

Only numeric values are accepted.

Example

45

The age is stored as an integer to improve future correlation.

---

## Step 2

👤

**Do you know the reported name?**

The name is optional.

Users may answer:

Unknown

The absence of a name must never prevent searching.

---

## Step 3

📍

**Where was this person reported?**

Examples

City

Neighborhood

Hospital

Shelter

Reference point

---

# 6. Correlation Philosophy

The objective is not to search for identities.

The objective is to search for compatible humanitarian observations.

A correlation represents the probability that two independent observations describe the same humanitarian event.

---

# 7. Correlation Priority

Correlation should consider multiple variables.

Not all variables have the same importance.

Recommended order:

## 1. Time and Place

Highest priority.

Observations occurring within compatible time windows and geographically compatible locations should receive the strongest correlation score.

Example

Two observations reported in the same city within minutes or hours are significantly more compatible than observations separated by hundreds of kilometers within the same time period.

Impossible travel scenarios should reduce correlation drastically.

---

## 2. Reported Name

Second highest priority.

Names should support:

- Exact matches
- Minor spelling variations
- Accent differences
- Common abbreviations
- Unknown names

Large differences between names should reduce correlation significantly.

Example

Luis

Luiz

L. Trapito

may represent compatible observations.

Mario

Pedro

José

should reduce correlation substantially.

---

## 3. Estimated Age

Estimated age should be compared using ranges.

Small differences are acceptable.

Examples

44

45

46

remain compatible.

Large differences should reduce correlation.

Example

20 years

65 years

are unlikely to describe the same observation.

---

## 4. Event Type

Event type should remain compatible.

Examples

Missing

Hospitalized

Sheltered

Safe

Some transitions may increase correlation.

Example

Missing

↓

Hospitalized

↓

Safe

may describe the natural evolution of the same humanitarian event.

---

## 5. Source

Source contributes additional confidence.

Examples

Hospital

Fire Department

Police

Family

Volunteer

Friend

Unknown

Institutional observations may receive additional trust but should never replace humanitarian verification.

---

# 8. Correlation Score

The final result should be expressed as

Probability %

Example

94 %

78 %

61 %

The percentage represents compatibility between observations.

It never represents certainty.

---

# 9. Search Results

The client should present up to three candidate observations ordered by probability.

Each result displays

- Event type
- Reported name
- Estimated age
- Location
- Source
- Status
- Probability

---

# 10. Explainable Correlation

Each result should provide an explanation.

Example

Why was this result suggested?

✓ Similar reported name

✓ Compatible estimated age

✓ Same city

✓ Compatible reporting time

✓ Compatible event type

✗ Different source

This allows users to understand the reason behind each probability.

---

# 11. Weak Correlations

If no strong matches exist the client should clearly communicate this.

Example

No highly compatible observations were found.

However, some reports share one or more similar characteristics.

These observations are presented because they may still be useful during humanitarian verification.

---

# 12. No Results

Example

No compatible observations were found using the provided information.

You may try again using different or additional information.

---

# 13. Human Verification

Correlation never replaces human judgment.

Search results are recommendations intended to assist humanitarian work.

Final verification always depends on people and organizations.

---

# 14. Summary

Searching in HCP is fundamentally different from searching for people.

The protocol searches for humanitarian observations.

By combining time, location, reported name, estimated age, event type and source, HCP produces explainable probabilities that help users locate potentially related humanitarian events while preserving transparency and avoiding assumptions about identity.
