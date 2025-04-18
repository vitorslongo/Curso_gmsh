"""
Nesse exempo aqui nós vamos fazer uma malha estruturada de uma viga I, primeiro criamos a geometria da viga por meio da definição de sua
seção transversal e extrudamos ela na direção z.
"""

import gmsh

gmsh.initialize()
occ = gmsh.model.occ
mesh = gmsh.model.mesh

w1 = .15
w2 = .2
h = .2
t1 = .03
t2 = .03
tw = .03
l = 1

# Vamos lá, primeiro eu defini os parâmetros da viga ali em cima para podermos fazer as mudanças que quisermos na viga depois de fazer o código 
# sem ter que ficar substituindo um milhão de vezes.

"""
Aqui para gerar essa malha estruturada nós vamos usar o recurso Transfinite, e para ele funcionar certo, é muito importante que:
1. Caso estejamos malhando um superfície 2D apenas, que ela seja subdividida em superfícies com 4 lados cada (não falo só em retângulos porque 
   essa malha pode ser feita em curvas não retas, mas isso vai ficar mais claro mais pra frente), o que deve ser fácil já que normalmente usamos
   malhas estruturadas em casos de geometrias quadradas ou mais simples
2. A mesma lógica segue para malhas 3D, devemos ter nosso volume subdividido em paralelepípedos com 6 lados
3. É crucial também que nao geremos linhas uma em cima da outra caso queiramos controlar o numero de nós em cada linha, pois isso bagunça tudo
4. Muito importante também que a gente seja bem organizado em relação às tags das linhas, senão nos perdemos (falo por experiência própria).
"""

# Aqui fazemos uma definição das coordenadas dos pontos de controle para gerarmos alguns retangulos constituintes da nossa seção transversal que queremos
rectangles_points_and_deltas = [
    [[-w2/2, -h/2, 0], [(w2-tw)/2, t2]],
    [[tw/2, -h/2, 0], [(w2-tw)/2, t2]],
    [[-tw/2, -h/2 + t2, 0], [tw, h - t1 - t2]],
    [[-w1/2, h/2 - t1, 0], [(w1 - tw)/2, t1]],
    [[tw/2, h/2 - t1, 0], [(w1 - tw)/2, t1]]
]

# Adiciono os retângulos, usando o ponto inicial e os deltas (por isso já fiz minha lista daquela forma)
for initial_point, delta in rectangles_points_and_deltas:
    occ.addRectangle(*initial_point, *delta)

# Vejo os pontos das linhas que quero conectar, no caso em cima e embaixo ((2, 5), (15, 20)), e crio uma linha entre eles.
extra_lines_points = [[2, 5], [15, 20]]
for start, end in extra_lines_points:
    occ.addLine(start, end)

# Agora crio o wire e a superfície desses retângulos extras, depois de ver quais são as tags das linhas em que quero criar esse retângulo, que no 
# caso são:
extra_rectangles_lines = [[11, 20, 22, 14], [21, 8, 9, 2]]
extra_wires = []
for rectangle in extra_rectangles_lines:
    extra_wires.append(occ.addCurveLoop(rectangle))

for wire in extra_wires:
    occ.addSurfaceFilling(wire)

# Com a malha 2D funcionando perfeitamente (testar ali na frente), podemos gerar a extrusão dessa cross section para formar uma viga de 1m.

# Sincronizo tudo, muito importante, e extrudo na direção z, falando que quero recombinar os triângulos em quads e os tets em hexas
occ.synchronize()
occ.extrude(gmsh.model.getEntities(2), 0, 0, l, recombine=True)
occ.synchronize()

# Agora, com o outline feito e com todas as superfícies criadas, eu gero uma malha estruturada.
for _, surface in gmsh.model.getEntities(2):
    mesh.setTransfiniteSurface(surface)
# mesh.generate(2) # testando

for _, volume in gmsh.model.getEntities(3):
    mesh.setTransfiniteVolume(volume)


# Mesmo eu dizendo que quero recombinar lá em cima, é importante que ativemos essa configuração aqui para não dar erro depois.
gmsh.option.setNumber("Mesh.RecombineAll", 1)

# Também dou uma controlada nos tamanhos
gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 0.1)

# Feito, agora definimos os volumes como transfinite, geramos a malha 3D e torcemos para dar tudo certo.
mesh.generate(3)
gmsh.fltk.run()
gmsh.finalize()