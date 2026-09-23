"""Database and service connectivity utilities for PostgreSQL, Redis, and Ollama.

Provides robust connection checking and beginner-friendly error messages
guiding the user on how to start any missing local service.
"""

from typing import Tuple, List
import requests
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import redis
from pgvector.psycopg2 import register_vector

import config


def ensure_postgres_database() -> Tuple[bool, str]:
    """Ensures PostgreSQL is running, the target database exists,

    and the pgvector extension is enabled.
    """
    # Step 1: Try connecting to PostgreSQL server (using default 'postgres' db if needed)
    try:
        conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            dbname="postgres",
            connect_timeout=3,
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Check if the specific database exists
        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s;",
            (config.POSTGRES_DB,),
        )
        exists = cur.fetchone()
        if not exists:
            cur.execute(
                sql.SQL("CREATE DATABASE {};").format(
                    sql.Identifier(config.POSTGRES_DB)
                )
            )
            print(f"[OK] Created database '{config.POSTGRES_DB}'.")

        cur.close()
        conn.close()

    except psycopg2.OperationalError as e:
        return (
            False,
            f"[ERROR] Cannot connect to PostgreSQL at {config.POSTGRES_HOST}:{config.POSTGRES_PORT}.\n"
            f"Details: {e}\n"
            "--> How to fix:\n"
            "    1. Make sure PostgreSQL is installed and running.\n"
            "    2. On Windows, start PostgreSQL via Services (services.msc) or run:\n"
            "       net start postgresql-x64-<version>\n"
            "    3. Verify credentials in config.py or .env.",
        )

    # Step 2: Connect to the target database and ensure pgvector extension
    try:
        target_conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            dbname=config.POSTGRES_DB,
            connect_timeout=3,
        )
        target_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        target_cur = target_conn.cursor()

        # Enable pgvector extension
        target_cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        register_vector(target_conn)

        target_cur.close()
        target_conn.close()
        return (
            True,
            f"[OK] Connected to PostgreSQL ('{config.POSTGRES_DB}') and pgvector extension is ready.",
        )

    except Exception as e:
        return (
            False,
            f"[ERROR] Connected to PostgreSQL, but failed to enable 'vector' extension.\n"
            f"Details: {e}\n"
            "--> How to fix:\n"
            "    Ensure the pgvector extension is installed in your PostgreSQL environment.",
        )


def check_redis_connection() -> Tuple[bool, str]:
    """Checks if the local Redis instance is running and reachable."""
    import socket

    # Quick TCP check first to avoid client hang
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.5)
    result = sock.connect_ex((config.REDIS_HOST, config.REDIS_PORT))
    sock.close()

    if result != 0:
        return (
            False,
            f"[ERROR] Cannot connect to Redis at {config.REDIS_HOST}:{config.REDIS_PORT}.\n"
            "--> How to fix:\n"
            "    1. Make sure Redis is installed and running.\n"
            "    2. On Windows, start Redis service or launch redis-server.exe.\n"
            "    3. If using WSL, run: sudo service redis-server start",
        )

    try:
        r = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        r.ping()
        return (
            True,
            f"[OK] Connected to Redis at {config.REDIS_HOST}:{config.REDIS_PORT} (DB {config.REDIS_DB}).",
        )
    except Exception as e:
        return (
            False,
            f"[ERROR] Redis connected on port but ping failed.\nDetails: {e}",
        )


def check_ollama_connection() -> Tuple[bool, str, List[str]]:
    """Checks if Ollama is running and whether the configured model is installed."""
    url = f"{config.OLLAMA_BASE_URL}/api/tags"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code != 200:
            return (
                False,
                f"[ERROR] Ollama responded with HTTP status {response.status_code}.",
                [],
            )

        data = response.json()
        models = [m.get("name", "") for m in data.get("models", [])]

        # Check if configured model exists (exact match or with :latest tag)
        target = config.OLLAMA_MODEL
        target_latest = f"{target}:latest" if ":" not in target else target

        found = any(m == target or m == target_latest or m.startswith(f"{target}:") for m in models)

        if not found:
            return (
                False,
                f"[WARNING] Ollama is running, but model '{target}' is NOT installed.\n"
                f"Installed models: {models if models else 'None'}\n"
                "--> Exact command to pull this model:\n"
                f"    ollama pull {target}",
                models,
            )

        return (
            True,
            f"[OK] Ollama is running at {config.OLLAMA_BASE_URL} with model '{target}' ready.",
            models,
        )

    except requests.exceptions.RequestException as e:
        return (
            False,
            f"[ERROR] Cannot connect to Ollama at {config.OLLAMA_BASE_URL}.\n"
            f"Details: {e}\n"
            "--> How to fix:\n"
            "    1. Install Ollama from https://ollama.com\n"
            "    2. Start Ollama: Open Ollama desktop application or run in terminal:\n"
            "       ollama serve\n"
            f"    3. In another terminal, pull the required model:\n"
            f"       ollama pull {config.OLLAMA_MODEL}",
            [],
        )
