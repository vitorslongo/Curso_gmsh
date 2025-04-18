"""
Esse aqui é um outro exemplo na pegada do da viga I, mas é uma saeção transversal diferente caso tenha ficado difícil de entender no primeiro a 
geração da geometria.
"""
import gmsh
occ = gmsh.model.occ
mesh = gmsh.model.mesh

gmsh.initialize()

b = 0.2
h = 0.2
t = 0.05

occ.addRectangle(-b/2, -h/2, 0, t, t)
occ.addRectangle(b/2 - t, -h/2, 0, t, t)
occ.addRectangle(-b/2, h/2 - t, 0, t, t)
occ.addRectangle(b/2 - t, h/2 - t, 0, t, t)

points = (2, 5, 3, 8, 7, 14, 8, 13, 13, 10, 16, 11, 10, 3, 9, 4)

for i in range(0, len(points), 2):
    occ.addLine(points[i], points[i+1])

lines = [
    [17, 8, 18, 2],
    [7, 19, 13, 20],
    [21, 16, 22, 10],
    [3, 23, 9, 24],
    ]
wires = []
for rectangle in lines:
    wires.append(occ.addCurveLoop(rectangle))

surfaces = []
for wire in wires:
    surfaces.append(occ.addSurfaceFilling(wire))

occ.synchronize()
occ.extrude(gmsh.model.getEntities(2), 0, 0, 1)

occ.synchronize()

surface_tags = [s[1] for s in gmsh.model.getEntities(2)]
for surface in surface_tags:
    mesh.setTransfiniteSurface(surface)

volume_tags = [v[1] for v in gmsh.model.getEntities(3)]
for volume in volume_tags:
    mesh.setTransfiniteVolume(volume)

gmsh.option.setNumber("Mesh.MeshSizeFactor", .3)
gmsh.option.setNumber("Mesh.RecombineAll", 1)

mesh.generate(3)
gmsh.fltk.run()
gmsh.finalize()