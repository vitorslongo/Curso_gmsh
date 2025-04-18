"""
Nesse exemplo nós vamos aprender a gerar uma geometria um pouco mais complexa, usando volumes para fazer as nossas
geometrias e fazendo operações booleanas com elas para obtermos a nossa forma final desejada.
Vamos também aprender como salvamos ela para visualizarmos em um software mais adequado (3D builder).
"""

import gmsh
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)

origin = [0]*3

# Vamos criar os nossos cilindros. Não tem nada de complicado, só pedir para ele adicionar um cilindro, e vemos os argumentos
# que precisamos passar para ele.
cylinder_x = gmsh.model.occ.addCylinder(*origin, 5, 0, 0, 1)
cylinder_y = gmsh.model.occ.addCylinder(*origin, 0, 5, 0, 1)
cylinder_z = gmsh.model.occ.addCylinder(*origin, 0, 0, 5, 1)

# Poderíamos ter feito uns cálculos e criado eles já na posição certinha, mas criamos ele todos na origem para vermos como 
# podemos transladá-los facilmente também.
gmsh.model.occ.translate([(3, cylinder_x)], -2.5, 0, 0)
gmsh.model.occ.translate([(3, cylinder_y)], 0, -2.5, 0)
gmsh.model.occ.translate([(3, cylinder_z)], 0, 0, -2.5)

# Feito isso, aqui vão mais algumas opções de volumes que podem ser criados:
sphere = gmsh.model.occ.addSphere(0, 0, 0, 2)
cube = gmsh.model.occ.addBox(0, 0, 0, 3, 3, 3)

# Transladamos também:
gmsh.model.occ.translate([(3, cube)], -1.5, -1.5, -1.5)

# Agora sim, vamos para as operações booleanas. Elas seguem essa lógica:
# Intersecção = intersect
# Subtração = cut
# União = fuse
# Deixar superfícies conformes = fragment
# ...
# Aqui vamos usar o intersect normale entre o cubo e a esfera, sempre usando dimTags
cube_sphere_intersect = gmsh.model.occ.intersect([(3, sphere)], [(3, cube)])
# 
# Aqui subtraímos os cilindrros do resto
final_result = gmsh.model.occ.cut(cube_sphere_intersect[0], [(3, cylinder_x), (3, cylinder_y), (3, cylinder_z)])

# Sincronizamos tudo e temos uma geometria legal.
gmsh.model.occ.synchronize()
gmsh.write("exemplo_2.stl")
gmsh.fltk.run()
gmsh.finalize()
