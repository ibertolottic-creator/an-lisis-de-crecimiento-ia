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
    
    # Identify data rows and column indices
    for i, row in enumerate(table.rows):
        cells = [cell.text.strip() for cell in row.cells]
        if not cells[0] or not cells[0].isdigit(): continue
        
        # Skip summary rows
        prog_idx = 3 if is_posgrado else 2
        if cells[prog_idx].lower().startswith('total'): continue
        
        # Mapping indices
        if is_posgrado:
            # Etapa(0), Fecha(1), Fecha(2), Program(3), Egresados(4), NoMat(5), Admit(6), AdmMat(7), Rec(8), Dist(9), Total(10), 2Mes(11)
            row_data = {
                'Mes': get_mes(cells[0]),
                'Programa': cells[3],
                'Egresados': clean_val(cells[4]),
                'No matrí.': clean_val(cells[5]),
                'Admitidos': clean_val(cells[6]),
                'Admitidos Matriculados': clean_val(cells[7]),
                'Recuperados': clean_val(cells[8]),
                'Matríc. regular a Distancia': clean_val(cells[9]),
                'Matríc. regular Presencial': 0,
                'Estudiantes matrí. TOTAL': clean_val(cells[10]),
                'Alumnos en Asignaturas de 2 Meses': clean_val(cells[11])
            }
        else:
            # Etapa(0), Fecha(1), Program(2), Egresados(3), NoMat(4), Admit(5), AdmMat(6), Rec(7), Dist(8), Pres(9), Total(10), 2Mes(11)
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
    
    # Apply special formatting for Integers
    df['Pérdida de Conversión Comercial(Fuga: Admit. - Adm. Mat.)'] = fuga.apply(format_signed_int)
    df['Deserción Neta(Irreversible: No mat. - Recup.)'] = desercion.apply(format_signed_int)
    df['Brecha de Reemplazo(Vacío: Egresados - Adm. Mat.)'] = brecha # Brecha usually integer sign as is
    df['Crecimiento Neto Estudiantil(Balance: Entradas - Salidas)'] = crecimiento.apply(format_signed_int)
    
    # Apply percentage formatting
    df['Tasa Efectividad Comercial(% Cierres: Adm.Mat./Admit.)'] = df.apply(lambda r: format_pct(r['Admitidos Matriculados'], r['Admitidos']), axis=1)
    df['Tasa Éxito Retención(% Hemorragia: Rec./No mat.)'] = df.apply(lambda r: format_pct(r['Recuperados'], r['No matrí.']), axis=1)
    df['Tasa Renovación Genuina(% Inyección: Adm.Mat./Dist.)'] = df.apply(lambda r: format_pct(r['Admitidos Matriculados'], r['Matríc. regular a Distancia']), axis=1)
    
    if is_posgrado:
        df['Proporción de Matrícula en Cierre(% Presencial: Pres./Total)'] = "0.0%"
    else:
        df['Proporción de Matrícula en Cierre(% Presencial: Pres./Total)'] = df.apply(lambda r: format_pct(r['Matríc. regular Presencial'], r['Estudiantes matrí. TOTAL']), axis=1)
    
    return df

# Main execution
carreras_path = r"c:\Users\Renato Bertolotti\Documents\an-lisis-de-crecimiento-ia\Resultados Generales Carreras Profesionales MAY26ob.docx"
maestrias_path = r"c:\Users\Renato Bertolotti\Documents\an-lisis-de-crecimiento-ia\Resultados Generales Maestrías MAY26ob.docx"

print("Processing Carreras...")
df_pre = process_docx(carreras_path, is_posgrado=False)
df_pre.to_csv(r"c:\Users\Renato Bertolotti\Documents\an-lisis-de-crecimiento-ia\Cuadro_Mando_Pregrado_Actualizado.csv", index=False, encoding='utf-8-sig')

print("Processing Maestrías...")
df_pos = process_docx(maestrias_path, is_posgrado=True)
df_pos.to_csv(r"c:\Users\Renato Bertolotti\Documents\an-lisis-de-crecimiento-ia\Cuadro_Mando_Posgrado_Actualizado.csv", index=False, encoding='utf-8-sig')

print("Done! Formats matched to reference.")
