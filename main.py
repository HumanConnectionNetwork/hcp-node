"""
HCP Telegram Client

Application entry point.

This module exists to provide a stable executable entry point for local
development, Docker containers and future deployment environments.
"""

from app.bot import main


if __name__ == "__main__":
    main()
