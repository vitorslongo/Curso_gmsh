import gmsh
import numpy as np
gmsh.initialize()
occ = gmsh.model.occ
mesh = gmsh.model.mesh

"""
o meu arquivo tem:
    14 nós
    12 linhas
    24 triângulos
    24 tetraedros
    8 pontos
"""

gmsh.option.setNumber("General.Verbosity", 0)

occ.addRectangle(0, 0, 0, 1, 1)
occ.synchronize()

gmsh.option.setNumber("Mesh.MeshSizeFactor", 10)
mesh.generate(3)

node_indexes, coords, _ = mesh.getNodes(2, -1, True)

n_nodes = len(node_indexes)
n_indexes = np.arange(n_nodes, dtype=int)
section_nodal_coordinates = np.zeros((n_nodes, 4))
section_nodal_coordinates[n_indexes, 1:] = coords.reshape(-1, 3)
section_nodal_coordinates[n_indexes, :1] = node_indexes.reshape(-1, 1) - 1


element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(2, -1)
for i in range(len(element_nodes)):
    element_name, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_types[i])

    n_elements = len(element_indexes)
    e_indexes = np.arange(n_elements, dtype=int)
    cols = nodes_per_element

    section_connectivity = np.zeros((n_elements, cols+1))
    section_connectivity[:, 0] = e_indexes
    section_connectivity[:, 1:] = element_nodes.reshape(-1, cols) - 1

    section_connectivities = dict()
    section_connectivities[element_name] = section_connectivity



# print("node_tags:", node_tags)

# print("coords", coords)





gmsh.fltk.run()
gmsh.finalize()