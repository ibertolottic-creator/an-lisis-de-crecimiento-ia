import docx
import pandas as pd
import os
import re

def clean_val(val):
    if not val: return 0
    clean = re.sub(r'[^\d-]', '', str(val))
    try:
        return int(clean)
    except:
        return 0

def get_mes(etapa):
    mapping = {
        '1': 'Enero', '2': 'Febrero', '3': 'Marzo', '4': 'Abril',
        '5': 'Mayo', '6': 'Junio', '7': 'Julio', '8': 'Agosto',
        '9': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
    }
    return mapping.get(str(etapa), etapa)

def format_pct(val, den):
    if den == 0: return "N/A*"
    pct = (val / den) * 100
    return f"{round(pct, 1)}%"

def format_signed_int(val):
    if val > 0: return f"+{val}"
    return str(val)

def process_docx(file_path, is_posgrado=False):
    doc = docx.Document(file_path)
    table = doc.tables[0]
    data = []
    
    for i, row in enumerate(table.rows):
        cells = [cell.text.strip() for cell in row.cells]
        if not cells[0] or not cells[0].isdigit(): continue
        
        prog_idx = 3 if is_posgrado else 2
        if cells[prog_idx].lower().startswith('total'): continue
        
        if is_posgrado:
            row_data = {
                'Mes': get_mes(cells[0]),
                'Programa': cells[3],
                'Egresados': clean_val(cells[4]),
                'No matrí.': clean_val(cells[5]),
                'Admitidos': clean_val(cells[6]),
                'Admitidos Matriculados': clean_val(cells[7]),
                'Recuperados': clean_val(cells[8]),
                'Matríc. regular a Distancia': clean_val(cells[9]),
                'Estudiantes matrí. TOTAL': clean_val(cells[10]),
                'Alumnos en Asignaturas de 2 Meses': clean_val(cells[11])
            }
        else:
            row_data = {
                'Mes': get_mes(cells[0]),
                'Programa': cells[2],
                'Egresados': clean_val(cells[3]),
                'No matrí.': clean_val(cells[4]),
                'Admitidos': clean_val(cells[5]),
                'Admitidos Matriculados': clean_val(cells[6]),
                'Recuperados': clean_val(cells[7]),
                'Matríc. regular a Distancia': clean_val(cells[8]),
                'Matríc. regular Presencial': clean_val(cells[9]),
                'Estudiantes matrí. TOTAL': clean_val(cells[10]),
                'Alumnos en Asignaturas de 2 Meses': clean_val(cells[11])
            }
        data.append(row_data)
    
    df = pd.DataFrame(data)
    
    # Calculations
    fuga = df['Admitidos'] - df['Admitidos Matriculados']
    desercion = df['No matrí.'] - df['Recuperados']
    brecha = df['Egresados'] - df['Admitidos Matriculados']
    crecimiento = (df['Admitidos Matriculados'] + df['Recuperados']) - (df['No matrí.'] + df['Egresados'])
    
    # Metrics
    df['Pérdida de Conversión Comercial(Fuga: Admit. - Adm. Mat.)'] = fuga.apply(format_signed_int)
    df['Deserción Neta(Irreversible: No mat. - Recup.)'] = desercion.apply(format_signed_int)
    df['Brecha de Reemplazo(Vacío: Egresados - Adm. Mat.)'] = brecha.apply(format_signed_int)
    df['Crecimiento Neto Estudiantil(Balance: Entradas - Salidas)'] = crecimiento.apply(format_signed_int)
    
    df['Tasa Efectividad Comercial(% Cierres: Adm.Mat./Admit.)'] = df.apply(lambda r: format_pct(r['Admitidos Matriculados'], r['Admitidos']), axis=1)
    df['Tasa Éxito Retención(% Hemorragia: Rec./No mat.)'] = df.apply(lambda r: format_pct(r['Recuperados'], r['No matrí.']), axis=1)
    df['Tasa Renovación Genuina(% Inyección: Adm.Mat./Dist.)'] = df.apply(lambda r: format_pct(r['Admitidos Matriculados'], r['Matríc. regular a Distancia']), axis=1)
    
    if not is_posgrado:
        df['Proporción de Matrícula en Cierre(% Presencial: Pres./Total)'] = df.apply(lambda r: format_pct(r['Matríc. regular Presencial'], r['Estudiantes matrí. TOTAL']), axis=1)
        
    return df

# Execution
carreras_path = r"c:\Users\Renato Bertolotti\Documents\an-lisis-de-crecimiento-ia\Resultados Generales Carreras Profesionales MAY26ob.docx"
maestrias_path = r"c:\Users\Renato Bertolotti\Documents\an-lisis-de-crecimiento-ia\Resultados Generales Maestrías MAY26ob.docx"

df_pre = process_docx(carreras_path, is_posgrado=False)
df_pre.to_csv(r"c:\Users\Renato Bertolotti\Documents\an-lisis-de-crecimiento-ia\Cuadro_Mando_Pregrado_Actualizado.csv", index=False, encoding='utf-8-sig')

df_pos = process_docx(maestrias_path, is_posgrado=True)
# Ensure only the requested columns for Posgrado
pos_cols = [
    'Mes', 'Programa', 'Egresados', 'No matrí.', 'Admitidos', 'Admitidos Matriculados', 'Recuperados', 
    'Matríc. regular a Distancia', 'Estudiantes matrí. TOTAL', 'Alumnos en Asignaturas de 2 Meses',
    'Pérdida de Conversión Comercial(Fuga: Admit. - Adm. Mat.)', 'Deserción Neta(Irreversible: No mat. - Recup.)',
    'Brecha de Reemplazo(Vacío: Egresados - Adm. Mat.)', 'Crecimiento Neto Estudiantil(Balance: Entradas - Salidas)',
    'Tasa Efectividad Comercial(% Cierres: Adm.Mat./Admit.)', 'Tasa Éxito Retención(% Hemorragia: Rec./No mat.)',
    'Tasa Renovación Genuina(% Inyección: Adm.Mat./Dist.)'
]
df_pos = df_pos[pos_cols]
df_pos.to_csv(r"c:\Users\Renato Bertolotti\Documents\an-lisis-de-crecimiento-ia\Cuadro_Mando_Posgrado_Actualizado.csv", index=False, encoding='utf-8-sig')

print("Files updated with specific column structures for Pregrado and Posgrado.")
