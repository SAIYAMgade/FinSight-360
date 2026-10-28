"""Generate a representative stratified sample of the lending dataset."""
from pathlib import Path
import logging
import pandas as pd
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("finsight360.sample")


def generate_stratified_sample(
    raw_path: str = "data/raw/lending_club_loan_two.csv",
    output_path: str = "data/sample/loans_sample.csv",
    sample_size: int = 25000,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generate a deterministic, stratified sample of the raw dataset.

    Args:
        raw_path: Path to the raw CSV file.
        output_path: Target path for the sample CSV.
        sample_size: Target record count.
        random_seed: Fixed random seed for complete reproducibility.

    Returns:
        Sampled DataFrame.
    """
    logger.info(f"Loading raw dataset from {raw_path} for stratified sampling...")
    df = pd.read_csv(raw_path, low_memory=False)

    total_records = len(df)
    fraction = sample_size / total_records

    logger.info(
        f"Sampling {sample_size:,} records from {total_records:,} "
        f"({fraction * 100:.2f}%) stratified by 'loan_status' (seed={random_seed})..."
    )

    sample_df, _ = train_test_split(
        df,
        train_size=sample_size,
        random_state=random_seed,
        stratify=df["loan_status"]
    )

    sample_df = sample_df.sort_index().reset_index(drop=True)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    sample_df.to_csv(output_path, index=False)
    logger.info(f"Sample saved to {output_path} ({len(sample_df):,} records).")

    # Verify distributions
    pop_dist = df["loan_status"].value_counts(normalize=True)
    sample_dist = sample_df["loan_status"].value_counts(normalize=True)
    logger.info(f"Population distribution:\n{pop_dist}")
    logger.info(f"Sample distribution:\n{sample_dist}")

    return sample_df


if __name__ == "__main__":
    generate_stratified_sample()
