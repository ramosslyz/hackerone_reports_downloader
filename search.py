import streamlit as st
import os
import json

# Function to read JSON files into memory and build an index
def build_index():
    index = {}
    json_dir = 'json_reports'  # Path to your JSON files directory
    
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            with open(os.path.join(json_dir, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                index[filename] = data
    return index

# Function to perform partial text search for a keyword
def partial_text_search(keyword, index):
    keyword = keyword.lower()
    results = []

    for filename, text in index.items():
        if keyword in str(text).lower():
            results.append([filename, text])
    
    return results

# Main Streamlit app
def main():
    st.title("JSON Search Engine")
    st.sidebar.header("Search")

    # Load JSON data into memory when the app is first run
    if 'index' not in st.session_state:
        st.session_state.index = build_index()

    # User input for partial text search
    search_query = st.sidebar.text_input("Enter a keyword (partial text search):")
    if st.sidebar.button("Search"):
        results = partial_text_search(search_query, st.session_state.index)
        
        if not results:
            st.warning("No matching JSON files found.")
        else:
            st.success(f"Found {len(results)} matching JSON files.")

        for result in results:
            with st.expander(f"{result[1]['title']}"):
                st.code(json.dumps(result[1], indent=4), language='json')

if __name__ == "__main__":
    main()
