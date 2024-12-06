# visualization.py

import streamlit as st
from Bio import PDB
import py3Dmol
import io
import json
import numpy as np
import plotly.express as px
import pandas as pd
from loguru import logger

# Configure logger
logger.add("afusion_visualization.log", rotation="1 MB", level="DEBUG")

# ========================================
# Functions that accept file paths
# ========================================

def read_cif_file(file_path):
    parser = PDB.MMCIFParser(QUIET=True)
    with open(file_path, 'r') as file:
        content = file.read()
    file_like = io.StringIO(content)
    structure = parser.get_structure('protein', file_like)
    return structure, content

def extract_pae_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    pae = np.array(data.get("pae", []), dtype=np.float16)  # Use np.float16
    token_chain_ids = data.get("token_chain_ids", [])
    return pae, token_chain_ids

def extract_summary_confidences(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# ========================================
# Functions that accept file objects (uploaded files)
# ========================================

def read_cif_file_obj(file_obj):
    parser = PDB.MMCIFParser(QUIET=True)
    content = file_obj.read().decode('utf-8')
    file_like = io.StringIO(content)
    structure = parser.get_structure('protein', file_like)
    return structure, content

def extract_pae_from_json_obj(file_obj):
    data = json.load(file_obj)
    pae = np.array(data.get("pae", []), dtype=np.float16)  # Use np.float16
    token_chain_ids = data.get("token_chain_ids", [])
    return pae, token_chain_ids

def extract_summary_confidences_obj(file_obj):
    data = json.load(file_obj)
    return data

# ========================================
# Common functions
# ========================================

def extract_residue_bfactors(structure):
    residue_bfactors = {}
    ligands = []
    for model in structure:
        for chain in model:
            for residue in chain:
                hetfield = residue.get_id()[0]
                resseq = residue.get_id()[1]
                resname = residue.get_resname()
                chain_id = chain.id

                atom_bfactors = []

                for atom in residue:
                    bfactor = atom.get_bfactor()

                    if hetfield.strip() == "":
                        atom_bfactors.append(bfactor)
                    else:
                        # Ligand atoms
                        ligands.append({
                            'chain_id': chain_id,
                            'resseq': resseq,
                            'resname': resname,
                            'atom_name': atom.get_name(),
                            'bfactor': bfactor
                        })

                if hetfield.strip() == "" and atom_bfactors:
                    avg_bfactor = sum(atom_bfactors) / len(atom_bfactors)
                    residue_bfactors[(chain_id, resseq)] = {
                        'avg_bfactor': avg_bfactor,
                        'resname': resname
                    }

    return residue_bfactors, ligands

def get_color_from_bfactor(bfactor):
    # Define color mapping
    color_mapping = [
        {'range': [90, 100], 'color': '#106dff'},   # Very high (pLDDT > 90)
        {'range': [70, 90],  'color': '#10cff1'},   # Confident (90 > pLDDT > 70)
        {'range': [50, 70],  'color': '#f6ed12'},   # Low (70 > pLDDT > 50)
        {'range': [0, 50],   'color': '#ef821e'}    # Very low (pLDDT < 50)
    ]
    for mapping in color_mapping:
        b_min, b_max = mapping['range']
        if b_min <= bfactor < b_max:
            return mapping['color']
    return 'grey'  # Default color

def visualize_structure(residue_bfactors, ligands, cif_content, background_color='#000000'):
    # Create a py3Dmol view
    view = py3Dmol.view(width='100%', height=600)
    view.addModel(cif_content, 'cif')

    # Set default style
    view.setStyle({'model': -1}, {'cartoon': {'color': 'grey'}})

    # Apply coloring based on B-factors
    for (chain_id, resseq), info in residue_bfactors.items():
        avg_bfactor = info['avg_bfactor']
        color = get_color_from_bfactor(avg_bfactor)
        selection = {'chain': chain_id, 'resi': resseq}
        style = {'cartoon': {'color': color}}
        view.addStyle(selection, style)

    # Color ligands
    for ligand in ligands:
        bfactor = ligand['bfactor']
        color = get_color_from_bfactor(bfactor)
        selection = {
            'chain': ligand['chain_id'],
            'resi': ligand['resseq'],
            'atom': ligand['atom_name']
        }
        style = {'stick': {'color': color}}
        view.addStyle(selection, style)

    # Set background color
    view.setBackgroundColor(background_color)

    # Generate HTML content
    view_html = view._make_html()
    return view_html

def display_visualization_header():
    st.write("### Visualization")
    color_mapping_html = """
    <div style='display: flex; flex-wrap: wrap; align-items: center; justify-content: center;'>
        <div style='display: flex; align-items: center; margin: 5px;'>
            <div style='width: 20px; height: 20px; background-color: #106dff;'></div>
            <span style='margin-left: 5px;'>Very high (pLDDT > 90)</span>
        </div>
        <div style='display: flex; align-items: center; margin: 5px;'>
            <div style='width: 20px; height: 20px; background-color: #10cff1;'></div>
            <span style='margin-left: 5px;'>Confident (90 > pLDDT > 70)</span>
        </div>
        <div style='display: flex; align-items: center; margin: 5px;'>
            <div style='width: 20px; height: 20px; background-color: #f6ed12;'></div>
            <span style='margin-left: 5px;'>Low (70 > pLDDT > 50)</span>
        </div>
        <div style='display: flex; align-items: center; margin: 5px;'>
            <div style='width: 20px; height: 20px; background-color: #ef821e;'></div>
            <span style='margin-left: 5px;'>Very low (pLDDT < 50)</span>
        </div>
    </div>
    """
    st.markdown(color_mapping_html, unsafe_allow_html=True)

def visualize_pae(pae_matrix, token_chain_ids):
    st.write("### Predicted Aligned Error (PAE)")
    fig = px.imshow(
        pae_matrix,
        color_continuous_scale='Greens_r',
        labels=dict(
            x="Residue index",
            y="Residue index",
            color="PAE (Å)"
        ),
        zmin=0.0,
        zmax=31.75
    )
    # Draw chain boundaries
    if token_chain_ids:
        chain_boundaries = []
        prev_chain = token_chain_ids[0]
        for idx, chain_id in enumerate(token_chain_ids):
            if chain_id != prev_chain:
                chain_boundaries.append(idx - 0.5)
                prev_chain = chain_id
        for boundary in chain_boundaries:
            fig.add_shape(
                type="line",
                x0=boundary,
                y0=0,
                x1=boundary,
                y1=len(token_chain_ids),
                line=dict(color="red", width=1)
            )
            fig.add_shape(
                type="line",
                x0=0,
                y0=boundary,
                x1=len(token_chain_ids),
                y1=boundary,
                line=dict(color="red", width=1)
            )
    st.plotly_chart(fig, use_container_width=True)

def display_summary_data(summary_data, chain_ids):
    st.write("### Summary of Confidence Metrics")

    # Map chain-level metrics to chain IDs
    chain_metrics = {}
    for key in ['chain_iptm', 'chain_ptm']:
        if key in summary_data:
            values = summary_data[key]
            if len(values) == len(chain_ids):
                chain_metrics[key] = dict(zip(chain_ids, values))
            else:
                st.warning(f"The number of values in {key} does not match the number of chains.")

    # Display chain-level metrics
    for key, metrics in chain_metrics.items():
        st.write(f"#### {key}")
        df = pd.DataFrame.from_dict(metrics, orient='index', columns=[key])
        # Format numbers to two decimal places
        df_style = df.style.format("{:.2f}").set_table_styles(
            [{'selector': 'th, td', 'props': [('border', '1px solid black')]}]
        ).set_properties(**{'text-align': 'center'})
        # Center the table and set a fixed width
        st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        st.table(df_style)
        st.markdown("</div>", unsafe_allow_html=True)

    # Display pair metrics as matrices and visualize them
    for key in ['chain_pair_iptm', 'chain_pair_pae_min']:
        pair_metrics = summary_data.get(key, {})
        if pair_metrics:
            st.write(f"#### {key}")
            if len(pair_metrics) == len(chain_ids):
                df = pd.DataFrame(pair_metrics, index=chain_ids, columns=chain_ids)
                # Format numbers to two decimal places
                df_style = df.style.format("{:.2f}").set_table_styles(
                    [{'selector': 'th, td', 'props': [('border', '1px solid black')]}]
                ).set_properties(**{'text-align': 'center'})
                # Create two columns
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
                    st.table(df_style)
                    st.markdown("</div>", unsafe_allow_html=True)
                with col2:
                    # Visualize the matrix
                    fig = px.imshow(
                        df,
                        x=chain_ids,
                        y=chain_ids,
                        color_continuous_scale='Viridis',
                        text_auto=".2f",
                        labels={'x': 'Chain', 'y': 'Chain', 'color': key}
                    )
                    fig.update_layout(autosize=True)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"The dimensions of {key} do not match the number of chains.")

    # Display other metrics
    other_metrics = {k: v for k, v in summary_data.items() if k not in ['chain_iptm', 'chain_ptm', 'chain_pair_iptm', 'chain_pair_pae_min']}
    if other_metrics:
        st.write("#### Other Metrics")
        df = pd.DataFrame(list(other_metrics.items()), columns=['Metric', 'Value'])
        # Format 'Value' column to two decimal places if numeric
        df['Value'] = df['Value'].apply(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
        df_style = df.style.set_table_styles(
            [{'selector': 'th, td', 'props': [('border', '1px solid black')]}]
        ).set_properties(**{'text-align': 'center'})
        # Center the table and set a fixed width
        st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        st.table(df_style)
        st.markdown("</div>", unsafe_allow_html=True)

# ========================================
# Main Application
# ========================================

def main():
    # Set page configuration and theme
    st.set_page_config(
        page_title="AFusion Visualization",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS styles
    st.markdown("""
        <style>
        /* Remove padding */
        .css-18e3th9 {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        /* Header styling */
        .css-10trblm {
            font-size: 2rem;
            color: #2c3e50;
        }
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f2f4f5;
        }
        /* Button styling */
        .stButton>button {
            background-color: #2c3e50;
            color: white;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Title and subtitle
    st.markdown("<h1 style='text-align: center;'>🔬 AFusion: Visualization</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 16px;'>Visualize your AlphaFold 3 predictions</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 14px;'>If this project helps you, please ⭐️ <a href='https://github.com/Hanziwww/AlphaFold3-GUI' target='_blank'>my project</a>!</p>", unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        st.sidebar.markdown("---")
        sections = {
            "Introduction": "introduction",
            "Upload Files": "upload_files",
            "Visualization": "visualization",
            "Summary Metrics": "summary_metrics",
        }
        for section_name, section_id in sections.items():
            st.markdown(f"<a href='#{section_id}' style='text-decoration: none;'>{section_name}</a>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<small>Created by Hanzi 2024.</small>", unsafe_allow_html=True)

    st.markdown('<div id="introduction"></div>', unsafe_allow_html=True)
    st.markdown("### Welcome to AFusion Visualization!")
    st.markdown("Use this app to visualize your AlphaFold 3 prediction results.")

    # File upload section
    st.markdown('<div id="upload_files"></div>', unsafe_allow_html=True)
    st.header("📂 Upload Prediction Files")
    with st.expander("Upload Files", expanded=True):
        model_cif_file = st.file_uploader("Upload model.cif file", type=["cif"])
        confidences_json_file = st.file_uploader("Upload confidences.json file", type=["json"])
        summary_confidences_file = st.file_uploader("Upload summary_confidences.json file", type=["json"])

    if model_cif_file and confidences_json_file and summary_confidences_file:
        try:
            # Read and process files
            structure, cif_content = read_cif_file_obj(model_cif_file)
            residue_bfactors, ligands = extract_residue_bfactors(structure)
            pae_matrix, token_chain_ids = extract_pae_from_json_obj(confidences_json_file)
            summary_data = extract_summary_confidences_obj(summary_confidences_file)
            logger.info("Successfully loaded and processed uploaded files.")

            # Get chain ID list
            chain_ids = list(set(token_chain_ids))
            chain_ids.sort()  # Sort for consistency

            # Display visualization results
            st.markdown('<div id="visualization"></div>', unsafe_allow_html=True)
            st.header("🌟 Visualizations")
            display_visualization_header()

            # Create two columns, ratio 3:2
            col1, col2 = st.columns([3, 2])

            with col1:
                st.write("### 3D Model Visualization")
                if residue_bfactors or ligands:
                    view_html = visualize_structure(residue_bfactors, ligands, cif_content, background_color='#000000')
                    st.components.v1.html(view_html, height=600, scrolling=False)
                else:
                    st.error("Failed to extract atom data.")
                    logger.error("Failed to extract atom data.")

            with col2:
                # Visualize PAE matrix
                visualize_pae(pae_matrix, token_chain_ids)

            # Display summary data
            st.markdown('<div id="summary_metrics"></div>', unsafe_allow_html=True)
            display_summary_data(summary_data, chain_ids)

        except Exception as e:
            st.error(f"An error occurred while processing the files: {e}")
            logger.error(f"Error processing files: {e}")
    else:
        st.info("Please upload all required files to proceed.")

    st.markdown("---")
    # Provide log file download option
    st.markdown("### Download Log File 📥")
    with open('afusion_visualization.log', 'r') as log_file:
        log_content = log_file.read()
    st.download_button(
        label="Download Log File",
        data=log_content,
        file_name='afusion_visualization.log',
        mime='text/plain'
    )

    # Display log content
    with st.expander("Show Log Content 📄", expanded=False):
        st.text_area("Log Content", value=log_content, height=200)

    st.markdown("---")
    # Add footer
    st.markdown("<p style='text-align: center; font-size: 12px; color: #95a5a6;'>© 2024 Hanzi. All rights reserved.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
