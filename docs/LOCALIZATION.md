# LOCALIZATION

Version: 0.1 (Draft)

Status: Draft

Category: Client Specification

Project: Human Connection Network

Repository: hcp-client-telegram

License: Apache-2.0

Depends On:

* HCP-0000 Overview
* HCP Client Role
* BOT-FLOW

---

# 1. Purpose

This document defines how the HCP Telegram Client should support multiple languages while preserving the consistency of the Humanitarian Connection Protocol.

The objective is to make the client accessible to people around the world without changing the meaning of HCP concepts.

Localization should improve usability while maintaining interoperability.

---

# 2. Design Principles

Localization should follow these principles.

---

## Universal

Every user should be able to interact with the client using their preferred language whenever available.

---

## Consistent

The same HCP concept should always represent the same meaning regardless of language.

Translations should never change protocol semantics.

---

## Maintainable

Adding a new language should not require modifications to the application logic.

Only translation files should change.

---

## Accessible

Translations should prioritize clarity over literal wording.

The goal is communication, not word-for-word translation.

---

# 3. Internationalization and Localization

The HCP Telegram Client distinguishes two related concepts.

---

## Internationalization (i18n)

Internationalization is the design of the software so that it can support multiple languages.

Examples

* No hardcoded messages
* External translation files
* Language-independent code
* Flexible date and number formatting

---

## Localization (l10n)

Localization is the adaptation of the client to a specific language and cultural context.

Examples

Spanish

Portuguese

English

French

Arabic

Japanese

Localization should not modify HCP concepts.

---

# 4. Language Files

Every supported language should be stored in an independent file.

Example

```text
app/

locales/

    en.json

    es.json

    pt.json

    fr.json

    de.json

    it.json

    ar.json

    zh.json

    ja.json

    uk.json

    ru.json
```

Each file contains only user-visible messages.

---

# 5. No Hardcoded Text

Application code should never contain fixed messages.

Avoid

```python
reply_text("Create Report")
```

Prefer

```python
reply_text(t("create_report"))
```

Where `t()` retrieves the appropriate translation according to the user's selected language.

---

# 6. Default Language

The Telegram Client should automatically detect the user's Telegram language whenever possible.

If that language is not available, the client should use English as the default language.

Users should always be able to change their preferred language manually.

---

# 7. Language Selection

The Main Menu should include

🌐 Language

Selecting this option presents the list of available languages.

Example

🇬🇧 English

🇪🇸 Español

🇧🇷 Português

🇫🇷 Français

🇩🇪 Deutsch

🇮🇹 Italiano

🇺🇦 Українська

🇯🇵 日本語

🇨🇳 中文

More languages may be added without changing application logic.

---

# 8. Official HCP Terminology

Certain protocol concepts represent standardized definitions.

Their meaning must remain identical across every translation.

Examples include:

* Humanitarian Record
* HCP Node
* Humanitarian Connection Protocol
* Correlation Candidate
* Correlation Probability
* Reported Case
* Humanitarian Observation

Localization should translate these concepts carefully without altering their technical meaning.

Future HCP specifications may define an official multilingual terminology glossary.

---

# 9. User Messages

Translations should use natural language.

Avoid literal technical translations whenever they reduce clarity.

Example

Instead of

"Execute Search"

Prefer

"Search Reported Cases"

The interface should feel conversational rather than technical.

---

# 10. Accessibility

Localization should improve accessibility.

Recommendations

* Short sentences.
* Clear wording.
* Simple grammar.
* Descriptive buttons.
* Icons together with text.
* Screen-reader friendly labels.

Icons should support understanding but never replace written language.

---

# 11. Cultural Neutrality

Translations should avoid culturally specific expressions whenever possible.

The client should remain understandable across different countries using the same language.

For example, Spanish translations should avoid region-specific vocabulary whenever a neutral alternative exists.

---

# 12. Future Languages

The localization system should allow unlimited future languages.

Adding a language should require only:

* Creating a new language file.
* Registering the language.
* Providing translations.

No application logic should change.

---

# 13. Future Clients

The same localization principles should apply to every HCP client.

Examples

* Telegram
* WhatsApp
* SMS
* Web Clients
* Mobile Applications
* Offline-first Clients
* Mesh Network Clients

This ensures a consistent experience across the entire HCP ecosystem.

---

# 14. Summary

Localization enables the HCP Telegram Client to communicate naturally with users around the world while preserving the integrity of the Humanitarian Connection Protocol.

Application logic remains language-independent, translations remain externally managed and standardized HCP terminology keeps the same technical meaning regardless of the language presented to the user.

This separation allows HCP to scale globally without sacrificing consistency, interoperability or accessibility.
