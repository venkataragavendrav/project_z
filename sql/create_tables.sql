-- sql/create_tables.sql

CREATE TABLE IF NOT EXISTS data_profile (
    id SERIAL PRIMARY KEY,
    datasource VARCHAR NOT NULL,
    table_name VARCHAR NOT NULL,
    profile_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    column_name VARCHAR NOT NULL,
    null_percentage FLOAT,
    distinct_count INT,
    duplicate_count INT,
    min_value VARCHAR,
    max_value VARCHAR,
    run_id UUID NOT NULL
);

CREATE TABLE IF NOT EXISTS schema_versions (
    id SERIAL PRIMARY KEY,
    datasource VARCHAR NOT NULL,
    table_name VARCHAR NOT NULL,
    detected_schema JSONB NOT NULL,
    detected_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    change_detected BOOLEAN DEFAULT FALSE,
    previous_schema_id INT
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    alert_type VARCHAR NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    severity VARCHAR CHECK (severity IN ('info', 'warning', 'critical')),
    run_id UUID NOT NULL
);
