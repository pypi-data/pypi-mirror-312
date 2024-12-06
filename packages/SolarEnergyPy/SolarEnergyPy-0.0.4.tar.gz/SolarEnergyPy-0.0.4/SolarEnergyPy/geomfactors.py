# from __future__ import absolute_import
from matplotlib import path 
import numpy as np
from VisualShape3D.mathutils import *
from VisualShape3D.geomutils import *

"""
    View Factors in an enclosure
       
             3D Cases
    
    Algorithm : iteration from one pair of points, 
             And then, it accumulates points in target surface;
             Finllay, it accumulates points in source surface.

    Made by Liqun He, May 28,2022
    Improved by Liqun He, Sept.7, 2024
"""
##
#  1）封闭空间内，任意平面之间的角系数
##

"""
        Note that j is the submitting surface: 
            such that  Vi = Fij * Vj
 
"""

def ViewFactorsEnclosure(Enclosure,nx=10,ny=10):
    #
    #  考虑遮挡情况
    #
    #   Enclosure is a list of surfaces enclosing a space, 
    #   Each surface is a polygon made of a list of vertex
    #
    #  返回:   Fij * Aj (阵列)
    #
    n = len(Enclosure)
    F = np.zeros((n,n))

    #  to set j as submitting surface, such that Vi = Fij * Vj
    for j,submitting in enumerate(Enclosure):
        start = j + 1
        remains = Enclosure[start:]
        for ii,receiving in enumerate(remains):
            ret = MutualVisibility(submitting,receiving)
            if ret == False :
                continue

            i = start + ii
            for k in range(n):
                if k == j :
                    continue

                if k != i :

                    shading = Enclosure[k]
                    ret = MutualVisibility(submitting,shading)
                    if ret == False :
                        continue

                    Fij = ViewFactor(submitting,receiving,shading,nx=nx,ny=ny)
                
                else:
                    Fij = ViewFactor(submitting,receiving,across=None,nx=nx,ny=ny)

            # print(f" F({i},{j}) = {Fij}")
            F[i,j] = Fij

    GF = AfterModified(Enclosure, F)         
    return GF

##
#  2）平面到平面的角系数
##
def ViewFactor( from_poly, to_poly, across=None, nx=10, ny=10):
    #
    #  有遮挡条件下
    #        f = ViewFactor(from_poly,to_poly,across)
    #
    #  无遮挡条件下
    #        f = ViewFactor(from_poly,to_poly,across,10,10)
    #  
    #  from_poly, to_poly : two polygons
    #  across             : potential shading polygons
    #
    #  返回:  Fij * Aj （单个值)

    source_points,dAj, _,_ = Mesh(from_poly, nx=nx, ny=ny)

    f = 0
    nj = UnitVector(dAj)
    dAj = Magnitude(dAj)[0]

    for Pj in source_points : # one by one
        fij = P2Polygon(Pj,nj,to_poly,across=across, nx=nx,ny=ny)
        f += fij*dAj
       
    Aj, Ai = GetArea(from_poly), GetArea(to_poly)
    Fij = f/Aj

    return Fij

##
#                  2.1) 分网格
#
#   A regular grid is made for a polygon 
#   returns : 
#       points, dA, dx, dy
#
#       points, dA : element centers and its area vector;
#       dx,dy      : sizes of one elements, for plotting.
##
def Mesh(polygon, nx=10, ny=10):
    R0 = polygon[0] 
    xy, U = to_2d(polygon)
    A = GetArea2D(xy)
    n = U[2,:]

    xv, yv = xy[:,0], xy[:,1]

    minx,maxx = min(xv),max(xv)
    miny,maxy = min(yv),max(yv)

    dx = abs(maxx-minx)/nx
    dy = abs(maxy-miny)/ny
    
    x = np.linspace(minx+0.5*dx,maxx-0.5*dx,nx)
    y = np.linspace(miny+0.5*dy,maxy-0.5*dy,ny)
    X,Y = np.meshgrid(x,y)

    indexing = in_polygon_2d(X,Y, xv, yv)

    a = X[indexing].flatten()
    b = Y[indexing].flatten()
    R = D2toD3_xy(a,b,U,R0)

    m = len(a)
    dA = A/m
    dA = dA*n
    
    # for plotting
    x = X[indexing]
    y = Y[indexing]    

    return R, dA, dx,dy

##
#        2.2）点到平面的角系数
##
def P2Polygon(P, nj, polygon, across=None, nx=10, ny=10):
    #
    #  在潜在遮挡条件下的点对面的角系数
    #
    #     P : source point 
    #
    #  View factors from P to mesh points in polygon 
    #  across : possible shading polygons.

    Pj = P
    Pi, dAi, _, _ = Mesh(polygon, nx=nx, ny=ny)
    
    if across is not None:
        
        n  = GetNormal(across)     # [dx,dy,dz] 
        R0 = Array(across[0,:])    # [x,y,z]
        P0 = Pj
        L  = UnitVector(Pi-Pj)

        R, intersect1 = LinesXPlane(P0,L,R0,n)  # intersection of line with plane
        # print(f" R, intersect1: {R}, {intersect1}")      
        
        if R is not None:
            not_shaded = ~intersect1 
            Pi0 = Pi[intersect1]
            Pi  = Pi[not_shaded]

            if Pi0.size == 0:
                return 0

            intersect2 = PointsInPolygon(R,across)
            # print(f" Shapes of R ,Pj and intersect2: {R.shape,Pj0.shape,intersect2.shape}")

            not_shaded = intersect2 == np.array(intersect2.shape)*False
            # print(f" not shaded : {not_shaded}")

            Pi = np.vstack([Pi, Pi0[not_shaded]])
    
    if Pi.size == 0 :
        return 0

    Fij = P2Ps(Pj,nj, Pi,dAi)

    return np.sum(Fij)

#      2.3 ）单点对多点的角系数
#
#     必须是单点，返回一个向量
#
def P2Ps(Pj, nj, Pi, dAi):
    #
    # 一个点（Pj）到一群点（Pi）的角系数
    #
    ni = UnitVector(dAi)
    Ai = Magnitude(dAi)

    ret = fij( Pj, Pi, nj, ni, Ai )

    # print(f" 单点对多点的角系数 : {ret}")

    return ret
    
##    
#           2.3 )  单元之间的角系数  
#     One point ( j ) to many points ( i ),  j->i indicating the radiation direction 
#     Results are packed into a matrix Fij 
#
# 1）点对点的角系数
#  
#      两个单点之间的角系数。
#
#      如果是两组点，目前仅仅是点运算，即获得对应位置两个单点之间的角系数。
#      尚不能进行交叉运算。
#      未来也许实现类似叉乘的叉运算版本，返回一个方阵。
#
##
def fij(Pj, Pi, nj, ni, dAi ):
    '''
      equivalent to the final division : Fij/Aj
    
        i, j    : receiving and submitting indexing
        Pi,Pj   : center points of two elements, np.array([x,y,z])
        ni,nj   : unit vectors of  two elements, np.array([x,y,z])
        dAi,dAj : areas of two elements
    '''
    S  = Magnitude(Pi - Pj).flatten()   # important : turns to a simple row

    Vij = Pj - Pi     # vector j -> i
    Vji = Pi - Pj     # vector i -> j
    dj  = Projection(Vij,ni) # project on nj
    di  = Projection(Vji,nj) # project on ni
    
    return di*dAi*dj/( np.pi* S*S*S*S)  # S has to be a row

##
#    Help Functions
##
def MutualVisibility(surface1,surface2):
    n1, n2 = GetNormal(surface1), GetNormal(surface2)
    rad, deg = AngleBetween2(n1,n2)
    if deg >= 180 :
        return False
    
    points,polygon = surface2, surface1
    points, path2d = D3ToD2(points,polygon)

    if AllNegative(points[:,2]) or AllZero(points[:,2]):
        return False
    """
           Points and polygon are mutual visible
           (1) AllPositive(points[:,2]) : 
              Points are scattering above the polygon.
          
           (2) Points are partially positive and negative 
              Points are scattering around the polygon.
    """
    return True

def AfterModified(Enclosure, f):
    
    n = len(Enclosure)
    area = np.zeros(n)

    for i, surface in enumerate(Enclosure):
        area[i] = GetArea(surface)

    GF = f
    GF_SUM = np.zeros(n)
    for _ in range(10):
        GF_SUM = np.sum(GF, axis = 0)  #  summing each col
        Error  = np.abs(GF_SUM - 1)

        if np.all(Error < 1.0E-3):
            return GF

        for j, surface in enumerate(Enclosure):
            GF[:,j] = GF[:,j]/GF_SUM[j]

    return GF
##
#    Help Functions
##
"""
                           光照系数

        封闭空间表面辐射换热计算所采用的是红外光照系数而不是角系数

"""
def IlluminativeFactors(Enclosure,nx=10,ny=10):
    #
    #  考虑遮挡情况下，计算每个表面的红外光照系数和可见光光照系数（散射）
    #   
    #   IFs = IlluminationFactors(Enclosure,10,10)
    #
    #   Enclosure is a list of surfaces enclosing a space, 
    #   Each surface is a dicttionary that include a polygon and its optical properties
    #   surface = {'polygon':polygon,'infrared':[alpha,rho],'visible':[alpha,rho]}
    pass

    
"""
                           光斑面积

"""
def SolarSpots(SolarPosition,Enclosure,nx=10,ny=10):
    # 
    #  考虑遮挡情况下，计算每个表面的光照面积(直射辐射)，
    #   spot_areas = SolarSpots(Enclosure,nx=10,ny=10)
    #
    #   Enclosure is a list of surfaces enclosing a space, 
    #   Each surface is a polygon that is a list of vertex
    #
    pass

def main():
    pass

if __name__ == '__main__':
    main()