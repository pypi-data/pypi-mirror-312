// This file is part of the mlhp project. License: See LICENSE

#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"

#include "src/python/pymlhpcore.hpp"

#include "mlhp/core/assembly.hpp"
#include "mlhp/core/basis.hpp"
#include "mlhp/core/integrands.hpp"
#include "mlhp/core/basisevaluation.hpp"
#include "mlhp/core/mapping.hpp"
#include "mlhp/core/triangulation.hpp"
#include "mlhp/core/boundary.hpp"

namespace mlhp::bindings
{

template<size_t D, typename MatrixType>
void bindAssemblyDimensionMatrixType( pybind11::module& m, std::string matrixName )
{
    m.def( ( "allocate" + matrixName ).c_str( ), []( const std::shared_ptr<AbsBasis<D>>& basis,
                                                     const DofIndexVector& dirichletDofs )
        { 
            return std::make_shared<MatrixType>( allocateMatrix<MatrixType>( *basis, dirichletDofs ) );
        },
        pybind11::arg( "basis" ), pybind11::arg( "dirichletDofs" ) = DofIndexVector { }
    );
}

template<size_t D>
void bindAssemblyDimension( pybind11::module& m )
{
    bindAssemblyDimensionMatrixType<D, linalg::SymmetricSparseMatrix>( m, "SymmetricSparseMatrix" );
    bindAssemblyDimensionMatrixType<D, linalg::UnsymmetricSparseMatrix>( m, "UnsymmetricSparseMatrix" );

    using PythonAssemblyTarget = std::variant
    <
        ScalarDouble*,
        DoubleVector*,
        linalg::UnsymmetricSparseMatrix*,
        linalg::SymmetricSparseMatrix*
    >;

    auto convertTargets = []( const std::vector<PythonAssemblyTarget>& pythonTargets )
    { 
        AssemblyTargetVector targets; 

        for( size_t i = 0; i < pythonTargets.size( ); ++i )
        {
            if( pythonTargets[i].index( ) == 0 ) 
                targets.push_back( std::get<ScalarDouble*>( pythonTargets[i] )->get( ) );
            else if( pythonTargets[i].index( ) == 1 ) 
                targets.push_back( std::get<DoubleVector*>( pythonTargets[i] )->get( ) );
            else if( pythonTargets[i].index( ) == 2 )
                targets.push_back( *std::get<linalg::UnsymmetricSparseMatrix*>( pythonTargets[i] ) );
            else if( pythonTargets[i].index( ) == 3 )
                targets.push_back( *std::get<linalg::SymmetricSparseMatrix*>( pythonTargets[i] ) );
        }

        return targets;
    };

    m.def( "integrateOnDomain", [convertTargets]( const AbsBasis<D>& basis,
                                                  const DomainIntegrand<D>& integrand,
                                                  const std::vector<PythonAssemblyTarget>& targets,
                                                  const AbsQuadrature<D>& quadrature,
                                                  const IntegrationOrderDeterminorWrapper<D>& orderDeterminor,
                                                  const DofIndicesValuesPair& boundaryDofs )
        { 
            return integrateOnDomain( basis, integrand, convertTargets( targets ),
            quadrature, orderDeterminor, boundaryDofs );
        },
        pybind11::arg( "basis" ),
        pybind11::arg( "integrand" ),
        pybind11::arg( "targets" ),
        pybind11::arg( "quadrature" ) = StandardQuadrature<D> { },
        pybind11::arg( "orderDeterminor" ) = IntegrationOrderDeterminorWrapper<D>{ makeIntegrationOrderDeterminor<D>( 1 ) },
        pybind11::arg( "dirichletDofs" ) = DofIndicesValuesPair { } 
    );
    
    m.def( "projectOnto", []( const AbsBasis<D>& basis,
                              const ScalarFunctionWrapper<D>& function )
           { return DoubleVector ( projectOnto<D>( basis, function ) ); } );
    
    m.def( "projectOnto", []( const AbsBasis<D>& basis,
                              const spatial::VectorFunction<D>& function )
           { return DoubleVector ( projectOnto<D>( basis, function ) ); } );
    
    m.def( "integrateOnDomain", [convertTargets]( const MultilevelHpBasis<D>& basis0,
                                                  const MultilevelHpBasis<D>& basis1,
                                                  const BasisProjectionIntegrand<D>& integrand,
                                                  const std::vector<PythonAssemblyTarget>& globalTargets,
                                                  const AbsQuadrature<D>& quadrature,
                                                  const IntegrationOrderDeterminorWrapper<D>& orderDeterminor,
                                                  const DofIndicesValuesPair& boundaryDofs )
        { 
            integrateOnDomain( basis0, basis1, integrand, convertTargets( globalTargets ),
                quadrature, orderDeterminor, boundaryDofs );
        },
        pybind11::arg( "basis0" ),
        pybind11::arg( "basis1" ),
        pybind11::arg( "integrand" ),
        pybind11::arg( "targets" ),
        pybind11::arg( "quadrature" ) = StandardQuadrature<D> { },
        pybind11::arg( "orderDeterminor" ) = IntegrationOrderDeterminorWrapper<D>{ makeIntegrationOrderDeterminor<D>( 1 ) },
        pybind11::arg( "dirichletDofs" ) = DofIndicesValuesPair { } 
    );

    // Surface support providers
    {
        [[maybe_unused]] auto absQuadratureC = pybind11::class_<AbsQuadratureOnMesh<D>, 
            std::shared_ptr<AbsQuadratureOnMesh<D>>>( m, add<D>( "AbsQuadratureOnMesh" ).c_str( ) );
        
        if constexpr ( D == 3 )
        {
            auto createQuadratureF = []( std::shared_ptr<Triangulation<D>> triangulation,
                                         std::shared_ptr<TriangleCellAssociation<D>> celldata,
                                         size_t order )
            {
                return std::make_shared<TriangulationQuadrature<D>>( triangulation, celldata, order );
            };

            auto triangulationQuadratureC = pybind11::class_<TriangulationQuadrature<D>, 
                std::shared_ptr<TriangulationQuadrature<D>>, AbsQuadratureOnMesh<D>>( 
                    m, add<D>( "TriangulationQuadrature" ).c_str( ) );

            m.def( "triangulationQuadrature", createQuadratureF, pybind11::arg( "triangulation" ), 
                pybind11::arg( "celldata" ), pybind11::arg( "order" ) );
        }

        [[maybe_unused]] auto meshBoundaryQuadratureC = pybind11::class_<boundary::QuadratureOnMeshFaces<D>, 
            std::shared_ptr<boundary::QuadratureOnMeshFaces<D>>, AbsQuadratureOnMesh<D>>( 
                m, add<D>( "QuadratureOnMeshFaces" ).c_str( ) );

        auto quadratureOnMeshFacesF = []( const AbsMesh<D>& mesh,
                                          const std::vector<size_t>& meshFaces,
                                          size_t order )
        {
            return std::make_shared<boundary::QuadratureOnMeshFaces<D>>( mesh, meshFaces, order );
        };

        m.def( "quadratureOnMeshFaces", quadratureOnMeshFacesF, pybind11::arg( "mesh" ), 
            pybind11::arg( "meshFaces" ), pybind11::arg( "order" ) );
    }

    auto integrateOnSurfaceF = [convertTargets]( const AbsBasis<D>& basis,
                                                 const SurfaceIntegrand<D>& integrand,
                                                 const std::vector<PythonAssemblyTarget>& globalTargets,
                                                 const AbsQuadratureOnMesh<D>& quadrature,
                                                 const DofIndicesValuesPair& boundaryDofs )
    {
        integrateOnSurface( basis, integrand, quadrature,
            convertTargets( globalTargets ), boundaryDofs );
    };

    m.def( "integrateOnSurface", integrateOnSurfaceF, pybind11::arg( "basis" ), 
        pybind11::arg( "integrand" ), pybind11::arg( "globalTargets" ), 
        pybind11::arg( "quadrature" ), pybind11::arg( "dirichletDofs" ) = DofIndicesValuesPair { } );

    [[maybe_unused]] auto surfaceIntegrand = pybind11::class_<SurfaceIntegrand<D>>
        ( m, add<D>( "SurfaceIntegrand" ).c_str( ) );

    // Surface integrands
    {
        auto neumannIntegrandF1 = []( const spatial::VectorFunction<D>& rhs )
        {
            return makeNeumannIntegrand( rhs );
        };

        auto neumannIntegrandF2 = []( const ScalarFunctionWrapper<D>& rhs, size_t ifield )
        {
            return makeNeumannIntegrand( rhs.get( ), ifield );
        };

        auto normalneumannIntegrandF = []( const ScalarFunctionWrapper<D>& pressure )
        {
            return makeNormalNeumannIntegrand( pressure.get( ) );
        };
    
        auto l2BoundaryIntegrandF1 = []( const spatial::VectorFunction<D>& mass,
                                         const spatial::VectorFunction<D>& rhs )
        {
            return makeL2BoundaryIntegrand( mass, rhs );
        };

        auto l2BoundaryIntegrandF2 = []( const ScalarFunctionWrapper<D>& mass,
                                         const ScalarFunctionWrapper<D>& rhs,
                                         size_t ifield )
        {
            return makeL2BoundaryIntegrand( mass.get( ), rhs.get( ), ifield );
        };

        m.def( "neumannIntegrand", neumannIntegrandF1, pybind11::arg( "rhs" ) );
        m.def( "neumannIntegrand", neumannIntegrandF2, pybind11::arg( "rhs" ), pybind11::arg( "ifield" ) = 0 );
        m.def( "normalNeumannIntegrand", normalneumannIntegrandF, pybind11::arg( "value" ) );
        m.def( "l2BoundaryIntegrand", l2BoundaryIntegrandF1, pybind11::arg( "mass" ), pybind11::arg( "rhs" ) );
        m.def( "l2BoundaryIntegrand", l2BoundaryIntegrandF2, pybind11::arg( "mass" ), pybind11::arg( "rhs" ),
            pybind11::arg( "ifield" ) = 0 );
    }

    auto projectGradientF = []( const AbsBasis<D>& basis, 
                                const DoubleVector& dofs, 
                                const AbsQuadrature<D>& quadrature )
    { 
        auto gradient = projectGradient( basis, dofs.get( ), quadrature, linalg::makeCGSolver( 1e-12 ) );
        auto converted = std::array<std::shared_ptr<DoubleVector>, D> { };

        for( size_t axis = 0; axis < D; ++axis )
        {
            converted[axis] = std::make_shared<DoubleVector>( std::move( gradient[axis] ) );
        }

        return converted;
    };

    m.def( "projectGradient", projectGradientF, pybind11::arg( "basis" ), pybind11::arg( "dofs" ),
        pybind11::arg( "quadrature" ) = StandardQuadrature<D> { } );
}

template<size_t... D>
void bindAssemblyDimensions( pybind11::module& m, std::index_sequence<D...>&& )
{
    [[maybe_unused]] std::initializer_list<int> tmp { ( bindAssemblyDimension<D + 1>( m ), 0 )... };
}

void bindAssemblyDimensionIndependent( pybind11::module& m )
{
    using QuadratureOrderVariant = DimensionVariant<IntegrationOrderDeterminorWrapper>;

    auto offsetOrderDeterminorF = []( size_t ndim, size_t offset )
    { 
        auto create = [&]<size_t D>( ) -> QuadratureOrderVariant {
            return IntegrationOrderDeterminorWrapper<D> { 
                makeIntegrationOrderDeterminor<D>( offset ) }; };

        return dispatchDimension( create, ndim );
    };

    m.def( "offsetOrderDeterminor", offsetOrderDeterminorF, 
           pybind11::arg( "ndim" ), pybind11::arg( "offset" ) );


    m.def( "allocateVectorWithSameSize", []( const linalg::AbsSparseMatrix& matrix )
    { 
        return DoubleVector( matrix.size1( ), 0.0 );
    } );
}

void bindCIntegrand( pybind11::module& m )
{
    pybind11::enum_<AssemblyType>( m, "AssemblyType" )
        .value( "Scalar", AssemblyType::Scalar )
        .value( "Vector", AssemblyType::Vector )
        .value( "UnsymmetricMatrix", AssemblyType::UnsymmetricMatrix );

    using DomainIntegrandVariant = DimensionVariant<DomainIntegrand>;

    using CType = void( double** targets,     double** shapes,     double** mapping, 
                        double*  rst,         double*  history,    double*  tmp, 
                        size_t*  locationMap, size_t*  totalSizes, size_t*  fieldSizes,
                        double   detJ,        double   weight,     size_t   ielement );

    auto domainIntegrandFromAddressF = []( size_t ndim, std::uint64_t address,
                                           std::vector<AssemblyType> types,
                                           int diffOrder, size_t tmpdofs )
    { 
        auto create = [&]<size_t D>( ) -> DomainIntegrandVariant
        {

            using Cache = typename DomainIntegrand<D>::Cache;
        
            struct ThisCache
            {
                std::vector<size_t> locationMap;
                std::vector<size_t> fieldSizes;
                std::vector<double*> targetPtrs;
                std::vector<double*> shapesPtrs;
                const MeshMapping<D>* mapping;
                AlignedDoubleVector tmp;
            };

            auto ntargets = types.size( );

            auto createCache = [ntargets]( )
            { 
                auto cache = ThisCache { };

                cache.targetPtrs.resize( ntargets );

                return Cache { std::move( cache ) };
            };

            auto prepare = [tmpdofs]( Cache& anyCache, 
                                      const MeshMapping<D>& mapping, 
                                      const LocationMap& locationMap )
            {
                auto& cache = utilities::cast<ThisCache>( anyCache );

                cache.tmp.resize( tmpdofs * memory::paddedLength<double>( locationMap.size( ) ) );
                cache.locationMap.resize( locationMap.size( ) );
                cache.mapping = &mapping;

                for( size_t idof = 0; idof < locationMap.size( ); ++idof )
                {
                    cache.locationMap[idof] = static_cast<size_t>( locationMap[idof] );
                }
            };

            auto evaluate = [address, ntargets]( Cache& anyCache, const BasisFunctionEvaluation<D>& shapes,
                                                 AlignedDoubleVectors& targets, double weightDetJ )
            { 
                auto& cache = utilities::cast<ThisCache>( anyCache );
            
                auto ndof = static_cast<size_t>( shapes.ndof( ) );
                auto nfields = shapes.nfields( );

                if( cache.shapesPtrs.empty( ) )
                {
                    cache.shapesPtrs.resize( nfields );
                    cache.fieldSizes.resize( nfields * 2 );
                }
     
                for( size_t itarget = 0; itarget < ntargets; ++itarget )
                {
                    cache.targetPtrs[itarget] = targets[itarget].data( );
                }

                for( size_t ifield = 0; ifield < nfields; ++ifield )
                {
                    cache.shapesPtrs[ifield] = const_cast<double*>( shapes.get( ifield, 0 ) );

                    cache.fieldSizes[2 * ifield + 0] = shapes.ndof( ifield );
                    cache.fieldSizes[2 * ifield + 1] = shapes.ndofpadded( ifield );
                }

                auto rst = shapes.rst( );
                auto xyz = shapes.xyz( );
                auto J = cache.mapping->J( rst );
                auto mappingPtrs = std::array<double*, 2> { xyz.data( ), J.data( ) };
                auto totalSizes = std::array { ndof, static_cast<size_t>( shapes.ndofpadded( ) ) };
                CType* callback = reinterpret_cast<CType*>( address );
            
                callback( cache.targetPtrs.data( ), cache.shapesPtrs.data( ), mappingPtrs.data( ), rst.data( ), 
                    nullptr, cache.tmp.data( ), cache.locationMap.data( ), totalSizes.data( ), 
                    cache.fieldSizes.data( ), 1.0, weightDetJ, static_cast<size_t>( shapes.elementIndex( ) ) );
            };

            return DomainIntegrand<D> { std::move( types ), static_cast<DiffOrders>( diffOrder ), 
                std::move( createCache ), std::move( prepare ), std::move( evaluate ) };
        };

        return dispatchDimension( std::move( create ), ndim );
    };

    m.def( "_domainIntegrandFromAddress", domainIntegrandFromAddressF );
}

void bindAssembly( pybind11::module& m )
{
    bindAssemblyDimensions( m, std::make_index_sequence<config::maxdim>( ) );

    bindAssemblyDimensionIndependent( m );
    bindCIntegrand( m );
}

} // mlhp::bindings

