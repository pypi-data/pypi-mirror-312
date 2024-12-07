// This file is part of the mlhpbf project. License: See LICENSE

#ifndef MLHPBF_HISTORY_HPP
#define MLHPBF_HISTORY_HPP

#include "mlhp/core.hpp"

namespace mlhp
{

template<size_t D, typename T>
struct HistoryContainer
{
    using Initialize = std::function<T( std::array<double, D> xyz )>;

    HistoryContainer( ) :
        grid { makeRefinedGrid<D>( array::makeSizes<D>( 1 ), array::make<D>( 1.0 ) ) },
        data ( 1, T { } ), maxdepth { 0 },
        backwardMappings { mesh::threadLocalBackwardMappings( *grid ) }
    { }

    HistoryContainer( const HierarchicalGridSharedPtr<D>& grid_,
                      const Initialize& initialize,
                      RefinementLevel maxdepth_ ) :
        grid { grid_ }, data( grid_->ncells( ) ), maxdepth { maxdepth_ }, 
        backwardMappings { mesh::threadLocalBackwardMappings( *grid ) }
    { 
        auto ncells = static_cast<std::int64_t>( grid->ncells( ) );

        #pragma omp parallel
        {
            auto mapping = grid->createMapping( );

            #pragma omp for
            for( std::int64_t ii = 0; ii < ncells; ++ii )
            {
                auto icell = static_cast<CellIndex>( ii );

                grid->prepareMapping( icell, mapping );

                data[icell] = initialize( mapping( { } ) );
            }
        }
    }

    HistoryContainer( const HierarchicalGridSharedPtr<D>& grid_, 
                      RefinementLevel maxdepth_,
                      std::vector<T>&& data_ ) :
        grid { grid_ }, data( std::move( data_ ) ), maxdepth { maxdepth_ }, 
        backwardMappings { mesh::threadLocalBackwardMappings( *grid ) }
    { 
        MLHP_CHECK( grid->ncells( ) == data.size( ), "Inconsistent history array size." );
    }

    T* operator() ( std::array<double, D> xyz )
    {
        if( auto result = backwardMappings.get( )->map( xyz ); result)
        {
            return &data[result->first];
        }
        else
        {
            return nullptr;
        }
    }

    const T* operator() ( std::array<double, D> xyz ) const
    {
        return const_cast<HistoryContainer*>( this )->operator() ( xyz );
    }

    HierarchicalGridSharedPtr<D> grid;
    std::vector<T> data;
    RefinementLevel maxdepth;
    ThreadLocalBackwardMappings<D> backwardMappings;
};

struct HistoryData
{
    MaterialType materialType;
};

template<size_t D>
using ThermoplasticHistory = HistoryContainer<D, HistoryData>;

template<size_t D> inline
ThermoplasticHistory<D> createNewHistory( auto&& materialInitializer,
                                          const GridConstSharedPtr<D>& baseGrid,
                                          size_t nseedpoints,
                                          size_t maxdepth )
{
    auto refinement = [&]( const MeshMapping<D>& mapping, 
                           RefinementLevel level )
    {
        auto refine = false;

        if( level < maxdepth )
        {
            auto pointsPerDirection = array::make<D>( nseedpoints );
            auto rstGenerator = spatial::makeRstGenerator( pointsPerDirection, 1.0 - 1e-6 );
            auto ijk0 = array::makeSizes<D>( 0 );
            auto initialType = materialInitializer( mapping.map( rstGenerator( ijk0 ) ) );

            nd::execute( pointsPerDirection, [&]( std::array<size_t, D> ijk )
            {
                if( refine == false && ijk != ijk0 )
                {
                    auto xyz = mapping.map( rstGenerator( ijk ) );

                    refine = materialInitializer( xyz ) != initialType;
                }
            } );
        }

        return refine;
    };

    auto grid = makeRefinedGrid<D>( baseGrid->cloneGrid( ) );

    grid->refine( refinement );

    auto initialize = [&]( std::array<double, D> xyz )
    {
        return HistoryData { .materialType = materialInitializer( xyz ) };
    };

    return ThermoplasticHistory<D>( grid, initialize, static_cast<RefinementLevel>( maxdepth ) );
}

template<size_t D> inline
ThermoplasticHistory<D> initializeHistory( const GridSharedPtr<D>& baseGrid,
                                           const ImplicitFunction<D>& part,
                                           double powderHeight,
                                           size_t nseedpoints, 
                                           size_t maxdepth ) 
{
    auto materialInitializer = [=]( std::array<double, D> xyz )
    {
        if( xyz[2] <= 0.0 )
        {
            return MaterialType::BasePlate;
        }
        else if( xyz[2] > powderHeight )
        {
            return MaterialType::Air;
        }
        else
        {
            return part( xyz ) ? MaterialType::Structure : MaterialType::Powder;
        }
    };

    return createNewHistory<D>( materialInitializer, baseGrid, nseedpoints, maxdepth );
}

template<size_t D> inline
ThermoplasticHistory<D> initializeHistory( const GridSharedPtr<D>& baseGrid,
                                           double powderHeight,
                                           size_t maxdepth ) 
{
    return initializeHistory<D>( baseGrid, utilities::returnValue( false ), powderHeight, 4, maxdepth );
}

namespace
{

template<size_t D> inline
auto updateMeltState( const MultilevelHpBasis<D>& tbasis, 
                      const std::vector<double>& tdofs, 
                      const AbsHierarchicalGrid<D>& grid,
                      std::vector<int>& meltstate,
                      double meltingTemperature,
                      size_t maxdepth,
                      size_t degree )
{
    auto abovecount = std::vector<size_t>( grid.ncells( ), 0 );
    auto belowcount = std::vector<size_t>( grid.ncells( ), 0 );
    auto ntelements = tbasis.nelements( );
    //auto levels = mesh::refinementLevels( grid );

    // Determine cells inside melt pool
    #pragma omp parallel
    {
        auto subcells = std::vector<mesh::SharedSupport<D>> { };
        auto shapes = BasisFunctionEvaluation<D> { };
        auto cache = tbasis.createEvaluationCache( );
        auto locationMap = LocationMap { };
        auto seedgrid = CoordinateGrid<D> { };
        auto seedbounds = std::array { array::make<D>( 2.0 ), array::make<D>( -1.0 ) };

        #pragma omp for schedule(dynamic)
        for( std::int64_t ii = 0; ii < static_cast<std::int64_t>( ntelements ); ++ii )
        {
            auto icell = static_cast<CellIndex>( ii );

            utilities::resize0( subcells, locationMap );

            mesh::findInOtherGrid( tbasis.hierarchicalGrid( ), grid,
                subcells, tbasis.hierarchicalGrid( ).fullIndex( icell ) );

            // If none of the history grid cells are to be checked
            bool skip = true;

            for( auto& subcell : subcells )
            {
                if( meltstate[grid.leafIndex( subcell.otherIndex )] == -1 )
                {
                    skip = false;
                    break;
                }
            }

            if( skip ) continue;

            // Otherwise prepare to evaluate this element
            tbasis.prepareEvaluation( icell, 0, shapes, cache );
            tbasis.locationMap( icell, locationMap );

            for( CellIndex isubcell = 0; isubcell < subcells.size( ); ++isubcell )
            {
                auto hindex = grid.leafIndex( subcells[isubcell].otherIndex );

                if( meltstate[hindex] != -1 ) continue;

                auto evaluateBounds = [&]( size_t npoints )
                {
                    spatial::cartesianTickVectors( array::makeSizes<D>( npoints - 1 ), 
                        seedbounds[0], seedbounds[1], seedgrid );

                    subcells[isubcell].thisCell.mapGrid( seedgrid );

                    tbasis.prepareGridEvaluation( seedgrid, cache );

                    auto Tmin = std::numeric_limits<double>::max( );
                    auto Tmax = std::numeric_limits<double>::lowest( );
                    auto limits = array::makeSizes<D>( npoints );

                    nd::execute( limits, [&]( std::array<size_t, D> ijk )
                    {
                        tbasis.evaluateGridPoint( ijk, shapes, cache );
                                    
                        auto T = evaluateSolution( shapes, locationMap, tdofs );
                                
                        Tmin = std::min( Tmin, T );
                        Tmax = std::max( Tmax, T );
                    } );

                    return std::tuple { Tmin, Tmax };
                };

                auto [Tmin, Tmax] = evaluateBounds( degree + 1 );

                // Evaluate again if bound is close to melting
                if( degree > 1 )
                {
                    if( ( Tmin < 1.5 * meltingTemperature && Tmin > meltingTemperature ) ||
                        ( Tmax > 0.5 * meltingTemperature && Tmax < meltingTemperature ) )
                    {
                        std::tie( Tmin, Tmax ) = evaluateBounds( degree + 4 );
                    }
                }

                if( Tmin < meltingTemperature )
                {
                    #pragma omp atomic
                    belowcount[hindex] += 1;
                }

                if( Tmax >= meltingTemperature )
                {
                    #pragma omp atomic
                    abovecount[hindex] += 1;
                }
            }
        }
    } // omp parallel

    for( CellIndex i = 0; i < abovecount.size( ); ++i )
    {
        if( meltstate[i] == -1 )
        {
            auto meltint = static_cast<int>( abovecount[i] > 0 ) - static_cast<int>( belowcount[i] > 0 );

            if( meltint == 0 && grid.refinementLevel( grid.fullIndex( i ) ) < maxdepth )
            {
                meltstate[i] = -1;
            }
            else
            {
                meltstate[i] = meltint >= 0 ? static_cast<int>( MaterialType::Structure ) : static_cast<int>( MaterialType::Powder );
            }
        }
    }

    return meltstate;
}


template<size_t D> inline
auto interpolateNewMaterialState( const AbsHierarchicalGrid<D>& previousHistoryGrid,
                                  const AbsHierarchicalGrid<D>& newGrid,
                                  const std::vector<int>& materialstate )
{
    auto ncells = newGrid.ncells( );
    auto newstate = std::vector<int>( ncells, 0 );

    #pragma omp parallel
    {
        auto subcells = std::vector<mesh::SharedSupport<D>> { };

        #pragma omp for
        for( std::int64_t ii = 0; ii < static_cast<std::int64_t>( ncells ); ++ii )
        {
            auto icell = static_cast<CellIndex>( ii );

            mesh::findInOtherGrid( newGrid, previousHistoryGrid,
                utilities::resize0( subcells ), newGrid.fullIndex( icell ) );

            newstate[icell] = materialstate[previousHistoryGrid.leafIndex( subcells[0].otherIndex )];
        }
    } // pragma omp parallel

    return newstate;
}

    
template<size_t D> inline
auto adaptGridAndMeltstate( const AbsHierarchicalGrid<D>& previousHistoryGrid,
                            const std::vector<int>& meltstate )
{
    auto adapt = std::vector<int>( previousHistoryGrid.ncells( ), 0 );
    auto nroots = previousHistoryGrid.baseGrid( ).ncells();

    auto recursive = [&]( auto&& self, CellIndex ifull ) -> std::pair<int, bool>
    {
        if( auto child = previousHistoryGrid.child( ifull, { } ); child != NoCell )
        {
            auto tmp = self( self, child );
            auto value = std::get<0>( tmp );
            auto coarsen = std::get<1>( tmp );
            auto limits = array::make<D>( LocalPosition { 2 } );
               
            // Determine material values of children are equal
            nd::execute( limits, [&, value=value]( auto ijk )
            {
                if( ijk != std::array<LocalPosition, D> { } )
                {
                    auto [valueI, coarsenI] = self( self, previousHistoryGrid.child( ifull, ijk ) );

                    coarsen = coarsen && coarsenI && ( valueI == value );
                }
            } );

            if( coarsen )
            {
                nd::execute( limits, [&]( auto ijk )
                {
                    if( auto child2 = previousHistoryGrid.child( ifull, ijk ); previousHistoryGrid.isLeaf( child2 ) )
                    {
                        adapt[previousHistoryGrid.leafIndex( child2 )] = std::numeric_limits<int>::min( );
                    }
                } );
            }

            return { value, coarsen };
        }
        else
        {
            auto ileaf = previousHistoryGrid.leafIndex( ifull );

            adapt[ileaf] = static_cast<int>( meltstate[ileaf] == -1 );

            return { meltstate[ileaf], meltstate[ileaf] != -1 };
        }
    };

    //auto t0 = utilities::tic( );
    #pragma omp parallel for schedule(dynamic, 512)
    for( std::int64_t iroot = 0; iroot < static_cast<std::int64_t>( nroots ); ++iroot )
    {
        recursive( recursive, static_cast<CellIndex>( iroot ) );
    }

    //auto t1 = utilities::toc( t0, "=================================== Second a: " );
    auto newGrid = makeRefinedGrid( previousHistoryGrid, adapt );

    //auto t2 = utilities::toc( t1, "=================================== Second b: " );
    auto newmeltstate = interpolateNewMaterialState( previousHistoryGrid, *newGrid, meltstate );

    //utilities::toc( t2, "=================================== Second c: " );
    return std::pair { std::move( newGrid ), std::move( newmeltstate ) };
}

// For Debugging
template<size_t D, typename T>
void postprocessHistory( const AbsHierarchicalGrid<D>& grid,
                         const std::vector<T>& data,
                         std::string name )
{ 
    auto writer = VtuOutput { name };
    auto meshcreator = cellmesh::createGrid<D>( array::makeSizes<D>( 1 ), PostprocessTopologies::Volumes );
    auto converted = std::vector<double>( data.size( ) );

    for( size_t i = 0; i < data.size( ); ++i )
    {
        if constexpr ( std::is_same_v<T, HistoryData> )
        {
            converted[i] = static_cast<double>( data[i].materialType );
        }
        else
        {
            converted[i] = static_cast<double>( data[i] );
        }
    }

    auto processor = makeCellDataProcessor<D>( converted );
    
    writeOutput( grid, meshcreator, processor, writer );
}

} // namespace

template<size_t D> inline
auto updateHistory( const ThermoplasticHistory<D>& history_,
                    const MultilevelHpBasis<D>& tbasis, 
                    const std::vector<double>& tdofs,
                    double meltingTemperature,
                    size_t degree )
{
    auto newGrid = history_.grid;
    auto meltstate = std::vector<int>( newGrid->ncells( ) );

    for( CellIndex i = 0; i < newGrid->ncells( ); ++i )
    {
        meltstate[i] = history_.data[i].materialType == MaterialType::Powder ?
            -1 : static_cast<int>( history_.data[i].materialType );
    }

    //std::cout << std::endl;
    //size_t it = 0;
    while( std::find( meltstate.begin( ), meltstate.end( ), -1 ) != meltstate.end( ) )
    {
        //std::cout << "Refinement iteration " << it << ": " << newGrid->ncells( ) << " cells" << std::endl;
        //postprocessHistory( *newhist.grid, newhist.data, "history_01_initial_" + std::to_string(it) + ".vtu" );
        //postprocessHistory( *newhist.grid, meltstate, "history_02_meltstate_before_" + std::to_string( it ) + ".vtu" );

        //auto t0 = utilities::tic( );
        updateMeltState( tbasis, tdofs, *newGrid, meltstate, meltingTemperature, history_.maxdepth, degree );

        //postprocessHistory( *newhist.grid, meltstate, "history_03_meltstate_after_" + std::to_string( it ) + ".vtu" );

        //auto t1 = utilities::toc( t0, "=================================== First: " );
        std::tie( newGrid, meltstate ) = adaptGridAndMeltstate( *newGrid, meltstate );

        //utilities::toc( t1, "=================================== Second: " );
        //postprocessHistory( *newhist.grid, newhist.data, "history_04_newhistory_" + std::to_string( it ) + ".vtu" );

        //if( it > 10 ) break;
        //it += 1;
    }

    //std::cout << std::endl;
    auto newdata = std::vector<HistoryData>( meltstate.size( ) );

    for( size_t i = 0; i < newdata.size( ); ++i )
    {
        newdata[i] = HistoryData { static_cast<MaterialType>( meltstate[i] ) };
    }

    return ThermoplasticHistory<D>( newGrid, history_.maxdepth, std::move( newdata ) );
}


namespace
{

template<size_t D> inline
ThermoplasticHistory<D> createNewHistoryAndInterpolate( const ThermoplasticHistory<D>& oldHistory,
                                                        const std::vector<int>& indicator )
{
    auto newGrid = makeRefinedGrid( *oldHistory.grid, indicator );
    auto ncells = newGrid->ncells( );
    auto newData = std::vector<HistoryData>( ncells );

    #pragma omp parallel
    {
        auto subcells = std::vector<mesh::SharedSupport<D>> { };

        #pragma omp for
        for( std::int64_t ii = 0; ii < static_cast<std::int64_t>( ncells ); ++ii )
        {
            auto icell = static_cast<CellIndex>( ii );

            mesh::findInOtherGrid( *newGrid, *oldHistory.grid, 
                utilities::resize0( subcells ), newGrid->fullIndex( icell ) );

            newData[icell] = oldHistory.data[oldHistory.grid->leafIndex( subcells[0].otherIndex )];
        }
    } // pragma omp parallel

    return ThermoplasticHistory<D>( newGrid, oldHistory.maxdepth, std::move( newData ) );
}

template<size_t D> inline
ThermoplasticHistory<D> coarsenHistory( const ThermoplasticHistory<D>& fineHistory )
{
    auto adapt = std::vector<int>( fineHistory.grid->ncells( ), 0 );
    auto nroots = fineHistory.grid->baseGrid( ).ncells();

    auto recursive = [&]( auto&& self, CellIndex ifull ) -> std::pair<HistoryData, bool>
    {
        if( auto child = fineHistory.grid->child( ifull, { } ); child != NoCell )
        {
            auto tmp = self( self, child );
            auto value = std::get<0>( tmp );
            auto coarsen = std::get<1>( tmp );
            auto limits = array::make<D>( LocalPosition { 2 } );
                    
            // Determine material values of children are equal
            nd::execute( limits, [&, value=value]( auto ijk )
            {
                if( ijk != std::array<LocalPosition, D> { } )
                {
                    auto [valueI, coarsenI] = self( self, fineHistory.grid->child( ifull, ijk ) );

                    coarsen = coarsen && coarsenI && ( valueI.materialType == value.materialType );
                }
            } );

            if( coarsen )
            {
                nd::execute( limits, [&]( auto ijk )
                {
                    if( auto child2 = fineHistory.grid->child( ifull, ijk ); fineHistory.grid->isLeaf( child2 ) )
                    {
                        adapt[fineHistory.grid->leafIndex( child2 )] = std::numeric_limits<int>::min( );
                    }
                } );
            }

            return { value, coarsen };
        }
        else
        {
            return { fineHistory.data[fineHistory.grid->leafIndex( ifull )], true };
        }
    };

    for( CellIndex iroot = 0; iroot < nroots; ++iroot )
    {
        recursive( recursive, iroot );
    }

    return createNewHistoryAndInterpolate( fineHistory, adapt );
}
                    
} // namespace

template<size_t D> inline
auto initializeNewLayerHistory( const ThermoplasticHistory<D>& oldHistory,
                                double layerThickness,
                                double supportHeight,
                                size_t layer,
                                size_t nseedpoints )
{
    double oldLayerHeight = layer * layerThickness + supportHeight;
    double newLayerHeight = oldLayerHeight + layerThickness;

    auto materialInitializer = [=]( std::array<double, D> xyz )
    {
        if( xyz[2] >= oldLayerHeight && xyz[2] < newLayerHeight )
        {
            return MaterialType::Powder;
        }
        else
        {
            return oldHistory( xyz )->materialType;
        }
    };

    auto baseGrid = oldHistory.grid->baseGridPtr( );
    auto newLayerHistory = createNewHistory<D>( materialInitializer, baseGrid, nseedpoints, oldHistory.maxdepth );

    // Coarsen history cells with equal material 
    return coarsenHistory( newLayerHistory );
}


} // namespace mlhp

#endif // MLHPBF_HISTORY_HPP
