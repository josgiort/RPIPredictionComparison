import sys
from matplotlib import pyplot as plt
from Bio.PDB import MMCIFParser
import numpy as np

# This script takes as input a CIF file of a 3D structure and creates a distance matrix between every
# nucleotide and residue, then it plots this matrix as a colored visual representation
# highlighting the distances less than five angstroms in green, and finally it prints all the nucleotides
# that have a distance less than five angstroms with at least one residue in a txt file

# Specify the CIF file of a RNA-protein complex 3d structure as input
cif_file = sys.argv[1]

# Specify the output file in which the interacting nucleotides will be printed (.txt file)
closest_nts_file = sys.argv[2]

# Load the CIF file
parser = MMCIFParser()
structure = parser.get_structure("rna_protein_complex", cif_file)

# Separate residues and nucleotides
protein_chain = structure[0]["A"]  # Assuming protein is chain A
rna_chain = structure[0]["B"]  # Assuming RNA is chain B

# Collect atoms by residue (protein) and nucleotide (RNA)
protein_residues = list(protein_chain.get_residues())
rna_nucleotides = list(rna_chain.get_residues())

# Initialize distance matrix
distance_matrix = np.zeros((len(protein_residues), len(rna_nucleotides)))

# Get distances between every residue with every nucleotide. Each distance calculated
# only with the closest atom from the residue or nucleotide to its counterpart
for i, residue in enumerate(protein_residues):
    residue_atoms = list(residue.get_atoms())
    for j, nucleotide in enumerate(rna_nucleotides):
        nucleotide_atoms = list(nucleotide.get_atoms())
        # Initialize minimal distance for a given pair of atoms from a residue - nucleotide pair
        min_distance = float("inf")
        # Compute distances of all possible atom pairs from a given residue - nucleotide pair
        # Note: One atom belonging to the residue and the other atom to the nucleotide
        # Find and store minimum distance
        for atom_res in residue_atoms:
            for atom_nuc in nucleotide_atoms:
                distance = atom_res - atom_nuc  # BioPython way to calculate Euclidean distance
                if distance < min_distance:
                    min_distance = distance

        # Save the final minimum distance in matrix
        # This represents the pair of atoms which are the closest for a given pair of
        # residue i and nucleotide j
        distance_matrix[i, j] = min_distance


# Print all nucleotides that have a distance of 5 angstroms with at least one protein residue
closest_nucleotides = ""
# Iterate with respect to nucleotides (columns)
for j in range(distance_matrix.shape[1]):
    # Search through protein residues
   for i in range(distance_matrix.shape[0]):
       # Five angstroms is the threshold for being close enough (interaction threshold)
       if distance_matrix[i, j] <= 5.0:
           current_rsd = protein_residues[i]
           current_nct = rna_nucleotides[j]
           closest_nucleotides += str({"index": j + 1, "nucleotide": current_nct, "residue":current_rsd}) + '\n'
           break
f = open(closest_nts_file, "w")
f.write(closest_nucleotides)
f.close()

# Creation of colored distance_matrix plot
fig, ax = plt.subplots()
cax = ax.matshow(distance_matrix, aspect='auto', cmap='Spectral')
plt.colorbar(cax)
plt.title("Interacting nucleotides of " + cif_file)
# Highlight the nucleotides with a distance less than five angstroms in green
for i in range(distance_matrix.shape[0]):
    for j in range(distance_matrix.shape[1]):
        value = distance_matrix[i, j]
        if value <= 5.0:
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor='#57e140', lw=3))
plt.savefig(cif_file, dpi=600, bbox_inches='tight')
plt.show()

"""
Old way to create the matrix and calculate the distances
Basically the same but this approach was atom-wise without 
considering the grouping of atoms by residues or nucleotides
l = defaultdict(list)
# Loop through all the models, chains, residues, and atoms
for model in structure:
    #print(f"Model {model.id}")
    for chain in model:
        results = []
        #print(f"  Chain {chain.id}")
        for residue in chain:
            #print(f"    Residue {residue.resname} {residue.id[1]}")
            for atom in residue:
                #print(f"      Atom {atom.name}: {atom.coord}")
                l[chain.id].append(atom)

mat = np.zeros((len(l['A']), len(l['B'])))

# do: Compute the distance with atom - atom2 somehow and put into the right position in the matrix

interacting_atoms = 0
for i in range(len(l['A'])):
    for j in range(len(l['B'])):
        # Take the Euclidean distance between the three coordinates of both atoms
        # Coordinates are in angstroms
        mat[i,j] = np.sqrt((l['A'][i].coord[0] - l['B'][j].coord[0])**2 + (l['A'][i].coord[1] - l['B'][j].coord[1])**2 + (l['A'][i].coord[2] - l['B'][j].coord[2])**2)
        # Calculate if this obtained distance is less than 5.0 angstroms, which is the believed distance for interaction
        if mat[i,j] <=  5.0:
            interacting_atoms += 1

"""



"""
# Calculate contact frequency
contact_frequency = interacting_atoms / (len(l['A']) * len(l['B'])) * 100
print("Contact frequency: " + str(contact_frequency))
# If contact frequency is above 10%, the RNA-protein pair is considered interacting
if contact_frequency >= 10.0 :
    print("POSITIVE INTERACTION")
else :
    print("NEGATIVE INTERACTION")
"""
