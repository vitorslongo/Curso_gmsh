import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)
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

    gmsh_lines.append(line)

# explicar que essa lógica é para tratar do caso do último ponto, que deve ser conectado ao primeiro

# se eu tentar fazer uma malha aqui nao vai funcionar, porque eu nao tenho uma superfície

curve_loop = gmsh.model.occ.addCurveLoop(gmsh_lines)
l_surface = gmsh.model.occ.addPlaneSurface([curve_loop])

# Agora sim. Deve funcionar

# tendo isso vamos testar as extrusões:
gmsh.model.occ.extrude([(2, l_surface)], 0, 0, 1)
# feito, simples assim

# não precisamos ficar gerando a malha dessa forma na interface, podemos fazer isso diretamente no nosso script:
# mas nós devemos colocar o synchronize antes de gerar a malha!!
# (colocamos o codigo de gerar a malha lá embaixo para nao termos mais erros)
gmsh.model.occ.synchronize()


# para definirmmos o tamanho da malha, podemos fazer da seguinte maneira:
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.1)
# podemos definir também o tamanho da malha em cada ponto, linha ou superfície, mas como isso entra na parte de controle de malha vamos falar disso depois

gmsh.model.occ.add













gmsh.model.mesh.generate(3)
gmsh.fltk.run()
gmsh.finalize()