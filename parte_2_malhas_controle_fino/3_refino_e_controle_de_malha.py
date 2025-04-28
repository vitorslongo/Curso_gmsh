"""
Nesse exemplo aqui aprendemos mais sobre um controle mais fino sobre as nossas malhas, inclusive refino local da malha.
Geramos uma geometria base e trabalhamos nela, e também podemos ver as diferenças entre os vários algoritmos de geração de malha.
"""
import gmsh
gmsh.initialize()
occ = gmsh.model.occ
mesh = gmsh.model.mesh
gmsh.option.setNumber("General.Verbosity", 0)
origin = [0]*3

"""
Existem vários tipos de controle de tamanho de malha:
- Por elemento geométrico (0, 1, 2?, 3?) (só pelo kernel integrado do Gmsh)
- Controle geral:
    - Size Factor
    - Range de Size Factor
    - Comprimento característico (o que é?)
- Refino de malha
    - Vários tipos de size fields: Por entidade (1?, 2, 3), Box, MathEval, Atractor etc (ver documentação do Gmsh)
- Malhas estruturadas --> linhas, superfícies e volumes transfinite
- Também temos vários diferentes algoritmos de malha. Para setar cada um usamos o comando, seguindo esta relação de nomenclatura:
"""
# 2D Mesh Algorithms
MESH_ADAPT_2D = 1
AUTOMATIC_2D = 2
INITIAL_MESH_ONLY_2D = 3
DELAUNAY_2D = 5
FRONTAL_DELAUNAY_2D = 6
BAMG_2D = 7
FRONTAL_DELAUNAY_FOR_QUADS_2D = 8
PACKING_OF_PARALLELOGRAMS_2D = 9
QUASI_STRUCTURED_QUADS_2D = 11



# 3D Mesh Algorithms
DELAUNAY_3D = 1
INITIAL_MESH_ONLY_3D = 3
FRONTAL_3D = 4
MMG_3D = 7
RTREE_3D = 9
HXT_3D = 10

# Recombination Algorithms
SIMPLE_RECOMBINATION = 0
BLOSSOM_RECOMBINATION = 1
SIMPLE_FULL_QUAD_RECOMBINATION = 2
BLOSSOM_FULL_QUAD_RECOMBINATION = 3

# Subdivision Algorithms
NO_SUBDIVISION = 0
ALL_QUADRANGLES_SUBDIVISION = 1
ALL_HEXAHEDRA_SUBDIVISION = 2
BARYCENTRIC_SUBDIVISION = 3

# Controle de tamanho geral: Esse aqui só escala pelo fator que colocarmos o tamanho da malha que teria se nao disséssemos nada
# gmsh.option.setNumber("Mesh.MeshSizeFactor", 10)
# gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 10)

# Para um controle mais preciso para malhas que contem refinamento local, fazemos dessa forma:
global_size = .05
refine_size = .01
surfaces_list = [5, 12]
fields_list = []

# Criação de uma geometria qualquer
main_cylinder = occ.add_cylinder(*origin, 0, 0, 1, 1)
small_cylinder = occ.add_cylinder(.5, 0, 1, 0, 0, 1, .2)
small_box = occ.addBox(-.5, 0, 1, .2, .2, 1 )
occ.synchronize()

# Refino de malha:
# Ele é feito usando "size fields", que são campos onde dentro deles nós podemos definir algumas características, uma delas é o tamanho da malha.
# Tem vários tipos de campo, nesse caso nós usamos o "Constant" pois nao queremos nada tão avançado, mas caso queira, olhe na documentação do Gmsh
# os vários outros tipos de campos pois neles podem ser definidas características da malha de uma maneira muito mais específica.

# O controle de malha que nós queremos é dentro e fora, então primeiro nós definimos um campo vazio (com nenhuma superfície), e FORA dele nós dizemos qual
# o tamanho da malha que queremos. Se pararmos por aí seria a mesma coisa que só controlar o tamanho da malha normalmente por outros métodos.
outer_field = mesh.field.add("Constant")
mesh.field.setNumbers(outer_field, "SurfacesList", [])
mesh.field.setNumber(outer_field, "VOut", global_size)
fields_list.append(outer_field)

# Mas o cerne da coisa vem aí, nós agora definimos um campo e passamos a lista de pontos, curvas, superfícies ou volumes nesse função a seguir que conseguimos
# definir o "VIn", eu seja o Value Inside, da malha desse size field.
refine_field = mesh.field.add("Constant")
mesh.field.setNumbers(refine_field, "SurfacesList", surfaces_list) # Atenção para setNumber e setNumberS 
mesh.field.setNumber(refine_field, "VIn", refine_size)
fields_list.append(refine_field)

# Depois aqui precimaos definir um outro campo "Min" para incluir os campos que definimos o VOut e o VIn
# (inclsive pode-se ter mais de um campo onde refinamos a malha com valores diferentes). Após isso nós definimos esse campo Min como backgorund mesh e 
# continuamos com qualuqer outra configuração normalmente.
minimum_field = gmsh.model.mesh.field.add("Min")
mesh.field.setNumbers(minimum_field, "FieldsList", fields_list)
mesh.field.setAsBackgroundMesh(minimum_field)

mesh.field.setAsBackgroundMesh(minimum_field)


mesh.generate(2)
# gmsh.write("cilindro_teste.stl")
gmsh.fltk.run()
gmsh.finalize()