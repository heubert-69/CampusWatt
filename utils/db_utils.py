import psycopg
import os

DB_PASSWORD = os.getenv("db_password")
DB_USER = os.getenv("db_user")

DB_INITIALIZED = False


async def init_db():

    global DB_INITIALIZED

    db = await psycopg.AsyncConnection.connect(
        host="localhost",
        port=5432,
        dbname="campuswatt",
        user=DB_USER,
        password=DB_PASSWORD
    )

    async with db.cursor() as cursor:

        await cursor.execute("""
        CREATE EXTENSION IF NOT EXISTS pgcrypto;

        CREATE TABLE IF NOT EXISTS users(
            id BIGSERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS prediction_results(
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            model_name VARCHAR(100) NOT NULL,
            input_data JSONB NOT NULL,
            prediction_output JSONB NOT NULL,
            explanation TEXT NOT NULL,
            confidence_score NUMERIC(5,4)
                CHECK (confidence_score >= 0 AND confidence_score <= 1),
            inference_time_ms INTEGER,
            has_error BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS causal_results(
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            model_name VARCHAR(100) NOT NULL,
            input_data JSONB NOT NULL,
            prediction_output JSONB NOT NULL,
            inference_time_ms INTEGER,
            has_error BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
        """)

    await db.commit()

    DB_INITIALIZED = True

    print("[DB] Initialized")

    return db

