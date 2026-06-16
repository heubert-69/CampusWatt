import psy2cog
import asyncio
import os
password = os.getenv("db_password")
user = os.getenv("db_user")

init_db = False

def init_db():
    db = async await psy2cog.AsyncConnection.connect("campuswatt.db", user="postgres", password="postgres")

    cursor = db.cursor()

    cursor.execute(
        """
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
            explanation VARCHAR(100000) NOT NULL,
            confidence_score NUMERIC(5, 4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
            inference_time_ms INTEGER,
            has_error BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS causal_results(
            id UUID PRIMARY KEY DEFAULt gen_random_uuid(),
            model_name VARCHAR(100) NOT NULL,
            input_data JSONB NOT NULL,
            prediction_output JSONB NOT NULL,
            inference_time_ms INTEGER,
            has_error BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
    )



