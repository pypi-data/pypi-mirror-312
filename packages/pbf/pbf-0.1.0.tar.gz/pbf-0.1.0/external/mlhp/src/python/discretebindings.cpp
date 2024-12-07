// This file is part of the mlhp project. License: See LICENSE

#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"

#include "mlhp/core.hpp"

#include "src/python/pymlhpcore.hpp"

#include <sstream>
#include <iomanip>

namespace mlhp::bindings
{

template<size_t D>
void defineGrid( pybind11::module& m )
{
    auto overloadMeshMembers = []<typename Type, typename...Args>( pybind11::class_<Type, Args...>& pybindclass, std::string type )
    {
        auto str = [=]( const Type& mesh )
        {
            std::ostringstream os;

            os << type << "<" << D << "> (adress: " << &mesh << ")\n";
            os << "    ncells       : " << mesh.ncells( ) << std::endl;
            os << "    memory usage : " << utilities::memoryUsageString( mesh.memoryUsage( ) ) << std::endl;

            return os.str( );
        };
        
        auto neighbours = []( const AbsMesh<D>& mesh, CellIndex icell, size_t iface )
        {
            auto target = std::vector<MeshCellFace> { };

            mesh.neighbours( icell, iface, target );

            return target;
        };

        pybindclass.def( "ncells", []( const Type& mesh ) { return mesh.ncells( ); } );
        pybindclass.def( "nfaces", []( const Type& mesh, CellIndex icell ) { return mesh.nfaces( icell ); }, pybind11::arg( "icell" ) );
        pybindclass.def( "ndim", []( const Type& ) { return D; } );
        pybindclass.def( "cellType", &Type::cellType, pybind11::arg( "icell" ) );
        pybindclass.def( "memoryUsage", []( const Type& mesh ) { return mesh.memoryUsage( ); } );
        pybindclass.def( "neighbours", neighbours, pybind11::arg( "icell" ), pybind11::arg( "iface" ) );
        pybindclass.def( "shallowClone", &Type::clone );
        pybindclass.def( "__str__", str );
    };

    auto __str__ = []( const HierarchicalGridSharedPtr<D>& grid )
    { 
        std::ostringstream os;

        print( *grid, os );

        return os.str( );
    };

    auto refine = []( AbsHierarchicalGrid<D>& self,
                      const RefinementFunctionWrapper<D>& refinement )
    { 
        self.refine( refinement );
    };  

    
    // https://pybind11.readthedocs.io/en/stable/advanced/classes.html#overriding-virtuals
    //class PyAbsMesh : public AbsMesh<D>
    //{
    //    using AbsMesh::AbsMesh;

    //    CellIndex ncells( ) const override
    //    {
    //        PYBIND11_OVERRIDE_PURE( CellIndex, AbsMesh<D>, ncells, 0 );
    //    }
    //};

    auto absMesh = pybind11::class_<AbsMesh<D>, MeshSharedPtr<D>>
        ( m, add<D>( "AbsMesh" ).c_str( ) );

    overloadMeshMembers( absMesh, "AbsMesh" );

    auto absGrid = pybind11::class_<AbsGrid<D>, AbsMesh<D>, GridSharedPtr<D>>
        ( m, add<D>( "AbsGrid" ).c_str( ) );
    
    overloadMeshMembers( absGrid, "AbsGrid" );
    
    auto cartesianGrid = pybind11::class_<CartesianGrid<D>, AbsGrid<D>, CartesianGridSharedPtr<D>>
        ( m, add<D>( "CartesianGrid" ).c_str( ) );
    
    cartesianGrid.def( "boundingBox", []( const CartesianGrid<D>& grid ) { return grid.boundingBox( ); } );
    cartesianGrid.def( "ncells", pybind11::overload_cast<size_t>( &CartesianGrid<D>::ncells, pybind11::const_ ), pybind11::arg( "axis" ) );
    cartesianGrid.def( "coordinates", &CartesianGrid<D>::coordinates );
    
    overloadMeshMembers( cartesianGrid, "CartesianGrid" );
    
    m.def( "makeGrid", &makeCartesianGrid<D>,
           pybind11::arg( "nelements" ),
           pybind11::arg( "lengths" ) = array::make<D>( 1.0 ),
           pybind11::arg( "origin" ) = array::make<D>( 0.0 ) );

    auto makeGridF = []( CoordinateGrid<D>&& grid ) 
    { 
        return std::make_shared<CartesianGrid<D>>( std::move( grid ) ); 
    };

    m.def( "makeGrid", makeGridF, pybind11::arg( "ticks" ) );
    
    pybind11::class_<AbsHierarchicalGrid<D>, AbsMesh<D>, HierarchicalGridSharedPtr<D>>
        ( m, add<D>( "AbsHierarchicalGrid" ).c_str( ) )
        .def( "nleaves", &AbsHierarchicalGrid<D>::nleaves )
        .def( "refine", refine )
        .def( "baseGrid", &AbsHierarchicalGrid<D>::baseGridPtr )
        .def( "__str__", __str__ );

    auto refinedGrid = pybind11::class_<RefinedGrid<D>, AbsHierarchicalGrid<D>, 
        std::shared_ptr<RefinedGrid<D>>> ( m, add<D>( "RefinedGrid" ).c_str( ) );

    refinedGrid.def( pybind11::init<std::shared_ptr<AbsGrid<D>>>( ) );
    
    using FactoryType = HierarchicalGridSharedPtr<D>( std::array<size_t, D>,
                                                      std::array<double, D>, 
                                                      std::array<double, D> );

    m.def( "makeRefinedGrid", static_cast<FactoryType*>( makeRefinedGrid<D> ),
           pybind11::arg( "nelements" ),
           pybind11::arg( "lengths" ) = array::make<D>( 1.0 ),
           pybind11::arg( "origin" ) = array::make<D>( 0.0 ) );
    
    m.def( "makeRefinedGrid", []( GridSharedPtr<D> grid ) { return makeRefinedGrid<D>( grid ); },
        pybind11::arg( "grid" ) );
    
    pybind11::class_<AbsFilteredMesh<D>, AbsMesh<D>, std::shared_ptr<
        AbsFilteredMesh<D>>>( m, add<D>( "AbsFilteredMesh" ).c_str( ) );

    auto filteredGrid = pybind11::class_<FilteredGrid<D>, AbsGrid<D>, AbsFilteredMesh<D>, 
        std::shared_ptr<FilteredGrid<D>>>( m, add<D>( "FilteredGrid" ).c_str( ) );

    filteredGrid.def( pybind11::init<std::shared_ptr<AbsGrid<D>>, 
        std::vector<bool>>( ), pybind11::arg( "grid" ), pybind11::arg( "mask" ) );

    overloadMeshMembers( filteredGrid, "FilteredGrid" );

    pybind11::class_<ImplicitFunctionWrapper<D>>( m, add<D>( "ImplicitFunction" ).c_str( ) )
        .def( "__call__", &ImplicitFunctionWrapper<D>::call );

    pybind11::class_<RefinementFunctionWrapper<D>>( m, add<D>( "RefinementFunction" ).c_str( ) )
        .def( "__call__", &RefinementFunctionWrapper<D>::call );
    
    auto filterCellsF = []( std::shared_ptr<AbsGrid<D>> grid,
                            const ImplicitFunctionWrapper<D>& function,
                            size_t nseedpoints )
    { 
        auto mask = mesh::cellFilter( *grid, function.get( ), nseedpoints );

        return std::make_shared<FilteredGrid<D>>( grid, std::move( mask ) );
    };

    m.def( "filterCells", filterCellsF, pybind11::arg( "grid" ), 
        pybind11::arg( "function" ), pybind11::arg( "nseedpoints" ) = 4 );

    auto transformation = pybind11::class_<spatial::HomogeneousTransformation<D>>( m,
        add<D>( "HomogeneousTransformation" ).c_str( ) );

    auto transformationMatrixF = []( const spatial::HomogeneousTransformation<D>& t )
    {
        auto matrix = std::array<std::array<double, D + 1>, D + 1> { };

        for( size_t i = 0; i < D; ++i )
        {
            for( size_t j = 0; j < D + 1; ++j )
            {
                matrix[i][j] = t.matrix[i * (D + 1) + j];
            }
        }

        return matrix;
    };

    auto concatenateF = []( const std::vector<spatial::HomogeneousTransformation<D>>& transformations )
    {
        auto n = transformations.size( );
        auto result = n ? transformations.back( ) : spatial::scale( array::make<D>( 1.0 ) );

        for( size_t i = 1; i < n; ++i )
        {
            auto tmp = spatial::HomogeneousTransformationMatrix<D> { };

            linalg::mmproduct( result.matrix.data( ), transformations[n - i - 1].matrix.data( ), tmp.data( ), D + 1 );

            result.matrix = tmp;
        }

        return result;
    };

    transformation.def( "matrix", transformationMatrixF );
    transformation.def( "invert", &spatial::HomogeneousTransformation<D>::invert );
    transformation.def( "__call__", &spatial::HomogeneousTransformation<D>::operator( ) );

    m.def( "translation", &spatial::translate<D> );
    m.def( "scaling", &spatial::scale<D> );
    m.def( "concatenate", concatenateF, pybind11::arg( "transformations" ) );

    if constexpr ( D == 2 ) m.def( "rotation", []( double phi ) 
        { return spatial::rotate( phi ); }, pybind11::arg( "phi" ) );

    if constexpr ( D == 3 ) m.def( "rotation", []( std::array<double, 3> normal, double phi ) 
        { return spatial::rotate( normal, phi ); }, pybind11::arg( "normal" ), pybind11::arg( "phi" ) );

    m.def( "implicitSphere", []( std::array<double, D> center, double radius )
        { return ImplicitFunctionWrapper<D>{ implicit::sphere( center, radius ) }; },
        pybind11::arg( "center" ), pybind11::arg( "radius" ) );

    m.def( "implicitCube", []( std::array<double, D> x1, std::array<double, D> x2 )
        { return ImplicitFunctionWrapper<D>{ implicit::cube( x1, x2 ) }; },
        pybind11::arg( "corner1" ), pybind11::arg( "corner2" ) );
    
    m.def( "implicitEllipsoid", []( std::array<double, D> origin, std::array<double, D> radii )
        { return ImplicitFunctionWrapper<D>{ implicit::ellipsoid( origin, radii ) }; },
        pybind11::arg( "origin" ), pybind11::arg( "radii" ) );
    
    m.def( "implicitThreshold", []( const ScalarFunctionWrapper<D>& function, 
                                    double threshold, double sign ) -> ImplicitFunctionWrapper<D>
        { return implicit::threshold( function.get( ), threshold, sign ); },
        pybind11::arg( "function" ), pybind11::arg( "threshold" ) = 0.0, pybind11::arg( "sign" ) = true );

    m.def( "implicitHalfspace", []( std::array<double, D> origin, 
                                    std::array<double, D> outwardNormal ) -> ImplicitFunctionWrapper<D>
        { return implicit::halfspace( origin, outwardNormal ); },
        pybind11::arg( "origin" ), pybind11::arg( "outwardNormal" ) );
    
    m.def( "implicitTransformation", []( const ImplicitFunctionWrapper<D>& function,
                                         const spatial::HomogeneousTransformation<D>& t )
        { return ImplicitFunctionWrapper<D> { implicit::transform( function.get( ), t ) }; },
        pybind11::arg( "function" ), pybind11::arg( "transformation" ) );

    auto implicitF = []( std::vector<ImplicitFunctionWrapper<D>>&& wrappers, auto&& op, bool initial )
    {
        if( !wrappers.empty( ) )
        {
            auto functions = utilities::convertVector<ImplicitFunction<D>>( std::move( wrappers ) );

            auto function = [=, functions = std::move(functions)]( std::array<double, D> xyz )
            {
                auto value = functions.front( )( xyz );

                for( size_t ifunction = 1; ifunction < functions.size( ); ++ifunction )
                {
                    value = op( value, functions[ifunction]( xyz ) );
                }

                return value;
            };

            return ImplicitFunctionWrapper<D> { std::function { function } };
        }
        else
        {
            return ImplicitFunctionWrapper<D> { ImplicitFunction<D> { 
                utilities::returnValue( initial ) } };
        }
    };

    auto implicitUnionF = [=]( std::vector<ImplicitFunctionWrapper<D>>&& functions )
    {
        return implicitF( std::move( functions ), []( bool v1, bool v2 ){ return v1 || v2; }, false );
    };

    auto implicitIntersectionF = [=]( std::vector<ImplicitFunctionWrapper<D>>&& functions )
    {
        return implicitF( std::move( functions ), []( bool v1, bool v2 ){ return v1 && v2; }, true );
    };

    auto implicitSubtractionF = [=]( std::vector<ImplicitFunctionWrapper<D>>&& functions )
    {
        return implicitF( std::move( functions ), []( bool v1, bool v2 ){ return v1 && !v2; }, true );
    };
    
    m.def( "implicitUnion", implicitUnionF, pybind11::arg( "functions" ) );
    m.def( "implicitIntersection", implicitIntersectionF, pybind11::arg( "functions" ) );
    m.def( "implicitSubtraction", implicitSubtractionF, pybind11::arg( "functions" ) );

    m.def( "invert", []( const ImplicitFunctionWrapper<D>& function )
        { return ImplicitFunctionWrapper<D>{ implicit::invert<D>( function ) }; },
        pybind11::arg( "function" ) );
          
    m.def( "extrude", []( const ImplicitFunctionWrapper<D>& function, double minValue, double maxValue, size_t axis )
        { return ImplicitFunctionWrapper<D + 1>{ implicit::extrude<D>( function, minValue, maxValue, axis ) }; },
        pybind11::arg( "function" ), pybind11::arg( "minValue" ), pybind11::arg( "maxValue" ), pybind11::arg( "axis" ) = D );

    m.def( "refineTowardsBoundary", []( const ImplicitFunctionWrapper<D>& function,
                                        size_t maxDepth,
                                        size_t nseedpoints )
    {
        return RefinementFunctionWrapper<D>{ refineTowardsDomainBoundary<D>( 
            function, maxDepth, nseedpoints ) };
    }, pybind11::arg( "function" ), pybind11::arg( "maxDepth" ), 
       pybind11::arg( "nseedpoints" ) = 7 );

    m.def( "refineInsideDomain", []( const ImplicitFunctionWrapper<D>& function,
                                     size_t maxDepth,
                                     size_t nseedpoints )
    {
        return RefinementFunctionWrapper<D>{ refineInsideDomain<D>(
            function, maxDepth, nseedpoints ) };
    }, pybind11::arg( "function" ), pybind11::arg( "maxDepth" ), 
       pybind11::arg( "nseedpoints" ) = 7 );

    auto refineWithLevelFunctionF = []( const ScalarFunctionWrapper<D>& function,
                                        size_t nseedpoints )
    {
        auto levelFunction = [=]( std::array<double, D> xyz )
        {
            auto level = std::round( function.get( )( xyz ) );

            MLHP_CHECK( level >= 0.0 && level < NoValue<RefinementLevel>, 
                        "Refinement level function values must be in [0, " + std::to_string(
                        static_cast<int>( NoValue<RefinementLevel> ) - 1 ) + "]." );

            return static_cast<RefinementLevel>( level );
        };

        return RefinementFunctionWrapper<D>{ refineWithLevelFunction<D>( levelFunction, nseedpoints ) };
    };
    
    m.def( "refineWithLevelFunction", refineWithLevelFunctionF, 
           pybind11::arg( "function" ), pybind11::arg( "nseedpoints" ) = 7 );

    auto refinementOrF = []( std::vector<RefinementFunctionWrapper<D>>&& wrappers )
    {
        auto refinements = utilities::convertVector<RefinementFunction<D>>( std::move( wrappers ) );

        return RefinementFunctionWrapper<D> { [refinements = std::move( refinements )] 
            (const MeshMapping<D>& mapping, RefinementLevel level )
        { 
            bool value = false;

            for( auto& refinement : refinements )
            {
                value = value ? true : refinement( mapping, level );
            }

            return value;
        } };
    };

    m.def( "refinementOr", refinementOrF, pybind11::arg( "refinements" ) );
}

template<size_t D>
void defineMesh( pybind11::module& m )
{
    auto printMesh = []( const UnstructuredMesh<D>& mesh )
    { 
        std::ostringstream os;

        print( mesh, os );

        return os.str( );
    };

    pybind11::class_<UnstructuredMesh<D>, AbsMesh<D>, std::shared_ptr<UnstructuredMesh<D>>>
        ( m, add<D>( "UnstructuredMesh" ).c_str( ) ) 
        .def( "__str__", printMesh );

    m.def( "makeUnstructuredMesh", []( CoordinateList<D>&& rst,
                                       std::vector<size_t>&& connectivity,
                                       std::vector<size_t>&& offsets )
        { return std::make_shared<UnstructuredMesh<D>>( std::move( rst ), 
            std::move( connectivity ), std::move( offsets ) ); },
        pybind11::arg( "nelements" ),
        pybind11::arg( "lengths" ) = array::make<D>( 1.0 ),
        pybind11::arg( "origin" ) = array::make<D>( 0.0 ) );
    
    auto kdtreeC = pybind11::class_<KdTree<D>, std::shared_ptr<KdTree<D>>, 
        AbsMesh<D>>( m, add<D>( "KdTree" ).c_str( ) );

    auto kdtreeStr = []( const KdTree<D>& tree ) 
    { 
        auto sstream = std::stringstream { };

        print( tree, sstream );

        return sstream.str( );
    };

    kdtreeC.def( "__str__", kdtreeStr );
    kdtreeC.def( "ncells", &KdTree<D>::ncells );
    kdtreeC.def( "nfull", &KdTree<D>::nfull );
    kdtreeC.def( "nleaves", &KdTree<D>::nleaves );
    kdtreeC.def( "ncells", &KdTree<D>::ncells );
    kdtreeC.def( "maxdepth", &KdTree<D>::maxdepth );
    kdtreeC.def( "memoryUsage", &KdTree<D>::memoryUsage );
    kdtreeC.def( "boundingBox", []( const KdTree<D>& t ) { return t.boundingBox( ); } );

    auto buildKdTreeF1 = []( const Triangulation<D>& triangulation )
    {
        return buildKdTree( triangulation );
    };

    m.def( "buildKdTree", buildKdTreeF1, pybind11::arg( "buildKdTree" ) );
}

void defineBasisSingle( pybind11::module& m )
{
    pybind11::class_<AnsatzTemplateVector>( m, "AnsatzTemplateVector" );

    pybind11::class_<PolynomialDegreeTuple>( m, "PolynomialDegreeTuple" )
        .def( pybind11::init<size_t>( ) )
        .def( pybind11::init<const std::vector<size_t>&>( ) );

    pybind11::class_<UniformGrading>( m, "UniformGrading", 
        "Same polynomial degrees everywhere." )
        .def( pybind11::init<PolynomialDegreeTuple>( ),
              pybind11::arg( "uniformDegrees" ) );

    pybind11::class_<LinearGrading>( m, "LinearGrading",
        "Set degrees on finest elements. Increment degrees by one per level coarser." )
        .def( pybind11::init<PolynomialDegreeTuple>( ),
              pybind11::arg( "fineDegrees" ) );

    pybind11::class_<InterpolatedGrading>( m, "InterpolatedGrading",
        "Interpolate between degrees on root elements and finest elements." )
        .def( pybind11::init<PolynomialDegreeTuple, 
                             PolynomialDegreeTuple>( ),
              pybind11::arg( "rootDegrees" ), pybind11::arg( "fineDegrees" ) );
}

template<size_t D, GradingConcept Grading>
void defineBasisFactoryWithGrading( pybind11::module& m )
{
    using FactoryType = MultilevelHpBasisSharedPtr<D>( 
        const HierarchicalGridSharedPtr<D>&, const Grading&, size_t );
    
    m.def( "makeHpTensorSpace", static_cast<FactoryType*>( makeHpBasis<TensorSpace> ),
           "Create tensor space multi-level hp basis with custom polynomial grading.",
           pybind11::arg( "grid" ), pybind11::arg( "grading" ), pybind11::arg( "nfields" ) = 1 );

    m.def( "makeHpTrunkSpace", static_cast<FactoryType*>( makeHpBasis<TrunkSpace> ),
           "Create trunk space multi-level hp basis with custom polynomial grading.",
           pybind11::arg( "grid" ), pybind11::arg( "grading" ), pybind11::arg( "nfields" ) = 1 );

    auto ptr1 = &makeHpBasisFactory<TensorSpace, D, Grading>;
    auto ptr2 = &makeHpBasisFactory<TrunkSpace, D, Grading>;

    m.def( add<D>( "makeHpTensorSpaceFactory" ).c_str( ), ptr1, "Create factory that creates tensor "
           "space hp bases with custom polynomial degree distribution.", pybind11::arg( "degrees" ) );

    m.def( add<D>( "makeHpTrunkSpaceFactory" ).c_str( ), ptr2, "Create factory that creates trunk "
           "space hp bases with custom polynomial degree distribution.", pybind11::arg( "degrees" ) );
}

template<size_t D>
void defineBasis( pybind11::module& m )
{
    auto overloadBasisMembers = []<typename Type, typename...Args>( pybind11::class_<Type, Args...>& pybindclass, 
                                                                    std::string type, bool doStr = true )
    {
        if( doStr )
        {
            auto str = [=]( const Type& basis )
            {
                std::ostringstream os;

                os << type << "<" << D << "> (adress: " << &basis << ")\n";
                os << "    number of elements         : " << basis.nelements( ) << std::endl;
                os << "    number of field components : " << basis.nfields( ) << std::endl;
                os << "    maximum polynomial degree  : " << basis::maxdegree( basis ) << std::endl;
                os << "    heap memory usage          : " << utilities::memoryUsageString( basis.memoryUsage( ) ) << std::endl;

                return os.str( );
            };

            pybindclass.def( "__str__", str );
        }
        
        pybindclass.def( "nelements", &AbsBasis<D>::nelements );
        pybindclass.def( "ndof", &AbsBasis<D>::ndof );
        pybindclass.def( "ndim", []( const AbsBasis<D>& ){ return D; } );
        pybindclass.def( "nfields", &AbsBasis<D>::nfields );
        pybindclass.def( "mesh", &AbsBasis<D>::meshPtr );
    };

    auto absBasis = pybind11::class_<AbsBasis<D>, std::shared_ptr<AbsBasis<D>>>( m, add<D>( "AbsBasis" ).c_str( ) );

    overloadBasisMembers( absBasis, "AbsBasis" );

    m.def( "maxdegree", basis::maxdegree<D>, pybind11::arg( "basis" ) );

    using MlhpBasis = MultilevelHpBasis<D>;
    using MlhpBasisBinding = pybind11::class_<MlhpBasis, AbsBasis<D>, std::shared_ptr<MlhpBasis>>;

    auto mlhpBasisStr = []( const MultilevelHpBasis<D>& basis )
    { 
        std::ostringstream os;

        print( basis, os );

        return os.str( );
    };

    auto mlhpBasis = MlhpBasisBinding( m, add<D>( "MultilevelHpBasis" ).c_str( ) );
        
    mlhpBasis.def( "__str__", mlhpBasisStr );
    
    overloadBasisMembers( mlhpBasis, "MultilevelHpBasis", false );

    pybind11::implicitly_convertible<size_t, PolynomialDegreeTuple>( );
    pybind11::implicitly_convertible<std::vector<size_t>, PolynomialDegreeTuple>( );

    using FactoryType1 = MultilevelHpBasisSharedPtr<D>( const HierarchicalGridSharedPtr<D>&,
                                                        const PolynomialDegreeTuple&, size_t );
    
    m.def( "makeHpTensorSpace", static_cast<FactoryType1*>( makeHpBasis<TensorSpace> ),
           "Create tensor space multi-level hp basis with uniform polynomial degree distribution.",
           pybind11::arg( "grid" ),  pybind11::arg( "degrees" ), pybind11::arg( "nfields" ) = 1 );

    m.def( "makeHpTrunkSpace", static_cast<FactoryType1*>( makeHpBasis<TrunkSpace> ),
           "Create trunk space multi-level hp basis with uniform polynomial degree distribution.",
           pybind11::arg( "grid" ),  pybind11::arg( "degrees" ), pybind11::arg( "nfields" ) = 1 );

    m.def( "makeHpTensorSpaceFactory", []( std::array<size_t, D> degrees )
           { return makeHpBasisFactory<TensorSpace, D>( degrees ); },
           "Create factory that creates tensor space hp bases with uniform polynomial degree distribution.",
           pybind11::arg( "degrees" ) );

    m.def( "makeHpTrunkSpaceFactory", []( std::array<size_t, D> degrees )
           { return makeHpBasisFactory<TrunkSpace, D>( degrees ); },
           "Create factory that creates trunk space hp bases with uniform polynomial degree distribution.",
           pybind11::arg( "degrees" ) );

    using FactoryType2 = MultilevelHpBasisFactory<D>( const PolynomialDegreeTuple& );

    auto ptr1 = static_cast<FactoryType2*>( makeHpBasisFactory<TensorSpace, D> );
    auto ptr2 = static_cast<FactoryType2*>( makeHpBasisFactory<TrunkSpace, D> );

    m.def( add<D>( "makeHpTensorSpaceFactory" ).c_str( ), ptr1, "Create factory that creates tensor "
           "space hp bases with custom polynomial degree distribution.", pybind11::arg( "degrees" ) );

    m.def( add<D>( "makeHpTrunkSpaceFactory" ).c_str( ), ptr2, "Create factory that creates trunk "
           "space hp bases with custom polynomial degree distribution.", pybind11::arg( "degrees" ) );

    defineBasisFactoryWithGrading<D, UniformGrading>( m );
    defineBasisFactoryWithGrading<D, LinearGrading>( m );
    defineBasisFactoryWithGrading<D, InterpolatedGrading>( m );

    auto count = []( std::array<size_t, D> degrees )
    {
        BooleanMask<D> mask;

        TrunkSpace::initialMaskProvider<D>( )( mask, degrees );

        return std::accumulate( mask.begin( ), mask.end( ), std::uint64_t { 0 } );
    };

    m.def( "countTrunkSpaceDofs", count, "Number element dofs using trunk space.", pybind11::arg( "degrees" ) );

    m.def( "additiveSchwarzPreconditioner", []( const linalg::UnsymmetricSparseMatrix& matrix,
                                                const AbsBasis<D>& basis,
                                                const DofIndexVector& dirichletDofs )
           { return makeAdditiveSchwarzPreconditioner( matrix, basis, dirichletDofs ); },
           pybind11::arg( "matrix" ), pybind11::arg( "basis" ), 
           pybind11::arg( "dirichletDofs" ) = DofIndexVector { } );

    auto printUnstructured = []( const UnstructuredBasis<D>& basis )
    {
        std::ostringstream os;

        print( basis, os );

        return os.str( );
    };

    auto unstructuredBasis = pybind11::class_<UnstructuredBasis<D>, AbsBasis<D>, 
        std::shared_ptr<UnstructuredBasis<D>>> ( m, add<D>( "UnstructuredBasis" ).c_str( ) );

    unstructuredBasis.def( "__str__", printUnstructured );
    
    overloadBasisMembers( unstructuredBasis, "UnstructuredBasis" );

    m.def( "makeUnstructuredBasis", []( const std::shared_ptr<UnstructuredMesh<D>>& mesh,
                                        size_t nfields )
        { return std::make_shared<UnstructuredBasis<D>>( mesh, nfields ); },
        pybind11::arg( "mesh" ), pybind11::arg( "nfields" ) = 1 );

    auto solutionEvaluatorF1 = []( BasisConstSharedPtr<D> basis,
                                   std::shared_ptr<DoubleVector> dofs,
                                   size_t ifield )
    {
        return ScalarFunctionWrapper<D> { basis::makeScalarEvaluator<D>( std::move( basis ), dofs->get( ), ifield ) };
    };

    m.def( "scalarEvaluator", solutionEvaluatorF1, pybind11::arg( "basis" ), 
        pybind11::arg( "dofs" ), pybind11::arg( "ifield" ) = 0 );

    m.def( "vectorEvaluator", basis::makeVectorEvaluator<D>, pybind11::arg( "basis" ),
           pybind11::arg( "dofs" ) );
}

template<size_t D>
void definePartitioners( pybind11::module& m )
{
    pybind11::class_<AbsQuadrature<D>, std::shared_ptr<AbsQuadrature<D>>>( m, 
        add<D>( "AbsQuadrature" ).c_str( ) );

    pybind11::class_<StandardQuadrature<D>, AbsQuadrature<D>, std::shared_ptr<
        StandardQuadrature<D>>>(m, add<D>("StandardQuadrature").c_str( ));

    pybind11::class_<GridQuadrature<D>, AbsQuadrature<D>, std::shared_ptr<
        GridQuadrature<D>>>( m, add<D>( "GridQuadrature" ).c_str( ) );

    pybind11::class_<SpaceTreeQuadrature<D>, AbsQuadrature<D>, std::shared_ptr<
        SpaceTreeQuadrature<D>>>( m, add<D>( "SpaceTreeQuadrature" ).c_str( ) );

    pybind11::class_<MomentFittingQuadrature<D>, AbsQuadrature<D>, std::shared_ptr<
        MomentFittingQuadrature<D>>>( m, add<D>( "MomentFittingQuadrature" ).c_str( ) );

    pybind11::class_<MeshProjectionQuadrature<D>, AbsQuadrature<D>, std::shared_ptr<
        MeshProjectionQuadrature<D>>>( m, add<D>( "MeshProjectionQuadrature" ).c_str( ) );
    
    m.def( "gridQuadrature", []( std::array<size_t, D> nvoxels )
           { return std::make_shared<GridQuadrature<D>>( nvoxels ); },
           pybind11::arg( "nvoxels" ) = array::makeSizes<D>( 1 ) );
    
    m.def( "spaceTreeQuadrature", []( const ImplicitFunctionWrapper<D>& function, size_t depth, double epsilon, size_t nseedpoints )
           { return std::make_shared<SpaceTreeQuadrature<D>>( function, epsilon, depth, nseedpoints ); },
           pybind11::arg( "function" ), pybind11::arg( "depth" ), 
           pybind11::arg( "epsilon" ) = 1.0, pybind11::arg( "nseedpoints" ) = 5 );
    
    m.def( "momentFittingQuadrature", []( const ImplicitFunctionWrapper<D>& function, size_t depth,
                                          double epsilon, bool adaptOrders, size_t nseedpoints )
           { return std::make_shared<MomentFittingQuadrature<D>>( function, epsilon, depth, adaptOrders, nseedpoints ); },
           pybind11::arg( "function" ), pybind11::arg( "depth" ), pybind11::arg( "epsilon" ) = 1.0,
           pybind11::arg( "adaptOrders" ) = true, pybind11::arg( "nseedpoints" ) = 5 );

    m.def( "meshProjectionQuadrature", []( const AbsHierarchicalGrid<D>& grid,
                                           const AbsQuadrature<D>& quadrature,
                                           size_t maxdepth )
           { return std::make_shared<MeshProjectionQuadrature<D>>( grid, quadrature, maxdepth ); },
           pybind11::arg( "grid" ), pybind11::arg( "quadrature" ) = StandardQuadrature<D> { },
           pybind11::arg( "maxdepth" ) = NoValue<size_t> );
}

template<size_t D>
using SharedQuadrature = std::shared_ptr<AbsQuadrature<D>>;

void definePartitionersSingle( pybind11::module& m )
{
    using QuadratureVariant = DimensionVariant<SharedQuadrature>;
        
    auto standardQuadratureF = []( size_t ndim )
    { 
        auto create = [&]<size_t D>( ) -> QuadratureVariant {
            return std::make_shared<StandardQuadrature<D>>( ); };

        return dispatchDimension( create, ndim );
    };

    m.def( "standardQuadrature", standardQuadratureF, pybind11::arg( "ndim" ) );
}

void defineFunctionWrappersSingle( pybind11::module& m )
{
    defineFunctionWrapper<RealFunction, RealFunctionTag>( m, "RealFunction" );
    defineFunctionWrapper<RealFunctionWithDerivative, RealFunctionTag>( m, "RealFunctionWithDerivative" );
    defineFunctionWrapper<linalg::LinearOperator>( m, "LinearOperator" );

    auto parseExtrapolate = []( std::string&& extrapolate ) -> interpolation::Extrapolate
    {
        for( char&c : extrapolate ) c = std::tolower( c );

        if( extrapolate == "default" ) return interpolation::Extrapolate::Default;
        if( extrapolate == "constant" ) return interpolation::Extrapolate::Constant;
        if( extrapolate == "linear" ) return interpolation::Extrapolate::Linear;

        MLHP_THROW( "Invalid extrapolation string \"" + extrapolate + 
            "\". Available"" are default, constant, and linear." );
    };
    
    auto constantInterpolationF = [=]( const std::vector<double>& positions,
                                       const std::vector<double>& values )
    {
        return RealFunctionWithDerivativeWrapper { 
            interpolation::makeConstantInterpolation( positions, values ) };
    };
    
    auto linearInterpolationF = [=]( const std::vector<double>& positions,
                                     const std::vector<double>& values,
                                     std::string extrapolate )
    {
        return RealFunctionWithDerivativeWrapper { interpolation::makeLinearInterpolation( 
            positions, values, parseExtrapolate( std::move( extrapolate ) ) ) };
    };
    
    auto splineInterpolationF = [=]( const std::vector<double>& positions,
                                     const std::vector<double>& values,
                                     size_t degree,
                                     std::string extrapolate )
    {
        return RealFunctionWithDerivativeWrapper { interpolation::makeBSplineInterpolation( 
            positions, values, degree, parseExtrapolate( std::move( extrapolate ) ) ) };
    };
    
    auto hermiteInterpolationF = [=]( const std::vector<double>& positions,
                                      const std::vector<double>& values,
                                      const std::vector<double>& derivatives,
                                      std::string extrapolate )
    {
        return RealFunctionWithDerivativeWrapper { interpolation::makeCubicHermiteSpline( 
            positions, values, derivatives, parseExtrapolate( std::move( extrapolate ) ) ) };
    };
    
    m.def( "constantInterpolation", constantInterpolationF,
        pybind11::arg( "positions" ), pybind11::arg( "values" ) );

    m.def( "linearInterpolation", linearInterpolationF, pybind11::arg( "positions" ), 
        pybind11::arg( "values" ), pybind11::arg( "extrapolate" ) = "linear" );

    m.def( "splineInterpolation", splineInterpolationF, pybind11::arg( "positions" ), 
        pybind11::arg( "values" ), pybind11::arg( "degree" ) = 3,
        pybind11::arg( "extrapolate" ) = "linear" );
    
    m.def( "hermiteInterpolation", hermiteInterpolationF, pybind11::arg( "positions" ), 
        pybind11::arg( "values" ), pybind11::arg( "derivatives" ), 
        pybind11::arg( "extrapolate" ) = "linear" );

    auto scaleFunctionF = []( const RealFunctionWithDerivativeWrapper& interpolation, double scaling )
    {
        return RealFunctionWithDerivativeWrapper { [=, f = interpolation.get( )]( double x )
        {
            return f( x ) * scaling;
        } };
    };

    m.def( "scaleFunction", scaleFunctionF, pybind11::arg( "function" ), pybind11::arg( "scaling" ) );
}

template<size_t D>
void defineIntegrands( pybind11::module& m )
{
    pybind11::class_<DomainIntegrand<D>>( m, add<D>( "DomainIntegrand" ).c_str( ) );
    pybind11::class_<Kinematics<D>>( m, add<D>( "Kinematics" ).c_str( ) );
    pybind11::class_<Constitutive<D>>( m, add<D>( "Constitutive" ).c_str( ) );

    m.def( "poissonIntegrand", []( const ScalarFunctionWrapper<D>& kappa,
                                   const ScalarFunctionWrapper<D>& source )
        { return makePoissonIntegrand<D>( kappa, source ); } );

    m.def( "l2ErrorIntegrand", []( const DoubleVector& dofs,
                                   const ScalarFunctionWrapper<D>& solution )
        { return makeL2ErrorIntegrand<D>( dofs.get( ), solution ); } );

    m.def( "energyErrorIntegrand", []( const DoubleVector& dofs,
                                       const spatial::VectorFunction<D>& derivatives )
        { return makeEnergyErrorIntegrand<D>( dofs.get( ), derivatives ); } );

    m.def( "staticDomainIntegrand", []( const Kinematics<D>& kinematics,
                                        const Constitutive<D>& constitutive,
                                        const spatial::VectorFunction<D>& rhs )
        { return makeIntegrand<D>( kinematics, constitutive, rhs ); },
        pybind11::arg( "kinematics" ), pybind11::arg( "constitutive" ),
        pybind11::arg( "source") = spatial::VectorFunction<D> { spatial::constantFunction<D>( array::make<D>( 0.0 ) ) } );

    if constexpr( D == 3 )
    {
        m.def( "isotropicElasticMaterial", []( const ScalarFunctionWrapper<3>& E,
                                               const ScalarFunctionWrapper<3>& nu )
            { return makeIsotropicElasticMaterial( E, nu ); } );
    }
    if constexpr( D == 2 )
    {
        m.def( "planeStressMaterial", []( const ScalarFunctionWrapper<D>& E,
                                          const ScalarFunctionWrapper<D>& nu )
            { return makePlaneStressMaterial( E, nu ); } );

        m.def( "planeStrainMaterial", []( const ScalarFunctionWrapper<D>& E,
                                          const ScalarFunctionWrapper<D>& nu )
            { return makePlaneStrainMaterial( E, nu ); } );
    }

    pybind11::class_<BasisProjectionIntegrand<D>>( m, add<D>( "BasisProjectionIntegrand" ).c_str( ) );

    m.def( "transientPoissonIntegrand", []( const ScalarFunctionWrapper<D + 1>& capacity,
                                            const ScalarFunctionWrapper<D + 1>& diffusivity,
                                            const ScalarFunctionWrapper<D + 1>& source,
                                            const DoubleVector& dofs,
                                            std::array<double, 2> timeStep,
                                            double theta )
        { return makeTransientPoissonIntegrand<D>( capacity, diffusivity, source, dofs.get( ), timeStep, theta ); } ); 

}

void defineIntegrandsSingle( pybind11::module& m )
{
    using BasisProjectionVariant = DimensionVariant<BasisProjectionIntegrand>;

    auto l2BasisProjectionIntegrandD = []( size_t ndim, const DoubleVector& dofs )
    { 
        auto create = [&]<size_t D>( ) -> BasisProjectionVariant {
            return makeL2BasisProjectionIntegrand<D>( dofs.get( ) ); };

        return dispatchDimension( create, ndim );
    };

    m.def( "l2BasisProjectionIntegrand", l2BasisProjectionIntegrandD,
        pybind11::arg( "ndim" ), pybind11::arg( "dofs" ) );
    
    using KinematicsVariant = DimensionVariant<Kinematics>;

    auto smallStrainKinematicsF = []( size_t ndim )
    { 
        auto create = [&]<size_t D>( ) -> KinematicsVariant {
            return makeSmallStrainKinematics<D>( ); };

        return dispatchDimension( create, ndim );
    };

    m.def( "smallStrainKinematics", smallStrainKinematicsF, pybind11::arg( "ndim" ) );
}

std::array<DoubleVector, 2> splitF( const DoubleVector& dofVector,
                                    const std::vector<DofIndex>& indices )
{
    auto& dofs = dofVector.get( );

    if( dofs.empty( ) )
    {
        MLHP_CHECK( indices.empty( ), "Empty dof vector with non-empty index vector." );

        return { };
    }

    if( indices.empty( ) )
    {
        return { DoubleVector { }, DoubleVector { dofs } };
    }

    auto max = std::max_element( indices.begin( ), indices.end( ) );

    MLHP_CHECK( *max < dofs.size( ), "Index " + std::to_string( *max ) + " at position " + 
        std::to_string( std::distance( indices.begin( ), max ) ) + " exceeds vector size of " + 
        std::to_string( dofs.size( ) ) + "." );

    auto mask = algorithm::indexMask( indices, dofs.size( ) );
    auto size0 = static_cast<size_t>( std::count( mask.begin( ), mask.end( ), size_t { 0 } ) );
    auto values0 = std::vector<double>( size0 );
    auto values1 = std::vector<double>( dofs.size( ) - size0 );

    size_t count0 = 0, count1 = 0;

    for( size_t idof = 0; idof < dofs.size( ); ++idof )
    {
        if( !mask[idof] )
        {
            values0[count0++] = dofs[idof];
        }
        else
        {
            values1[count1++] = dofs[idof];
        }
    }

    return { std::move( values1 ), std::move( values0 ) };
}

void bindLinalg( pybind11::module& m )
{
    pybind11::class_<linalg::AbsSparseMatrix,
        std::shared_ptr<linalg::AbsSparseMatrix>>
        absSparseMatrix( m, "AbsSparseMatrix" );

    absSparseMatrix.def( "memoryUsage", &linalg::AbsSparseMatrix::memoryUsage );

    [[maybe_unused]]
    pybind11::class_<linalg::SymmetricSparseMatrix,
        std::shared_ptr<linalg::SymmetricSparseMatrix>>
        symmetricSparse( m, "SymmetricSparseMatrix", absSparseMatrix );

    [[maybe_unused]]
    pybind11::class_<linalg::UnsymmetricSparseMatrix,
        std::shared_ptr<linalg::UnsymmetricSparseMatrix>>
        unsymmetricSparse( m, "UnsymmetricSparseMatrix", absSparseMatrix );
    
    auto bindMatrix = []<typename Matrix>( auto& pyclass )
    {
        auto print = []( const auto& matrix )
        { 
            std::stringstream sstream;

            linalg::print( matrix, sstream );

            return sstream.str( );
        };

        auto indptr = []( const Matrix& M ) { return std::vector( M.indptr( ), M.indptr( ) + M.size1( ) + 1 ); };
        auto indices = []( const Matrix& M ) { return std::vector( M.indices( ), M.indices( ) + M.nnz( ) ); };
        auto data = []( const Matrix& M ) { return std::vector( M.data( ), M.data( ) + M.nnz( ) ); };
        auto shape = []( const Matrix& M ) { return std::array { M.size1( ), M.size2( ) }; };

        auto multiply = []( const Matrix& M, const DoubleVector& rhs ) 
        { 
            auto result = std::vector( rhs.size( ), 0.0 );
            
            linalg::makeDefaultMultiply( M )( rhs.get( ).data( ), result.data( ) );

            return DoubleVector { std::move( result ) };
        };

        auto todense = []( const Matrix& M )
        {
            auto result = std::vector<std::vector<double>>( M.size1( ), std::vector<double>( M.size2( ), 0.0 ) );

            for( size_t i = 0; i < M.size1( ); ++i )
            {
                for( auto index = M.indptr( )[i]; index < M.indptr( )[i + 1]; ++index )
                {
                    result[i][M.indices( )[index]] = M.data( )[index];
                }
            }

            return result;
        };

        pyclass.def( "__str__", [=]( const Matrix& matrix ) { return print( matrix ); } );
        pyclass.def( "nnz", &Matrix::nnz );
        pyclass.def( "memoryUsage", &Matrix::memoryUsage );
        pyclass.def( "__call__", &Matrix::operator() );
        pyclass.def( "__mul__", multiply );
        pyclass.def( "todense", todense );
        pyclass.def_property_readonly( "indptr", indptr );
        pyclass.def_property_readonly( "indices", indices );
        pyclass.def_property_readonly( "data", data );
        pyclass.def_property_readonly( "shape", shape );
    };
    
    bindMatrix.template operator()<linalg::SymmetricSparseMatrix>( symmetricSparse );
    bindMatrix.template operator()<linalg::UnsymmetricSparseMatrix >( unsymmetricSparse );

    [[maybe_unused]]
    pybind11::class_<DoubleVector, std::shared_ptr<DoubleVector>> doubleVector( m, "DoubleVector" );

    doubleVector.def( pybind11::init<std::size_t>( ) );
    doubleVector.def( pybind11::init<std::size_t, double>( ) );
    doubleVector.def( pybind11::init<std::vector<double>>( ) );
    doubleVector.def( "__len__", []( const DoubleVector& self ){ return self.get( ).size( ); } );
    doubleVector.def( "get", static_cast<const std::vector<double>& ( DoubleVector::* )( ) const>( &DoubleVector::get ) );
    doubleVector.def( "size", static_cast<size_t ( DoubleVector::* )( ) const>( &DoubleVector::size ) );
    doubleVector.def_property_readonly( "shape", []( const DoubleVector& v ){ return std::array { v.size( ) }; } );
      
    [[maybe_unused]]
    pybind11::class_<ScalarDouble> scalarDouble( m, "ScalarDouble" );
    
    scalarDouble.def( pybind11::init<>( ) );
    scalarDouble.def( pybind11::init<double>( ) );
    scalarDouble.def( "get", []( const ScalarDouble& value ) { return value.get( ); } );
    
    m.def( "makeCGSolver", []( double tolerance )
    { 
        auto solver = linalg::makeCGSolver( tolerance );

        return std::function { [=]( const linalg::AbsSparseMatrix& matrix,
                                    DoubleVector& rhs )
        {
            return DoubleVector { solver( matrix, rhs.get( ) ) };
        } };
    }, pybind11::arg( "tolerance" ) = 1e-8 );
    
    m.def( "makeMultiply", []( const linalg::AbsSparseMatrix& matrix )
           { return LinearOperatorWrapper { linalg::makeDefaultMultiply( matrix ) }; },
           "Create default linear operator for sparse matrix-vector product.",
           pybind11::arg( "matrix" ) );

    auto internalCGF = []( const LinearOperatorWrapper& multiply,
                           const DoubleVector& b,
                           const LinearOperatorWrapper& preconditioner,
                           size_t maxit, double tolerance )
    {
        std::vector<double> solution;

        auto residuals = linalg::cg( multiply, b.get( ), solution, preconditioner, maxit, tolerance );

        return std::make_pair( DoubleVector { std::move( solution ) }, residuals );
    };
    
    auto internalBiCGStabF = []( const LinearOperatorWrapper& multiply,
                                 const DoubleVector& b,
                                 const LinearOperatorWrapper& preconditioner,
                                 size_t maxit, double tolerance )
    {
        std::vector<double> solution;

        auto residuals = linalg::bicgstab( multiply, b.get( ), solution, preconditioner, maxit, tolerance );

        return std::make_pair( DoubleVector { std::move( solution ) }, residuals );
    };

    m.def( "internalCG", internalCGF );
    m.def( "internalBiCGStab", internalBiCGStabF );

    m.def( "noPreconditioner", []( size_t size ){ return 
           LinearOperatorWrapper { linalg::makeNoPreconditioner( size ) }; },
           pybind11::arg( "size" ) );

    m.def( "diagonalPreconditioner", []( const linalg::AbsSparseMatrix& matrix )
           { return LinearOperatorWrapper { linalg::makeDiagonalPreconditioner( matrix ) }; },
           pybind11::arg( "matrix" ) );

    m.def( "fill", []( linalg::AbsSparseMatrix& matrix, double value )
           { std::fill( matrix.data( ), matrix.data( ) + matrix.nnz( ), value ); },
           pybind11::arg( "matrix" ), pybind11::arg( "value" ) = 0.0 );

    m.def( "fill", []( DoubleVector& vector, double value )
           { std::fill( vector.get( ).begin( ), vector.get( ).end( ), value ); },
           pybind11::arg( "matrix" ), pybind11::arg( "value" ) = 0.0 );
    
    auto copyF =[]( const DoubleVector& vectorWrapper, double scaling, double offset ) -> DoubleVector
    { 
        auto vector = vectorWrapper.get( );

        for( auto& entry : vector )
        {
            entry = scaling * entry + offset;
        }

        return vector;
    };

    m.def( "copy", copyF, pybind11::arg( "vector" ), pybind11::arg( 
        "scaling" ) = 1.0, pybind11::arg( "offset" ) = 0.0 );

    m.def( "norm", []( const DoubleVector& vector )
           { return std::sqrt( std::inner_product( vector.get( ).begin( ), 
                vector.get( ).end( ), vector.get( ).begin( ), 0.0 ) );; },
           pybind11::arg( "vector" ) );
    
    m.def( "split", splitF, pybind11::arg( "vector" ), pybind11::arg( "indices" ) );

    m.def( "add", []( const DoubleVector& vector1, 
                      const DoubleVector& vector2, 
                      double factor ) -> DoubleVector
           { 
               MLHP_CHECK( vector1.get( ).size( ) == vector2.get( ).size( ),
                           "Inconsistent vector sizes in addition." );

               auto result = std::vector<double>( vector1.get( ).size( ) );

               std::transform( vector1.get( ).begin( ), vector1.get( ).end( ), 
                    vector2.get( ).begin( ), result.begin( ), 
                    [=]( double v1, double v2 ) { return v1 + factor * v2; } );

               return result;
           },
           pybind11::arg( "vector1" ), pybind11::arg( "vector2" ),
           pybind11::arg( "factor" ) = 1.0 );

    
    m.def( "inflateDofs", []( const DoubleVector& interiorDofs,
                              const DofIndicesValuesPair& dirichletDofs ) -> DoubleVector
        { return DoubleVector { boundary::inflate( interiorDofs.get( ), dirichletDofs ) }; }, 
        pybind11::arg( "interiorDofs" ), 
        pybind11::arg( "dirichletDofs" ) );
}

template<size_t D>
void defineBoundaryCondition( pybind11::module& m )
{
    IntegrationOrderDeterminorWrapper<D> defaultDeterminor { makeIntegrationOrderDeterminor<D>( 1 ) };
    
    m.def( "integrateDirichletDofs", [=]( const spatial::VectorFunction<D>& function,
                                          const AbsBasis<D>& basis, std::vector<size_t> faces,
                                          const IntegrationOrderDeterminorWrapper<D>& orderDeterminor )
        { return boundary::boundaryDofs<D>( function, basis, faces, orderDeterminor ); },
        pybind11::arg( "boundaryFunctions" ), pybind11::arg( "basis" ), pybind11::arg( "faces" ), 
        pybind11::arg( "orderDeterminor" ) = defaultDeterminor );

    m.def( "integrateDirichletDofs", [=]( const ScalarFunctionWrapper<D>& function,
                                          const AbsBasis<D>& basis, std::vector<size_t> faces,
                                          const IntegrationOrderDeterminorWrapper<D>& orderDeterminor,
                                          size_t fieldComponent )
        { return boundary::boundaryDofs<D>( function, basis, faces, orderDeterminor, fieldComponent ); }, 
        pybind11::arg( "boundaryFunctions" ), pybind11::arg( "basis" ), pybind11::arg( "faces" ),
        pybind11::arg( "orderDeterminor" ) = defaultDeterminor, pybind11::arg( "ifield" ) = 0 );
}

void definePostprocessingSingle( pybind11::module& m )
{
    pybind11::enum_<PostprocessTopologies>( m, "PostprocessTopologies" )
        .value( "Nothing", PostprocessTopologies::None )
        .value( "Corners", PostprocessTopologies::Corners )
        .value( "Edges", PostprocessTopologies::Edges )
        .value( "Faces", PostprocessTopologies::Faces )
        .value( "Volumes", PostprocessTopologies::Volumes )
        .def( "__or__", []( PostprocessTopologies a,
                            PostprocessTopologies b )
                            { return a | b; } );

    pybind11::class_<OutputMeshPartition, std::shared_ptr<OutputMeshPartition>>( m, "OutputMeshPartition" )
        .def( pybind11::init<>( ) )
        .def( "index", []( const OutputMeshPartition& o ){ return o.index; } )
        .def( "points", []( const OutputMeshPartition& o ){ return o.points; } )
        .def( "connectivity", []( const OutputMeshPartition& o ){ return o.connectivity; } )
        .def( "offsets", []( const OutputMeshPartition& o ){ return o.offsets; } )
        .def( "types", []( const OutputMeshPartition& o ){ return o.types; } );

    pybind11::class_<VtuOutput>( m, "VtuOutput" )
        .def( pybind11::init( []( std::string filename, std::string writemode )
            { return VtuOutput { .filename = filename, .mode = writemode }; } ), 
            pybind11::arg( "filename" ) = "output.vtu",
            pybind11::arg( "writemode" ) = "RawBinaryCompressed" );

    pybind11::class_<PVtuOutput>( m, "PVtuOutput" )
        .def( pybind11::init( []( std::string filename, std::string writemode, size_t maxpartitions )
            { return PVtuOutput { .filename = filename, .mode = writemode, .maxpartitions = maxpartitions }; } ),
            pybind11::arg( "filename" ) = "output.vtu",
            pybind11::arg( "writemode" ) = "RawBinaryCompressed",
            pybind11::arg( "maxpartitions" ) = 2 * parallel::getMaxNumberOfThreads( ) );
    
    pybind11::class_<DataAccumulator, std::shared_ptr<DataAccumulator>>( m, "DataAccumulator" )
        .def( pybind11::init<>( ) )
        .def( "mesh", []( const DataAccumulator& d ){ return *d.mesh; } )
        .def( "data", []( const DataAccumulator& d ){ return *d.data; } );
}

template<size_t D>
using ElementProcessorSharedPtr = std::shared_ptr<ElementProcessor<D>>;

template<size_t D>
using CellProcessorSharedPtr = std::shared_ptr<CellProcessor<D>>;

template<size_t D>
void definePostprocessingDimensions( pybind11::module& m )
{
    pybind11::class_<ElementProcessor<D>, std::shared_ptr<ElementProcessor<D>>>
        ( m, add<D>( "ElementProcessor" ).c_str( ) );

    pybind11::class_<CellProcessor<D>, std::shared_ptr<CellProcessor<D>>>
        ( m, add<D>( "CellProcessor" ).c_str( ) );

    m.def( "functionProcessor", []( const ScalarFunctionWrapper<D>& function,
                                    const std::string& name )
           { return std::make_shared<CellProcessor<D>>(
                   makeFunctionProcessor<D>( function.get( ), name ) ); },
           pybind11::arg( "function" ), pybind11::arg( "name" ) );

    m.def( "functionProcessor", []( const ImplicitFunctionWrapper<D>& function,
                                    const std::string& name )
           { return std::make_shared<CellProcessor<D>>(
                   makeFunctionProcessor<D>( function.get( ), name ) ); },
           pybind11::arg( "function" ), pybind11::arg( "name" ) = "Domain" );

    m.def( "vonMisesProcessor", []( const DoubleVector& dofs,
                                    const Kinematics<D>& kinematics,
                                    const Constitutive<D>& constitutive,
                                    const std::string& name )
        { 
            return std::make_shared<ElementProcessor<D>>( 
                makeVonMisesProcessor<D>( dofs.get( ), kinematics, constitutive, name ) );
        }, 
        pybind11::arg( "dofs" ), pybind11::arg( "kinematics" ), pybind11::arg( "contitutive" ),
        pybind11::arg( "name" ) = "VonMisesStress" );
     
    auto defDerivativeProcessor = [&]( const std::string& functionName,
                                       const std::string& fieldName,
                                       auto&& create )
    {
        auto stressProcessorF = [=]( std::array<std::shared_ptr<DoubleVector>, D> gradient,
                                     const Kinematics<D>& kinematics,
                                     const Constitutive<D>& constitutive,
                                     const std::string& name )
        {
            auto gradientSpan = std::array<std::span<const double>, D> { };

            for( size_t axis = 0; axis < D; ++axis )
            {
                gradientSpan[axis] = gradient[axis]->get( );
            }

            return create( gradientSpan, kinematics, constitutive, name );
        };

        m.def( functionName.c_str( ), stressProcessorF, pybind11::arg( "gradient" ), 
            pybind11::arg( "kinematics" ), pybind11::arg( "constitutive" ), 
            pybind11::arg( "name" ) = fieldName );
    };

    auto stressF = []( auto&&... args ) { return makeStressProcessor<D>( args... ); };
    auto vonMisesF = []( auto&&... args ) { return makeVonMisesProcessor<D>( args... ); };
    auto strainF = []( auto&&... args ) { return makeStrainProcessor<D>( args... ); };
    auto strainEnergyF = []( auto&&... args ) { return makeStrainEnergyProcessor<D>( args... ); };

    defDerivativeProcessor( "stressProcessor", "Stress", stressF );
    defDerivativeProcessor( "vonMisesProcessor", "VonMisesStress", vonMisesF );
    defDerivativeProcessor( "strainProcessor", "Strain", strainF );
    defDerivativeProcessor( "strainEnergyProcessor", "StrainEnergyDensity", strainEnergyF );

    if constexpr( D <= 3 )
    {
        defineFunctionWrapper<CellMeshCreator<D>>( m, add<D>( "PostprocessingMeshCreator" ).c_str( ) );

        auto define1 = [&]<typename WriterType>( )
        {
            auto defaultMesh = wrapFunction( cellmesh::createGrid<D>( array::makeSizes<D>( 1 ) ) );

            m.def( "internalWriteBasisOutput", []( const AbsBasis<D>& basis,
                                                   const CellMeshCreatorWrapper<D>& postmesh,
                                                   WriterType& writer,
                                                   std::vector<ElementProcessor<D>>&& processors )
            {
                writeOutput( basis, postmesh.get( ), mergeProcessors( std::move( processors ) ), writer );
            },
            pybind11::arg( "basis" ), pybind11::arg( "postmesh" ) = defaultMesh,
            pybind11::arg( "writer" ), pybind11::arg( "processors" ) = std::vector<ElementProcessor<D>>{ } );

            m.def( "internalWriteMeshOutput", []( const AbsMesh<D>& mesh,
                                                  const CellMeshCreatorWrapper<D>& postmesh,
                                                  WriterType& writer,
                                                  std::vector<CellProcessor<D>>&& processors )
            {
                writeOutput( mesh, postmesh.get( ), mergeProcessors( std::move( processors ) ), writer );
            },
            pybind11::arg( "mesh" ), pybind11::arg( "postmesh" ) = defaultMesh,
            pybind11::arg( "writer" ), pybind11::arg( "processors" ) = std::vector<CellProcessor<D>>{ } );
        };
        
        define1.template operator()<DataAccumulator>( );
        define1.template operator()<VtuOutput>( );
        define1.template operator()<PVtuOutput>( );

        m.def( "convertToElementProcessor", []( CellProcessor<D> processor ) { return
            convertToElementProcessor<D>( std::move( processor ) ); }, pybind11::arg( "elementProcessor" ) );
        
        defineFunctionWrapper<ResolutionDeterminor<D>>( m, add<D>( "ResolutionDeterminor" ).c_str( ) );

        auto instantiateResoluton = [&]<typename Resolution>( )
        {
            auto createGridOnCellsF = []( Resolution resolution,
                                          PostprocessTopologies topologies )
            {
                return CellMeshCreatorWrapper<D> { cellmesh::createGrid<D>( resolution, topologies ) };
            };

            m.def( "gridOnCells", createGridOnCellsF, pybind11::arg( "resolution" ), 
                   pybind11::arg( "topologies" ) = defaultOutputTopologies[D] );

            if constexpr ( D == 3 )
            {   
                auto createMarchingCubesBoundaryF = []( const ImplicitFunctionWrapper<D>& function,
                                                        Resolution resolution,
                                                        bool recoverMeshBoundaries )
                {
                    return CellMeshCreatorWrapper<D> { cellmesh::marchingCubesBoundary( 
                        function, resolution, recoverMeshBoundaries ) };
                };
        
                auto createMarchingCubesVolumeF = []( const ImplicitFunction<D>& function,
                                                      Resolution resolution )
                {
                    return CellMeshCreatorWrapper<D> { 
                        cellmesh::marchingCubesVolume( function, resolution ) };
                };

                m.def( "marchingCubesBoundary", createMarchingCubesBoundaryF, pybind11::arg( "function" ),
                        pybind11::arg( "resolution" ), pybind11::arg( "recoverMeshBoundaries" ) = true );
                m.def( "marchingCubesVolume", createMarchingCubesVolumeF, 
                        pybind11::arg( "function" ), pybind11::arg( "resolution" ) );
            }
        };

        instantiateResoluton.template operator()<std::array<size_t, D>>( );
        instantiateResoluton.template operator()<ResolutionDeterminorWrapper<D>>( );

        auto degreeOffsetResolutionF = []( BasisConstSharedPtr<D> basis, size_t offset, bool exceptLinear )
        {
            return ResolutionDeterminorWrapper<D> { degreeOffsetResolution<D>( *basis, offset, exceptLinear ) };
        };

        m.def( "degreeOffsetResolution", degreeOffsetResolutionF, pybind11::arg("basis"),
            pybind11::arg( "offset" ) = 2, pybind11::arg( "exceptLinear" ) = true );

        auto quadraturePointCellMeshF1 = []( const AbsQuadrature<D>& quadrature, const AbsBasis<D>& basis,
                                             const IntegrationOrderDeterminorWrapper<D>& determinor )
        {
            return CellMeshCreatorWrapper<D> { cellmesh::quadraturePoints( quadrature, basis, determinor.get( ) ) };
        };
        
        auto quadraturePointCellMeshF2 = []( const AbsQuadratureOnMesh<D>& quadrature )
        {
            return CellMeshCreatorWrapper<D> { cellmesh::quadraturePoints( quadrature ) };
        };

        m.def( "quadraturePointCellMesh", quadraturePointCellMeshF1, pybind11::arg( "quadrature" ), 
               pybind11::arg( "basis" ), pybind11::arg( "orderDeterminor" ) = 
               IntegrationOrderDeterminorWrapper<D> { makeIntegrationOrderDeterminor<D>( ) } );

        m.def( "quadraturePointCellMesh", quadraturePointCellMeshF2, pybind11::arg( "quadrature" ) );
    }
}

void definePostprocessingSingle2( pybind11::module& m )
{
    auto solutionProcessorF = []( size_t ndim, const DoubleVector& dofs, const std::string& name )
    { 
        using ElementProcessorVariant = DimensionVariant<ElementProcessorSharedPtr>;

        auto create = [&]<size_t D>( ) -> ElementProcessorVariant
        { 
            return std::make_shared<ElementProcessor<D>>( makeSolutionProcessor<D>( dofs.get( ), name ) );
        };

        return dispatchDimension( create, ndim );
    };

    m.def( "solutionProcessor", solutionProcessorF, pybind11::arg( "ndim" ), 
        pybind11::arg( "dofs" ), pybind11::arg( "solutionName" ) = "Solution" );

    auto cellDataProcessorF = []( size_t ndim, const DoubleVector& data, const std::string& name )
    { 
        using CellProcessorVariant = DimensionVariant<CellProcessorSharedPtr>;

        auto create = [&]<size_t D>( ) -> CellProcessorVariant
        { 
            return std::make_shared<CellProcessor<D>>( makeCellDataProcessor<D>( data.get( ), name ) );
        };

        return dispatchDimension( create, ndim );
    };

    m.def( "cellDataProcessor", cellDataProcessorF, pybind11::arg( "ndim" ), 
        pybind11::arg( "data" ), pybind11::arg( "name" ) = "CellData" );
}

void defineConfig( pybind11::module& m )
{
    struct Config { };

    auto conf = pybind11::class_<Config>( m, "config" );

    conf.def_property_readonly_static( "commitId",        []( pybind11::object ) { return std::string { config::commitId        }; } );
    conf.def_property_readonly_static( "osName",          []( pybind11::object ) { return std::string { config::osName          }; } );
    conf.def_property_readonly_static( "osVersion",       []( pybind11::object ) { return std::string { config::osVersion       }; } );
    conf.def_property_readonly_static( "architecture",    []( pybind11::object ) { return std::string { config::architecture    }; } );
    conf.def_property_readonly_static( "compilerId",      []( pybind11::object ) { return std::string { config::compilerId      }; } );
    conf.def_property_readonly_static( "compilerVersion", []( pybind11::object ) { return std::string { config::compilerVersion }; } );
    conf.def_property_readonly_static( "compileDate",     []( pybind11::object ) { return std::string { __DATE__                }; } );
    conf.def_property_readonly_static( "compileTime",     []( pybind11::object ) { return std::string { __TIME__                }; } );
    conf.def_property_readonly_static( "threading",       []( pybind11::object ) { return std::string { config::threading       }; } );
    conf.def_property_readonly_static( "maxdim",          []( pybind11::object ) { return config::maxdim; } );
    conf.def_property_readonly_static( "simdAlignment",   []( pybind11::object ) { return config::simdAlignment; } );
    conf.def_property_readonly_static( "debugChecks",     []( pybind11::object ) { return config::debugChecks; } );

    auto str = []( pybind11::object )
    { 
        auto sstream = std::ostringstream { };
        auto debugChecks = config::debugChecks ? std::string { "On" } : std::string { "Off" };

        sstream << "MLHP python bindings\n";
        sstream << "    Commit ID         : " << config::commitId        << "\n";
        sstream << "    OS name           : " << config::osName          << "\n";
        sstream << "    OS version        : " << config::osVersion       << "\n";
        sstream << "    Architecture      : " << config::architecture    << "\n";
        sstream << "    Compiler ID       : " << config::compilerId      << "\n";
        sstream << "    Compiler version  : " << config::compilerVersion << "\n";
        sstream << "    Compilation date  : " << __DATE__                << "\n";
        sstream << "    Compilation time  : " << __TIME__                << "\n";
        sstream << "    Multi-threading   : " << config::threading       << "\n";
        sstream << "    Highest dimension : " << config::maxdim          << "\n";
        sstream << "    SIMD alignment    : " << config::simdAlignment   << "\n";
        sstream << "    Debug checks      : " << debugChecks << "\n";

        return sstream.str( );
    };

    auto call = [=]( pybind11::object obj )
    {
        pybind11::print( str( obj ) );
    };

    conf.def( "__str__", str );
    conf.def( "__call__", call );

    static constexpr Config obj;

    m.attr( "config" ) = &obj;
}

void defineDimensionIndendent( pybind11::module& m )
{    
    pybind11::enum_<CellType>( m, "CellType" )
        .value( "NCube", CellType::NCube )
        .value( "Simplex", CellType::Simplex );
    
    m.def( "combineDirichletDofs", &boundary::combine, pybind11::arg( "boundaryDofs" ) );

    defineFunctionWrappersSingle( m );
    defineBasisSingle( m );
    definePostprocessingSingle( m );
    defineConfig( m );
}

template<size_t D>
void defineDimension( pybind11::module& m )
{
    defineGrid<D>( m );
    defineMesh<D>( m );
    defineBasis<D>( m );
    definePartitioners<D>( m );
    defineIntegrands<D>( m );
    defineBoundaryCondition<D>( m );
    definePostprocessingDimensions<D>( m );
}

template<size_t... D>
void defineDimensions( pybind11::module& m, std::index_sequence<D...>&& )
{
    [[maybe_unused]] std::initializer_list<int> tmp { ( defineDimension<D + 1>( m ), 0 )... };
}

void bindDiscretization( pybind11::module& m )
{
    defineDimensionIndendent( m );

    defineDimensions( m, std::make_index_sequence<config::maxdim>( ) );

    defineIntegrandsSingle( m );
    definePartitionersSingle( m );
    definePostprocessingSingle2( m );
    
    bindLinalg( m );
}

} // mlhp::bindings

