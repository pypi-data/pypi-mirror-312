import streamlit as st
from loguru import logger

def handle_bond(b):
    bond_col1, bond_col2 = st.columns(2)
    with bond_col1:
        st.markdown("**First Atom**")
        entity_id1 = st.text_input(f"Entity ID 1", key=f"bond_entity1_{b}")
        residue_id1 = st.number_input(f"Residue ID 1", min_value=1, step=1, key=f"bond_residue1_{b}")
        atom_name1 = st.text_input(f"Atom Name 1", key=f"bond_atom1_{b}")
    with bond_col2:
        st.markdown("**Second Atom**")
        entity_id2 = st.text_input(f"Entity ID 2", key=f"bond_entity2_{b}")
        residue_id2 = st.number_input(f"Residue ID 2", min_value=1, step=1, key=f"bond_residue2_{b}")
        atom_name2 = st.text_input(f"Atom Name 2", key=f"bond_atom2_{b}")

    if not (entity_id1 and atom_name1 and entity_id2 and atom_name2):
        st.error("All fields are required for defining a bond.")
        logger.error(f"Fields missing for bond {b+1}.")
        return None

    bond = [
        [entity_id1, residue_id1, atom_name1],
        [entity_id2, residue_id2, atom_name2]
    ]
    logger.debug(f"Bond {b+1} defined as: {bond}")
    return bond
