import gmsh
gmsh.initialize()

occ = gmsh.model.occ
mesh = gmsh.model.mesh
option = gmsh.option.setNumber

option("General.Terminal", 0)


points_coords = [
    [0, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [1, 1, 0],
    [1, 3, 0],
    [0, 3, 0]
]

points = []
for coords in points_coords:
    points.append(occ.addPoint(*coords))

lines = []
for i in range(len(points)-1):
    lines.append(occ.addLine(points[i], points[i+1]))

lines.append(occ.addLine(points[-1], points[0]))

wire = occ.addCurveLoop(lines)
surface = occ.addPlaneSurface([wire])
occ.synchronize()



occ.extrude([(2, surface)], 0, 0, 1)
occ.synchronize()






mesh.generate(3)
gmsh.fltk.run()
gmsh.finalize()