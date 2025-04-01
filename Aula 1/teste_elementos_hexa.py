import gmsh

gmsh.initialize()

gmsh.option.setNumber("Mesh.Algorithm3D", 10)  # 10 is the code for hxt_3D
gmsh.option.setNumber("Mesh.ElementOrder", 1)  # Set element order to 1 for linear elements
gmsh.option.setNumber("Mesh.RecombineAll", 1)  # Recombine into hexahedra

gmsh.model.occ.addBox(0, 0, 0, 1, 1, 1)

gmsh.model.occ.synchronize()




gmsh.model.mesh.generate(3)
gmsh.fltk.run()