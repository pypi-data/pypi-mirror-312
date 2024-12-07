// This file is part of the mlhpbf project. License: See LICENSE

#include "mlhp/pbf.hpp"

namespace mlhp
{

struct Compute : Units
{
    static void compute( )
    {
        static constexpr size_t D = 3;

        auto laserSpeed = 800.0 * mm / s;
        auto laserD4Sigma = 170.0 * um;
        auto laserPower = 178.0 * W;
        auto laserAbsorptivity = 0.45;
        auto laserDepthScaling = 45.0 * um;

        // z = 0 is the base plate
        auto layerHeight = 40 * um; // 32 * um;

        auto buildChamber = std::array { std::array { 0.0 * mm, -0.3 * mm, -0.2 * mm },
                                         std::array { 1.0 * mm,  0.3 * mm, layerHeight } };

        auto x0 = 0.25 * mm;
        auto x1 = 0.75 * mm;
        auto lt1 = ( x1 - x0 ) / laserSpeed;

        // NIST example
        auto laserTrack = std::vector
        {
            laser::Point<3> { .xyz = { x0, 0.0, layerHeight }, .time = 0.0, .power = laserPower },
            laser::Point<3> { .xyz = { x1, 0.0, layerHeight }, .time = lt1, .power = laserPower },
            //laser::Point<3> {.xyz = { 0.0, 0.0, layerHeight }, .time = 100 * ms, .power = 0.0 },
        };

        // Discretization
        auto trefinement = size_t { 0 };
        auto mrefinement = size_t { 0 };
        auto hrefinement = size_t { 0 };

        auto telementsize =  0.12 * laserD4Sigma; // 20 * um;
        auto timestep = 0.2 * laserD4Sigma / laserSpeed;
        auto rootElements = telementsize * utilities::binaryPow<size_t>( trefinement );

        // Create base mesh ticks and reduce top layer element height
        auto baseMeshTicks = createBaseMeshTicks<D>( buildChamber, rootElements, layerHeight);

        auto general = ProblemSetup<D>
        {
            .buildChamber = buildChamber,
            .duration = laserTrack.back( ).time,
            .baseplate = makeIN625( ),
            .structure = makeIN625( ),
            .powder = makePowder( makeIN625( ) ),
            .baseGrid = std::make_shared<CartesianGrid<D>>( std::move( baseMeshTicks ) ),
        };

        auto sharedSetup = std::make_shared<ProblemSetup<D>>( std::move( general ) );
        auto beamShape = laser::gaussianBeamShape<D>( laserD4Sigma / 4.0, laserAbsorptivity );

        auto thermal = ThermalProblem<D>
        {
            .general = sharedSetup,
            .ambientTemperature = 25.0 * C,
            .refinement = makeUniformRefinement<D>( 1 ),
            .degree = 1,
            .timeStep = timestep,
            .source = laser::volumeSource<D>( laserTrack, beamShape, laserDepthScaling ),
            .dirichlet = { makeTemperatureBC<D>( boundary::bottom, 25.0 * C ) },
            .postprocess = makeThermalPostprocessing<D>( "outputs/single_track_", 1 )//8 )
        };

        auto ux = makeDisplacementBC<D>( boundary::bottom, 0 );
        auto uy = makeDisplacementBC<D>( boundary::bottom, 1 );
        auto uz = makeDisplacementBC<D>( boundary::bottom, 2 );

        auto mechanical = MechanicalProblem<D>
        {
            .general = sharedSetup,
            .refinement = makeUniformRefinement<D>( 0 ),
            .degree = 2,
            .dirichlet = { ux, uy, uz },
            .postprocess = makeMechanicalPostprocessing<D>( "outputs/single_track_", 1 )//8 ) 
        };

        auto history0 = initializeHistory<D>( sharedSetup->baseGrid, layerHeight, hrefinement );

        //computeThermalProblem( thermal, std::move( history0 ) );
        computeThermomechanicalProblem( thermal, mechanical, std::move( history0 ) );
    }
};

} // namespace mlhp

int main( int argn, char** argv )
{
    mlhp::Compute::compute( );
}
