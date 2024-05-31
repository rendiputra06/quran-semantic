import pandas as pd
import json

def excel_to_hierarchy_json(file_path):
    # Membaca file Excel
    df = pd.read_excel(file_path, header=None)

    def build_hierarchy(df):
        def add_children(df, parent_row, level):
            children = []
            i = parent_row + 1
            while i < len(df) and pd.isna(df.iloc[i, level - 1]):
                if pd.notna(df.iloc[i, level]):
                    child_node = {'name': df.iloc[i, level], 'children': []}
                    child_node['children'] = add_children(df, i, level + 1)
                    children.append(child_node)
                i += 1
            return children

        hierarchy = []
        i = 0
        while i < len(df):
            if pd.notna(df.iloc[i, 0]):
                node = {'name': df.iloc[i, 0], 'children': add_children(df, i, 1)}
                hierarchy.append(node)
            i += 1

        return hierarchy
    
    # Build hierarchy from DataFrame
    hierarchy = build_hierarchy(df)

    # Save hierarchy to JSON file
    with open('cek_3.json', 'w') as f:
        json.dump(hierarchy, f, indent=2)

# Contoh penggunaan
excel_to_hierarchy_json('data_hirarki.xlsx')
