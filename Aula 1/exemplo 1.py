import gmsh

gmsh.initialize()
# IMPORTANTÍSSIMO: SYNCHRONIZE DO OCC 

# poderia fazer assim
# p1 = gmsh.model.occ.addPoint(0, 0, 0)
# p2 = gmsh.model.occ.addPoint(2, 0, 0)
# p3 = gmsh.model.occ.addPoint(2, 1, 0)
# p4 = gmsh.model.occ.addPoint(1, 1, 0)
# p5 = gmsh.model.occ.addPoint(1, 3, 0)
# p6 = gmsh.model.occ.addPoint(0, 3, 0)

# ou assim (maneira mais compacta)
points_coords = [
    [0, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [1, 1, 0],
    [1, 3, 0],
    [0, 3, 0]
]
gmsh_points =[]
for coords in points_coords:
    point = gmsh.model.occ.addPoint(*coords)
    # fazer dessa maneira de cima é a mesma coisa que fazer
    # gmsh.model.occ.addPoint(coords[0], coords[1], coords[2])
    gmsh_points.append(point)

# perguntar se as pessoas estão entendendo, se for muito complexo, fazer da maneira mais simples


# OU ASSIM, DA MANEIRA MAIS COMPACTA POSSÍVEL:
# gmsh_points = [gmsh.model.occ.addPoint(*coords) for coords in points_coords]


# print(gmsh_points)
gmsh_lines = []
for tag in gmsh_points:
    if tag == gmsh_points[-1]:
        line = gmsh.model.occ.addLine(tag, gmsh_points[0])
    else:
        line = gmsh.model.occ.addLine(tag, tag+1)

# explicar que essa lógica é para tratar do caso do último ponto, que deve ser conectado ao primeiro



















gmsh.model.occ.synchronize()
gmsh.fltk.run()
gmsh.finalize()