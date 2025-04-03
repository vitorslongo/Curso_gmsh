import gmsh

gmsh.initialize()

origin = [0]*3
cylinder_x = gmsh.model.occ.addCylinder(*origin, 5, 0, 0, 1)
cylinder_y = gmsh.model.occ.addCylinder(*origin, 0, 5, 0, 1)
cylinder_z = gmsh.model.occ.addCylinder(*origin, 0, 0, 5, 1)

gmsh.model.occ.translate([(3, cylinder_x)], -2.5, 0, 0)
gmsh.model.occ.translate([(3, cylinder_y)], 0, -2.5, 0)
gmsh.model.occ.translate([(3, cylinder_z)], 0, 0, -2.5)

sphere = gmsh.model.occ.addSphere(0, 0, 0, 2)
cube = gmsh.model.occ.addBox(0, 0, 0, 3, 3, 3)
gmsh.model.occ.translate([(3, cube)], -1.5, -1.5, -1.5)

cube_sphere_intersect = gmsh.model.occ.intersect([(3, sphere)], [(3, cube)])
final_result = gmsh.model.occ.cut(cube_sphere_intersect[0], [(3, cylinder_x), (3, cylinder_y), (3, cylinder_z)])

gmsh.model.occ.synchronize()
gmsh.write("exemplo_2.stl")
# gmsh.fltk.run()
gmsh.finalize()
