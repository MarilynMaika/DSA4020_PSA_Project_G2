import pandas as pd

# --- File paths (update if needed) ---
file1 = "agriculture_psas_TRANSLATED.csv"
file2 = "combined_psa_all_languages.csv"
file3 = "kenya_psa_filtered.csv"

target_cols = ["PSA_ID", "Domain", "English", "Kiswahili", "Ekegusii"]

# Map each file's actual column names -> target column names
rename_maps = {
    file1: {
        "PSA_Id": "PSA_ID",
        "Domain": "Domain",
        "English": "English",
        "Kiswahili": "Kiswahili",
        "Ekegusii": "Ekegusii",
    },
    file2: {
        "PSA_ID": "PSA_ID",
        "Domain": "Domain",
        "English": "English",
        "Kiswahili": "Kiswahili",
        "Ekegusii": "Ekegusii",
    },
    file3: {
        "PSA_ID": "PSA_ID",
        "Domain": "Domain",
        "text_en": "English",
        "text_sw": "Kiswahili",
        "text_guz": "Ekegusii",
    },
}

dfs = []
for path, colmap in rename_maps.items():
    df = pd.read_csv(path, encoding="utf-8-sig")
    df = df.rename(columns=colmap)
    # Keep only the target columns that exist, add missing ones as empty
    for col in target_cols:
        if col not in df.columns:
            df[col] = ""
    df = df[target_cols]
    dfs.append(df)

merged = pd.concat(dfs, ignore_index=True)

output_path = "Final_merged_psas.csv"
merged.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Merged {len(dfs)} files into '{output_path}' with {len(merged)} total rows.")
