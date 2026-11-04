"""CLI application."""

import logging

import typer

from src.config.settings import settings
from src.data.dataset import prepare_dataset
from src.data.preprocessing import DataPreprocessor

logger = logging.getLogger(__name__)

app = typer.Typer(
    help="Medical Review Sentiment Analysis CLI",
)


@app.command()
def prepare_data(force: bool = typer.Option(False, help="Force re-download of dataset")) -> None:
    """Prepare and download dataset."""
    typer.echo("Preparing dataset...")
    path = prepare_dataset(force=force)
    typer.echo(f"Dataset ready at: {path}")


@app.command()
def preprocess(input_file: str = typer.Option(..., help="Input CSV file")) -> None:
    """Preprocess dataset."""
    import pandas as pd

    typer.echo(f"Preprocessing {input_file}...")
    df = pd.read_csv(input_file)

    preprocessor = DataPreprocessor()
    df_clean = preprocessor.clean(df)
    df_clean.to_csv(input_file.replace(".csv", "_processed.csv"), index=False)
    typer.echo("Done!")


@app.command()
def train() -> None:
    """Train sentiment model."""
    typer.echo("Training model...")
    typer.echo("This feature requires running the full pipeline with Python directly.")


if __name__ == "__main__":
    app()
