// This file is part of the mlhpbf project. License: See LICENSE

#include "mlhp/pbf.hpp"
#include "main_test.hpp"

namespace mlhp
{

// Manufactured solution defined later
spatial::VectorFunction<3, 3> elasticSolution ( );
spatial::VectorFunction<3, 3> elasticSource( double E, double nu );
spatial::VectorFunction<3, 6> elasticStress( double E, double nu );
spatial::VectorFunction<3, 3> elasticTraction( double E, double nu, size_t axis, size_t side );

auto compute( size_t degree, RefinementLevel nrefinements, std::string name )
{
    static constexpr size_t D = 3;

    auto material = makeIN625( );

    auto E = 2.3;
    auto nu = 0.3;

    material.youngsModulus = utilities::returnValue( std::array { E, 0.0 } );
    material.poissonRatio = utilities::returnValue( std::array { nu, 0.0 } );
    material.yieldStress = utilities::returnValue( std::array { 1e50, 0.0 } );
    material.thermalExpansionCoefficient = utilities::returnValue( std::array { 0.0, 0.0 } );

    auto nelements = std::array<size_t, D> { 4, 2, 3 };
    auto baseGrid = makeCartesianGrid<3>( nelements, { 5.0, 3.0, 4.0 } );

    auto general = ProblemSetup<D>
    {
        .buildChamber = baseGrid->boundingBox( ),
        .duration = 1.0,
        .air = material,
        .baseGrid = baseGrid
    };

    auto sharedSetup = std::make_shared<ProblemSetup<D>>( std::move( general ) );
       
    auto scaleFunction = [=]( auto&& function )
    {
        return std::function { [=]( std::array<double, 4> xyzt )
        {
            auto scaling = xyzt.back( ) / sharedSetup->duration;

            return scaling * function( array::slice( xyzt, 3 ) );
        } };
    };

    auto solutionComponent = [=]( size_t ifield )
    {
        auto solution = scaleFunction( elasticSolution( ) );

        return std::function { [=](std::array<double, D + 1> xyzt )
        {
            return solution( xyzt )[ifield];
        } };
    };

    auto dirichlet = std::vector<MechanicalDirichletBC<D>>
    {
        makeDisplacementBC<D>( boundary::right, 0, solutionComponent( 0 ) ),
        makeDisplacementBC<D>( boundary::right, 1, solutionComponent( 1 ) ),
        makeDisplacementBC<D>( boundary::right, 2, solutionComponent( 2 ) ),
        makeDisplacementBC<D>( boundary::top, 0, solutionComponent( 0 ) ),
        makeDisplacementBC<D>( boundary::top, 1, solutionComponent( 1 ) ),
        makeDisplacementBC<D>( boundary::top, 2, solutionComponent( 2 ) ),
        makeDisplacementBC<D>( boundary::front, 0, solutionComponent( 0 ) ),
        makeDisplacementBC<D>( boundary::front, 1, solutionComponent( 1 ) ),
        makeDisplacementBC<D>( boundary::front, 2, solutionComponent( 2 ) ),
    };

    auto tractions = std::vector<MechanicalContribution<D>>
    {
        makeTractionBC<D>( boundary::back, scaleFunction( elasticTraction( E, nu, 1, 1 ) ) ),
        makeTractionBC<D>( boundary::bottom, scaleFunction( elasticTraction( E, nu, 2, 0 ) ) ),
    };

    auto mechanical = MechanicalProblem<D>
    {
        .general = sharedSetup,
        .refinement = makeUniformRefinement<D>( nrefinements ),
        .degree = degree,
        .dirichlet = dirichlet,
        .residual = tractions,
        .bodyForce = scaleFunction( elasticSource( E, nu ) ),
    };

    auto norms = std::vector<std::array<double, 3>> { };

    mechanical.postprocess = [&]( const MechanicalProblem<D>& problem,
                                  const MechanicalState<D>& state )
    {
        makeMechanicalPostprocessing<D>( "outputs/mlhpbf_tests/"
            "linearelastic_" + name + "_", 1 )( problem, state );

        auto kinematics = makeSmallStrainKinematics<D>( );
        auto material = makeIsotropicElasticMaterial( spatial::constantFunction<D>( E ), spatial::constantFunction<D>( nu ) );

        auto evaluate = [&]( const BasisFunctionEvaluation<D>& shapes,
                             const LocationMap& locationMap,
                             AlignedDoubleVectors& targets,
                             AlignedDoubleVector&, 
                             double weightDetJ )
        {
            static constexpr size_t ncomponents = 6;

            auto gradient = std::array<double, D * D> { };
            auto strain = std::array<double, ncomponents> { };

            auto stress = std::array<double, 6> { };
            auto elasticStrain = state.history( shapes.elementIndex( ), shapes.rst( ) ).elasticStrain;
            material.evaluate( shapes, elasticStrain, stress, 1 );

            evaluateSolutions( shapes, locationMap, state.dofs, gradient, 1 );

            kinematics.evaluate( shapes, gradient, strain, std::span<double> { } );
        
            targets[0][0] += 0.5 * spatial::dot( strain, stress ) * weightDetJ;
        };

        auto diffOrder = DiffOrders::FirstDerivatives;
        auto types = std::vector { AssemblyType::Scalar };

        auto energyIntegrand = DomainIntegrand<D>( types, diffOrder, evaluate );

        auto computedEnergy = double { 0.0 };

        integrateOnDomain<D>( *state.basis, energyIntegrand, { computedEnergy } );
    
        auto finalEnergy = 10.0 * E * ( 96975178.0 * nu - 64469539.0 ) / 
            ( 21.0 * ( 2.0 * nu * nu + nu - 1.0 ) ) / ( 8000.0 * 8000.0 );
    
        computedEnergy = std::sqrt( computedEnergy );

        auto analyticalEnergy = state.time / sharedSetup->duration * std::sqrt( finalEnergy );
        auto relative = state.time == 0.0 ? 0.0 : std::abs( analyticalEnergy - computedEnergy ) / analyticalEnergy;

        norms.push_back( { computedEnergy, analyticalEnergy, relative } );

        std::cout << std::setprecision(20) << std::fixed<< 
            "\n    Numerical  : " << computedEnergy <<
            "\n    Analytical : " << analyticalEnergy << 
            "\n    Relative   : " << 100.0 * relative << " %" << std::endl;
    };

    auto history0 = initializeHistory<D>( sharedSetup->baseGrid, 0.0 * Units::mm, 0 );

    computeMechanicalProblem( mechanical, std::move( history0 ), 1.0 / 4.0 );

    return norms;
}

TEST_CASE( "linearelastic_highorder_test" )
{
    auto norms = compute( 6, 0, "highorder" );

    for( auto [numeric, analytic, relative] : norms )
    {
        CHECK( relative < 1e-10 );
    }
}

TEST_CASE( "linearelastic_loworder_test" )
{
    auto norms = compute( 1, 0, "loworder" );
}

//! Python sympy script for analytical solution (scale by 1/8000)
/*
 * import sympy
 * 
 * x = sympy.symarray('x', 3)
 * E, nu = sympy.symbols('E nu')
 * 
 * # Manufactured solution
 * u = [x[0] * x[0] * ( x[0] - 8 ) * ( 5 * x[1] * x[2] - 2 * ( x[1] - 4 ) * ( x[2] - 5 ) ),
 *      2 * x[0] * x[0] * x[1] * ( -x[0] + 3 * ( x[0] - 7 ) * ( x[2] - 4 ) ) + 108 * x[2] * ( x[2] - 6 ),
 *      2 * x[0] * x[0] * ( -x[2] * x[2] * ( x[0] - 6 ) * ( x[1] - 4 ) + 75 ) + 57 * x[1] * ( x[1] - 2 )]
 *      
 * # Deformation gradient     
 * du = sympy.Matrix([[sympy.diff(ui, xi) for xi in x] for ui in u])
 * 
 * # Engineering strain in Voigt notation
 * strain = sympy.Matrix([[du[0, 0], 
 *                         du[1, 1], 
 *                         du[2, 2], 
 *                         du[1, 2] + du[2, 1], 
 *                         du[0, 2] + du[2, 0], 
 *                         du[0, 1] + du[1, 0]]]).T
 * 
 * # Material matrix: only mu on lower diagonal due to engineering strain
 * la = nu * E / ((1 + nu)*(1 - 2 * nu))
 * mu = E / (2 * (1 + nu))
 * 
 * C = sympy.Matrix([[2 * mu + la,          la,          la,     0,      0,     0],
 *                   [         la, 2 * mu + la,          la,     0,      0,     0],
 *                   [         la,          la, 2 * mu + la,     0,      0,     0],
 *                   [          0,           0,           0,    mu,      0,     0],
 *                   [          0,           0,           0,     0,     mu,     0],
 *                   [          0,           0,           0,     0,      0,    mu]])
 * 
 * # Material times strain gives stress
 * stress = C @ strain
 * 
 * S = sympy.Matrix([[stress[0], stress[5], stress[4]],
 *                   [stress[5], stress[1], stress[3]],
 *                   [stress[4], stress[3], stress[2]]])
 *      
 * # Divergence of stress gives force vector
 * force = [sympy.diff(S[0, 0], x[0]) + sympy.diff(S[1, 0], x[1]) + sympy.diff(S[2, 0], x[2]),
 *          sympy.diff(S[0, 1], x[0]) + sympy.diff(S[1, 1], x[1]) + sympy.diff(S[2, 1], x[2]),
 *          sympy.diff(S[0, 2], x[0]) + sympy.diff(S[1, 2], x[1]) + sympy.diff(S[2, 2], x[2])]
 * 
 * energy = sympy.integrate(stress[0] * strain[0] + stress[1] * strain[1] + stress[2] * strain[2] + 
 *                          stress[3] * strain[3] + stress[4] * strain[4] + stress[5] * strain[5], 
 *                          (x[0], 0, 5), (x[1], 0, 3), (x[2], 0, 4)) / 2
 * 
 * for i, s in enumerate(stress[:, 0]):
 *     print(f"stress[{i}] = {sympy.simplify(s)}")
 * 
 * for i, f in enumerate(force):
 *     print(f"force[{i}] = {sympy.simplify(-f)}")
 *     
 * print(f"energy = {sympy.simplify(energy)}")
 * 
 */

// Manufactured solution with homogeneous Neumann on left face
spatial::VectorFunction<3, 3> elasticSolution( )
{
    return [=] ( std::array<double, 3> xyz ) noexcept
    {
        auto [x, y, z] = xyz;

        auto u = x * x * ( x - 8 ) * ( 5 * y * z - 2 * ( y - 4 ) * ( z - 5 ) );
        auto v = 2 * x * x * y * ( -x + 3 * ( x - 7 ) * ( z - 4 ) ) + 108 * z * ( z - 6 );
        auto w = 2 * x * x * ( -z * z * ( x - 6 ) * ( y - 4 ) + 75 ) + 57 * y * ( y - 2 );
        
        return std::array { u / 8000.0, v / 8000.0, w / 8000.0 - 1.0 / 4.0 };
    };
}

// Corresponding volume force
spatial::VectorFunction<3, 3> elasticSource( double E, double nu )
{
    return [=]( std::array<double, 3> xyz ) noexcept
    {
        auto [x, y, z] = xyz;

        auto fx = ( 2 * nu * x * ( -2 * x * z * ( y - 4 ) + x * ( 3 * z - 13 ) - 
            2 * x - 4 * z * ( x - 6 ) * ( y - 4 ) + 6 * ( x - 7 ) * ( z - 4 ) ) + 
            x * ( 2 * nu - 1 ) * (-x * ( 3 * z - 13 ) + 2 * x + 6 * z * ( x - 4 ) * 
                ( y - 4 ) - 6 * ( x - 7 ) * ( z - 4 ) ) + 2 * ( 1 - nu ) * ( 3 * x - 8 ) * 
            ( 5 * y * z - 2 * ( y - 4 ) * ( z - 5 ) ) ) / ( ( nu + 1 ) * ( 2 * nu - 1 ) );
        auto fy = ( -72 * nu * x * y * z + 312 * nu * x * y + 168 * nu * y * z - 
            672 * nu * y - 432 * nu - 4 * x * x * x * z + 33 * x * x * z + 30 * x * x + 
            36 * x * y * z - 156 * x * y - 48 * x * z - 160 * x - 84 * y * z + 
            336 * y + 216) / ( 2 * ( 2 * nu * nu + nu - 1 ) );
        auto fz = ( 2 * nu * x * ( 6 * x * ( x - 7 ) + ( 3 * x - 16 ) * ( 3 * y + 8 ) ) - 
            8 * x * x * ( 1 - nu ) * ( x - 6 ) * ( y - 4 ) + ( 2 * nu - 1 ) * ( -6 * x * x * 
                ( x - 7 ) - x * x * ( 3 * y + 8 ) + 8 * x * z * z * ( y - 4 ) - 2 * x * 
                ( x - 8 ) * ( 3 * y + 8 ) + 4 * z * z * ( x - 6 ) * ( y - 4 ) - 414 ) ) / 
            ( 2 * ( nu + 1 ) * ( 2 * nu - 1 ) );
        
        return std::array { E * fx / 8000.0, E * fy / 8000.0, E * fz / 8000.0 };
    };
}

// Corresponding stress tensor
spatial::VectorFunction<3, 6> elasticStress( double E, double nu  )
{
    return [=]( std::array<double, 3> xyz ) noexcept
    {
        auto S = std::array<double, 6> { };
        auto [x, y, z] = xyz;

        S[0] = x * ( 2 * nu * x * ( x + 2 * z * ( x - 6 ) * ( y - 4 ) - 3 * ( x - 7 ) *  
            ( z - 4 ) ) - ( 1 - nu ) * ( 3 * x - 16 ) * ( 5 * y * z - 2 * ( y - 4 ) * 
            ( z - 5 ) ) ) / ( ( nu + 1 ) * ( 2 * nu - 1 ) );
        S[1] = x * ( nu * ( 4 * x * z * ( x - 6 ) * ( y - 4 ) - ( 3 * x - 16 ) * 
            ( 5 * y * z - 2 * ( y - 4 ) * ( z - 5 ) ) ) + 2 * x * ( 1 - nu ) * 
            ( x - 3 * ( x - 7 ) * ( z - 4 ) ) ) / ( ( nu + 1 ) * ( 2 * nu - 1 ) );
        S[2] = x * ( nu * (2 * x * ( x - 3 * ( x - 7 ) * ( z - 4 ) ) - ( 3 * x - 16 ) * 
            ( 5 * y * z - 2 * ( y - 4 ) * ( z - 5 ) ) ) + 4 * x * z * ( 1 - nu ) * 
            ( x - 6 ) * ( y - 4 ) ) / ( ( nu + 1 ) * ( 2 * nu - 1 ) );
        S[3] = ( 3 * x * x * y * ( x - 7 ) + x * x * z * z * ( 6 - x ) + 57 * y + 
            108 * z - 381 ) / ( nu + 1 );
        S[4] = -x * ( 2 * x * z * z * ( y - 4 ) - x * ( x - 8 ) * ( 3 * y + 8 ) + 
            4 * z * z * ( x - 6 ) * ( y - 4 ) - 300 ) / ( 2 * nu + 2 );
        S[5] = x * ( 2 * x * y * ( 3 * z - 13 ) + x * ( x - 8 ) * ( 3 * z + 10 ) - 
            4 * y * ( x - 3 * ( x - 7 ) * ( z - 4 ) ) ) / ( 2 * ( nu + 1 ) );

        auto transform = [=]( auto value ) { return E * value / 8000.0; };

        std::transform( S.begin( ), S.end( ), S.begin( ), transform );

        return S;
    };
}

spatial::VectorFunction<3, 3> elasticTraction( double E, double nu, size_t axis, size_t side )
{
    auto stress = elasticStress( E, nu );

    return [=]( std::array<double, 3> xyz ) noexcept
    {
        auto S = stress( xyz );
        auto normal = array::makeAndSet<double, 3>( 0.0, axis, side ? 1.0 : -1.0 );

        auto stressTensor = std::array { S[0], S[5], S[4], 
                                         S[5], S[1], S[3],
                                         S[4], S[3], S[2] };

        return linalg::mvproduct<3, 3>( stressTensor, normal );
    };
}

} // namespace mlhp
