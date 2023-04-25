import re

from Bio import SeqIO


def read_fasta_file(fasta_file_path):
    records = []
    for record in SeqIO.parse(fasta_file_path, "fasta"):
        records.append(record)
    records_dict = {i: record for i, record in enumerate(records)}
    return records_dict


def check_parentheses(text):
    stack = []

    for i, char in enumerate(text):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if not stack:
                return False
            else:
                stack.pop()

    return len(stack) == 0


def strip_modifications(peptide_sequence: str) -> str:
    """
    Removes any non-amino-acid characters from the given peptide sequence.

    Args:
        peptide_sequence: The peptide sequence to be stripped of modifications.

    Returns:
        The peptide sequence with all non-amino-acid characters removed.
    """
    if check_parentheses(peptide_sequence) is False:
        raise ValueError(f'Incorrect modification notation in peptide sequence : {peptide_sequence}!')

    unmodified_sequence = re.sub(r'\([^)]*\)', '', peptide_sequence)
    return unmodified_sequence


def parse_modified_peptide(peptide_sequence: str) -> dict[int, str]:
    """
    This function reads a peptide sequence with modifications and returns a dictionary
    with the modification values indexed by the position of the modified amino acid.

    :param peptide_sequence: The peptide sequence to read, with modifications indicated
                             by opening parenthesis followed by the modification value,
                             followed by a closing parenthesis, before the modified amino acid.
    :type peptide_sequence: str
    :return: A dictionary with the modification values indexed by the position of the modified
             amino acid.
    :rtype: dict[int, int]
    :raises ValueError: If the peptide sequence contains incorrect modification notation.
    """
    if check_parentheses(peptide_sequence) is False:
        raise ValueError(f'Incorrect modification notation in peptide sequence : {peptide_sequence}!')

    matches = re.finditer(r'\(([^)]*)\)', peptide_sequence)

    modifications = {}
    mod_offset = 0

    # Loop through the substrings
    for match in matches:
        modifications[match.start() - mod_offset - 1] = match.group()[1:-1]
        mod_offset += match.end() - match.start()
    return modifications
