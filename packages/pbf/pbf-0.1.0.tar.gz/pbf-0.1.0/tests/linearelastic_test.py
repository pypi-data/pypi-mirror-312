import pbf
import mlhp

D = 3

print( "1. Setting up mesh and basis", flush=True )

refinementDepth = 0
polynomialDegree = 2
nelements = [10] * D
lengths = [1.0] * D

grid = mlhp.makeRefinedGrid(nelements, lengths)
basis = mlhp.makeHpTensorSpace(grid, polynomialDegree, nfields=D)

print( "2. Computing dirichlet boundary conditions", flush=True )

dirichlet = mlhp.integrateDirichletDofs(mlhp.vectorField(D, [0.0]*D), basis, [0])

print( "3. Setting up physics", flush=True )

E = mlhp.scalarField(D, 200 * 1e9)
nu = mlhp.scalarField(D, 0.3 )
rhs = mlhp.vectorField(D, [0.0, 0.0, 78.5 * 1e3])

kinematics = mlhp.smallStrainKinematics(D) 
constitutive = mlhp.isotropicElasticMaterial(E, nu)
integrand = mlhp.staticDomainIntegrand(kinematics, constitutive, rhs)

print( "4. Allocating linear system", flush=True )

matrix = mlhp.allocateUnsymmetricSparseMatrix( basis, dirichlet[0] )
vector = mlhp.allocateVectorWithSameSize( matrix )

print( "5. Integrating linear system", flush=True )

quadrature = mlhp.standardQuadrature( D )

mlhp.integrateOnDomain( basis, integrand, [matrix, vector], 
    dirichletDofs=dirichlet, quadrature=quadrature )

print( "6. Solving linear system", flush=True )

interiorDofs = mlhp.cg( matrix, vector )

allDofs = mlhp.inflateDofs( interiorDofs, dirichlet )

print( "7. Postprocessing solution", flush=True )

processors = [mlhp.solutionProcessor( D, allDofs, "Displacement" )]

#displX = mlhp.solutionEvaluator(basis, allDofs, 0)
#displY = mlhp.solutionEvaluator(basis, allDofs, 1)

postmesh = mlhp.gridOnCells( [polynomialDegree + 3] * D )
writer = mlhp.PVtuOutput( filename="outputs/linear_elasticity" )
            
mlhp.writeBasisOutput( basis, postmesh, writer, processors )