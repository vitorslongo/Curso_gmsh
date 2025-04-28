"""
Aqui nós vamos pegar as informações que o Gmsh nos sobre a malha dá de uma maneira meio ruim e vamos organizar os dados de forma com a qual possamos
trabalhar com eles e implementar nos nossos solvers.
"""
import gmsh
import numpy as np
gmsh.initialize()
occ = gmsh.model.occ
mesh = gmsh.model.mesh
gmsh.option.setNumber("General.Verbosity", 0)

# Vamos só criar um retângulo e malhar ele normalmente.
occ.addRectangle(0, 0, 0, 1, 1)
occ.synchronize()

gmsh.option.setNumber("Mesh.MeshSizeFactor", 10)
mesh.generate(3)

# Aqui pegamos as informações de coordenadas nodais, de maneira crua. O Gmsh entrega ela em uma lista gigante, tudo concatenado.
node_indexes, coords, _ = mesh.getNodes(2, -1, True)

# O que fazemos aqui é basicamente darmos o nosso próprio nome para os nós, basicamente um apelido, e organizamos uma matriz de forma que:
# Sendo "n" o número de nós da malha, criamos uma matriz n x 4, onde a primeira coluna é o apelido do nó e as outras 3 são as coordenadas dele.
n_nodes = len(node_indexes)
n_indexes = np.arange(n_nodes, dtype=int)
section_nodal_coordinates = np.zeros((n_nodes, 4))
section_nodal_coordinates[n_indexes, 1:] = coords.reshape(-1, 3)
section_nodal_coordinates[n_indexes, :1] = node_indexes.reshape(-1, 1) - 1

# A outra matriz que precisamos é a de conectividade nodal, onde nela podemos tirar todas as informações de quais nós estão conectados a quais.
# Ela é feita da seguinte forma: Considerando que nossa malha tenha apenas triangulos (já que é uma malha 2D), cada elemento vai ter m = 3 nós.
# Então, 
element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(2, -1)

section_connectivities = dict()

for i in range(len(element_nodes)):
    element_name, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_types[i])
    
    element_indexes_i = element_indexes[i]
    element_nodes_i = element_nodes[i]

    n_elements = len(element_indexes_i)
    e_indexes = np.arange(n_elements, dtype=int)
    cols = nodes_per_element

    section_connectivity = np.zeros((n_elements, cols + 1))
    section_connectivity[:, 0] = e_indexes
    section_connectivity[:, 1:] = element_nodes_i.reshape(-1, cols) - 1

    section_connectivities[element_name] = section_connectivity




# print("node_tags:", node_tags)

# print("coords", coords)





# gmsh.fltk.run()
gmsh.finalize()