import gmsh
import numpy as np
gmsh.initialize()


occ = gmsh.model.occ
mesh = gmsh.model.mesh
option = gmsh.option.setNumber

option("General.Verbosity", 0)

occ.addRectangle(0,0,0, 1, 1, 1)
occ.synchronize()

option("Mesh.MeshSizeFactor", 10)
mesh.generate(2)

node_indexes, coords, _ = mesh.getNodes(2, -1, True)




n_nodes = len(node_indexes)
n_indexes = np.arange(n_nodes, dtype=int)
section_nodal_coordinates = np.zeros((n_nodes, 4))
section_nodal_coordinates[n_indexes, 1:] = coords.reshape(-1, 3)
section_nodal_coordinates[n_indexes, :1] = node_indexes.reshape(-1, 1) - 1

# print(section_nodal_coordinates)

element_types, element_indexes, element_nodes = mesh.getElements(2, -1)

section_conectivities = dict()
for i in range(len(element_nodes)):
    element_name, _, _, nodes_per_element, _, _ = mesh.getElementProperties(element_types[i])

    n_elements = len(element_indexes[i])
    e_indexes = np.arange(n_elements, dtype=int)

    section_conectivity = np.zeros((n_elements, nodes_per_element + 1))
    section_conectivity[:, 0] = e_indexes
    section_conectivity[:, 1:] = element_nodes[i].reshape(-1, nodes_per_element) - 1

    section_conectivities[element_name] = section_conectivity

print(section_conectivities)






option("Mesh.NodeLabels", 1)
gmsh.fltk.run()
gmsh.finalize()