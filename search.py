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
    # set config to wide mode
    st.set_page_config(layout="wide", page_title="HackerOne Search Engine", page_icon="🔍", )



    st.title("HackerOne Search Engine")
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
            st.success(f"Found {len(results)} matching Reports for Query : {search_query}.")


        for result in results[:50]:
            try:
                report_title = result[1]['title']
            except KeyError:
                report_title = "Default Title"

            try:
                report_url = result[1]['url']
            except KeyError:
                report_url = "Default URL"

            try:
                severity = result[1]['severity_rating']
            except KeyError:
                severity = "Default Severity"

            try:
                submitted_at = result[1]['submitted_at']
            except KeyError:
                submitted_at = "Default Submitted At"

            try:
                reporter_username = result[1]['reporter']['username']
            except (KeyError, TypeError):
                reporter_username = "Default Reporter Username"

            try:
                team = result[1]['team']['handle']
            except (KeyError, TypeError):
                team = "Default Team Handle"

            try:
                vulnerability_information = result[1]['vulnerability_information']
            except KeyError:
                vulnerability_information = "Default Vulnerability Information"

            try:
                weakness = result[1]['weakness']['name']
            except (KeyError, TypeError):
                weakness = "Default Weakness Name"

            st.markdown(f"### {report_title}")
            column1, column2 = st.columns([1, 1])
            column1.markdown(f"**URL:** {report_url}")
            column2.markdown(f"**Severity:** {severity}")
            column3, column4 = st.columns([1, 1])
            column3.markdown(f"**Submitted at:** {submitted_at}")
            column4.markdown(f"**Reporter:** {reporter_username}")
            column5 , column6 = st.columns([1, 1])
            column5.markdown(f"**Team:** {team}")
            column6.markdown(f"**Weakness:** {weakness}")
            
            with st.expander(f"Expand Report"):
                st.markdown(f"**Vulnerability Information:** {vulnerability_information}")
            with st.expander(f"Raw Report Data in JSON"):
                st.code(json.dumps(result[1], indent=4))
            st.markdown("---")

if __name__ == "__main__":
    main()
