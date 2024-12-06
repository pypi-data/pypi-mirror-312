import streamlit as st
import re
from loguru import logger

def collect_protein_sequence_data(i):
    sequence = st.text_area(f"Protein Sequence (Entity {i+1})", key=f"sequence_{i}", help="Enter the protein sequence.")
    logger.debug(f"Protein sequence input for Entity {i+1}.")

    # Modifications
    modifications_list = []
    add_modifications = st.checkbox(f"Add Modifications", key=f"add_modifications_{i}")
    if add_modifications:
        num_modifications = st.number_input(f"Number of Modifications", min_value=1, step=1, key=f"num_modifications_{i}")
        for j in range(int(num_modifications)):
            st.markdown(f"**Modification {j+1}**")
            mod_col1, mod_col2 = st.columns(2)
            with mod_col1:
                mod_type = st.text_input(f"Modification Type (ptmType)", key=f"mod_type_{i}_{j}")
            with mod_col2:
                mod_position = st.number_input(f"Modification Position (ptmPosition)", min_value=1, step=1, key=f"mod_position_{i}_{j}")
            modifications_list.append({"ptmType": mod_type, "ptmPosition": mod_position})
            logger.debug(f"Added modification: {modifications_list[-1]}")

    # MSA Options
    msa_option = st.selectbox(f"MSA Option", ["Auto-generate 🛠️", "Don't use MSA 🚫", "Upload MSA 📄"], key=f"msa_option_{i}")

    unpaired_msa = ""
    paired_msa = ""
    if msa_option == "Upload MSA 📄":
        unpaired_msa = st.text_area(f"Unpaired MSA", key=f"unpaired_msa_{i}")
        paired_msa = st.text_area(f"Paired MSA", key=f"paired_msa_{i}")
        logger.debug(f"Entity {i+1} uploaded MSA.")
    elif msa_option == "Don't use MSA 🚫":
        unpaired_msa = ""
        paired_msa = ""
        logger.debug(f"Entity {i+1} chose not to use MSA.")
    elif msa_option == "Auto-generate 🛠️":
        unpaired_msa = None
        paired_msa = None
        logger.debug(f"Entity {i+1} chose to auto-generate MSA.")

    # Templates
    templates_list = []
    add_templates = st.checkbox(f"Add Templates", key=f"add_templates_{i}")
    if add_templates:
        num_templates = st.number_input(f"Number of Templates", min_value=1, step=1, key=f"num_templates_{i}")
        for k in range(int(num_templates)):
            st.markdown(f"**Template {k+1}**")
            mmcif_content = st.text_area(f"mmCIF Content", key=f"mmcif_{i}_{k}")
            query_indices = st.text_input(f"Query Indices List (comma-separated)", key=f"query_indices_{i}_{k}")
            template_indices = st.text_input(f"Template Indices List (comma-separated)", key=f"template_indices_{i}_{k}")
            try:
                query_indices_list = [int(idx.strip()) for idx in query_indices.split(",") if idx.strip()]
                template_indices_list = [int(idx.strip()) for idx in template_indices.split(",") if idx.strip()]
            except ValueError:
                st.error("Indices lists should be integers separated by commas.")
                logger.error("Error parsing indices lists.")
                query_indices_list = []
                template_indices_list = []
            templates_list.append({
                "mmcif": mmcif_content,
                "queryIndices": query_indices_list,
                "templateIndices": template_indices_list
            })
            logger.debug(f"Added template: {templates_list[-1]}")

    protein_entry = {
        "sequence": sequence
    }
    if modifications_list:
        protein_entry["modifications"] = modifications_list
    if unpaired_msa is not None:
        protein_entry["unpairedMsa"] = unpaired_msa
    if paired_msa is not None:
        protein_entry["pairedMsa"] = paired_msa
    if templates_list or (unpaired_msa is not None) or (paired_msa is not None):
        if "unpairedMsa" not in protein_entry:
            protein_entry["unpairedMsa"] = ""
        if "pairedMsa" not in protein_entry:
            protein_entry["pairedMsa"] = ""
        if templates_list:
            protein_entry["templates"] = templates_list
        else:
            protein_entry["templates"] = []
    elif msa_option == "Don't use MSA 🚫":
        protein_entry["unpairedMsa"] = ""
        protein_entry["pairedMsa"] = ""
        protein_entry["templates"] = []
    return protein_entry

def collect_rna_sequence_data(i):
    sequence = st.text_area(f"RNA Sequence (Entity {i+1})", key=f"sequence_{i}", help="Enter the RNA sequence.")
    logger.debug(f"RNA sequence input for Entity {i+1}.")

    # Modifications
    modifications_list = []
    add_modifications = st.checkbox(f"Add Modifications", key=f"add_modifications_{i}")
    if add_modifications:
        num_modifications = st.number_input(f"Number of Modifications", min_value=1, step=1, key=f"num_modifications_{i}")
        for j in range(int(num_modifications)):
            st.markdown(f"**Modification {j+1}**")
            mod_col1, mod_col2 = st.columns(2)
            with mod_col1:
                mod_type = st.text_input(f"Modification Type (modificationType)", key=f"mod_type_{i}_{j}")
            with mod_col2:
                mod_position = st.number_input(f"Modification Position (basePosition)", min_value=1, step=1, key=f"mod_position_{i}_{j}")
            modifications_list.append({"modificationType": mod_type, "basePosition": mod_position})
            logger.debug(f"Added modification: {modifications_list[-1]}")

    # MSA Options
    msa_option = st.selectbox(f"MSA Option", ["Auto-generate 🛠️", "Don't use MSA 🚫", "Upload MSA 📄"], key=f"msa_option_{i}")

    unpaired_msa = ""
    if msa_option == "Upload MSA 📄":
        unpaired_msa = st.text_area(f"Unpaired MSA", key=f"unpaired_msa_{i}")
        logger.debug(f"Entity {i+1} uploaded MSA.")
    elif msa_option == "Don't use MSA 🚫":
        unpaired_msa = ""
        logger.debug(f"Entity {i+1} chose not to use MSA.")
    elif msa_option == "Auto-generate 🛠️":
        unpaired_msa = None
        logger.debug(f"Entity {i+1} chose to auto-generate MSA.")

    rna_entry = {
        "sequence": sequence
    }
    if modifications_list:
        rna_entry["modifications"] = modifications_list
    if unpaired_msa is not None:
        rna_entry["unpairedMsa"] = unpaired_msa
    return rna_entry

def collect_dna_sequence_data(i):
    sequence = st.text_area(f"DNA Sequence (Entity {i+1})", key=f"sequence_{i}", help="Enter the DNA sequence.")
    logger.debug(f"DNA sequence input for Entity {i+1}.")

    # Modifications
    modifications_list = []
    add_modifications = st.checkbox(f"Add Modifications", key=f"add_modifications_{i}")
    if add_modifications:
        num_modifications = st.number_input(f"Number of Modifications", min_value=1, step=1, key=f"num_modifications_{i}")
        for j in range(int(num_modifications)):
            st.markdown(f"**Modification {j+1}**")
            mod_col1, mod_col2 = st.columns(2)
            with mod_col1:
                mod_type = st.text_input(f"Modification Type (modificationType)", key=f"mod_type_{i}_{j}")
            with mod_col2:
                mod_position = st.number_input(f"Modification Position (basePosition)", min_value=1, step=1, key=f"mod_position_{i}_{j}")
            modifications_list.append({"modificationType": mod_type, "basePosition": mod_position})
            logger.debug(f"Added modification: {modifications_list[-1]}")

    dna_entry = {
        "sequence": sequence
    }
    if modifications_list:
        dna_entry["modifications"] = modifications_list

    return dna_entry

def collect_ligand_sequence_data(i):
    ccd_codes = st.text_input(f"CCD Codes (comma-separated)", key=f"ccd_codes_{i}", help="Provide CCD Codes, separated by commas. Ions can be specified as ligands with ccdCodes (e.g., MG).")
    smiles = st.text_input(f"SMILES String", key=f"smiles_{i}", help="Provide SMILES string of the ligand.")
    if ccd_codes and smiles:
        st.error("Please provide only one of CCD Codes or SMILES String.")
        logger.error("Ligand provided both CCD Codes and SMILES String.")
        return {}
    elif ccd_codes:
        ccd_codes_list = re.split(r"\s*,\s*", ccd_codes)
        ligand_entry = {
            "ccdCodes": ccd_codes_list
        }
        logger.debug(f"Ligand CCD Codes: {ccd_codes_list}")
        return ligand_entry
    elif smiles:
        ligand_entry = {
            "smiles": smiles
        }
        logger.debug(f"Ligand SMILES: {smiles}")
        return ligand_entry
    else:
        st.error("Ligand requires either CCD Codes or SMILES String.")
        logger.error("Ligand missing CCD Codes or SMILES String.")
        return {}
