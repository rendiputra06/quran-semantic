import pandas as pd
import json

def excel_to_hierarchy_json(file_path, sheet_name):
    # Membaca seluruh sheet dari file Excel
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    # Membuat sub-dataframe yang dimulai dari kolom B dan melewati dua baris pertama
    df = df.iloc[2:, 1:]

    def build_hierarchy(df):
        def add_children(df, parent_row, level, current_id):
            if level > 5:
                return [], current_id
            children = []
            i = parent_row + 1
            while i < len(df) and pd.isna(df.iloc[i, level - 1]):
                if pd.notna(df.iloc[i, level]):
                    current_id += 1
                    child_node = {'id': current_id, 'name': df.iloc[i, level], 'children': []}
                    child_node['children'], current_id = add_children(df, i, level + 1, current_id)
                    children.append(child_node)
                i += 1
            return children, current_id

        hierarchy = []
        current_id = 0
        i = 0
        while i < len(df):
            if pd.notna(df.iloc[i, 0]):
                current_id += 1
                node = {'id': current_id, 'name': df.iloc[i, 0], 'children': []}
                node['children'], current_id = add_children(df, i, 1, current_id)
                hierarchy.append(node)
            i += 1

        return hierarchy

    def extract_special_data(df, hierarchy):
        special_data = {}
        for i in range(len(df)):
            row = df.iloc[i]
            for col in range(5, len(row)):  # Mulai dari kolom keenam (index 5)
                if pd.notna(row[col]):
                    node_id = find_id_by_row(hierarchy, i)
                    if node_id not in special_data:
                        special_data[node_id] = []
                    special_data[node_id].append(row[col])
        return special_data

    def find_id_by_row(hierarchy, row_number):
        def search_node(node, current_row):
            if node['id'] == current_row + 1:
                return node['id']
            for child in node['children']:
                result = search_node(child, current_row)
                if result:
                    return result
            return None

        for node in hierarchy:
            result = search_node(node, row_number)
            if result:
                return result
        return None

    # Build hierarchy from DataFrame
    hierarchy = build_hierarchy(df)

    # Extract special data
    special_data = extract_special_data(df, hierarchy)

    # Save hierarchy to JSON file
    with open('cek_4.json', 'w') as f:
        json.dump(hierarchy, f, indent=2)

    # Save special data to JSON file
    with open('special_data.json', 'w') as f:
        json.dump(special_data, f, indent=2)

# Contoh penggunaan
excel_to_hierarchy_json('data_hirarki.xlsx', 'Sheet1')