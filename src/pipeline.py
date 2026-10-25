
from pathlib import Path
import subprocess
import sys
import logging

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

STEPS = [
    "src/inspect_data.py",
    "src/data_quality.py",
    "src/transform.py",
    "src/load_sql.py",
    "src/run_sql.py",
    "src/pyspark_transform.py",
]

def run_step(script):
    logging.info("Starting %s", script)
    print(f"\n{'=' * 12} Running {script} {'=' * 12}", flush=True)

    result = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=ROOT,
        text=True
    )

    if result.returncode != 0:
        logging.error("Failed: %s", script)
        raise RuntimeError(f"Pipeline stopped at {script}")

    logging.info("Completed %s", script)
    print(f"Completed: {script}", flush=True)

def main():
    try:
        for step in STEPS:
            run_step(step)

        logging.info("ETL pipeline completed successfully")
        print("\nETL PIPELINE COMPLETED SUCCESSFULLY!")

    except Exception:
        logging.exception("ETL pipeline failed")
        raise

if __name__ == "__main__":
    main()
