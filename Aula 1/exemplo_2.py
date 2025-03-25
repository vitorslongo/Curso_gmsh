import gmsh

gmsh.initialize()
origin = [0]*3
cylinder_x = gmsh.model.occ.addCylinder(*origin, 5, 0, 0, 1)
cylinder_y = gmsh.model.occ.addCylinder(*origin, 0, 5, 0, 1)
cylinder_z = gmsh.model.occ.addCylinder(*origin, 0, 0, 5, 1)

gmsh.model.occ.translate([(3, cylinder_x)], -2.5, 0, 0)
gmsh.model.occ.translate([(3, cylinder_y)], 0, -2.5, 0)
gmsh.model.occ.translate([(3, cylinder_z)], 0, 0, -2.5)





gmsh.model.occ.synchronize()
gmsh.fltk.run()
gmsh.finalize()
