import gmsh
gmsh.initialize()
occ = gmsh.model.occ
mesh = gmsh.model.mesh
option = gmsh.option.setNumber





gmsh.fltk.run()
gmsh.finalize()