// This file is part of the mlhpbf project. License: See LICENSE

#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"

#include "mlhp/pbf.hpp"
#include "external/mlhp/src/python/pymlhpcore.hpp"

namespace mlhp::bindings
{

PYBIND11_MODULE( pymlhpbf, m )
{
    m.doc( ) = "Work-in-progress part-scale powder bed fusion simulation.";

    // Base grid
    auto createBaseMeshTicksF = []( std::array<double, 3> min, std::array<double, 3> max, 
                                    double elementSize, double layerHeight, double zfactor )
    {
        return createBaseMeshTicks<3>( { min, max }, elementSize, layerHeight, zfactor );
    };
     
    m.def( "createMeshTicks", createBaseMeshTicksF, 
        pybind11::arg( "min" ), 
        pybind11::arg( "max" ),
        pybind11::arg( "elementSize" ), 
        pybind11::arg( "layerHeight" ) = 0.0, 
        pybind11::arg( "zfactor" ) = 1.0 );

    // Materials
    auto material = pybind11::class_<Material, std::shared_ptr<Material>>( m, "Material" );

    auto bindTemperatureFunction = [&]<typename C, typename D>( const char *name, D C::*pm )
    {
        auto get = [=]( const Material& mat ) {
            return RealFunctionWithDerivativeWrapper { mat.*pm }; };
        
        auto set = [=]( Material& mat, const RealFunctionWithDerivativeWrapper& f ) 
            { mat.*pm = f.get( ); };

        material.def_property( name, get, set );
    };

    material.def( pybind11::init<>( ) );
    material.def( "__str__", []( const Material& self ){ return "Material (name: " + self.name + ")"; } );
    material.def_readwrite( "initialized", &Material::initialized );
    material.def_readwrite( "name", &Material::name );
    bindTemperatureFunction( "density", &Material::density );
    bindTemperatureFunction( "specificHeatCapacity", &Material::specificHeatCapacity );
    bindTemperatureFunction( "heatConductivity", &Material::heatConductivity );
    material.def_readwrite( "solidTemperature", &Material::solidTemperature );
    material.def_readwrite( "liquidTemperature", &Material::liquidTemperature );
    material.def_readwrite( "latentHeatOfFusion", &Material::latentHeatOfFusion );
    material.def_readwrite( "regularization", &Material::regularization );
    bindTemperatureFunction( "thermalExpansionCoefficient", &Material::thermalExpansionCoefficient );
    bindTemperatureFunction( "youngsModulus", &Material::youngsModulus );
    bindTemperatureFunction( "poissonRatio", &Material::poissonRatio );
    bindTemperatureFunction( "yieldStress", &Material::yieldStress );
    bindTemperatureFunction( "hardening", &Material::hardeningParameter );
    material.def_readwrite( "plasticModelSelector", &Material::plasticModelSelector );

    m.def( "readMaterialFile", []( std::string path ) { return readMaterialFile( path ); }, 
        pybind11::arg( "Path to material json file." ) );

    m.def( "readMaterialString", readMaterialString, 
        pybind11::arg( "Json string with material data." ) );

    auto makeMaterialF = []( std::string name ) -> Material
    {
        if( name == "IN625" ) return makeIN625( );
        if( name == "IN718" ) return makeIN718( );
        if( name == "SS316L" ) return makeSS316L( );

        MLHP_THROW( "Unknown material " + name + ". Available are [IN625, IN718, SS316L]." );
    };

    m.def( "makeMaterial", makeMaterialF, pybind11::arg( "name" ) );

    // Laser
    auto laserPosition = pybind11::class_<laser::Point<3>>( m, "LaserPosition" );

    auto laserPositionStr = []( const laser::Point<3>& position )
    {
        auto sstream = std::ostringstream { };

        sstream << "LaserPosition: xyz = " << position.xyz << 
            ", time = " << position.time << ", power = " << position.power << "";

        return sstream.str( );
    };

    laserPosition.def( pybind11::init<std::array<double, 3>, double, double>( ),
                       pybind11::arg( "xyz" ), pybind11::arg( "time" ), pybind11::arg( "power" ) );
    laserPosition.def( "__str__", laserPositionStr );
    laserPosition.def_readwrite( "xyz", &laser::Point<3>::xyz );
    laserPosition.def_readwrite( "time", &laser::Point<3>::time );
    laserPosition.def_readwrite( "power", &laser::Point<3>::power );

    auto gaussianBeamF = []( double sigma, double absorptivity ) -> ScalarFunctionWrapper<2>
    {
        return std::function { spatial::integralNormalizedGaussBell<2>( { }, sigma, absorptivity ) };
    };
    
    m.def( "gaussianBeam", gaussianBeamF, pybind11::arg( "sigma" ), pybind11::arg( "absorptivity" ) = 1.0 );

    auto volumeSourceF = []( const laser::LaserTrack<3>& track,
                             const ScalarFunctionWrapper<2>& beamShape,
                             double depthSigma )
    {
        auto function = ScalarFunctionWrapper<4> { laser::volumeSource<3>( track, beamShape, depthSigma ) };

        return std::pair { std::string { "VolumeSource" }, std::move( function ) };
    };

    auto surfaceSourceF = []( const laser::LaserTrack<3>& track,
                              const ScalarFunctionWrapper<2>& beamShape )
    {
        auto function = ScalarFunctionWrapper<4>{ laser::surfaceSource<3>(track, beamShape) };

        return std::pair { std::string { "SurfaceSource" }, std::move( function ) };
    };
    
    m.def( "volumeSource", volumeSourceF, pybind11::arg( "laserTrack" ), 
        pybind11::arg( "beamShape" ), pybind11::arg( "depthSigma" ) = 1.0 );

    m.def( "surfaceSource", surfaceSourceF, pybind11::arg( "laserTrack" ), pybind11::arg( "beamShape" ) );

    auto refinement = pybind11::class_<laser::Refinement>( m, "LaserRefinementPoint" );

    auto refinementInit = []( double t, double s, double r, double z ) 
    { 
        return laser::Refinement { t, s, r, z }; 
    };

    auto refinementStr = []( laser::Refinement ref )
    {
        auto sstream = std::ostringstream { };

        sstream << "LaserRefinementPoint (" <<
            "delay = " << ref.timeDelay << "," <<
            "sigma = " << ref.sigma << ", " <<
            "depth = " << ref.refinementLevel << ", " <<
            "zfactor = " << ref.zfactor << ")";

        return sstream.str( );
    };

    refinement.def( pybind11::init( refinementInit ),
        pybind11::arg( "delay" ) = 0.0, pybind11::arg( "sigma" ) = 0.0, 
        pybind11::arg( "depth" ) = 0.0, pybind11::arg( "zfactor" ) = 1.0 );

    refinement.def( "__str__", refinementStr );
    refinement.def_readwrite( "delay", &laser::Refinement::timeDelay );
    refinement.def_readwrite( "sigma", &laser::Refinement::sigma );
    refinement.def_readwrite( "depth", &laser::Refinement::refinementLevel );
    refinement.def_readwrite( "zfactor", &laser::Refinement::zfactor );

    auto refineUniformlyF = []( size_t refinementLevel )
    {
        MLHP_CHECK( refinementLevel < NoValue<RefinementLevel> -1, "Invalid refinement level." );

        return RefinementFunctionWrapper<3>{ refineUniformly<3>( static_cast<RefinementLevel>( refinementLevel ) ) };
    };

    m.def( "refineUniformly", refineUniformlyF, pybind11::arg( "maxDepth" ) );

    auto makeRefinementF = []( const laser::LaserTrack<3>& track,
                               const std::vector<laser::Refinement>& refinements,
                               double time, size_t nseedpoints)
    {
        return RefinementFunctionWrapper<3> { laser::makeRefinement<3>( 
            track, refinements, time, nseedpoints ) };
    };

    m.def( "laserTrackPointRefinement", makeRefinementF, pybind11::arg( "laserTrack" ),
        pybind11::arg( "refinements" ), pybind11::arg( "time" ), pybind11::arg( "nseedpoints" ) );

    auto makeRefinementFunctionF = []( const laser::LaserTrack<3>& track,
                                       const std::vector<laser::Refinement>& refinements )
    {
        return ScalarFunctionWrapper<4> { std::function { refinementLevelBasedOnLaserHistory( track, refinements ) } };
    };

    m.def( "laserTrackPointRefinementFunction", makeRefinementFunctionF,
        pybind11::arg( "laserTrack" ), pybind11::arg( "refinements" ) );

    // Thermal history
    auto thermalHistory = pybind11::class_<ThermoplasticHistory<3>, 
        std::shared_ptr<ThermoplasticHistory<3>>>( m, "ThermalHistory" );

    auto thermalHistoryString = []( const ThermoplasticHistory<3>& self )
    {
        auto sstream = std::stringstream { };
        auto memory = self.grid->memoryUsage( ) + utilities::vectorInternalMemory( self.data );

        sstream << "ThermalHistory (address: " << &self << ")\n";
        sstream << "    nleaves / ncells         : " << self.grid->nleaves( ) << " / " << self.grid->ncells( ) << "\n";
        sstream << "    maximum refinement level : " << static_cast<int>( self.maxdepth ) << "\n";
        sstream << "    heap memory usage        : " << utilities::memoryUsageString( memory ) << "\n";

        return sstream.str( );
    };

    auto dataF = []( const ThermoplasticHistory<3>& self )
    {
        auto converted = DoubleVector( self.data.size( ), 0 );
        
        for( size_t i = 0 ; i < self.data.size( ); ++i )
        {
            converted.get( )[i] = static_cast<int>( self.data[i].materialType );
        }

        return converted;
    };

    thermalHistory.def( pybind11::init<>( ) );
    thermalHistory.def( pybind11::init<HierarchicalGridSharedPtr<3>&,
                        RefinementLevel, std::vector<HistoryData>>( ) );
    thermalHistory.def( "__str__", thermalHistoryString );
    thermalHistory.def( "grid", []( const ThermoplasticHistory<3>& history ){ return history.grid; } );
    thermalHistory.def( "data", dataF );

    auto initializeThermalHistoryF = []( const GridSharedPtr<3>& baseGrid,
                                         const ImplicitFunctionWrapper<3>& part,
                                         size_t maxdepth, 
                                         double powderHeight, 
                                         size_t nseedpoints )
    {
        auto history = initializeHistory<3>( baseGrid, part.get( ), powderHeight, nseedpoints, maxdepth );

        return std::make_shared<ThermoplasticHistory<3>>( std::move( history ) );
    };

    m.def( "initializeThermalHistory", initializeThermalHistoryF,
        pybind11::arg( "baseGrid" ), pybind11::arg( "part" ), pybind11::arg( "maxdepth" ), 
        pybind11::arg( "powderHeight" ) = 0.0, pybind11::arg( "nseedpoints" ) = 4 );

    auto updateHistoryF = []( const ThermoplasticHistory<3>& history,
                              const MultilevelHpBasis<3>& tbasis, 
                              const DoubleVector& tdofs,
                              double meltingTemperature,
                              size_t degree )
    {
        return updateHistory( history, tbasis, tdofs.get( ), meltingTemperature, degree );
    };

    m.def( "updateHistory", updateHistoryF, pybind11::arg( "history" ), pybind11::arg("basis"),
        pybind11::arg( "tdofs" ), pybind11::arg( "meltingTemperature" ), pybind11::arg( "degree" ) );

    auto initializeNewLayerHistoryF = []( const ThermoplasticHistory<3>& history,
                                          double layerThickness,
                                          double supportHeight,
                                          size_t layer,
                                          size_t nseedpoints )
        {
            return initializeNewLayerHistory( history, layerThickness, supportHeight, layer, nseedpoints );
        };

    m.def( "initializeNewLayerHistory", initializeNewLayerHistoryF, pybind11::arg( "history" ), pybind11::arg( "layerThickness" ),
           pybind11::arg( "supportHeight" ) = 0.0, pybind11::arg( "layer" ) = 0, pybind11::arg( "nseedpoints" ) = 4 );

    // Thermal physics
    using MaterialMap = std::map<std::string, std::shared_ptr<Material>>;

    auto convertMaterials = []( MaterialMap&& map )
    {
        auto find = [&]( const char* name ) -> const Material*
        { 
            auto result = map.find( name );

            return result != map.end( ) ? result->second.get( ) : nullptr;
        };

        return MaterialPtrs
        {
            .baseplate = find( "baseplate" ),
            .structure = find( "structure" ),
            .powder = find( "powder" ),
            .air = find( "air" )
        };
    };

    auto combineSourcesF = []( std::vector<ScalarFunctionWrapper<4>>&& sources )
    {
        auto function = [sources = std::move( sources )]( std::array<double, 4> xyzt ) -> double
        {
            auto intensity = 0.0;

            for( auto& source : sources )
            {
                intensity += source.get( )( xyzt );
            }
        
            return intensity;
        };

        return ScalarFunctionWrapper<4> { spatial::ScalarFunction<4> { std::move( function ) } };
    };

    m.def( "combineSources", combineSourcesF, pybind11::arg("sources") );

    auto makeConvectionRadiationIntegrandF = [=]( const DoubleVector& dofs,
                                                  double emissivity,
                                                  double conductivity,
                                                  double ambientTemperature,
                                                  double theta )
    { 
        return makeConvectionRadiationIntegrand<3>( dofs.get( ), emissivity, conductivity,
                                                    ambientTemperature, theta );
    };

    m.def( "makeConvectionRadiationIntegrand", makeConvectionRadiationIntegrandF,
           pybind11::arg( "dof" ), pybind11::arg( "emissivity" ), pybind11::arg( "conductivity" ),
           pybind11::arg( "ambientTemperature" ), pybind11::arg( "theta" ) = 1.0 );

    auto makeThermalInitializationIntegrandF = [=]( MaterialMap map,
                                                    const ScalarFunctionWrapper<4>& source,
                                                    std::shared_ptr<ThermoplasticHistory<3>> history0,
                                                    const DoubleVector& dofs0,
                                                    double time0, double dt, double theta )
    {
        auto materials = convertMaterials( std::move( map ) );
 
        return makeThermalInitializationIntegrand<3>( materials, source.get( ),
            *history0, dofs0.get( ), time0, dt, theta );
    };

    m.def( "makeThermalInitializationIntegrand", makeThermalInitializationIntegrandF,
        pybind11::arg( "materials" ), pybind11::arg( "sources" ), pybind11::arg( "history" ), 
        pybind11::arg( "dofs0" ), pybind11::arg( "time0" ), pybind11::arg( "deltaT" ), 
        pybind11::arg( "theta" ) );

    auto makeTimeSteppingThermalIntegrandF = [=]( MaterialMap map,
                                                  std::shared_ptr<ThermoplasticHistory<3>> history,
                                                  const DoubleVector& projectedDofs0,
                                                  const DoubleVector& dofs1,
                                                  double dt, double theta )
    {
        auto materials = convertMaterials( std::move( map ) );
        
        return makeTimeSteppingThermalIntegrand<3>( materials,
            *history, projectedDofs0.get( ), dofs1.get( ), dt, theta );
    };

    m.def( "makeTimeSteppingThermalIntegrand", makeTimeSteppingThermalIntegrandF,
        pybind11::arg( "materials" ), pybind11::arg( "history" ), 
        pybind11::arg( "projectedDofs0" ), pybind11::arg( "dofs1" ), 
        pybind11::arg( "deltaT" ), pybind11::arg( "theta" ) );

    auto makeEnergyConsistentProjectionIntegrandF = [=]( MaterialMap map,
                                                         std::shared_ptr<ThermoplasticHistory<3>> history0,
                                                         std::shared_ptr<ThermoplasticHistory<3>> history1,
                                                         const DoubleVector& projectedDofs0,
                                                         double ambientTemperature,
                                                         double dt )
        {
            auto materials = convertMaterials( std::move( map ) );

            return makeEnergyConsistentProjectionIntegrand<3>( materials, *history0, *history1,
                                                               projectedDofs0.get( ), ambientTemperature, dt );
        };

    m.def( "makeEnergyConsistentProjectionIntegrand", makeEnergyConsistentProjectionIntegrandF,
           pybind11::arg( "materials" ), pybind11::arg( "history0" ), pybind11::arg( "history1" ),
           pybind11::arg( "projectedDofs0" ),pybind11::arg( "ambientTemperature" ), pybind11::arg( "deltaT" ));

    auto makeSteadyStateThermalIntegrandF = [=]( MaterialMap map,
                                                 const ScalarFunctionWrapper<3>& source,
                                                 std::shared_ptr<ThermoplasticHistory<3>> history,
                                                 const DoubleVector& dofs,
                                                 std::array<double, 3> laserVelocity )
    {
        auto materials = convertMaterials( std::move( map ) );

        return makeSteadyStateThermalIntegrand<3>( materials, 
            source.get( ), *history, dofs.get(), laserVelocity);
    };
    
    m.def( "makeSteadyStateThermalIntegrand", makeSteadyStateThermalIntegrandF,
        pybind11::arg( "materials" ), pybind11::arg( "sources" ), pybind11::arg( "history" ),
        pybind11::arg( "dofs" ), pybind11::arg( "laserVelocity" ) = std::array { 1.0, 0.0, 0.0 } );

    // Mechanical problem

    auto mechanicalHistory = pybind11::class_<MechanicalHistory<3>, 
        std::shared_ptr<MechanicalHistory<3>>>( m, "MechanicalHistory" );

    mechanicalHistory.def( "clone", []( const MechanicalHistory<3>& history )
        { return std::make_shared<MechanicalHistory<3>>( history ); } );

    auto initializeMechanicalHistoryF = []( const AbsBasis<3>& basis, 
                                            size_t quadratureOrder )
    { 
        auto history = std::make_shared<MechanicalHistory<3>>( );
        history->reset( basis.nelements( ), quadratureOrder );

        return history;
    };

    m.def( "initializeMechanicalHistory", initializeMechanicalHistoryF,
           pybind11::arg( "basis" ), pybind11::arg( "quadratureOrder" ) );

    auto plasticityProcessorF = []( const MechanicalHistory<3>& historyAccessor)
    {

         return postprocessPlasticity( historyAccessor );
            
    };

    m.def( "plasticityProcessor", plasticityProcessorF, pybind11::arg( "history" ) );

    // TODO remove from once fixed in mlhp
    auto strainProcessorF = []( const DoubleVector& mdofs )
        {

            return makeStrainProcessor( mdofs.get() );

        };

    m.def( "strainProcessor", strainProcessorF, pybind11::arg( "strain" ) );

    auto neumannBoundaryCondition = []( size_t iface, const std::array<double, 3> traction )
        {
            return makeTractionBC<3>( iface, spatial::constantFunction<4>( traction ) );
        };

    m.def( "makeTractionBC", neumannBoundaryCondition, pybind11::arg( "iface" ), pybind11::arg( "values" ) );

    auto neumannBoundaryConditionF2 = []( size_t iface, spatial::VectorFunction<4, 3> traction )
        {
            return makeTractionBC<3>( iface, traction );
        };

    m.def( "makeTractionBC", neumannBoundaryConditionF2, pybind11::arg( "iface" ), pybind11::arg( "function" ) );


    using ThermalEvaluatorWrapper = FunctionWrapper<ThermalEvaluator<3>>;

    pybind11::class_<ThermalEvaluatorWrapper>( m, "ThermalEvaluator" );

    auto makeThermalEvaluatorF1 = [=]( const BasisConstSharedPtr<3>& tbasis0,
                                       const BasisConstSharedPtr<3>& tbasis1,
                                       const DoubleVector& tdofs0,
                                       const DoubleVector& tdofs1,
                                       const ThermoplasticHistory<3>& thermalHistory1,
                                       MaterialMap materialMap,
                                       double ambientTemperature ) -> ThermalEvaluatorWrapper
    {
        return makeThermalEvaluator<3>( tbasis0, tbasis1, tdofs0.get( ), tdofs1.get( ),
            thermalHistory1, convertMaterials( std::move( materialMap ) ), ambientTemperature );
    };

    m.def( "makeThermalEvaluator", makeThermalEvaluatorF1,
           pybind11::arg( "tbasis0" ), pybind11::arg( "tbasis1" ),
           pybind11::arg( "tdofs0" ), pybind11::arg( "tdofs1" ),
           pybind11::arg( "thermalHistory1" ), pybind11::arg( "materials" ),
           pybind11::arg( "ambientTemperature") );

    auto makeThermalEvaluatorF2 = [=]( const ThermoplasticHistory<3>& thermalHistory1,
                                       MaterialMap materialMap,
                                       double ambientTemperature ) -> ThermalEvaluatorWrapper
    {
        auto materials = convertMaterials( std::move( materialMap ) );

        return ThermalEvaluator<3> { [=, &thermalHistory1]( std::array<double, 3> xyz )
        {
            auto thistory1 = thermalHistory1( xyz );

            MLHP_CHECK( thistory1 != nullptr, "No history found." );

            auto materialAt = materialFor( materials, thistory1->materialType );

            return std::tuple { ambientTemperature, materialAt, 0.0 };
        } };
    };

    m.def( "makeThermalEvaluator", makeThermalEvaluatorF2,
           pybind11::arg( "thermalHistory1" ), pybind11::arg( "materials" ),
           pybind11::arg( "ambientTemperature" ) );

    pybind11::class_<NonlinearMaterial<3, 6>>( m, "ConstitutiveEquation" );

    auto makeJ2PlasticityF = []( const MechanicalHistory<3>& mhistoryContainer0,
                                 MechanicalHistory<3>& mhistoryContainer1,
                                 const ThermalEvaluatorWrapper& evaluator,
                                 double meltingTemperature )
    { 
        return makeJ2Plasticity( mhistoryContainer0, mhistoryContainer1, evaluator.get( ), meltingTemperature );
    };

    m.def( "makeJ2Plasticity", makeJ2PlasticityF, pybind11::arg( "mhistory0" ),
           pybind11::arg( "mhistory1"), pybind11::arg( "thermalEvaluator" ), pybind11::arg( "meltingTemperature" ) = 1.0e+10 );

    auto nonlinearStaticDomainIntegrandF = []( const Kinematics<3>& kinematics,
                                               const NonlinearMaterial<3, 6>& constitutive,
                                               const DoubleVector& dofIncrement,
                                               const spatial::VectorFunction<3>& force )
    {
        return makeNonlinearStaticIntegrand<3, 6>( kinematics, constitutive, dofIncrement.get( ), force );
    };

    m.def( "nonlinearStaticDomainIntegrand", nonlinearStaticDomainIntegrandF,
           pybind11::arg( "kinematics" ), pybind11::arg( "constitutive" ), 
           pybind11::arg( "dofIncrement" ), pybind11::arg( "bodyForce" ) );


    // Other stuff
    auto computeDirichletIncrementF = []( const DofIndicesValuesPair& dirichlet,
                                          const DoubleVector& dofs,
                                          double factor )
    { 
        auto dirichletIncrement = dirichlet;

        MLHP_CHECK( dirichlet.first.size( ) == dirichlet.second.size( ),
                    "Dirichlet dof vectors have different size." );

        for( size_t idof = 0; idof < dirichlet.first.size( ); ++idof )
        {
            MLHP_CHECK( dirichlet.first[idof] < dofs.get( ).size( ), "Dirichlet dof index out of bounds." );

            dirichletIncrement.second[idof] = factor * ( dirichlet.second[idof] - 
                dofs.get( )[dirichlet.first[idof]] );
        }    

        return dirichletIncrement;
    };

    m.def( "computeDirichletIncrement", computeDirichletIncrementF, pybind11::arg( "dirichletDofs" ), 
           pybind11::arg( "dofs" ), pybind11::arg( "factor" ) = 1.0 );
}

} // mlhp::bindings

