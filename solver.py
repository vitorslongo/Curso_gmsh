import numpy as np
import meshio
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def shape_functions_hex8(xi, eta, zeta):
    return 0.125 * np.array([
        (1 - xi)*(1 - eta)*(1 - zeta),
        (1 + xi)*(1 - eta)*(1 - zeta),
        (1 + xi)*(1 + eta)*(1 - zeta),
        (1 - xi)*(1 + eta)*(1 - zeta),
        (1 - xi)*(1 - eta)*(1 + zeta),
        (1 + xi)*(1 - eta)*(1 + zeta),
        (1 + xi)*(1 + eta)*(1 + zeta),
        (1 - xi)*(1 + eta)*(1 + zeta)
    ])

def dN_dxi(xi, eta, zeta):
    dN = np.zeros((8, 3))
    signs = [-1, 1]
    idx = 0
    for k in signs:
        for j in signs:
            for i in signs:
                dN[idx, 0] = 0.125 * i * (1 + j * eta) * (1 + k * zeta)
                dN[idx, 1] = 0.125 * j * (1 + i * xi)  * (1 + k * zeta)
                dN[idx, 2] = 0.125 * k * (1 + i * xi)  * (1 + j * eta)
                idx += 1
    return dN

def get_D(E, nu):
    c = E / ((1 + nu)*(1 - 2*nu))
    return c * np.array([
        [1 - nu, nu,     nu,     0, 0, 0],
        [nu,     1 - nu, nu,     0, 0, 0],
        [nu,     nu,     1 - nu, 0, 0, 0],
        [0,      0,      0,      (1 - 2*nu)/2, 0, 0],
        [0,      0,      0,      0, (1 - 2*nu)/2, 0],
        [0,      0,      0,      0, 0, (1 - 2*nu)/2]
    ])

def element_matrices_hex8(coords, E, nu, rho):
    D = get_D(E, nu)
    Ke = np.zeros((24, 24))
    Me = np.zeros((24, 24))
    gp = [-np.sqrt(1/3), np.sqrt(1/3)]

    for xi in gp:
        for eta in gp:
            for zeta in gp:
                dNdxi = dN_dxi(xi, eta, zeta)
                J = dNdxi.T @ coords
                detJ = np.linalg.det(J)
                if detJ <= 0:
                    print(detJ)
                    raise ValueError("detJ <= 0")
                invJ = np.linalg.inv(J)
                dNdx = dNdxi @ invJ

                B = np.zeros((6, 24))
                for i in range(8):
                    xi_, yi, zi = dNdx[i]
                    B[0, 3*i]     = xi_
                    B[1, 3*i+1]   = yi
                    B[2, 3*i+2]   = zi
                    B[3, 3*i]     = yi
                    B[3, 3*i+1]   = xi_
                    B[4, 3*i+1]   = zi
                    B[4, 3*i+2]   = yi
                    B[5, 3*i]     = zi
                    B[5, 3*i+2]   = xi_

                Ke += B.T @ D @ B * detJ

                N = shape_functions_hex8(xi, eta, zeta)
                Nmat = np.zeros((3, 24))
                for i in range(8):
                    Nmat[0, 3*i]   = N[i]
                    Nmat[1, 3*i+1] = N[i]
                    Nmat[2, 3*i+2] = N[i]
                Me += rho * (Nmat.T @ Nmat) * detJ

    return Ke, Me

def main():
    # Parâmetros
    E = 210e9      # Pa
    nu = 0.3
    rho = 7800     # kg/m³
    num_modes = 6
    tol = 1e-6

    # Lê malha
    mesh = meshio.read("viga_i_estruturada.msh")
    points = mesh.points
    cells = mesh.cells_dict["hexahedron"]
    num_nodes = len(points)
    ndof = 3 * num_nodes

    K = sp.lil_matrix((ndof, ndof))
    M = sp.lil_matrix((ndof, ndof))

    for conn in cells:
        coords = points[conn]
        Ke, Me = element_matrices_hex8(coords, E, nu, rho)
        dof_map = []
        for n in conn:
            dof_map.extend([3*n, 3*n+1, 3*n+2])
        for i in range(24):
            for j in range(24):
                K[dof_map[i], dof_map[j]] += Ke[i, j]
                M[dof_map[i], dof_map[j]] += Me[i, j]

    # Restrições no plano z = 0
    fixed_nodes = [i for i, p in enumerate(points) if abs(p[2]) < tol]
    fixed_dofs = []
    for n in fixed_nodes:
        fixed_dofs.extend([3*n, 3*n+1, 3*n+2])
    all_dofs = np.arange(ndof)
    free_dofs = np.setdiff1d(all_dofs, fixed_dofs)

    Kf = K[free_dofs][:, free_dofs].tocsc()
    Mf = M[free_dofs][:, free_dofs].tocsc()

    vals, vecs = spla.eigsh(Kf, k=num_modes, M=Mf, sigma=0, which='LM')
    freqs = np.sqrt(np.abs(vals)) / (2 * np.pi)

    print("Frequências naturais (Hz):")
    for i, f in enumerate(freqs):
        print(f"Modo {i+1}: {f:.2f} Hz")

    # Reconstrói solução completa
    U_full = np.zeros((ndof, num_modes))
    U_full[free_dofs, :] = vecs
    U_nodal = U_full.reshape((num_nodes, 3, num_modes))

    for m in range(num_modes):
        meshio.write_points_cells(
            f"modo_{m+1}.vtu",
            points,
            [("hexahedron", cells)],
            point_data={"modo": U_nodal[:, :, m]}
        )

if __name__ == "__main__":
    main()
