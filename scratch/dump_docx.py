import docx
import pandas as pd
import os

def dump_docx_table(file_path):
    print(f"\n{'='*50}\nDumping: {file_path}\n{'='*50}")
    doc = docx.Document(file_path)
    table = doc.tables[0]
    data = []
    for i, row in enumerate(table.rows):
        cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
        data.append(cells)
    
    df = pd.DataFrame(data)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)
    print(df.to_string(index=False, header=False))

files = [
    "Resultados Generales Carreras Profesionales MAY26ob.docx",
    "Resultados Generales Maestrías MAY26ob.docx"
]

for f in files:
    full_path = os.path.join(r"c:\Users\Renato Bertolotti\Documents\an-lisis-de-crecimiento-ia", f)
    if os.path.exists(full_path):
        dump_docx_table(full_path)
    else:
        print(f"File not found: {full_path}")
