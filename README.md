# Backend Wizards — Stage 0: Dynamic Profile Endpoint

This project implements the Stage 0 task: a simple REST API endpoint that returns your profile information along with a dynamic cat fact fetched from an external API.

## Features

- `GET /me` endpoint returns:
  - `status`: always `"success"`
  - `user`: `{ email, name, stack }`
  - `timestamp`: current UTC time in ISO 8601 format (e.g. `2025-10-16T16:12:44Z`)
  - `fact`: a random cat fact fetched from `https://catfact.ninja/fact`
- External API call uses timeout and graceful error handling.
- JSON-only responses (`Content-Type: application/json`).

---

## Quickstart — Run locally

1. Clone the repo:
```bash
git clone  https://github.com/Zeethebeast/Stage-0-Task-Build-a-Dynamic-Profile-Endpoint.git
cd api
