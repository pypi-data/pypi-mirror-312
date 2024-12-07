# This file is part of the mlhpbf project. License: See LICENSE

import unittest, pbf

units = pbf.units


class MeltingBarTest(unittest.TestCase):
    def test(self):
        # Material setup
        material = pbf.Material()
        material.density = pbf.temperatureFunction(4510 * units.kg / units.m ** 3)
        material.specificHeatCapacity = pbf.temperatureFunction(520 * units.J / units.kg)
        material.heatConductivity = pbf.temperatureFunction(16 * units.W / units.m)
        material.solidTemperature = 1670 * units.C - 1 * units.C
        material.liquidTemperature = 1670 * units.C + 1 * units.C
        material.latentHeatOfFusion = 325e3 * units.J / units.kg

        # Analytical solution
        Ts, Tl, Tm = 1500 * units.C, 2000 * units.C, 1670 * units.C
        lmbda = 0.388150542167233
        alpha = 6.8224e-06 * units.m ** 2 / units.s

        front = f"2 * {lmbda} * sqrt({alpha} * x[3])"
        left = f"{Tl} - ({Tl} - {Tm}) * erf (x / sqrt(4 * {alpha} * x[3])) / erf ({lmbda})"
        right = f"{Ts} + ({Tm} - {Ts}) * erfc(x / sqrt(4 * {alpha} * x[3])) / erfc({lmbda})"
        solution = pbf.scalarField(ndim=4, func=f"{left} if x < {front} else {right}")

        # Problem setup
        lengths = [100.0 * units.mm, 10.0 * units.mm, 10.0 * units.mm]
        grid = pbf.makeGrid([160, 1, 1], lengths)

        setup = pbf.ProcessSimulation(grid, material=material)
        setup.ambientTemperature = Ts

        tsetup = pbf.ThermalProblem(setup)
        tsetup.degree = 3
        tsetup.addDirichletBC(pbf.temperatureBC(0, Tl))
        tsetup.addDirichletBC(pbf.temperatureBC(1, solution))
        tsetup.addPostprocessor(
            pbf.thermalVtuOutput("outputs/pbftests/meltingbar", functions=[(solution, "Analytical")]))

        # Solution
        tstate0 = pbf.makeThermalState(tsetup, grid)
        tstate1 = pbf.computeThermalProblem(tsetup, tstate0, deltaT=1.0 * units.s, duration=100 * units.s)

        # Compare result to analytical solution
        evaluator = pbf.thermalEvaluator(tstate1)

        for i in range(100):
            xyz = [i * units.mm, 5.0 * units.mm, 5.0 * units.mm]

            assert abs(evaluator(xyz) - solution(xyz + [tstate1.time])) < 1.0490990024 + 1e-6
