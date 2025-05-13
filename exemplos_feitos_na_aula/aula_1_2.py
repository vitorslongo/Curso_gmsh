import gmsh
gmsh.initialize()

occ = gmsh.model.occ
mesh = gmsh.model.mesh


origin = [0, 0, 0]

c_1 = occ.addCylinder(*origin, 5, 0, 0, 1)
c_2 = occ.addCylinder(*origin, 0, 5, 0, 1)
c_3 = occ.addCylinder(*origin, 0, 0, 5, 1)
occ.translate([(3, c_1)], -2.5, 0, 0)
occ.translate([(3, c_2)], 0, -2.5, 0)
occ.translate([(3, c_3)], 0, 0, -2.5)

cube = occ.addBox(*origin, 3, 3, 3)
sphere = occ.addSphere(*origin, 2)
occ.translate([(3, cube)], -1.5, -1.5, -1.5)

intersection = occ.intersect([(3, cube)], [(3, sphere)])[0]

occ.cut(intersection, [(3, c_1), (3, c_2), (3, c_3)])

gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
occ.synchronize()




gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.1)
mesh.generate(2)
# gmsh.fltk.run()

gmsh.write("exemplo.stl")
gmsh.finalize()