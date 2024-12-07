# This file is part of the mlhpbf project. License: See LICENSE
import os, sys

try:
    # mlhp.py script folder
    path = os.path.abspath(os.path.dirname(sys.argv[0]))

    # Try to open path/mlhpPythonPath containing the python module path. This
    # file is written as post build command after compiling pymlhpcore.
    with open(os.path.join(path, 'mlhpPythonPath'), 'r') as f:
        sys.path.append(os.path.normpath(f.read().splitlines()[0]))

except IOError:
    pass

from pymlhpbf import *

import mlhp
import math
from dataclasses import dataclass

vtudefault = "RawBinary"


class units:
    mm = 1.0
    m = 1e3 * mm
    cm = 10.0 * mm
    um = 1e-3 * mm
    s = 1.0
    ms = 1e-3 * s
    g = 1.0
    kg = 1e3 * g
    N = 1.0
    kN = 1e3 * N
    J = N * m
    kJ = 1e3 * J
    W = J / s
    kW = 1e3 * W
    C = 1.0
    Pa = N / (m * m)
    MPa = 1e6 * Pa
    GPa = 1e9 * Pa
    Hz = 1.0
    kHz = 1e3 * Hz


def beamShapeFromPixelMatrix(values, pixelsize, npixels=None):
    if isinstance(values, list) or (hasattr(values, "shape") and len(values.shape) == 1):
        if npixels is None:
            raise ValueError("When passing pixel values as list, npixels must be specified")
        data = mlhp.DoubleVector(values)
        shape = npixels
    elif hasattr(values, "shape") and hasattr(values, "ravel"):
        if len(values.shape) != 2:
            raise ValueError("Pixel data dimension too high")
        data = mlhp.DoubleVector(values.ravel())
        shape = values.shape
    else:
        raise ValueError("Pixel data must be passed as list or as 2D numpy array")

    cellsize = [pixelsize] * 2 if isinstance(pixelsize, (float, int)) else list(pixelsize)

    if not isinstance(cellsize, list) or len(cellsize) != 2:
        raise ValueError("pixelsize must be a scalar value or a list of scalar values.")

    lengths = [dx * nx for dx, nx in zip(cellsize, shape)]

    return scalarFieldFromVoxelData(data, shape, lengths, origin=[-l / 2 for l in lengths], outside=0.0)


# Pass single value or interpolate using two lists of temperatures and values.
# extrapolate can be "constant", "linear", or "polynomial".
def temperatureFunction(temperatures=None, values=None, degree=1, extrapolate="constant"):
    if values is None:
        if not isinstance(temperatures, float): raise ValueError("Single value must be of type float.")
        return mlhp.constantInterpolation([0.0], [temperatures])

    extrapolateStr = "default" if extrapolate.lower() == "polynomial" else extrapolate
    if degree == 1:
        return mlhp.linearInterpolation(temperatures, values, extrapolateStr)
    else:
        return mlhp.splineInterpolation(temperatures, values, degree, extrapolateStr)


def makePowder(material, densityScaling=0.5, conductivityScaling=0.08, youngsModulusScaling=1e-4):
    if not isinstance(material, Material):
        raise ValueError(f"Invalid data type for material ({type(material)}).")

    scale = lambda f, factor: temperatureFunction(factor * f(20.0)[0])
    powder = Material()
    powder.initialized = material.initialized
    powder.name = material.name + "Powder"
    powder.density = scale(material.density, densityScaling)
    powder.specificHeatCapacity = scale(material.specificHeatCapacity, 1.0)
    powder.heatConductivity = scale(material.heatConductivity, conductivityScaling)
    powder.plasticModelSelector = 0.0
    powder.solidTemperature = material.solidTemperature
    powder.liquidTemperature = material.liquidTemperature
    powder.latentHeatOfFusion = material.latentHeatOfFusion
    powder.regularization = material.regularization
    powder.thermalExpansionCoefficient = temperatureFunction(0.0)
    powder.youngsModulus = temperatureFunction(youngsModulusScaling)
    powder.poissonRatio = temperatureFunction(0.0)
    powder.yieldStress = temperatureFunction(1e50)
    powder.hardening = temperatureFunction(0.0)
    powder.plasticModelSelector = 0.0

    return powder


def makeAir(epsilon=1e-5, material=makeMaterial("IN625")):
    if not isinstance(epsilon, (int, float, bool)):
        raise ValueError("Invalid data type for epsilon")
    return makePowder(material, epsilon, epsilon, epsilon)


def temperatureBC(faceIndex, temperature):
    def process(thermalProblem, tstate):
        sliced = mlhp.sliceLast(process.function, tstate.time)
        return mlhp.integrateDirichletDofs(sliced, tstate.basis, [process.iface])

    process.function = mlhp.scalarField(4, temperature) if isinstance(temperature, float) else temperature
    process.iface = faceIndex

    return process


def _vtuConfig(degree):
    if degree == 1:
        return [1] * 3, mlhp.PostprocessTopologies.Volumes
    else:
        return [degree + 2] * 3, mlhp.PostprocessTopologies.Volumes | mlhp.PostprocessTopologies.Edges

def thermalVtuOutput(filebase, interval=1, writemode=vtudefault, functions=[]):
    def process(thermalProblem, tstate):
        if tstate.index % process.interval == 0:
            processors = [mlhp.functionProcessor(mlhp.sliceLast(f, tstate.time), "VolumeSource") for i, f in
                          enumerate(thermalProblem.volumeSources)]
            processors += [mlhp.solutionProcessor(3, tstate.dofs, "Temperature")]
            sliceF = lambda f: mlhp.sliceLast(f, tstate.time) if isinstance(f, mlhp.ScalarFunction4D) else f
            processors += [mlhp.functionProcessor(sliceF(f), name) for f, name in functions]
            fileindex = tstate.index // process.interval
            postmesh = mlhp.gridOnCells(*_vtuConfig(thermalProblem.degree))
            writer = mlhp.PVtuOutput(filename=process.path + "_thermal_" + str(fileindex), writemode=writemode)
            mlhp.writeBasisOutput(tstate.basis, postmesh, writer, processors)

    process.path = filebase
    process.interval = interval

    return process


def materialVtuOutput(filebase, interval=1, writemode=vtudefault):
    def process(thermalProblem, tstate):
        if tstate.index % process.interval == 0:
            processors = [mlhp.cellDataProcessor(3, tstate.history.data(), "MaterialState")]
            postmesh = mlhp.gridOnCells([1] * 3, mlhp.PostprocessTopologies.Volumes)
            writer = mlhp.PVtuOutput(filename=process.path + "_material_" + str(tstate.index // process.interval),
                writemode=writemode)
            mlhp.writeMeshOutput(tstate.history.grid(), postmesh, writer, processors)

    process.path = filebase
    process.interval = interval

    return process


def thermalEvaluator(state):
    return mlhp.scalarEvaluator(state.basis, state.dofs)


def meltingTemperature(materials, phi=0.5):
    if "structure" not in materials:
        raise ValueError("Structure material is not present.")
    return (1.0 - phi) * materials["structure"].solidTemperature + phi * materials["structure"].liquidTemperature
    

def meltPoolContourOutput(output, interval=1, resolution=None, writemode=vtudefault, recoverMeshBoundaries=False):
    def process(thermalProblem, tstate):
        if tstate.index % process.interval == 0:
            threshold = meltingTemperature(thermalProblem.simulation.materials, 0.5)
            function = mlhp.implicitThreshold(thermalEvaluator(tstate), threshold)
            postmesh = mlhp.marchingCubesBoundary(function, recoverMeshBoundaries=recoverMeshBoundaries,
                resolution=mlhp.degreeOffsetResolution(tstate.basis, offset=2) if resolution is None else resolution)
            writer = mlhp.DataAccumulator()
            if isinstance(process.output, str):
                writer = mlhp.PVtuOutput(filename=process.output + "_meltpool_" + str(tstate.index // process.interval),
                    writemode=writemode)
            mlhp.writeMeshOutput(tstate.mesh, postmesh, writer, [])
            if not isinstance(process.output, str):
                process.output(writer.mesh())

    process.output = output
    process.interval = interval

    return process


def meltPoolBoundsPrinter(interval=1, resolution=None):
    def meltPoolBoundsCallback(mesh):
        points = mesh.points()
        bounds = [[1e50, 1e50, 1e50], [-1e50, -1e50, -1e50]]
        for ipoint in range(int(len(points) / 3)):
            for icoord in range(3):
                bounds[0][icoord] = min(bounds[0][icoord], points[3 * ipoint + icoord])
                bounds[1][icoord] = max(bounds[1][icoord], points[3 * ipoint + icoord])
        print(f"    melt pool bounds: {[max(u - l, 0.0) for l, u in zip(*bounds)]}", flush=True)

    return meltPoolContourOutput(meltPoolBoundsCallback, interval, resolution)


def createMesh(min, max, elementSize, layerThickness=0.0, zfactor=1.0):
    return mlhp.makeGrid(createMeshTicks(min, max, elementSize, layerThickness, zfactor))


def laserRefinement(laserTrack, laserSigma, laserSpeed, depth):
    def refinement(problem, state0, state1):
        refinementPoints = [# delay, sigma (refinement width), depth (maximum refinement depth), zfactor
            LaserRefinementPoint(0.00 * units.ms, 4 * laserSigma + 0.01 * units.mm, depth + 0.4, 0.5),
            LaserRefinementPoint(0.60 * units.ms, 4 * laserSigma + 0.07 * units.mm, depth - 0.5, 0.5),
            LaserRefinementPoint(6.00 * units.ms, 4 * laserSigma + 0.40 * units.mm, depth - 1.5, 0.8),
            LaserRefinementPoint(30.0 * units.ms, 4 * laserSigma + 0.90 * units.mm, depth - 2.5, 1.0),
            LaserRefinementPoint(0.10 * units.s, 4 * laserSigma + 1.10 * units.mm, depth - 3.0, 1.0)]
        return laserTrackPointRefinement(laserTrack, refinementPoints, state1.time, mlhp.maxdegree(state0.basis) + 2)

    refinement.laserTrack = laserTrack
    refinement.laserSigma = laserSigma
    refinement.laserSpeed = laserSpeed
    refinement.depth = depth
    return refinement


class ProcessSimulation:
    def __init__(self, grid, material=None, layerThickness=0.0, ambientTemperature=25.0 * units.C):
        self.materials = { }
        if material is not None:
            self.materials["air"] = makeAir(material=material)
            self.materials["powder"] = makePowder(material)
            self.materials["baseplate"] = material
            self.materials["structure"] = material
        self.bbox = grid.boundingBox()
        self.lengths = [self.bbox[1][0] - self.bbox[0][0], 
                        self.bbox[1][1] - self.bbox[0][1], 
                        self.bbox[1][2] - self.bbox[0][2]]
        self.origin = self.bbox[0]
        self.layerThickness = layerThickness
        self.ambientTemperature = ambientTemperature

    def setMaterials(self, **kwargs):
        for key, value in kwargs.items():
            if key != "air" and key != "powder" and key != "baseplate" and key != "structure":
                raise ValueError("Invalid material \"{key}\".")
            self.materials[key] = value


class ThermalProblem:
    def __init__(self, simulation, degree=1, theta=1):
        self.dirichlet = []
        self.thermalBoundary = False
        self.postprocess = []
        self.degree = degree
        self.simulation = simulation
        self.theta = theta
        self.volumeSources = []
        self.surfaceSources = []
        self.refinements = []
        self.nfields = 1
        self.emissivity = []
        self.convectionCoefficient = []

    def addPostprocessor(self, postprocessor):
        self.postprocess.append(postprocessor)

    def addDirichletBC(self, condition):
        self.dirichlet.append(condition)

    def setConvectionRadiationBC(self, 
                                 emissivity=0.1, 
                                 convectionCoefficient=1e-5 * units.W / units.mm ** 2 / units.C, 
                                 surfaceHeight=0.0):
        self.thermalBoundary = True
        self.emissivity = emissivity
        self.convectionCoefficient = convectionCoefficient
        origin = self.simulation.origin
        lengths = self.simulation.lengths
        ztop = surfaceHeight

        # Create triangulation with two triangles on the powder layer upper surface
        vertices = [[origin[0], origin[1], ztop], [origin[0], origin[1] + lengths[1], ztop],
                    [origin[0] + lengths[0], origin[1], ztop], [origin[0] + lengths[0], origin[1] + lengths[1], ztop]]
        triangles = [[0, 1, 2], [1, 3, 2]]
        self._topSurface = mlhp.Triangulation(vertices, triangles)

    def addSource(self, source):
        if source[0] == "VolumeSource":
            self.volumeSources.append(source[1])
        elif source[0] == "SurfaceSource":
            self.surfaceSources.append(source[1])
        else:
            raise ValueError("Unknown source type")

    def clearSources(self):
        self.volumeSources.clear()
        self.surfaceSources.clear()

    def addRefinement(self, refinement):
        self.refinements.append(refinement)

    def clearRefinements(self):
        self.refinements = []


@dataclass
class State:
    time: float
    index: int
    mesh: None
    basis: None
    dofs: None
    history: None


def makeThermalState(thermalProblem, mesh, part=None, srefinement=0, powderHeight=0.0, time=0.0, index=0):
    if part is None:
        domain = mlhp.implicitHalfspace([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
    elif isinstance(part, (float, int)):
        domain = mlhp.implicitHalfspace([0.0, 0.0, part], [0.0, 0.0, 1.0])
    elif isinstance(part, mlhp.ImplicitFunction3D):
        domain = part
    else:
        raise ValueError("Invalid data type for part.")

    history = initializeThermalHistory(mesh, domain, srefinement, powderHeight, nseedpoints=4)
    refinedMesh = mlhp.makeRefinedGrid(mesh)
    basis = mlhp.makeHpTrunkSpace(refinedMesh, thermalProblem.degree, nfields=thermalProblem.nfields)
    dofs = mlhp.projectOnto(basis, mlhp.scalarField(3, thermalProblem.simulation.ambientTemperature))
    state = State(time, index, refinedMesh, basis, dofs, history)
    dirichletDofs = mlhp.combineDirichletDofs([f(thermalProblem, state) for f in thermalProblem.dirichlet])
    state.dofs = mlhp.inflateDofs(mlhp.split(state.dofs, dirichletDofs[0])[1], dirichletDofs)
    return state


def _makeSurfaceSourceIntegrator(thermalProblem: ThermalProblem):
    def integrateRhs(tstate: State, K: mlhp.AbsSparseMatrix, F: mlhp.DoubleVector, dirichletDofs):
        if len(thermalProblem.surfaceSources):
            surfaceSource = mlhp.sliceLast(combineSources(thermalProblem.surfaceSources), tstate.time)
            topQuadrature = mlhp.quadratureOnMeshFaces(tstate.mesh, [5], thermalProblem.degree + 3)
            topIntegrand = mlhp.neumannIntegrand(surfaceSource)

            mlhp.integrateOnSurface(tstate.basis, topIntegrand, [F], topQuadrature, dirichletDofs=dirichletDofs)

    return integrateRhs


def _makeConvectionRadiationIntegrator(thermalProblem: ThermalProblem, mesh: mlhp.AbsMesh3D):
    if thermalProblem.thermalBoundary:
        intersected, celldata = mlhp.intersectTriangulationWithMesh(mesh, thermalProblem._topSurface)
        powderLayerQuadrature = mlhp.triangulationQuadrature(intersected, celldata, thermalProblem.degree + 1)
        
        def integrateOnLayerSurface(tstate: State, K: mlhp.AbsSparseMatrix, F: mlhp.DoubleVector, dirichletDofs):
            convectionRadiationIntegrand = makeConvectionRadiationIntegrand(tstate.dofs, thermalProblem.emissivity,
                thermalProblem.convectionCoefficient, thermalProblem.simulation.ambientTemperature)
                
            mlhp.integrateOnSurface(tstate.basis, convectionRadiationIntegrand, [K, F], powderLayerQuadrature,
                dirichletDofs=dirichletDofs)
                
        return integrateOnLayerSurface
        
    else:
        return lambda *args: None

def thermalTimeStep(thermalProblem, tstate0, deltaT, maxiter=40):
    tstate1 = State(time=tstate0.time + deltaT, index=tstate0.index + 1, mesh=mlhp.makeRefinedGrid(
        tstate0.mesh.baseGrid()), basis=None, dofs=None, history=tstate0.history)

    if len(thermalProblem.refinements):
        refinements = [r(thermalProblem, tstate0, tstate1) for r in thermalProblem.refinements]
        tstate1.mesh.refine(mlhp.refinementOr(refinements))

    tstate1.basis = mlhp.makeHpTrunkSpace(tstate1.mesh, thermalProblem.degree)

    print(f"    Thermal problem: {tstate1.basis.nelements()} elements, {tstate1.basis.ndof()}"
          f" dofs, {tstate0.history.grid().ncells()} material cells", flush=True)

    # Gather dirichlet dofs
    dirichletDofs = mlhp.combineDirichletDofs([f(thermalProblem, tstate1) for f in thermalProblem.dirichlet])

    # Project solution from previous state
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate1.basis)
    F = mlhp.allocateVectorWithSameSize(K)

    l2Integrand = mlhp.l2BasisProjectionIntegrand(3, tstate0.dofs)

    mlhp.integrateOnDomain(tstate0.basis, tstate1.basis, l2Integrand, [K, F])

    projectedDofs0 = mlhp.makeCGSolver(1e-12)(K, F)
    tstate1.dofs = projectedDofs0

    del K, F

    return solveNonlinearThermalProblem(thermalProblem, tstate0, tstate1, projectedDofs0, dirichletDofs, maxiter)


def addNewPowderLayer(thermalProblem, tstate0, deltaT, supportPartHeight=0.0, ilayer=0, nseedpoints=4):
    history1 = initializeNewLayerHistory(history=tstate0.history, layerThickness=thermalProblem.simulation.layerThickness,
            supportHeight=supportPartHeight, layer=ilayer, nseedpoints=nseedpoints)
            
    tstate1 = State(time=tstate0.time + deltaT, index=tstate0.index, mesh=mlhp.makeRefinedGrid(
        tstate0.mesh.baseGrid()), basis=None, dofs=None, history=history1)

    if len(thermalProblem.refinements):
        refinements = [r(thermalProblem, tstate0, tstate1) for r in thermalProblem.refinements]
        tstate1.mesh.refine(mlhp.refinementOr(refinements))

    tstate1.basis = mlhp.makeHpTrunkSpace(tstate1.mesh, thermalProblem.degree)

    print(f"    Thermal problem: {tstate1.basis.nelements()} elements, {tstate1.basis.ndof()} dofs", flush=True)

    # Project solution from previous state
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate1.basis)
    F = mlhp.allocateVectorWithSameSize(K)

    projectionIntegrand = makeEnergyConsistentProjectionIntegrand(thermalProblem.simulation.materials, tstate0.history,
        tstate1.history, tstate0.dofs, thermalProblem.simulation.ambientTemperature, deltaT)

    mlhp.integrateOnDomain(tstate0.basis, tstate1.basis, projectionIntegrand, [K, F])

    projectedDofs0 = mlhp.makeCGSolver(1e-12)(K, F)
    tstate1.dofs = projectedDofs0

    return tstate1

def solveNonlinearThermalProblem(thermalProblem, tstate0, tstate1, projectedDofs0, dirichletDofs, maxiter=40):
    
    # Prepare nonlinear iterations
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate1.basis, dirichletDofs[0])
    F = mlhp.allocateVectorWithSameSize(K)
    F0 = mlhp.allocateVectorWithSameSize(K)

    volumeSource = combineSources(thermalProblem.volumeSources)
    integrateSurfaceSource = _makeSurfaceSourceIntegrator(thermalProblem)
    integrateConvectionRadiation = _makeConvectionRadiationIntegrator(thermalProblem, tstate1.mesh)

    projectionIntegrand = makeThermalInitializationIntegrand(thermalProblem.simulation.materials, volumeSource,
        tstate0.history, tstate0.dofs, tstate0.time, tstate1.time - tstate0.time, thermalProblem.theta)

    mlhp.integrateOnDomain(tstate0.basis, tstate1.basis, projectionIntegrand, [F0], dirichletDofs=dirichletDofs)

    norm0, convergenceFlag = 0.0, False
    print("    || F || --> ", end="", flush=True)

    # Newton-Raphson iterations
    for i in range(maxiter):
        F = mlhp.copy(F0)
        mlhp.fill(K, 0.0)

        dirichletIncrement = computeDirichletIncrement(dirichletDofs, tstate1.dofs, -1.0)

        domainIntegrand = makeTimeSteppingThermalIntegrand(thermalProblem.simulation.materials, tstate1.history,
            projectedDofs0, tstate1.dofs, tstate1.time - tstate0.time, thermalProblem.theta)

        quadrature = mlhp.meshProjectionQuadrature(tstate1.history.grid(), maxdepth=2)
        orderDeterminor = mlhp.offsetOrderDeterminor(3, 1)

        mlhp.integrateOnDomain(tstate1.basis, domainIntegrand, [K, F], quadrature=quadrature,
            dirichletDofs=dirichletIncrement, orderDeterminor=orderDeterminor)

        integrateSurfaceSource(tstate1, K, F, dirichletIncrement)
        integrateConvectionRadiation(tstate1, K, F, dirichletIncrement)

        norm1 = mlhp.norm(F)
        norm0 = norm1 if i == 0 else norm0

        print(f"{norm1:.2e} ", end="", flush=True)

        dx = mlhp.inflateDofs(mlhp.makeCGSolver(1e-12)(K, F), dirichletIncrement)

        tstate1.dofs = mlhp.add(tstate1.dofs, dx, -1.0)

        if i == 0:
            tstate1.history = updateHistory(tstate0.history, tstate1.basis, tstate1.dofs,
                meltingTemperature(thermalProblem.simulation.materials, phi=0.5), thermalProblem.degree)

        if norm1 / norm0 <= 1e-6 or norm1 < 1e-11:
            convergenceFlag = True
            break
        if (i + 1) % 6 == 0:
            print("\n                ", end="", flush=True)

    tstate1.history = updateHistory(tstate0.history, tstate1.basis, tstate1.dofs,
        meltingTemperature(thermalProblem.simulation.materials, phi=0.5), thermalProblem.degree)

    print("", flush=True)

    return tstate1, convergenceFlag


def computeThermalProblem(thermalProblem, tstate0, deltaT, duration, ilayer=None, maxiter=40):
    nsteps = int(math.ceil(duration / deltaT))
    realDT = duration / nsteps

    for pp in thermalProblem.postprocess:
        pp(thermalProblem, tstate0)

    for i in range(nsteps):
        if ilayer is not None:
            print(f"Layer {ilayer + 1}, ", end="")
        print(f"Time step {i + 1} / {nsteps} ({tstate0.index + 1} in total)", flush=True)
        print(f"    Time: {tstate0.time:.10g} s, time step size: {realDT:.8g} s", flush=True)
        
        istepI, nstepsI, dtI, index0 = 0, 1, realDT, tstate0.index
        
        while istepI < nstepsI:
            tstate1, convergence = thermalTimeStep(thermalProblem, tstate0, dtI, maxiter)
            
            if convergence:
                tstate0, istepI = tstate1, istepI + 1
                
                if istepI % 2 == 0:
                    istepI, nstepsI, dtI = istepI // 2, nstepsI // 2, dtI * 2
                    print(f"    Thermal Newton iterations converged, increasing time step size to {dtI:.6g}")
                    
            else:
                istepI, nstepsI, dtI = istepI * 2, nstepsI * 2, dtI / 2
                print(f"    Thermal Newton iterations did not converge! Reducing time step to {dtI:.6g}")
          
        tstate1.index = index0 + 1
                
        for pp in thermalProblem.postprocess:
            pp(thermalProblem, tstate1)

    return tstate1


def computeSteadyStateThermal(thermalProblem, tstate, laserVelocity):
    print(f"Computing steady-state problem ({tstate.basis.nelements()} elements, {tstate.basis.ndof()} dofs)",
        flush=True)

    # Gather dirichlet dofs
    dirichletDofs = mlhp.combineDirichletDofs([f(thermalProblem, tstate) for f in thermalProblem.dirichlet])

    # Prepare for nonlinear iterations
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate.basis, dirichletDofs[0])
    F = mlhp.allocateVectorWithSameSize(K)
    tstate.dofs = mlhp.DoubleVector(tstate.basis.ndof(), 0.0)

    volumeSource = mlhp.sliceLast(combineSources(thermalProblem.volumeSources), tstate.time)
    integrateSurfaceSource = _makeSurfaceSourceIntegrator(thermalProblem)

    if thermalProblem.thermalBoundary:
        raise Warning("Convection/radiation boundary condition not available for steady state analysis.")

    norm0 = 1.0
    print("    || F || --> ", end="", flush=True)

    for i in range(40):
        mlhp.fill(F, 0.0)
        mlhp.fill(K, 0.0)

        dirichletIncrement = computeDirichletIncrement(dirichletDofs, tstate.dofs, -1.0)

        domainIntegrand = makeSteadyStateThermalIntegrand(thermalProblem.simulation.materials, volumeSource,
                                                          tstate.history,tstate.dofs, laserVelocity)

        quadrature = mlhp.meshProjectionQuadrature(tstate.history.grid())
        orderDeterminor = mlhp.offsetOrderDeterminor(3, 1)

        mlhp.integrateOnDomain(tstate.basis, domainIntegrand, [K, F], quadrature=quadrature,
            dirichletDofs=dirichletIncrement, orderDeterminor=orderDeterminor)

        integrateSurfaceSource(tstate, K, F, dirichletIncrement)

        norm1 = mlhp.norm(F)
        norm0 = norm1 if i == 0 else norm0

        print(f"{norm1:.2e} ", end="", flush=True)

        P = mlhp.additiveSchwarzPreconditioner(K, tstate.basis, dirichletIncrement[0])
        dx = mlhp.bicgstab(K, F, preconditioner=P, maxit=1000, tolerance=1e-12)
        dx = mlhp.inflateDofs(dx, dirichletIncrement)

        tstate.dofs = mlhp.add(tstate.dofs, dx, -1.0)

        if norm1 / norm0 <= 1e-6 or norm1 < 1e-11:
            break
        if (i + 1) % 6 == 0:
            print("\n                ", end="", flush=True)

    print("", flush=True)

    del K, F, dirichletDofs

    for pp in thermalProblem.postprocess:
        pp(thermalProblem, tstate)


def mechanicalVtuOutput(filebase, interval=1, writemode=vtudefault, functions=[]):
    def process(mechanicalProblem, mstate):
        if mstate.index % process.interval == 0:
            processors = []
            # processors = [mlhp.functionProcessor(mlhp.sliceLast(f, mstate.time),
            #    "VolumeSource" + str(i)) for i, f in enumerate(thermalProblem.volumeSources)]
            processors += [mlhp.solutionProcessor(3, mstate.dofs, "Displacement")]
            # processors += [mlhp.strainProcessor()) ] # To be discussed...
            processors += [plasticityProcessor(mstate.history)]
            # sliceF = lambda f : mlhp.sliceLast(f, mstate.time) if isinstance(f, mlhp.ScalarFunction4D) else f
            # processors += [mlhp.functionProcessor(sliceF(f), name) for f, name in functions]
            postmesh = mlhp.gridOnCells(mlhp.degreeOffsetResolution(mstate.basis, offset=2))
            writer = mlhp.PVtuOutput(filename=process.path + "_mechanical_" + str(mstate.index // process.interval),
                writemode=writemode)
            mlhp.writeBasisOutput(mstate.basis, postmesh, writer, processors)

    process.path = filebase
    process.interval = interval

    return process


class MechanicalProblem:
    def __init__(self, processSimulation, degree=1, quadratureOrderOffset=1):
        self.dirichlet = []
        self.degree = degree
        self.postprocess = []
        self.refinements = []
        self.nfields = 3
        self.offsetQuadrature = quadratureOrderOffset
        self.materials = processSimulation.materials

    def addPostprocessor(self, postprocessor):
        self.postprocess.append(postprocessor)

    def addDirichletBC(self, condition):
        self.dirichlet.append(condition)

    def addRefinement(self, refinement):
        self.refinements.append(refinement)


def makeMechanicalState(mechanicalProblem, mesh, part=None, time=0.0, index=0):
    domain = part if part is not None else mlhp.implicitHalfspace([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    refinedMesh = mlhp.makeRefinedGrid(mesh)
    basis = mlhp.makeHpTrunkSpace(refinedMesh, mechanicalProblem.degree, nfields=mechanicalProblem.nfields)
    history = initializeMechanicalHistory(basis, mlhp.maxdegree(basis) + mechanicalProblem.offsetQuadrature)
    dofs = mlhp.projectOnto(basis, mlhp.vectorField(3, [0.0] * 3))
    state = State(index=index, time=time, basis=basis, mesh=refinedMesh, dofs=dofs, history=history)
    dirichletDofs = mlhp.combineDirichletDofs([f(mechanicalProblem, state) for f in mechanicalProblem.dirichlet])
    state.dofs = mlhp.inflateDofs(mlhp.split(state.dofs, dirichletDofs[0])[1], dirichletDofs)
    return state


def mechanicalTimeStep(mechanicalProblem, mstate0, time1, thermalEvaluator):
    if mstate0.time > time1:
        raise ValueError("Previous mechanical time before next thermal time")

    mstate1 = State( time=time1, index=mstate0.index + 1, mesh=mlhp.makeRefinedGrid(mstate0.mesh.baseGrid()),
        basis=None, dofs=None, history=mstate0.history.clone() )

    mstate1.basis = mlhp.makeHpTrunkSpace(mstate1.mesh, degrees=mechanicalProblem.degree,
        nfields=mechanicalProblem.nfields)

    print(f"    mechanical problem: {mstate1.basis.nelements()} elements, {mstate1.basis.ndof()} dofs", flush=True)

    # Gather dirichlet dofs
    dirichletDofs = mlhp.combineDirichletDofs([f(mechanicalProblem, mstate1) for f in mechanicalProblem.dirichlet])

    # Project solution from previous state
    K = mlhp.allocateUnsymmetricSparseMatrix(mstate1.basis)
    F = mlhp.allocateVectorWithSameSize(K)

    l2Integrand = mlhp.l2BasisProjectionIntegrand(3, mstate0.dofs)

    mlhp.integrateOnDomain(mstate0.basis, mstate1.basis, l2Integrand, [K, F])

    solve = mlhp.makeCGSolver(1e-12)
    projectedDofs0 = solve(K, F)
    mstate1.dofs = projectedDofs0

    del K, F

    # Prepare nonlinear iterations
    K = mlhp.allocateUnsymmetricSparseMatrix(mstate1.basis, dirichletDofs[0])
    F = mlhp.allocateVectorWithSameSize(K)

    norm0 = 0.0
    convergenceFlag = False
    print("    || F || --> ", end="", flush=True)

    # Newton-Raphson iterations
    for i in range(20):
        mlhp.fill(K, 0.0)
        mlhp.fill(F, 0.0)

        dirichletIncrement = computeDirichletIncrement(dirichletDofs, mstate1.dofs, -1.0)
        dofIncrement = mlhp.add(mstate1.dofs, projectedDofs0, -1.0)

        kinematics = mlhp.smallStrainKinematics(3)
        material = makeJ2Plasticity(mstate0.history, mstate1.history, thermalEvaluator)

        domainIntegrand = nonlinearStaticDomainIntegrand(kinematics, material, dofIncrement,
            mlhp.vectorField(3, [0.0] * 3))

        orderDeterminor = mlhp.offsetOrderDeterminor(3, mechanicalProblem.offsetQuadrature)

        mlhp.integrateOnDomain(mstate1.basis, domainIntegrand, [K, F], dirichletDofs=dirichletIncrement,
            orderDeterminor=orderDeterminor)

        norm1 = mlhp.norm(F)
        norm0 = norm1 if i == 0 else norm0

        print(f"{norm1:.2e} ", end="", flush=True)

        dx = mlhp.inflateDofs(solve(K, F), dirichletIncrement)

        mstate1.dofs = mlhp.add(mstate1.dofs, dx)

        if norm1 / norm0 <= 1e-6 or norm1 < 1e-11:
            convergenceFlag = True
            break
        if (i + 1) % 6 == 0:
            print("\n                ", end="", flush=True)

    print("", flush=True)

    return mstate1, convergenceFlag


def computeThermomechanicalProblem(thermalProblem, mechanicalProblem, tstate0, mstate0, deltaT, duration):
    nsteps = int(math.ceil(duration / deltaT))

    print(f"Integrating thermomechanical problem:", flush=True)
    print(f"    duration        = {duration}", flush=True)
    print(f"    number of steps = {nsteps}", flush=True)

    for pp in thermalProblem.postprocess:
        pp(thermalProblem, tstate0)
    for pp in mechanicalProblem.postprocess:
        pp(mechanicalProblem, mstate0)

    for istep in range(nsteps):

        realDT = duration / nsteps
        print(f"    Time {tstate0.time} [s], time step size {realDT} [s]", flush=True)

        convergenceThermal = False
        convergenceMechanical = False

        tstate1 = tstate0
        mstate1 = mstate0

        # Both thermal and mechanical problem have to converge in the time step
        while not convergenceThermal or not convergenceMechanical:
            tstate1, convergenceThermal = thermalTimeStep(thermalProblem, tstate0, realDT)

            thermalEvaluator = makeThermalEvaluator(tstate0.basis, tstate1.basis, tstate0.dofs, tstate1.dofs,
                tstate1.history, thermalProblem.simulation.materials, thermalProblem.simulation.ambientTemperature)

            mstate1, convergenceMechanical = mechanicalTimeStep(mechanicalProblem, mstate0, tstate1.time,
                thermalEvaluator)

            if convergenceThermal and convergenceMechanical: break
            realDT = realDT / 2
            print(f"    Solution does not converge. New time step size {realDT} [s]", flush=True)

        for pp in thermalProblem.postprocess:
                pp(thermalProblem, tstate1)

        for pp in mechanicalProblem.postprocess:
                pp(mechanicalProblem, mstate1)

        tstate0 = tstate1
        mstate0 = mstate1

    return tstate0, mstate0

del os, sys, path
from mlhp import *
