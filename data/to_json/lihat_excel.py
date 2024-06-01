import pandas as pd
import json

def build_hierarchy(df, level=0):
    hierarchy = []
    i = 0
    while i < len(df):
        row = df.iloc[i]
        if pd.notna(row[level]):
            node = {'name': row[level], 'children': []}
            i += 1
            # Build children for the next level
            children = build_hierarchy(df.iloc[i:], level + 1)
            node['children'] = children
            i += len(children)
            hierarchy.append(node)
        else:
            break
    return hierarchy

def excel_to_hierarchy_json(file_path):
    # Membaca file Excel
    df = pd.read_excel(file_path, header=None)

    # Build hierarchy from DataFrame
    hierarchy = build_hierarchy(df)

    # Save hierarchy to JSON file
    with open('hierarchy.json', 'w') as f:
        json.dump(hierarchy, f, indent=2)

# Contoh penggunaan
excel_to_hierarchy_json('data_hirarki.xlsx')
