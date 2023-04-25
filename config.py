help_msg = """
    ### Help Menu for Peptide Site Locator Streamlit App

    Welcome to the Peptide Site Locator app! This app is designed to help you analyze your .fasta and DTASelect-filter.txt 
    files and provide a convenient way to display and download the processed data. To get started, follow the instructions below:

    1) Upload your .fasta file using the "Choose a .fasta file" button.

    2) Upload your DTASelect-filter.txt file using the "Choose a DTASelect-filter.txt file" button.

    3) Once both files are uploaded, click the "Run" button to process the data.

    4) The resulting table will be displayed on the screen, and you can download the results as a .csv 
    file by clicking the "Download" button.


    ### Column Definitions

    The output table contains the following columns:

    - Sequence: The raw sequence of the peptide, including modifications.

    - ProteinGroup: The protein group to which the peptide belongs.

    - CleanSequence: The sequence of the peptide without the first N and C term amino acids

    - ModMap: A dictionary containing the positions of modifications in the peptide sequence

    - UnmodSequence: The peptide sequence without any modifications.

    - ProteinLocus: The protein locus that corresponds to the given protein group.

    - ProteinIndex: The index position of the peptide sequence within the protein sequence. 
    A value of -1 indicates the sequence was not found.

    - ProteinIndexModMap: A dictionary containing the positions of modifications in the protein sequence. 
    An empty dictionary is returned if the protein sequence was not found.

    """