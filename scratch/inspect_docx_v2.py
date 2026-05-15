import docx
import pandas as pd
import os

def inspect_docx(file_path):
    print(f"\n{'='*50}\nInspecting: {file_path}\n{'='*50}")
    doc = docx.Document(file_path)
    for i, table in enumerate(doc.tables):
        print(f"\nTable {i}:")
        data = []
        for row in table.rows:
            data.append([cell.text.strip().replace('\n', ' ') for cell in row.cells])
        if data:
            df = pd.DataFrame(data)
            # Use the first row as header if it looks like one
            if len(df) > 1:
                df.columns = df.iloc[0]
                df = df[1:]
            print(f"Columns: {list(df.columns)}")
            print(df.head(5).to_string())
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
