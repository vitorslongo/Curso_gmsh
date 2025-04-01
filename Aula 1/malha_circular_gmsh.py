import gmsh

gmsh.initialize()







gmsh.model.occ.addCircle(0, 0, 0, 1)

gmsh.model.occ.addCurveLoop([1])
gmsh.model.occ.addPlaneSurface([1])
gmsh.model.occ.synchronize()
gmsh.model.mesh.setTransfiniteAutomatic([(1, 1)])
gmsh.model.mesh.setRecombine(2, 1)

gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", 1)
gmsh.option.setNumber("Mesh.Algorithm", 8)
gmsh.option.setNumber("Mesh.RecombineAll", 1)

gmsh.model.mesh.generate(2)
gmsh.fltk.run()