# SEARCH-RECORD-FLOW

Version: 0.3 (Draft)

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
- HCP-0004 Correlation Model

---

# 1. Purpose

This document defines the user experience for searching reported humanitarian cases using an HCP Client.

HCP does not search identities.

HCP searches compatible humanitarian observations about living beings during humanitarian situations.

Supported subjects:

- Human
- Animal

---

# 2. Search Philosophy

The Search flow must communicate clearly that results are not identity confirmations.

Search results represent possible correlations between independent humanitarian observations.

A result means:

> This observation may be related to the information you provided.

It does not mean:

> This is certainly the person or animal you are looking for.

---

# 3. Flow Overview

```text
/start

↓

🔍 Buscar Caso Reportado

↓

¿Qué tipo de ser vivo deseas buscar?

👤 Persona
🐾 Animal

↓

Tipo de caso

↓

Datos de búsqueda

↓

Resultados correlacionados

↓

Explicación de probabilidad
