import pandas as pd

# Caminho de entrada e saída
csv_path = r"C:\Users\leona\Downloads\expermentSurvey\RQ1\respostas.csv"
output_path = r"C:\Users\leona\Downloads\expermentSurvey\RQ1\respostas_rq1intuitiveAge.csv"

# Carrega o CSV original
df = pd.read_csv(csv_path)
df.columns = df.columns.str.replace('\n', ' ', regex=False).str.replace(r'\s+', ' ', regex=True).str.strip()

# --- Filtragem de participantes inválidos --- #
def get_participants_no_consent(df):
    col = next((c for c in df.columns if "agree" in c.lower()), None)
    if not col:
        return []
    return df[df[col].str.strip().str.lower() == "no"].index.tolist()

def get_participants_all_same_answers(df):
    comparison_cols = [c for c in df.columns if "Comparison" in c]
    same = []
    for idx, row in df[comparison_cols].iterrows():
        values = row.fillna("").astype(str).str.strip().str.upper()
        filtered = values[values.isin(["A", "B"])]
        if len(filtered) == 44 and filtered.nunique() == 1:
            same.append(idx)
    return same

# Aplicar exclusões
excluded_indices = sorted(set(get_participants_no_consent(df) + get_participants_all_same_answers(df)))
df_valid = df.drop(index=excluded_indices).reset_index(drop=True)
df_valid.insert(0, "pID", [f"P{i+1}" for i in range(len(df_valid))])

# --- Mapeamento e Extração das Colunas --- #
ab_mapping = {
    1:  ('JavaMOP', 'MSL'),
    2:  ('MSL', 'JavaMOP'),
    3:  ('JavaMOP', 'MSL'),
    4:  ('JavaMOP', 'MSL'),
    5:  ('MSL', 'JavaMOP'),
    6:  ('JavaMOP', 'MSL'),
    7:  ('MSL', 'JavaMOP'),
    8:  ('JavaMOP', 'MSL'),
    9:  ('JavaMOP', 'MSL'),
    10: ('MSL', 'JavaMOP'),
    11: ('JavaMOP', 'MSL')
}

question_labels = [
    ('Is more intuitive and understandable', 'intuitive')#,
   # ('Allows for faster and more direct specification writing for the proposed scenario', 'faster'),
   # ('Requires greater detail and rigor when writing specifications', 'detailed'),
   # ('Offers simpler syntax', 'simpler')
]

# Seleção de colunas demográficas específicas
demographic_cols = [
  #  'Do you agree in participate?',
    'What is your age group?',
  #  'Gender:',
  #  'Professional experience as a software developer :',
  #  'What is your main area of expertise?',
  #  'Which programming languages do you regularly use?',
  #  'Have you ever heard of runtime verification tools or specification languages?'
]

# Iniciar nova estrutura com pID + demográficas
new_data = df_valid[['pID'] + demographic_cols].copy()

# Adicionar colunas mapeadas por cenário e pergunta
for scenario in range(1, 12):
    a_label, b_label = ab_mapping[scenario]
    for q_idx, (q_text, short_label) in enumerate(question_labels, start=1):
        col_match = [c for c in df.columns if f"{scenario}" in c.split(')')[0] and q_text in c]
        if col_match:
            raw_col = col_match[0]
            answers = df_valid[raw_col].fillna("").astype(str).str.strip().str.upper()
            mapped = answers.map({'A': a_label, 'B': b_label}).fillna("")
            new_col = f"{scenario}.{q_idx}_{short_label}"
            new_data[new_col] = mapped

# Salvar CSV final
new_data.to_csv(output_path, index=False)
print(f"✅ Arquivo gerado: {output_path}")
