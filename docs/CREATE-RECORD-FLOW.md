# CREATE-RECORD-FLOW

Version: 0.1 (Draft)

Status: Draft

Category: Client Specification

Project: Human Connection Network

Repository: hcp-client-telegram

License: Apache-2.0

Depends On:

* HCP-0000 Overview
* HCP-0001 Humanitarian Record
* HCP Client Role
* BOT-FLOW

---

# 1. Purpose

This document defines the complete conversational flow used by the HCP Telegram Client to create a Humanitarian Record.

The objective is to ensure that every client implementing HCP collects information in a consistent, structured and user-friendly manner.

The conversation should feel natural while producing a valid Humanitarian Record.

---

# 2. Design Principles

The record creation process should follow these principles.

## One Question at a Time

The client should ask only one question per screen.

---

## Minimum Necessary Information

Only information useful for humanitarian correlation should be requested.

Avoid collecting unnecessary personal information.

---

## Accessible

Questions should be understandable by anyone regardless of education level.

Every message should include descriptive text and may be complemented with icons.

---

## Optional Information

If the user does not know an answer, the client should allow the field to remain empty whenever possible.

The goal is to record observations, not perfect information.

---

# 3. Conversation Flow

```text
Create Report

↓

Reported Name

↓

Estimated Age

↓

Reported Location

↓

Event Type

↓

Current Status

↓

Information Source

↓

Short Description

↓

Review

↓

Confirm

↓

Create Humanitarian Record

↓

POST /hcp/records

↓

Success
```

---

# 4. Step 1

## 👤 Reported Name

Question

"What name was reported?"

Examples

Maria Perez

Carlos Rodriguez

Unknown

Validation

This field is recommended.

If the name is unknown, the client should allow "Unknown".

---

# 5. Step 2

## 🎂 Estimated Age

Question

"What is the estimated age?"

Examples

34

Around 30

Child

Adult

Unknown

Validation

Exact age is not required.

Approximate values are acceptable.

---

# 6. Step 3

## 📍 Reported Location

Question

"Where was this person reported?"

Examples

Caracas

Maracaibo

Hospital

Shelter

School

Neighborhood

If the exact place is unknown, a general location is acceptable.

---

# 7. Step 4

## 🚨 Event Type

The client should offer predefined options.

Examples

Missing

Hospitalized

Sheltered

Evacuated

Injured

Safe

Deceased

Other

The user may select "Other" when necessary.

---

# 8. Step 5

## 📌 Current Status

Examples

Reported

Confirmed

Updated

Closed

This field describes the status of the humanitarian observation, not the person's identity.

---

# 9. Step 6

## 🏥 Information Source

Examples

Family

Volunteer

Hospital

Fire Department

Police

NGO

Government

Other

The information source contributes to later probability calculations performed by the HCP Node.

The Telegram Client simply records the reported source.

---

# 10. Step 7

## 📝 Short Description

Question

"Please provide a short description."

Example

Reported by relatives after the landslide.

Seen entering the local hospital.

Last reported near the evacuation center.

Descriptions should remain factual and concise.

---

# 11. Review Screen

Before submission the client should display a complete summary.

Example

Reported Name

Maria Perez

Estimated Age

34

Location

Caracas

Event Type

Hospitalized

Status

Reported

Source

Hospital

Description

Reported after the landslide.

Buttons

✅ Confirm

✏ Edit

❌ Cancel

The record should not be submitted before confirmation.

---

# 12. Record Creation

After confirmation

The Telegram Client creates a valid Humanitarian Record according to the HCP Specification.

The client does not decide how the record will be stored.

Its responsibility ends after successfully submitting the JSON to the configured HCP Node.

---

# 13. Successful Submission

If the HCP Node accepts the record

The client displays

✅ Humanitarian Report submitted successfully.

Reference ID

xxxxxxxx

This identifier allows future reference to the submitted report.

---

# 14. Error Handling

If communication fails

The client should explain the problem using clear language.

Examples

Unable to contact the HCP Node.

Please try again later.

The information you entered has not been lost.

Avoid technical error messages whenever possible.

---

# 15. Data Validation

The Telegram Client performs only basic validation.

Examples

* Empty required fields
* Invalid age format
* Excessively long descriptions
* Unsupported characters

Semantic validation belongs to the HCP Node.

---

# 16. Privacy

The Telegram Client should remind users that:

The information provided will become part of a humanitarian record.

Only information necessary for humanitarian assistance should be reported.

Sensitive personal information unrelated to the event should not be included.

---

# 17. Future Compatibility

This conversational flow should remain compatible with future HCP clients including:

* Telegram
* WhatsApp
* SMS
* Mobile Applications
* Web Clients
* Offline-first implementations
* Mesh Network Clients

Only the communication channel should change.

The Humanitarian Record should remain identical.

---

# 18. Summary

The Create Record flow transforms a simple conversation into a standardized Humanitarian Record.

By asking one clear question at a time, validating only essential information and confirming the final summary before submission, the Telegram Client enables anyone to contribute structured humanitarian observations while remaining faithful to the principles of the Humanitarian Connection Protocol.

