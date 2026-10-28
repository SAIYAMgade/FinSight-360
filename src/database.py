"""Database interface module supporting PostgreSQL and SQLite for FinSight 360."""
from pathlib import Path
import logging
from typing import Optional, Dict, Any
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

logger = logging.getLogger("finsight360.database")


def get_db_engine(config: Dict[str, Any]) -> Engine:
    """
    Construct a SQLAlchemy Engine based on configuration.
    Defaults to SQLite if PostgreSQL is unavailable or configured.
    """
    db_cfg = config.get("database", {})
    engine_type = db_cfg.get("engine", "sqlite").lower()

    if engine_type == "postgresql":
        pg_user = db_cfg.get("pg_user", "postgres")
        pg_pwd = db_cfg.get("pg_password", "password123")
        pg_host = db_cfg.get("pg_host", "localhost")
        pg_port = db_cfg.get("pg_port", 5432)
        pg_db = db_cfg.get("pg_database", "finsight360")
        url = f"postgresql://{pg_user}:{pg_pwd}@{pg_host}:{pg_port}/{pg_db}"
        logger.info(f"Connecting to PostgreSQL database at {pg_host}:{pg_port}/{pg_db}")
    else:
        db_path = config.get("paths", {}).get("db_path", "data/processed/finsight360.db")
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        url = f"sqlite:///{db_path}"
        logger.info(f"Connecting to local SQLite database at {db_path}")

    return create_engine(url, pool_pre_ping=True)


def execute_sql_file(engine: Engine, sql_path: str) -> None:
    """Read and execute a multi-statement SQL script file safely."""
    path = Path(sql_path)
    if not path.exists():
        logger.warning(f"SQL file not found: {sql_path}")
        return

    logger.info(f"Executing SQL file: {sql_path}...")
    with open(path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    def clean_statement(stmt: str) -> str:
        lines = [line for line in stmt.split("\n") if not line.strip().startswith("--")]
        return "\n".join(lines).strip()

    raw_statements = sql_content.split(";")
    statements = [clean_statement(stmt) for stmt in raw_statements if clean_statement(stmt)]

    with engine.begin() as conn:
        for stmt in statements:
            if not stmt:
                continue
            try:
                conn.execute(text(stmt))
            except Exception as e:
                logger.warning(f"Statement execution notice in {path.name}: {e}")


def load_dataframe_to_table(
    engine: Engine,
    df: pd.DataFrame,
    table_name: str,
    if_exists: str = "replace",
    chunksize: int = 50000
) -> int:
    """
    Efficiently stream and load a pandas DataFrame into a SQL table.

    Returns:
        Number of records loaded.
    """
    logger.info(f"Loading {len(df):,} records into SQL table '{table_name}' (mode: {if_exists})...")
    df.to_sql(
        table_name,
        con=engine,
        if_exists=if_exists,
        index=False,
        chunksize=chunksize,
        method=None
    )
    logger.info(f"Successfully loaded {len(df):,} records into '{table_name}'.")
    return len(df)


def run_query(engine: Engine, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Execute a read-only analytical SQL query and return DataFrame."""
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn, params=params)
