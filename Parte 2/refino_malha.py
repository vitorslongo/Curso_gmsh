import gmsh

gmsh.initialize()
occ = gmsh.model.occ
mesh = gmsh.model.mesh
gmsh.option.setNumber("General.Verbosity", 0)
origin = [0]*3
# Controle de tamanho geral:
# gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.1)

global_size = 5
refine_size = .01
surfaces_list = [5, 12]
fields_list = []

# Criação de uma geometria qualquer
main_cylinder = occ.add_cylinder(*origin, 0, 0, 1, 1)
small_cylinder = occ.add_cylinder(.5, 0, 1, 0, 0, 1, .2)
small_box = occ.addBox(-.5, 0, 1, .2, .2, 1 )
occ.synchronize()

# Refino de malha
outer_field = mesh.field.add("Constant")
mesh.field.setNumbers(outer_field, "SurfacesList", [])
mesh.field.setNumber(outer_field, "VOut", global_size)
fields_list.append(outer_field)

refine_field = mesh.field.add("Constant") # chamar atenção para setNumber e setNumbers com "s" e sem "s"
mesh.field.setNumbers(refine_field, "SurfacesList", surfaces_list)
mesh.field.setNumber(refine_field, "VIn", refine_size)
fields_list.append(refine_field)

minimum_field = gmsh.model.mesh.field.add("Min")
mesh.field.setNumbers(minimum_field, "FieldsList", fields_list)
mesh.field.setAsBackgroundMesh(minimum_field)

mesh.field.setAsBackgroundMesh(minimum_field)


mesh.generate(2)
# gmsh.write("cilindro_teste.stl")
gmsh.fltk.run()
gmsh.finalize()