"""
Nesse exemplo vamos aprender o básico do Gmsh de geração de geometrias e malhas.
Vamos gerar uma superície em forma de L e malhar ela, depois, vamos extrudá-la e gerar uma malha 3D.
"""
import gmsh
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)

# É muito importante inicializar o gmsh, senão nada funciona.
# Também falamos para o Gmsh não printar nada no terminal pois por enquanto nao precisamos, só usamos isso normalmente
# caso queiramos debugar o nosso código.

# Primeiro vamos gerar os pontos que definem as nossas linahs:

# Pooderíamos fazer assim:
# p1 = gmsh.model.occ.addPoint(0, 0, 0)
# p2 = gmsh.model.occ.addPoint(2, 0, 0)
# p3 = gmsh.model.occ.addPoint(2, 1, 0)
# p4 = gmsh.model.occ.addPoint(1, 1, 0)
# p5 = gmsh.model.occ.addPoint(1, 3, 0)
# p6 = gmsh.model.occ.addPoint(0, 3, 0)

# Ou assim (maneira mais compacta)
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
    # fazer o unpacking dessa maneira é a mesma coisa que fazer
    # gmsh.model.occ.addPoint(coords[0], coords[1], coords[2])
    gmsh_points.append(point)

# Ou assim, se você quiser fazer da maneira mais compacta possível:
# gmsh_points = [gmsh.model.occ.addPoint(*coords) for coords in points_coords]

# Essas 3 opções fazem exatamente a mesma coisa, gera os pontos conforme as coordenadas que passamos.

# print(gmsh_points) # <-- teste para ver se os pontos e coordenadas que colocamos faz sentido.
gmsh_lines = []
for tag in gmsh_points:
    if tag == gmsh_points[-1]:
        line = gmsh.model.occ.addLine(tag, gmsh_points[0])
    else:
        line = gmsh.model.occ.addLine(tag, tag+1)

    gmsh_lines.append(line)

# Essa lógica do if e else é para tratar o ultimo ponto, que nao segue a mesma lógica dos outros, pois ele nao vai
# se conectar com o próximo, mas sim com o primeiro.

# Se eu tentar fazer uma malha aqui nao vai funcionar, porque eu nao tenho uma superfície!
# Mas antes ainda de fazermos a superfície, precisamos falar para o Gmsh que essas linhas que eu criei fazem um loop:
curve_loop = gmsh.model.occ.addCurveLoop(gmsh_lines)

# Depois disso podemos dizer que esse loop é uma superfície:
l_surface = gmsh.model.occ.addPlaneSurface([curve_loop])

# Antes só de testar, um ponto muito importante: como o kernel com o qual a gente gerou a geometria é apenas uma adjacência
# do Gmsh, precisamos dizer para ele sincronizar o que foi feito com esse kernel com o Gmsh em si.
gmsh.model.occ.synchronize()

# Agora sim, deve funcionar.
# gmsh.model.mesh.generate(2)

# Vamos um passo além agora, uma malha 3D. Nesse caso aqui vamos só extrudar a superfície que a gente fez na direção z
# para obtermos um sólido. Vale ressltar que nao precisamos definir nada aqui que o que extrudamos é um volume, superfície, etc.
# O OCC já cuida disso para nós.
gmsh.model.occ.extrude([(2, l_surface)], 0, 0, 1)
# Feito, simples assim temos uma geometria 3D.

# Vamos sincronizar novamente e gerar a malha 3D agora.
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)

# Caso você esteja se perguntando como controlamos o tamanho da nossa malha, isso será visto no exemplo 3, mas ainda temos
# mais algumas coisas legais sobre geometrias que precisamos ver. Vamos para o próximo exemplo!
gmsh.fltk.run()
gmsh.finalize()