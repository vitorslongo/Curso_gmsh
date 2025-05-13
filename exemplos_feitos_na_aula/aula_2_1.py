import gmsh
gmsh.initialize()
occ = gmsh.model.occ
mesh = gmsh.model.mesh
option = gmsh.option.setNumber

w1 = .15
w2 = .2
h = .2
t1 = .03
t2 = .03
tw = .03
l = 1


rectangles_points_and_deltas = [
    [[-w2/2, -h/2, 0], [(w2-tw)/2, t2]],
    [[tw/2, -h/2, 0], [(w2-tw)/2, t2]],
    [[-tw/2, -h/2 + t2, 0], [tw, h - t1 - t2]],
    [[-w1/2, h/2 - t1, 0], [(w1 - tw)/2, t1]],
    [[tw/2, h/2 - t1, 0], [(w1 - tw)/2, t1]]
]

for initial_point, deltas in rectangles_points_and_deltas:
    occ.addRectangle(*initial_point, *deltas)

extra_lines_points = [[2, 5], [15, 20]]
for start, end in extra_lines_points:
    occ.addLine(start, end)

extra_rectangles_lines = [[11, 20, 22, 14], [21, 8, 9, 2]]
extra_wires = []

for rectangle in extra_rectangles_lines:
    extra_wires.append(occ.addCurveLoop(rectangle))

for wire in extra_wires:
    occ.addSurfaceFilling(wire)

occ.synchronize()

occ.extrude(gmsh.model.getEntities(2), 0, 0, 1, recombine=True)
occ.synchronize()

for _, surface in gmsh.model.getEntities(2):
    mesh.setTransfiniteSurface(surface)

for _, volume in gmsh.model.getEntities(3):
    mesh.setTransfiniteVolume(volume)

option("Mesh.RecombineAll", 1)
# option("Mesh.ElementOrder", 2)

option("Mesh.MeshSizeFactor", .1)

mesh.generate(3)




gmsh.fltk.run()
gmsh.finalize()