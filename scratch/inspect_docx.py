import docx
import pandas as pd
import os

def inspect_docx(file_path):
    print(f"--- Inspecting: {file_path} ---")
    doc = docx.Document(file_path)
    for i, table in enumerate(doc.tables):
        print(f"\nTable {i}:")
        data = []
        for row in table.rows:
            data.append([cell.text.strip() for cell in row.cells])
        if data:
            df = pd.DataFrame(data)
            print(df.head(10).to_string())
        else:
            print("Empty table")

files = [
    "Resultados Generales Carreras Profesionales MAY26ob.docx",
    "Resultados Generales Maestrías MAY26ob.docx"
]

for f in files:
    full_path = os.path.join(r"c:\Users\Renato Bertolotti\Documents\an-lisis-de-crecimiento-ia", f)
    if os.path.exists(full_path):
        inspect_docx(full_path)
    else:
        print(f"File not found: {full_path}")
