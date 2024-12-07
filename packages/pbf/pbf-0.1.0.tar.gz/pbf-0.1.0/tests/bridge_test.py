import unittest, math, pbf
from functools import reduce

units = pbf.units

distance = lambda xyz0, xyz1: math.sqrt(reduce(lambda a, b: a + b, [(x1 - x0) ** 2 for x0, x1 in zip(xyz0, xyz1)]))


class BridgeTest(unittest.TestCase):
    def test(self):
        material = pbf.makeMaterial("SS316L")

        # General parameters
        laserD4Sigma = 120 * units.um
        laserSpeed = 1000 * units.mm / units.s
        laserPower = 180 * units.W
        layerThickness = 30 * units.um

        recoaterLevel = 20 * layerThickness
        totalHeight = 30 * layerThickness

        xyz0 = [-0.55 * units.mm, 1.45 * units.mm, recoaterLevel]
        xyz1 = [0.55 * units.mm, 2.55 * units.mm, recoaterLevel]

        dur = distance(xyz0, xyz1) / laserSpeed

        # Set to dur to simulate full benchmark
        simulationTime = 1.7 * dur

        elementSize = 0.12 * laserD4Sigma
        trefinement = 5
        srefinement = 5
        timestep = 0.3 * laserD4Sigma / laserSpeed

        laserTrack = [pbf.LaserPosition(xyz=xyz0, time=0.0, power=laserPower),
                      pbf.LaserPosition(xyz=xyz1, time=dur, power=laserPower)]

        laserBeam = pbf.gaussianBeam(sigma=laserD4Sigma / 4, absorptivity=0.32)
        heatSource = pbf.volumeSource(laserTrack, laserBeam, depthSigma=10 * units.um)

        domainMin = [-2.0 * units.mm, 0.0 * units.mm, -1.0 * units.mm]
        domainMax = [2.0 * units.mm, 4.0 * units.mm, totalHeight]

        # Construct part
        circles = pbf.implicitSubtraction(
            [pbf.implicitSphere([0.0, 0.0], 1 * units.mm), pbf.implicitSphere([0.0, 0.0], 0.55 * units.mm)])

        cylinder = pbf.extrude(circles, 0.0, 2 * units.mm, 0)

        translation = [-(1 / math.sqrt(2)) * units.mm, (1 / math.sqrt(2) + 2) * units.mm, 0 * units.mm]
        transformation = pbf.concatenate([pbf.rotation([0.0, 0.0, 1.0], -0.25 * math.pi), pbf.translation(translation)])

        part = pbf.implicitIntersection([pbf.implicitTransformation(cylinder, transformation),
                                         pbf.implicitHalfspace([0.0, 0.0, recoaterLevel - layerThickness],
                                                               [0.0, 0.0, 1.0])])

        # Setup problem
        filebase = "outputs/pbftests/bridge"
        grid = pbf.createMesh(domainMin, domainMax, elementSize * 2 ** trefinement, layerThickness=layerThickness,
                              zfactor=0.5)

        setup = pbf.ProcessSimulation(grid, material=material)
        setup.setMaterials(air=pbf.makeAir())
        
        tsetup = pbf.ThermalProblem(setup)
        tsetup.addSource(heatSource)

        # Setup custom refinement
        refinementPoints = [pbf.LaserRefinementPoint(0.00 * units.ms, 0.18 * units.mm, 5.4, 0.5),
                            pbf.LaserRefinementPoint(1.20 * units.ms, 0.24 * units.mm, 3.5, 0.5),
                            pbf.LaserRefinementPoint(6.00 * units.ms, 0.40 * units.mm, 2.5, 0.8),
                            pbf.LaserRefinementPoint(30.0 * units.ms, 0.90 * units.mm, 1.5, 1.0),
                            pbf.LaserRefinementPoint(0.10 * units.s, 1.10 * units.mm, 1.0, 1.0)]

        refinement = lambda problem, state0, state1: pbf.laserTrackPointRefinement(laserTrack, refinementPoints,
                                                                                   state1.time,
                                                                                   pbf.maxdegree(state0.basis) + 2)
        refinementFunction = pbf.laserTrackPointRefinementFunction(laserTrack, refinementPoints)

        tsetup.addRefinement(refinement)
        tsetup.addPostprocessor(pbf.materialVtuOutput(filebase, interval=8))
        tsetup.addPostprocessor(
            pbf.thermalVtuOutput(filebase, interval=8, functions=[(refinementFunction, "RefinementLevel")]))

        # Compute melt pool dimensions every other step
        meltPoolBoundsList = []

        def meltPoolBoundsAccumulator(mesh):
            points = mesh.points()
            bounds = [[1e50, 1e50, 1e50], [-1e50, -1e50, -1e50]]
            for ipoint in range(int(len(points) / 3)):
                for icoord in range(3):
                    bounds[0][icoord] = min(bounds[0][icoord], points[3 * ipoint + icoord])
                    bounds[1][icoord] = max(bounds[1][icoord], points[3 * ipoint + icoord])
            meltPoolBoundsList.append([max(u - l, 0.0) for l, u in zip(*bounds)])

        tsetup.addPostprocessor(pbf.meltPoolContourOutput(meltPoolBoundsAccumulator, interval=2))

        # Save number of elements and number of dofs every time step
        computedNElementsList, computedMaterialNCellsList, computedNDofList = [], [], []

        def meshDataAccumulator(thermalProblem, tstate):
            computedNElementsList.append(tstate.basis.nelements())
            computedNDofList.append(tstate.basis.ndof())
            computedMaterialNCellsList.append(tstate.history.grid().ncells())

        tsetup.addPostprocessor(meshDataAccumulator)

        # Setup initial state and compute problem
        tstate0 = pbf.makeThermalState(tsetup, grid, powderHeight=recoaterLevel, srefinement=srefinement, part=part)
        tstate1 = pbf.computeThermalProblem(tsetup, tstate0, timestep, simulationTime)

        # Check whether results are consistent with previous versions
        expectedNElementsList = [512, 5370, 5748, 6406, 7036, 7414, 8170, 8408, 8912, 9416, 9598, 10151, 10389, 10683,
                                 11033, 11061, 11313, 11383, 11635, 11789, 11901, 12041, 12111, 12321, 12531, 12643,
                                 12755, 12839, 12825, 12979, 13147, 13126, 13238, 13280, 13266, 13476, 13378, 13462,
                                 13672, 13476, 13714, 13700, 13644, 13854, 13504, 12902, 12272, 11656, 11124, 10354,
                                 9948, 9290, 8842, 8436, 7708, 7414, 6826, 6490, 6196, 5706, 5594, 5356, 5244, 5076,
                                 4866, 4838, 4628, 4628, 4460, 4334, 4306, 4110, 4054, 3984, 3802]

        expectedMaterialNCellsList = [187524, 111735, 111805, 111854, 111882, 111889, 111959, 112029, 112078, 112106,
                                      112113, 112183, 112253, 112302, 112330, 112393, 112407, 112456, 112526, 112554,
                                      112610, 112631, 112666, 112778, 112792, 112848, 112855, 112897, 113002, 113030,
                                      113072, 113079, 113121, 113226, 113240, 113296, 113317, 113345, 113436, 113464,
                                      113520, 113548, 113569, 113632, 113632, 113632, 113632, 113632, 113632, 113632,
                                      113632, 113632, 113632, 113632, 113632, 113632, 113632, 113632, 113632, 113632,
                                      113632, 113632, 113632, 113632, 113632, 113632, 113632, 113632, 113632, 113632,
                                      113632, 113632, 113632, 113632, 113632]

        expectedNDofList = [729, 4447, 4789, 5325, 5857, 6172, 6794, 6983, 7385, 7794, 7939, 8375, 8558, 8777, 9078,
                            9109, 9304, 9362, 9545, 9684, 9797, 9885, 9943, 10062, 10260, 10363, 10433, 10507, 10449,
                            10584, 10713, 10687, 10796, 10801, 10817, 10975, 10912, 10969, 11117, 10966, 11152, 11144,
                            11104, 11237, 10956, 10455, 9919, 9388, 8932, 8299, 7957, 7419, 7050, 6702, 6121, 5866,
                            5404, 5141, 4909, 4542, 4460, 4271, 4189, 4052, 3894, 3866, 3699, 3695, 3564, 3466, 3441,
                            3294, 3250, 3195, 3069]

        assert (len(expectedNElementsList) == len(computedNElementsList))
        assert (len(expectedMaterialNCellsList) == len(computedMaterialNCellsList))
        assert (len(expectedNDofList) == len(computedNDofList))

        for expectedNCells, computedNCells in zip(expectedNElementsList, computedNElementsList):
            assert (expectedNCells == computedNCells)
        for expectedNCells, computedNCells in zip(expectedMaterialNCellsList, computedMaterialNCellsList):
            assert (expectedNCells == computedNCells)
        for expectedNDof, computedNDof in zip(expectedNDofList, computedNDofList):
            assert (expectedNDof == computedNDof)

        # for lst in meltPoolBoundsList:
        #    print(f"[{lst[0]:.20f}, {lst[1]:.20f}, {lst[2]:.20f}],")

        expectedBoundsList = [[0.0, 0.0, 0.0], [0.10977172851562500000, 0.10977172851562500000, 0.03600585937500000444],
                              [0.15490722656250000000, 0.15490722656250000000, 0.04766601562500005773],
                              [0.19589233398437500000, 0.19589233398437500000, 0.05170898437499993339],
                              [0.22308349609375000000, 0.22308349609375000000, 0.05257324218749992450],
                              [0.24993896484375000000, 0.24993896484375000000, 0.05270507812500002665],
                              [0.27029418945312500000, 0.27029418945312500000, 0.05255859375000004885],
                              [0.28088378906250000000, 0.28088378906250000000, 0.05260253906250000888],
                              [0.28656005859375000000, 0.28656005859375000000, 0.05267578124999994227],
                              [0.28463745117187500000, 0.28463745117187500000, 0.05277832031249996003],
                              [0.28564453125000000000, 0.28564453125000000000, 0.05314453124999996003],
                              [0.28881835937500000000, 0.28881835937500000000, 0.05520996093750007994],
                              [0.29080200195312500000, 0.29080200195312500000, 0.05944335937500000444],
                              [0.29571533203125000000, 0.29571533203125000000, 0.06191894531249997335],
                              [0.31460571289062500000, 0.31460571289062500000, 0.06481201171874995115],
                              [0.33789062500000000000, 0.33789062500000000000, 0.06526611328124998224],
                              [0.37185668945312500000, 0.37185668945312500000, 0.05592773437500009326],
                              [0.40444946289062500000, 0.40444946289062500000, 0.05252929687499996447],
                              [0.42950439453125000000, 0.42950439453125000000, 0.05252929687499996447],
                              [0.46141052246093750000, 0.46141052246093750000, 0.05257324218749992450],
                              [0.29040527343750000000, 0.29040527343750000000, 0.05264648437499996891],
                              [0.28579711914062500000, 0.28579711914062500000, 0.05266113281249995559],
                              [0.25820922851562500000, 0.25820922851562500000, 0.05188476562499999556],
                              [0.20223999023437500000, 0.20223999023437500000, 0.04338867187500006217],
                              [0.13128662109375000000, 0.13128662109375000000, 0.02444824218750007994],
                              [0.01699829101562500000, 0.01699829101562500000, 0.00077636718750007105], [0.0, 0.0, 0.0],
                              [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                              [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                              [0.0, 0.0, 0.0]]

        assert (len(meltPoolBoundsList) == len(expectedBoundsList))

        for computedBounds, expectedBounds in zip(meltPoolBoundsList, expectedBoundsList):
            for computedAxis, expectedAxis in zip(computedBounds, expectedBounds):
                self.assertAlmostEqual(computedAxis, expectedAxis, delta=1e-6)

        temperature = pbf.thermalEvaluator(tstate1)

        self.assertAlmostEqual(temperature([0.0, 2.0, recoaterLevel]), 730.0893117694662, delta=1e-6)
