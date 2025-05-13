"""
Aqui nós vamos pegar as informações que o Gmsh nos sobre a malha dá de uma maneira meio ruim e vamos organizar os dados de forma com a qual possamos
trabalhar com eles e implementar nos nossos solvers.

A matriz representa quais nós formam cada elemento. Ela é usada para:
    - construir malhas em outros programas (ex: ParaView, solver próprio)
    - entender a topologia da malha
    - aplicar condições de contorno com base em elementos
"""
import gmsh
import numpy as np
from pprint import pprint
gmsh.initialize()
occ = gmsh.model.occ
mesh = gmsh.model.mesh
gmsh.option.setNumber("General.Verbosity", 0)

# Vamos só criar um quadrado e malhar ele normalmente.
occ.addRectangle(0, 0, 0, 1, 1)
occ.synchronize()

gmsh.option.setNumber("Mesh.MeshSizeFactor", 10)
mesh.generate(3)

# Aqui pegamos as informações de coordenadas nodais, de maneira crua. O Gmsh entrega ela em uma lista gigante, tudo concatenado.
node_indexes, coords, _ = mesh.getNodes(2, -1, True)

# O que fazemos aqui é basicamente dar o nosso próprio nome para os nós, basicamente um apelido, e organizamos uma matriz de forma que:
# Sendo "n" o número de nós da malha, criamos uma matriz n x 4, onde a primeira coluna é o apelido do nó e as outras 3 são as coordenadas dele.

n_nodes = len(node_indexes) # o numero de nós é a quantidade de indexes de nós
n_indexes = np.arange(n_nodes, dtype=int) # crio a lista com os indexes pra facilitar a atribuição depois
section_nodal_coordinates = np.zeros((n_nodes, 4)) # inicializo a matriz de coordenadas nodais
section_nodal_coordinates[n_indexes, 1:] = coords.reshape(-1, 3) # atribuo as coordenadas do "coords" pra cada nó
section_nodal_coordinates[n_indexes, :1] = node_indexes.reshape(-1, 1) - 1 # depois eu coloco os indexes (apelidos) na matriz 

# A outra matriz que precisamos é a de conectividade nodal, onde nela podemos tirar todas as informações de quais nós estão conectados a quais.
# Ela é feita da seguinte forma: Considerando que nossa malha tenha apenas triangulos (já que é uma malha 2D), cada elemento vai ter m = 3 nós.
# Então, pego as infomações de tipo de elementos que temos na nossa malha, os indexes de cada um deles e os nós que fazem parte de cada elemento
element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(2, -1)

section_connectivities = dict()
# Para cada elemento:
print(element_nodes)
for i in range(len(element_nodes)):
    element_name, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_types[i])
    
    n_elements = len(element_indexes[i])
    e_indexes = np.arange(n_elements, dtype=int)

    section_connectivity = np.zeros((n_elements, nodes_per_element + 1))
    section_connectivity[:, 0] = e_indexes # coloco os apelidos dos elementos
    section_connectivity[:, 1:] = element_nodes[i].reshape(-1, nodes_per_element) - 1 # coloco os nós que estão conectados a cada elemento,
    # e faço essa lista ter começo no 0, e não no 1, como é originalmente no gmsh

    section_connectivities[element_name] = section_connectivity # no nosso caso temos apenas um tipo de elementos na malha, que são triangulos, mas essa parte aqui faz o mapeamento para 
    # malhas que podem ter vários tipos de elementos (triangulos, quadrados, etc.)


# pprint(section_nodal_coordinates)
# pprint(section_connectivities)

# print("node_tags:", node_tags)

# print("coords", coords)





gmsh.fltk.run()
gmsh.finalize()