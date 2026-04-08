# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Planet API** is a simple REST API that returns planet (and Sun) names by index:

| Index | Name    |
|-------|---------|
| 0     | Sun     |
| 1     | Mercury |
| 2     | Venus   |
| 3     | Earth   |
| 4     | Mars    |
| 5     | Jupiter |
| 6     | Saturn  |
| 7     | Uranus  |
| 8     | Neptune |

The API is containerized and runs on Docker.

## Current State

The project requires:
- A single API endpoint (`GET /planet/{id}`) returning the planet name for a given index
- A `Dockerfile` to containerize the application
- A `docker-compose.yml` (optional but recommended) for easy local development

## Tech Stack

- **Backend Framework**: FastAPI (Python) — lightweight and fast for a single-endpoint API
- **Server**: Uvicorn (ASGI server)
- **Containerization**: Docker

## Project Structure

planet-api/
├── app/
│   └── main.py          # FastAPI app with single endpoint
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── CLAUDE.md