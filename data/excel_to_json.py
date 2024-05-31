import pandas as pd
import json

def excel_to_hierarchy_json(file_path):
    # Membaca file Excel
    df = pd.read_excel(file_path, header=None)
    
    def build_hierarchy(df):
        hierarchy = []
        i = 0
        level = 1;
        while i < len(df):
            row = df.iloc[i]
            if pd.notna(row[0]):
                node = {'name': row[0], 'children': []}
                i += 1
                level = 2
                # Build children for level 2
                children = []
                while i < len(df) and pd.isna(df.iloc[i, 0]):
                    if pd.notna(df.iloc[i, 1]):
                        child_node = {'name': df.iloc[i, 1], 'children': [], 'level':level}
                        i += 1
                        children.append(child_node)
                    i += 1
                node['children'] = children
                hierarchy.append(node)
            else:
                i += 1
                
        return hierarchy

    # Build hierarchy from DataFrame
    hierarchy = build_hierarchy(df)

    # Save hierarchy to JSON file
    with open('hierarchy_level_2.json', 'w') as f:
        json.dump(hierarchy, f, indent=2)

# Contoh penggunaan
excel_to_hierarchy_json('data_hirarki.xlsx')
