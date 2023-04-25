from io import StringIO
import streamlit as st
from filterframes import from_dta_select_filter

import config
from util import read_fasta_file, parse_modified_peptide, strip_modifications

st.title("Peptide Site Locator")

with st.expander('Help'):
    st.markdown(config.help_msg)

uploaded_fasta_file = st.file_uploader("Choose a .fasta file", type="fasta")
uploaded_filter_file = st.file_uploader("Choose a DTASelect-filter.txt file", type="txt")

if uploaded_fasta_file and uploaded_filter_file:

    if not st.button('Run'):
        st.stop()

    records_dict = read_fasta_file(StringIO(uploaded_fasta_file.getvalue().decode('utf-8')))
    locus_to_sequence = {record.name: record.seq for record in records_dict.values()}

    header_lines, peptide_df, protein_df, end_lines = from_dta_select_filter(
        StringIO(uploaded_filter_file.getvalue().decode('utf-8')))

    protein_group_to_locus_protein_identifier = {}
    for protein_group, locus in protein_df[['ProteinGroup', 'Locus']].values:
        if protein_group in protein_group_to_locus_protein_identifier:
            continue
        protein_group_to_locus_protein_identifier[protein_group] = locus

    peptide_df['CleanSequence'] = [seq[2:-2] for seq in peptide_df['Sequence']]
    peptide_df['ModMap'] = [parse_modified_peptide(seq) for seq in peptide_df['CleanSequence']]
    peptide_df['UnmodSequence'] = [strip_modifications(seq) for seq in peptide_df['CleanSequence']]
    peptide_df['ProteinLocus'] = [protein_group_to_locus_protein_identifier.get(grp) for grp in peptide_df['ProteinGroup']]

    indexes = []
    for locus, peptide in zip(peptide_df['ProteinLocus'], peptide_df['UnmodSequence']):
        protein_sequence = str(locus_to_sequence.get(locus))
        if protein_sequence is not None:
            indexes.append(protein_sequence.find(peptide))
        else:
            indexes.append(-1)

    peptide_df['ProteinIndex'] = indexes

    peptide_index_mod_dict = []
    for mod_map, protein_index in zip(peptide_df['ModMap'], peptide_df['ProteinIndex']):
        if protein_index == -1:
            peptide_index_mod_dict.append({})
            continue
        new_mod_dict = {i + protein_index: mod_map[i] for i in mod_map}
        peptide_index_mod_dict.append(new_mod_dict)

    peptide_df['ProteinIndexModMap'] = peptide_index_mod_dict

    st.subheader('DataFrame:')
    st.dataframe(peptide_df)

    st.download_button(label="Download",
                       data=peptide_df.to_csv(sep='\t', header=False, index=False),
                       file_name="peptides.csv",
                       mime="text/plain")
