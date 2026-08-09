import subprocess
from pathlib import Path

REACTIFPTM = r"C:\Users\freyj\AppData\Local\Python\pythoncore-3.14-64\Scripts\reactifptm.exe"

for folder in Path("af3_wgcna_output").iterdir():
    name = folder.name
    subprocess.run([
        REACTIFPTM,
        folder / f"{name}_confidences.json",
        folder / f"{name}_model.cif",
        "-o", folder / "results.json",
    ])
