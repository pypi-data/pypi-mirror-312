import unittest
import pbf

units = pbf.units


class MultilayerThermalTest(unittest.TestCase):
    def test(self):
        inconel = pbf.makeMaterial("SS316L")

        # process parameters
        laserD4Sigma = 0.100 * units.mm
        laserSpeed = 800.0 * units.mm / units.s
        laserPower = 280.0 * units.W
        layerThickness = 0.050 * units.mm
        powderDepositionTime = 0.001 * units.s
        nlayers = 3
        nLayerTracks = 1

        # domain
        basePlateHeight = 0.15 * units.mm

        domainMin = [0 * units.mm, -0.15 * units.mm, -basePlateHeight]
        domainMax = [1 * units.mm, +0.15 * units.mm, layerThickness * nlayers]

        # scan path
        eps = 2.17e-4 * units.mm
        x0 = 0.01 * units.mm + eps
        x1 = 0.98 * units.mm + eps
        y = 0.0 * units.mm - eps
        
        totalTime = (x1 - x0) * nLayerTracks * nlayers / laserSpeed + powderDepositionTime * nlayers
        layerTime = (x1 - x0) * nLayerTracks / laserSpeed
        singleTrackTime = (x1 - x0) / laserSpeed

        # discretization
        trefinement = 2
        srefinement = 3
        
        elementSize = 0.05  # 0.12 * laserD4Sigma
        grid = pbf.createMesh(domainMin, domainMax, elementSize, layerThickness * nlayers)  # zfactor??
        timestep = 0.5 * laserD4Sigma / laserSpeed  # 0.2 * laserD4Sigma / laserSpeed

        # laser beam shape
        laserBeam = pbf.gaussianBeam(sigma=laserD4Sigma / 4, absorptivity=0.32)

        # setup process simulation
        setup = pbf.ProcessSimulation(grid=grid, material=inconel, layerThickness=50 * units.um, ambientTemperature=50.0)
        setup.setMaterials(air=pbf.makeAir())

        # thermal problem definition
        tsetup = pbf.ThermalProblem(setup, degree=1)
        tsetup.addDirichletBC(pbf.temperatureBC(4, setup.ambientTemperature))
        
        # Save number of elements and number of dofs every time step
        computedNElementsList, computedMaterialNCellsList, computedNDofList = [], [], []

        def meshDataAccumulator(thermalProblem, tstate):
            computedNElementsList.append(tstate.basis.nelements())
            computedNDofList.append(tstate.basis.ndof())
            computedMaterialNCellsList.append(tstate.history.grid().ncells())


        tsetup.addPostprocessor(meshDataAccumulator)
        #tsetup.addPostprocessor(pbf.thermalVtuOutput("outputs/pbftests/multilayer", interval=1))
        #tsetup.addPostprocessor(pbf.materialVtuOutput("outputs/pbftests/multilayer", interval=1))

        tstate0 = pbf.makeThermalState(tsetup, grid, srefinement=srefinement)

        # solve problem
        # initialize moving heat source
        laserTrack = [pbf.LaserPosition(xyz=[x0, y, layerThickness], time=0.0, power=0),
                      pbf.LaserPosition(xyz=[x0, y, layerThickness], time=powderDepositionTime, power=laserPower),
                      pbf.LaserPosition(xyz=[x1, y, layerThickness], time=powderDepositionTime + layerTime,
                                        power=laserPower),
                      pbf.LaserPosition(xyz=[x0, y, 2 * layerThickness], time=powderDepositionTime + layerTime, power=0.0),
                      pbf.LaserPosition(xyz=[x0, y, 2 * layerThickness], time=2 * powderDepositionTime + layerTime,
                                        power=laserPower),
                      pbf.LaserPosition(xyz=[x1, y, 2 * layerThickness],
                                        time=2 * powderDepositionTime + layerTime + layerTime, power=laserPower),
                      pbf.LaserPosition(xyz=[x0, y, 3 * layerThickness], time=2 * powderDepositionTime + 2 *
                                                                                layerTime, power=0.0),
                      pbf.LaserPosition(xyz=[x0, y, 3 * layerThickness], time=3 * powderDepositionTime + 2 *
                                                                                layerTime, power=laserPower),
                      pbf.LaserPosition(xyz=[x1, y, 3 * layerThickness], time=3 * powderDepositionTime + 3 *
                                                                                layerTime, power=laserPower)]

        # define heat source
        heatSource = pbf.volumeSource(laserTrack, laserBeam, depthSigma=0.045 * units.mm)
        tsetup.addSource(heatSource)

        # geometric laser refinement
        refinement = pbf.laserRefinement(laserTrack, laserD4Sigma / 4, laserSpeed, trefinement)
        tsetup.addRefinement(refinement)

        # solve thermal problem
        print(f"Integrating thermal problem:", flush=True)
        print(f"    duration        = {totalTime}", flush=True)

        for pp in tsetup.postprocess:
            pp(tsetup, tstate0)

        for ilayer in range(nlayers):
            maxNewtonIter = 10 if ilayer < 2 else 9
            
            print(f"Layer {ilayer + 1} / {nlayers}", flush=True)

            tstate = pbf.addNewPowderLayer(tsetup, tstate0, deltaT=powderDepositionTime, ilayer=ilayer)
            tstate0 = pbf.computeThermalProblem(tsetup, tstate, timestep, layerTime, ilayer, maxNewtonIter)

        # Check whether results are consistent with previous versions
        expectedNElementsList = [500, 500, 2782, 3454, 4126, 4812, 5414, 5960, 6478, 6968, 7360, 7598, 7773, 7920, 
                                 8116, 8291, 8424, 8571, 8606, 8641, 8424, 7983, 4000, 5456, 5960, 6436, 6940, 7381, 
                                 7766, 8144, 8494, 8746, 8816, 8830, 8816, 8830, 8830, 8816, 8788, 8760, 8760, 8508, 
                                 8060, 4000, 4784, 5064, 5330, 5610, 5841, 6044, 6233, 6408, 6534, 6569, 6576, 6569, 
                                 6576, 6576, 6562, 6548, 6534, 6534, 6408, 6170]
                                 
        expectedMaterialNCellsList = [500, 500, 1088, 1312, 1347, 1585, 1907, 2166, 2306, 2474, 2733, 2971, 3377, 
                                      3643, 3972, 4238, 4504, 4756, 5050, 5323, 5575, 5659, 5659, 6261, 6366, 6436, 
                                      6898, 7052, 7227, 7311, 7451, 7990, 8354, 8578, 8802, 9103, 9299, 9348, 9418, 
                                      9579, 9775, 9908, 9789, 9789, 10475, 10566, 10286, 11070, 11007, 11028, 11588, 
                                      11770, 11721, 11784, 12232, 12295, 12309, 12204, 12617, 12946, 13009, 13079, 
                                      13100, 13303]
                                      
        expectedNDofList = [756, 756, 2813, 3421, 4029, 4653, 5161, 5633, 6089, 6530, 6867, 7051, 7235, 7407, 7646, 
                            7852, 8008, 8238, 8330, 8412, 8310, 7998, 4961, 6309, 6783, 7230, 7704, 8089, 8424, 8765, 
                            9088, 9290, 9283, 9292, 9291, 9302, 9302, 9291, 9269, 9235, 9265, 9091, 8701, 4961, 5691, 
                            5953, 6204, 6466, 6667, 6850, 7021, 7184, 7292, 7298, 7300, 7293, 7300, 7300, 7289, 7275, 
                            7261, 7277, 7187, 6981]

        assert (len(expectedNElementsList) == len(computedNElementsList))
        assert (len(expectedMaterialNCellsList) == len(computedMaterialNCellsList))
        assert (len(expectedNDofList) == len(computedNDofList))

        for expectedNCells, computedNCells in zip(expectedNElementsList, computedNElementsList):
            assert (expectedNCells == computedNCells)
            
        for expectedNCells, computedNCells in zip(expectedMaterialNCellsList, computedMaterialNCellsList):
            assert (expectedNCells == computedNCells)
            
        for expectedNDof, computedNDof in zip(expectedNDofList, computedNDofList):
            assert (expectedNDof == computedNDof)

        temperature = pbf.thermalEvaluator(tstate0)

        self.assertAlmostEqual(temperature([1.0, 0.0, basePlateHeight]), 3721.71785199963, delta=1e-9)
