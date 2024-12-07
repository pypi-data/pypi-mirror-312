#!/usr/bin/env python3

import trexio
import numpy as np
from . import nucleus as trexio_nucleus
from . import basis as trexio_basis
from . import ao as trexio_ao
from . import mo as trexio_mo

try:
    import qmckl
    def run(trexio_file, n_points):
        """
        Computes numerically the overlap matrix in the AO basis and compares it to
        the matrix stored in the file.
        """

        trexio_filename = trexio_file.filename
        context = qmckl.context_create()
        qmckl.trexio_read(context, trexio_filename)

        mo = trexio_mo.read(trexio_file)
        ao = mo["ao"]
        basis = ao["basis"]
        nucleus = basis["nucleus"]
        assert basis["type"] == "Gaussian"

        rmin = np.array( list([ np.min(nucleus["coord"][:,a]) for a in range(3) ]) )
        rmax = np.array( list([ np.max(nucleus["coord"][:,a]) for a in range(3) ]) )

        shift = np.array([8.,8.,8.])
        linspace = [ None for i in range(3) ]
        step = [ None for i in range(3) ]
        for a in range(3):
          linspace[a], step[a] = np.linspace(rmin[a]-shift[a], rmax[a]+shift[a], num=n_points, retstep=True)

        print("Integration steps:", step)
        dv = step[0]*step[1]*step[2]

        point = []
        for x in linspace[0]:
          #print(".",end='',flush=True)
          for y in linspace[1]:
            for z in linspace[2]:
               point += [ [x, y, z] ]
        point = np.array(point)
        point_num = len(point)
        mo_num = mo["num"]

        qmckl.set_point(context, 'N', point_num, np.reshape(point, (point_num*3)))
        chi = qmckl.get_mo_basis_mo_value(context, point_num*mo_num)
        chi = np.reshape( chi, (point_num,mo_num) )
        S = chi.T @ chi * dv
        print()

        S_ex = np.eye(mo_num)

        for i in range(mo_num):
          for j in range(i,mo_num):
            print("%3d %3d %15f %15f"%(i,j,S[i][j],S_ex[i,j]))
        S_diff = S - S_ex
        print ("Norm of the error: %f"%(np.linalg.norm(S_diff)))

except ImportError:

    def run(trexio_file, n_points):
        """
        Computes numerically the overlap matrix in the AO basis and compares it to
        the matrix stored in the file.
        """

        mo = trexio_mo.read(trexio_file)
        ao = mo["ao"]
        basis = ao["basis"]
        nucleus = basis["nucleus"]
        assert basis["type"] == "Gaussian"

        rmin = np.array( list([ np.min(nucleus["coord"][:,a]) for a in range(3) ]) )
        rmax = np.array( list([ np.max(nucleus["coord"][:,a]) for a in range(3) ]) )

        shift = np.array([8.,8.,8.])
        linspace = [ None for i in range(3) ]
        step = [ None for i in range(3) ]
        for a in range(3):
          linspace[a], step[a] = np.linspace(rmin[a]-shift[a], rmax[a]+shift[a], num=n_points, retstep=True)

        print("Integration steps:", step)
        dv = step[0]*step[1]*step[2]

        mo_num = mo["num"]
        S = np.zeros( [ mo_num, mo_num ] )
        for x in linspace[0]:
          #print(".",end='',flush=True)
          for y in linspace[1]:
            for z in linspace[2]:
               chi = trexio_mo.value(mo, np.array( [x,y,z] ) )
               S += np.outer(chi, chi)*dv
        print()

        S_ex = np.eye(mo_num)
        S_diff = S - S_ex
        print ("%e %e"%(np.linalg.norm(S), np.linalg.norm(S_ex) ))
        print ("Norm of the error: %e"%(np.linalg.norm(S_diff)))
        #print(S_diff)

        for i in range(mo_num):
          for j in range(i,mo_num):
            print("%3d %3d %15f %15f"%(i,j,S[i][j],S_ex[i,j]))



