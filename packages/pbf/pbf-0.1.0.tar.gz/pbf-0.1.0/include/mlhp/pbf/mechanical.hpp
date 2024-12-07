// This file is part of the mlhpbf project. License: See LICENSE

#ifndef MLHPBF_MECHANICAL_HPP
#define MLHPBF_MECHANICAL_HPP

#include "thermal.hpp"

namespace mlhp
{

template<size_t D> inline
auto makeQuadraturePointIndexFinder( size_t quadratureOrder )
{
    auto points = gaussLegendrePoints( quadratureOrder )[0];
    auto strides = nd::stridesFor( array::make<D>( quadratureOrder ) );

    auto find1D = [=]( double r )
    {
        auto index = utilities::findInterval( points, r );
        auto local = utilities::mapToLocal0( points[index], points[index + 1], r );

        return local < 0.5 ? index : index + 1;
    };

    return [=]( std::array<double, D> rst )
    {
        auto index = size_t { 0 };

        for( size_t axis = 0; axis < D; ++axis )
        {
            index += strides[axis] * find1D( rst[axis] );
        }

        return index;
    };
}

struct PlasticityData
{
    std::array<double, 6> elasticStrain = { };
    std::array<double, 6> backstress = { };
    double effectivePlasticStrain;
};

//template<size_t D, typename HistoryVariables>
//using HistoryAccessor = std::function<HistoryVariables&( CellIndex, std::array<double, D> )>;

template<size_t D, typename Type>
struct HistoryAccessor
{
    void reset( CellIndex nelements, size_t quadratureOrder )
    {
        indexFinder = makeQuadraturePointIndexFinder<D>( quadratureOrder );
        auto generator = [=, n = size_t { 0 }] ( ) mutable { 
            return n = n + utilities::integerPow( quadratureOrder, 3 ); };
        
        std::get<0>( data ).resize( nelements + 1 );
        std::generate( std::get<0>( data ).begin( ), std::get<0>( data ).end( ), generator );
        std::get<1>( data ).resize( std::get<0>( data ).back( ) );

    }

    Type& operator()( CellIndex icell, std::array<double, D> rst )
    {
        return std::get<1>( data )[std::get<0>( data )[icell] + indexFinder( rst )];
    }
    
    const Type& operator()( CellIndex icell, std::array<double, D> rst ) const
    {
        return std::get<1>( data )[std::get<0>( data )[icell] + indexFinder( rst )];
    }

    LinearizedVectors<Type> data;
    std::function<size_t( std::array<double, D> rst )> indexFinder;

};

template<size_t D>
using MechanicalHistory = HistoryAccessor<D, PlasticityData>;

template<size_t D> 
struct MechanicalProblem;

template<size_t D>
struct MechanicalState
{
    size_t index;
    double time;

    std::shared_ptr<MultilevelHpBasis<D>> basis;
    std::shared_ptr<AbsHierarchicalGrid<D>> grid;
    std::vector<double> dofs;
    MechanicalHistory<D> history;
};

template<size_t D>
using MechanicalRefinement = std::function<RefinementFunction<D>( const MechanicalProblem<D>& mechanical,
                                                                  const MechanicalState<D>& state0,
                                                                  const MechanicalState<D>& state1 )>;

template<size_t D>
using MechanicalPostprocessing = std::function<void( const MechanicalProblem<D>& thermal,
                                                     const MechanicalState<D>& state )>;

template<size_t D>
using MechanicalDirichletBC = std::function<DofIndicesValuesPair( const MechanicalState<D>& state )>;

template<size_t D>
using MechanicalContribution = std::function<void( const MechanicalProblem<D>& mechanical,
                                                   const MechanicalState<D>& state0,
                                                   const MechanicalState<D>& state1,
                                                   const std::vector<double>& dofIncrement,
                                                   const DofIndicesValuesPair& dirichletIncrement,
                                                   linalg::UnsymmetricSparseMatrix& jacobian,
                                                   std::vector<double>& residual )>;

template<size_t D>
struct MechanicalProblem
{
    std::shared_ptr<ProblemSetup<D>> general;

    MechanicalRefinement<D> refinement = makeUniformRefinement<D>( 0 );
    size_t degree = 1;

    std::vector<MechanicalDirichletBC<D>> dirichlet = { };
    std::vector<MechanicalContribution<D>> residual = { };
    spatial::VectorFunction<D + 1, D> bodyForce = spatial::constantFunction<D + 1, D>( array::make<D>( 0.0 ) );

    auto initialState( ) const;

    auto step( const MechanicalState<D>& mstate0,
               const ThermalProblem<D>& thermal,
               const ThermalState<D>& tstate0,
               const ThermalState<D>& tstate1 ) const;

    MechanicalPostprocessing<D> postprocess = utilities::doNothing( );

};

template<size_t D>
MechanicalDirichletBC<D> makeDisplacementBC( size_t iface, size_t ifield, 
                                             spatial::ScalarFunction<D + 1> function )
{
    return [=]( const MechanicalState<D>& mstate )
    {
        auto sliced = spatial::sliceLast<D + 1>( function, mstate.time );

        return boundary::boundaryDofs( sliced, *mstate.basis, { iface }, ifield );
    };
}

template<size_t D>
MechanicalDirichletBC<D> makeDisplacementBC( size_t iface, size_t ifield, double value = 0.0 )
{
    return makeDisplacementBC<D>( iface, ifield, spatial::constantFunction<D + 1>( value ) );
}

template<size_t D>
MechanicalContribution<D> makeTractionBC( size_t iface, spatial::VectorFunction<D + 1, D> traction )
{
    return [=]( const MechanicalProblem<D>& mechanical,
                const MechanicalState<D>& /* state0 */,
                const MechanicalState<D>& state1,
                const std::vector<double>& /* dofIncrement */,
                const DofIndicesValuesPair& dirichletIncrement,
                linalg::UnsymmetricSparseMatrix& /* jacobian */,
                std::vector<double>& residual )
    {
        auto integrand = makeNeumannIntegrand<D>( spatial::sliceLast( traction, state1.time ) );
        auto order = mechanical.degree + 1;
        auto quadrature = boundary::QuadratureOnMeshFaces<D> { state1.basis->mesh( ), { iface }, order };

        integrateOnSurface( *state1.basis, integrand, quadrature, { residual }, dirichletIncrement );
    };
}

template<size_t D>
MechanicalContribution<D> makeTractionBC( size_t iface, std::array<double, D> traction )
{
    return makeTractionBC( iface, spatial::constantFunction<D + 1>( traction ) );
}

template<size_t D> inline
auto MechanicalProblem<D>::initialState( ) const
{
    auto state0 = MechanicalState<D> { 0, 0.0 };

    state0.grid = makeRefinedGrid<D>( general->baseGrid );
    state0.grid->refine( refinement( *this, state0, state0 ) );
    state0.basis = makeHpBasis<typename ProblemSetup<D>::AnsatzSpace>( state0.grid, degree, D );
    state0.dofs.resize( state0.basis->ndof( ), 0.0 );
    
    //auto maxdepth = RefinementLevel { 0 };
    //auto data = std::vector<PlasticityData> { };
    auto grid = state0.grid;

    state0.history.reset( grid->ncells( ), degree + 1 );
    //state0.history = MechanicalHistory<D>( grid->ncells( ), degree + 1 );// { grid, maxdepth, std::move( data ) };
   
    return state0;
}

template<size_t D, size_t N>
struct NonlinearMaterial
{
    using Evaluate = std::array<double, N>( const BasisFunctionEvaluation<D>& shapes,
                                            std::array<double, N> totalStrainIncrement,
                                            std::span<double, N * N> tangentStiffness );

    static constexpr size_t ndim = D;
    static constexpr size_t ncomponents = N;
    
    bool symmetric = false;

    std::function<Evaluate> evaluate;
};

template<size_t D>
using ThermalEvaluator = std::function<std::tuple<double, const Material*, double>( std::array<double, D> )>;

template<size_t D>
inline ThermalEvaluator<D> makeThermalEvaluator( const BasisConstSharedPtr<D>& tbasis0,
                                                 const BasisConstSharedPtr<D>& tbasis1,
                                                 const std::vector<double>& tdofs0,
                                                 const std::vector<double>& tdofs1,
                                                 const ThermoplasticHistory<D>& thermalHistory1,
                                                 const MaterialPtrs& materials,
                                                 double ambientTemperature )
{
    auto evaluate0 = basis::makeScalarEvaluator<3>( tbasis0, tdofs0 );
    auto evaluate1 = basis::makeScalarEvaluator<3>( tbasis1, tdofs1 );

    return [evaluate0 = std::move( evaluate0 ), 
            evaluate1 = std::move( evaluate1 ), 
            &thermalHistory1, materials, ambientTemperature]( std::array<double, D> xyz )
    { 
        auto T1 = evaluate1( xyz );
        auto T0 = evaluate0( xyz );

        auto thistory1 = thermalHistory1( xyz );

        MLHP_CHECK( thistory1 != nullptr, "No history found." );

        auto material = materialFor( materials, thistory1->materialType );

        auto exp0 = material->thermalExpansionCoefficient( T0 )[0];
        auto exp1 = material->thermalExpansionCoefficient( T1 )[0];

        if( T0 > T1 && material->thermalExpansionCoefficientCooling != nullptr )
        {
            exp0 = material->thermalExpansionCoefficientCooling( T0 )[0];
            exp1 = material->thermalExpansionCoefficientCooling( T1 )[0];
        }

        auto e0 = ( T0 - ambientTemperature ) * exp0;
        auto e1 = ( T1 - ambientTemperature ) * exp1;

        return std::tuple { T1, material, e0 - e1 };
    };
}

inline auto makeJ2Plasticity( const MechanicalHistory<3>& mhistoryContainer0,
                              MechanicalHistory<3>& mhistoryContainer1,
                              const ThermalEvaluator<3>& evaluator,
                              double meltingTemperature = 1.0e+10 )
{

    auto evaluate = [=, &mhistoryContainer0, &mhistoryContainer1] 
        ( const BasisFunctionEvaluation<3>& shapes,
          std::array<double, 6> totalStrainIncrement,
          std::span<double, 36> tangentStiffness )
    {
        auto [T1, material, thermalStrainIncrement] = evaluator( shapes.xyz( ) );

        // History variables
        auto history0 = &mhistoryContainer0( shapes.elementIndex( ), shapes.rst( ) );
        auto history1 = &mhistoryContainer1( shapes.elementIndex( ), shapes.rst( ) );

        // Thermal strain
        totalStrainIncrement[0] += thermalStrainIncrement;
        totalStrainIncrement[1] += thermalStrainIncrement;
        totalStrainIncrement[2] += thermalStrainIncrement;

        // Linear elastic parameters
        auto nu = material->poissonRatio( T1 )[0];
        auto tmp1 = ( 1.0 - 2.0 * nu );
        auto tmp2 = material->youngsModulus( T1 )[0] / ( ( 1.0 + nu ) * tmp1 );

        auto lambda = nu * tmp2;
        auto mu = 0.5 * tmp1 * tmp2;

        // Elastic tangent stiffness
        auto tangent = std::array<double, 6 * 6> { };
        auto D = linalg::adapter( tangent, 6 );
        auto diagonal = lambda + 2.0 * mu;

        D( 0, 0 ) = diagonal; D( 0, 1 ) = lambda;   D( 0, 2 ) = lambda;
        D( 1, 0 ) = lambda;   D( 1, 1 ) = diagonal; D( 1, 2 ) = lambda;
        D( 2, 0 ) = lambda;   D( 2, 1 ) = lambda;   D( 2, 2 ) = diagonal;
        D( 3, 3 ) = mu; D( 4, 4 ) = mu; D( 5, 5 ) = mu;

        // Trial stress
        auto sigmaTrial = std::array<double, 6> { };
        auto elasticStrainTrial =  totalStrainIncrement;

        if ( T1 < meltingTemperature )  elasticStrainTrial = elasticStrainTrial + history0->elasticStrain;

        linalg::mmproduct( tangent.data( ), elasticStrainTrial.data( ),
            sigmaTrial.data( ), 6, 6, 1 );

        auto sigmaTrialTrace = sigmaTrial[0] + sigmaTrial[1] + sigmaTrial[2];
        auto unitTensor = std::array<double, 6> { 1.0, 1.0, 1.0, 0.0, 0.0, 0.0 };

        // Shifted stress
        auto etaTrial = sigmaTrial - history0->backstress - 1.0 / 3.0 * sigmaTrialTrace * unitTensor;

        auto etaTrialNorm = std::sqrt( etaTrial[0] * etaTrial[0] +
                                       etaTrial[1] * etaTrial[1] + 
                                       etaTrial[2] * etaTrial[2] +
                               2.0 * ( etaTrial[3] * etaTrial[3] + 
                                       etaTrial[4] * etaTrial[4] + 
                                       etaTrial[5] * etaTrial[5] ) );

        // Yield function
        auto sigmaY = material->yieldStress( T1 )[0];
        auto H = material->hardeningParameter( T1 )[0];
        auto beta = material->plasticModelSelector;
        
        auto Hn = H;
        auto ep = history0->effectivePlasticStrain;

        auto f = etaTrialNorm - std::sqrt( 2.0 / 3.0 ) * ( sigmaY + ( 1.0 - beta ) * Hn * ep );
        
        // If elastic
        if( f < 0.0 )
        {
            if( !tangentStiffness.empty( ) )
            {
                std::copy( tangent.begin( ), tangent.end( ), tangentStiffness.begin( ) );
            }

            history1->elasticStrain = elasticStrainTrial;
            history1->backstress = history0->backstress;
            history1->effectivePlasticStrain = history0->effectivePlasticStrain;

            return sigmaTrial;
        }

        // Consistency parameter: flow amount
        auto deltaLambda = f / ( 2.0 * mu + 2.0 / 3.0 * H );

        // Unit deviatoric vector: flow direction
        auto N = etaTrial / etaTrialNorm;

        // Update history variables
        auto sigma = sigmaTrial - 2.0 * mu * deltaLambda * N;

        if ( T1 < meltingTemperature ) history1->elasticStrain = elasticStrainTrial - deltaLambda * N;

        history1->backstress = history0->backstress + ( 2.0 / 3.0 ) * beta * H * deltaLambda * N;
        history1->effectivePlasticStrain = history0->effectivePlasticStrain + std::sqrt( 2.0 / 3.0 ) * deltaLambda;

        // Consistent / algorithmic tangent stiffness
        if( !tangentStiffness.empty( ) )
        {
            // Tangent stiffness
            auto c1 = 4.0 * mu * mu / ( 2.0 * mu + 2.0 / 3.0 * H );

            // Algorithmic contribution 
            auto c2 = 4.0 * mu * mu * deltaLambda / etaTrialNorm;

            auto Dalg = linalg::adapter( tangentStiffness, 6 );

            // Elastic with plastic correction
            for( size_t i = 0; i < 6; i++ )
            {
                for( size_t j = 0; j < 6; j++ )
                {
                    Dalg( i, j ) = D( i, j ) - ( c1 - c2 ) * N[i] * N[j];
                }
            }
            
            // Deviatoric projection
            for( size_t i = 0; i < 3; ++i )
            {
                for( size_t j = 0; j < 3; ++j )
                {
                    Dalg( i, j ) -= -1.0 / 3.0 * c2;
                }
                
                Dalg( i + 0, i + 0 ) -= c2;
                Dalg( i + 3, i + 3 ) -= c2 / 2.0;
            }
        }
        
        return sigma;
    };

    return NonlinearMaterial<3, 6>
    {
        .symmetric = true,
        .evaluate = std::move( evaluate )
    };
}

template<size_t D, size_t N> inline
DomainIntegrand<D> makeNonlinearStaticIntegrand( const Kinematics<D>& kinematics,
                                                 const NonlinearMaterial<D, N>& material,
                                                 const std::vector<double>& dofIncrement,
                                                 const spatial::VectorFunction<D>& force )
{
    using AnyCache = typename DomainIntegrand<D>::Cache;

    struct Cache
    {
        const LocationMap* locationMap;

        memory::AlignedVector<double> tmp;
    };

    // Create cache at beginning of omp parallel
    auto create = []( ) -> AnyCache
    {
        return Cache { };
    };

    // Prepare cache for the given element
    auto prepare = [](  AnyCache& anyCache, 
                       const MeshMapping<D>&, 
                       const LocationMap& locationMap )
    {
        utilities::cast<Cache>( anyCache ).locationMap = &locationMap;
    };

    // Evaluate at Gauss point
    auto evaluate = [=, &material]( AnyCache& anyCache,
                                    const BasisFunctionEvaluation<D>& shapes,
                                    AlignedDoubleVectors& targets, 
                                    double weightDetJ )
    {
        MLHP_CHECK( shapes.nfields( ) == D, "Invalid number of fields in elasticity integrand." );

        auto& cache = utilities::cast<Cache>( anyCache );
        auto& locationMap = *cache.locationMap;
        auto& tmp = cache.tmp;
        
        auto sizes = shapes.sizes( );
        auto ndof = std::get<0>( sizes );
        auto nblocks = std::get<1>( sizes );
        auto ndofpadded = std::get<2>( sizes );
        
        tmp.resize( 2 * N * ndofpadded );       

        std::fill( tmp.begin( ), tmp.end( ), 0.0 );

        auto B = memory::assumeAlignedNoalias( tmp.data( ) );
        auto S = memory::assumeAlignedNoalias( B + N * ndofpadded );
        auto C = std::array<double, N * N> { };

        auto gradientIncrement = std::array<double, D * D> { };
        auto strainIncrement = std::array<double, N> { };
        auto strainOperator = std::span( B, N * ndofpadded );

        evaluateSolutions( shapes, locationMap, dofIncrement, gradientIncrement, 1 );

        // Compute B matrix from shape function evaluation
        kinematics.evaluate( shapes, gradientIncrement, strainIncrement, strainOperator );

        // Compute stress and tangent stiffness
        auto stress = material.evaluate( shapes, strainIncrement, C );

        // Compute S = C * B
        linalg::mmproduct( C.data( ), B, S, N, N, ndofpadded );

        // Compute B^T * S
        linalg::symmetricElementLhs( targets[0].data( ), ndof, nblocks, [=]( size_t i, size_t j )
        {
            double value = 0.0;

            for( size_t axis = 0; axis < N; ++axis )
            {
                value += B[axis * ndofpadded + i] * S[axis * ndofpadded + j];

            } // component

            return value * weightDetJ;
        } );

        auto rhs = targets[1].data( );
        
        // Internal forces
        linalg::elementRhs( rhs, ndof, nblocks, [&]( size_t idof )
        { 
            double value = 0.0;
        
            for( size_t icomponent = 0; icomponent < N; ++icomponent)
            {
                value += B[icomponent * ndofpadded + idof] * stress[icomponent];
            }
            
            return -value * weightDetJ;
        } );
        
        auto forceValues = std::array<double, D> { };
        
        force( shapes.xyz( ), forceValues );

        // External forces
        for( size_t ifield = 0; ifield < 3; ++ifield )
        {
            auto Ni = shapes.noalias( ifield, 0 );
            auto size = shapes.ndof( ifield );

            linalg::elementRhs( rhs, size, shapes.nblocks( ifield ), [=]( size_t j )
            { 
                return Ni[j] * forceValues[ifield] * weightDetJ;
            } );

            rhs += size;
        }
    };

    auto matrixType = material.symmetric ? AssemblyType::SymmetricMatrix : 
                                           AssemblyType::UnsymmetricMatrix;

    auto types = std::vector { matrixType, AssemblyType::Vector };

    return DomainIntegrand<D>( types, DiffOrders::FirstDerivatives, create, prepare, evaluate );
}

template<size_t D> inline
auto MechanicalProblem<D>::step( const MechanicalState<D>& mstate0,
                                 const ThermalProblem<D>& thermal,
                                 const ThermalState<D>& tstate0,
                                 const ThermalState<D>& tstate1 ) const
{
    auto mstate1 = MechanicalState<D> { mstate0.index + 1, tstate1.time };

    mstate1.grid = makeRefinedGrid<D>( general->baseGrid );
    mstate1.grid->refine( refinement( *this, mstate0, mstate1 ) );
    //mstate1.grid->refine( [=]( const AbsMeshMapping<D>& mapping, RefinementLevel cellLevel ) { return cellLevel < 1; } );
    mstate1.basis = makeHpBasis<typename ProblemSetup<D>::AnsatzSpace>( mstate1.grid, degree, D );
    mstate1.history = mstate0.history;

    auto partitioner = StandardQuadrature<D> { };
    auto materialGridPartitioner = MeshProjectionQuadrature<D>( *tstate1.history.grid, partitioner );

    std::cout << "    mechanical problem: " << mstate1.basis->nelements( ) << 
        " elements, " << mstate1.basis->ndof( ) << " dofs" << std::endl;

    auto components = std::vector<DofIndicesValuesPair> { };

    for( auto& condition : dirichlet )
    {
        components.push_back( condition( mstate1 ) );
    }

    auto dirichletDofs = boundary::combine( components );

    auto solve = linalg::makeCGSolver( 1e-12 );

    // Project solution
    {
        auto M = allocateMatrix<linalg::UnsymmetricSparseMatrix>( *mstate1.basis );
        auto d = std::vector<double>( M.size1( ), 0.0 );
        auto l2Integrand = makeL2BasisProjectionIntegrand<D>( mstate0.dofs );

        integrateOnDomain( *mstate0.basis, *mstate1.basis, l2Integrand, { M, d },
                           StandardQuadrature<D>{ }, makeIntegrationOrderDeterminor<D>( 1 ) );

        mstate1.dofs = solve( M, d );
    }
    
    auto materialPtrs = static_cast<MaterialPtrs>( *thermal.general );
    auto evaluator = makeThermalEvaluator<3>( tstate0.basis, tstate1.basis, tstate0.dofs,
        tstate1.dofs, tstate1.history, materialPtrs, thermal.ambientTemperature );

    auto kinematics = makeSmallStrainKinematics<D>( );
    auto material = makeJ2Plasticity( mstate0.history, mstate1.history, evaluator );
   
    auto df = allocateMatrix<linalg::UnsymmetricSparseMatrix>( *mstate1.basis, dirichletDofs.first );
    auto f = std::vector<double>( df.size1( ), 0.0 );

    auto dofs0 = mstate1.dofs;
    auto dirichletIncrement = dirichletDofs;


    auto norm0 = 0.0;
    std::cout << "    || F || --> " << std::flush;

    // Newton-Raphson iterations
    for( size_t i = 0; i < 40; ++i )
    {
        std::fill( df.data( ), df.data( ) + df.nnz( ), 0.0 );
        std::fill( f.begin( ), f.end( ), 0.0 );
                            
        auto dofIncrement = mstate1.dofs;

        for( size_t idof = 0; idof < dirichletDofs.first.size( ); ++idof )
        {
            dirichletIncrement.second[idof] = dirichletDofs.second[idof] - 
                mstate1.dofs[dirichletDofs.first[idof]];
        }    

        for( size_t idof = 0; idof < dofs0.size(); ++idof )
        {
            dofIncrement[idof] -= dofs0[idof];
        }

        for( auto& contribution : residual )
        {
            contribution( *this, mstate0, mstate1, dofIncrement, dirichletIncrement, df, f );
        }

        auto slicedForce = spatial::sliceLast<D + 1>( bodyForce, mstate1.time );
        auto domainIntegrand = makeNonlinearStaticIntegrand<D>( kinematics, material, dofIncrement, slicedForce );
        auto quadrature = makeIntegrationOrderDeterminor<D>( 1 ); // p + 1
                    
        integrateOnDomain<D>( *mstate1.basis, domainIntegrand, { df, f }, dirichletIncrement, quadrature, partitioner );
            
        auto norm1 = std::sqrt( std::inner_product( f.begin( ), f.end( ), f.begin( ), 0.0 ) );

        norm0 = i == 0 ? norm1 : norm0;

        std::cout << std::scientific << std::setprecision( 2 ) << norm1 << " " << std::flush;

        auto dx = boundary::inflate( solve( df, f ), dirichletIncrement );

        std::transform( mstate1.dofs.begin( ), mstate1.dofs.end( ), dx.begin( ), mstate1.dofs.begin( ), std::plus<double> { } );

        if( norm1 / norm0 <= 1e-6 || norm1 < 1e-6 ) break;
        if( ( i + 1 ) % 6 == 0 ) std::cout << "\n                ";
    }

    std::cout << std::endl;

    return mstate1;
}

inline ElementProcessor<3> postprocessPlasticity( const MechanicalHistory<3>& historyAccessor )
{
    auto evaluate = [&historyAccessor]( auto& shapes, auto&, auto&, auto target )
    {
        auto history = historyAccessor( shapes.elementIndex( ), shapes.rst( ) );

        auto [E11, E22, E33, E23, E13, E12] = history.elasticStrain;

        target[0] = E11;
        target[1] = E22;
        target[2] = E33;
        target[3] = E12;
        target[4] = E13;
        target[5] = E23;
        target[6] = history.effectivePlasticStrain;

    };

    auto outputData = []( const AbsBasis<3>& ) -> Output
    {
        return { .name = "ElasticAndPlasticStrain",
                 .type = Output::Type::PointData, 
                 .ncomponents = 7 };
    };

    return detail::makeElementPointProcessor<3>( std::move( 
        evaluate ), std::move( outputData ), DiffOrders::NoShapes );
}

inline ElementProcessor<3> makeStrainProcessor( const std::vector<double>& dofs )
{
    auto evaluate = [=]( auto& shapes, auto&, auto& locationMap, auto strainIncrement )
        {
            auto const D = 3;

            auto gradientIncrement = std::array<double, D * D> { };

            evaluateSolutions( shapes, locationMap, dofs, gradientIncrement, 1 );

            auto kinematics = makeSmallStrainKinematics<3>( );
            kinematics.evaluate( shapes, gradientIncrement, std::span { strainIncrement }, std::span<double> { } );

        };

    auto diff = DiffOrders::FirstDerivatives;

    auto outputData = [=]( auto& ) -> Output
        {
            return { .name = "TotalStrain",
                     .type = Output::Type::PointData,
                     .ncomponents = 6 };
        };

    return detail::makeElementPointProcessor<3>( std::move( evaluate ), std::move( outputData ), diff );
}

template<size_t D> inline
auto makeMechanicalPostprocessing( const std::string& filebase,
                                   size_t vtuinterval )
{
    auto postprocess = [=]( const MechanicalProblem<D>& mechanical,
                            const MechanicalState<D>& state )
    {
        if( state.index % vtuinterval == 0 )
        {
            auto mprocessors = std::tuple
            {
                makeSolutionProcessor<D>( state.dofs, "Displacement" ),
                makeFunctionProcessor<D>( spatial::sliceLast( mechanical.bodyForce, state.time ), "BodyForce"),
                postprocessPlasticity( state.history )
            };

            auto meshProvider = cellmesh::createGrid( array::makeSizes<D>( mechanical.degree ) );
            auto moutput = PVtuOutput { filebase + "mechanical_" + std::to_string( state.index / vtuinterval ) };

            //std::cout << "    Writing mechanical output ... " << std::flush;
            writeOutput( *state.basis, meshProvider, std::move( mprocessors ), moutput );
            //std::cout << "done." << std::endl;
        }
    };

    return MechanicalPostprocessing<D> { std::move( postprocess ) };
}

template<size_t D> inline
auto computeThermomechanicalProblem( const ThermalProblem<D>& thermal,
                                     const MechanicalProblem<D>& mechanical,
                                     ThermoplasticHistory<D>&& history0 )
{
    auto duration = thermal.general->duration;
    auto nsteps = static_cast<size_t>( std::ceil( duration / thermal.timeStep ) );
    auto dt = duration / nsteps;

    std::cout << "Integrating thermomechanical problem:" << std::endl;
    std::cout << "    duration        = " << duration << std::endl;
    std::cout << "    number of steps = " << nsteps << std::endl;
    std::cout << "    step size       = " << dt << std::endl;
    std::cout << "    base mesh size  = " << thermal.general->baseGrid->ncells( ) << std::endl;

    auto tstate0 = thermal.initialState( std::move( history0 ) );
    auto mstate0 = mechanical.initialState( );
    
    thermal.postprocess( thermal, tstate0 );
    mechanical.postprocess( mechanical, mstate0 );

    for( size_t istep = 0; istep < nsteps; ++istep )
    {
        std::cout << "Time step " << istep + 1 << " / " << nsteps << std::endl;

        auto tstate1 = thermal.step( tstate0, dt );

        thermal.postprocess( thermal, tstate1 );

        auto mstate1 = mechanical.step( mstate0, thermal, tstate0, tstate1 );
        
        mechanical.postprocess( mechanical, mstate1 );

        tstate0 = std::move( tstate1 );
        mstate0 = std::move( mstate1 );
    } 

    return std::pair { std::move( tstate0 ), std::move( mstate0 ) };
}

template<size_t D> inline
auto computeMechanicalProblem( const MechanicalProblem<D>& mechanical,
                               ThermoplasticHistory<D>&& history0,
                               double timestep )
{
    auto thermal = ThermalProblem<D>
    {
        .general = mechanical.general,
        .timeStep = timestep,
        //.postprocess = makeThermalPostprocessing<D>( "outputs/verification/SimpleJ2Plasticity_", 1 )
    };

    return computeThermomechanicalProblem( thermal, mechanical, std::move( history0 ) ).second;
}

} // namespace mlhp

#endif // MLHPBF_MECHANICAL_HPP
