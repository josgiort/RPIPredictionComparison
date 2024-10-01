from Bio import PDB
import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt

# Specify the path to your CIF file
cif_file = "fold_number_2_model_0.cif"

# Create a CIF parser object from BioPython
parser = PDB.MMCIFParser()

# Parse the structure
structure = parser.get_structure("Structure", cif_file)

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

# TODO: Compute the distance with atom - atom2 somehow and put into the right position in the matrix

interacting_atoms = 0
for i in range(len(l['A'])):
    for j in range(len(l['B'])):
        # Take the Euclidean distance between the three coordinates of both atoms
        # Coordinates are in angstroms
        mat[i,j] = np.sqrt((l['A'][i].coord[0] - l['B'][j].coord[0])**2 + (l['A'][i].coord[1] - l['B'][j].coord[1])**2 + (l['A'][i].coord[2] - l['B'][j].coord[2])**2)
        # Calculate if this obtained distance is less than 5.0 angstroms, which is the believed distance for interaction
        if mat[i,j] <=  5.0:
            interacting_atoms += 1

# Calculate contact frequency
contact_frequency = interacting_atoms / (len(l['A']) * len(l['B'])) * 100
print("Contact frequency: " + str(contact_frequency))
# If contact frequency is above 10%, the RNA-protein pair is considered interacting
if contact_frequency >= 10.0 :
    print("POSITIVE INTERACTION")
else :
    print("NEGATIVE INTERACTION")

"""
mtres = np.zeros((3, 3))
ext1 = [[4,5,6], [7,8,9]]

for i in range(len(ext1[0])):
    for j in range(len(ext1[1])):
        mtres[i,j] = ext1[0][i] * ext1[1][j]

print(mtres)
"""

# Plot the distance matrix
plt.figure(figsize=(10,5))
plt.matshow(mat, fignum=1, aspect='auto')
plt.colorbar()
plt.show()
