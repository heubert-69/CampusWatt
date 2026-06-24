import psycopg
import os
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("db_password")
DB_USER = os.getenv("db_user")

DB_INITIALIZED = False
DB_CONNECTION = None

async def init_db():

    global DB_INITIALIZED
    global DB_CONNECTION

    if DB_INITIALIZED:
        print("[DB] Already initialized")
        return DB_CONNECTION

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
            model_version VARCHAR(50),
            input_data JSONB NOT NULL,
            prediction_output JSONB NOT NULL,
            explanation TEXT NOT NULL,
            feature_importance JSONB,
            confidence_score NUMERIC(5,4)
                CHECK (confidence_score >= 0 AND confidence_score <= 1),
            inference_time_ms INTEGER,
            has_error BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS causal_results(
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            model_name VARCHAR(100) NOT NULL,
            model_version VARCHAR(50),
            input_data JSONB NOT NULL,
            prediction_output JSONB NOT NULL,
            inference_time_ms INTEGER,
            has_error BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS recommendation_results(
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            recommendation TEXT NOT NULL,
            confidence_score NUMERIC(5,4),
            source_documents JSONB,
            generated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS audit_logs(
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            action VARCHAR(255),
            endpoint VARCHAR(255),
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_prediction_created
        ON prediction_results(created_at);

        CREATE INDEX IF NOT EXISTS idx_causal_created
        ON causal_results(created_at);
        """)

    await db.commit()

    DB_CONNECTION = db
    DB_INITIALIZED = True

    print("[DB] Initialized")

    return DB_CONNECTION


async def user_retrieval(username: str):

    db = await init_db()

    async with db.cursor() as cursor:

        await cursor.execute(
            """
            SELECT
                id,
                username,
                email,
                password_hash
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        row = await cursor.fetchone()

    await db.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "password_hash": row[3]
    }


async def create_user(
    username: str,
    email: str,
    password: str
):

    db = await init_db()

    password_hash = generate_password_hash(password)

    async with db.cursor() as cursor:

        await cursor.execute(
            """
            INSERT INTO users(
                username,
                email,
                password_hash
            )
            VALUES(%s, %s, %s)
            RETURNING id
            """,
            (
                username,
                email,
                password_hash
            )
        )

        user_id = await cursor.fetchone()

    await db.commit()
    await db.close()

    return user_id[0]

#Sanity Check
print("DB_USER =", DB_USER)
print("DB_PASSWORD_SET =", DB_PASSWORD is not None)





async def save_prediction_result(
    model_name,
    input_data,
    prediction_output,
    explanation="",
    confidence_score=None,
    inference_time_ms=None,
    has_error=False
):

    db = await init_db()

    async with db.cursor() as cursor:

        await cursor.execute(
            """
            INSERT INTO prediction_results(
                model_name,
                input_data,
                prediction_output,
                explanation,
                confidence_score,
                inference_time_ms,
                has_error
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                model_name,
                psycopg.types.json.Jsonb(input_data),
                psycopg.types.json.Jsonb(prediction_output),
                explanation,
                confidence_score,
                inference_time_ms,
                has_error
            )
        )

    await db.commit()
