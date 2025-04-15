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

# Geração de uma malha estruturada por meio da subdivisao da seção transversal da viga 
# em retângulos seguida pela extrusão da seção.

rectangles_points_and_deltas = [
    [[-w2/2, -h/2, 0], [(w2-tw)/2, t2]],
    [[tw/2, -h/2, 0], [(w2-tw)/2, t2]],
    [[-tw/2, -h/2 + t2, 0], [tw, h - t1 - t2]],
    [[-w1/2, h/2 - t1, 0], [(w1 - tw)/2, t1]],
    [[tw/2, h/2 - t1, 0], [(w1 - tw)/2, t1]]
]

for initial_point, delta in rectangles_points_and_deltas:
    occ.addRectangle(*initial_point, *delta)

# Vejo os pontos das linhas que quero conectar, no caso em cima e embaixo ((2, 5), (15, 20)), e crio uma linha entre eles.
extra_lines_points = [[2, 5], [15, 20]]

for start, end in extra_lines_points:
    occ.addLine(start, end)

# Agora crio o wire e a superfície desses retângulos, depois de ver quais são as tags das linhas em que quero criar esse retângulo, que no caso são:
extra_rectangles_lines = [[11, 20, 22, 14], [21, 8, 9, 2]]

extra_wires = []
for rectangle in extra_rectangles_lines:
    extra_wires.append(occ.addCurveLoop(rectangle))

for wire in extra_wires:
    occ.addSurfaceFilling(wire)

occ.synchronize()
occ.extrude(gmsh.model.getEntities(2), 0, 0, l, recombine=True)
occ.synchronize()

# Agora, com o outline feito e com todas as superfícies criadas, eu gero uma malha estruturada.

for _, surface in gmsh.model.getEntities(2):
    mesh.setTransfiniteSurface(surface)
# mesh.generate(2) # testando

# Com a malha funcionando perfeitamente, podemos gerar a extrusão dessa cross section para formar uma viga de 1m.

for _, volume in gmsh.model.getEntities(3):
    mesh.setTransfiniteVolume(volume)

# Feito, agora definimos os volumes como transfinite, geramos a malha 3D e torcemos para dar tudo certo.

gmsh.option.setNumber("Mesh.RecombineAll", 1)
gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 0.1)
mesh.generate(3)
gmsh.fltk.run()
gmsh.finalize()