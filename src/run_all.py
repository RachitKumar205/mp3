"""Run the full MP3 analysis from the raw Excel file to every table and figure."""

import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent

for step in ["01_prepare.py", "02_eda.py", "03_cluster.py", "04_profile.py"]:
    print(f"== {step}")
    runpy.run_path(str(HERE / step), run_name="__main__")
