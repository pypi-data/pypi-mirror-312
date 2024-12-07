// This file is part of the mlhpbf project. License: See LICENSE

#ifndef MLHPBF_MATERIALS_HPP
#define MLHPBF_MATERIALS_HPP

#include "json/json.hpp"
#include "mlhp/core.hpp"

namespace mlhp
{

struct Units
{
    static constexpr double m = 1000.0;
    static constexpr double cm = 1e-2 * m;
    static constexpr double mm = 1e-3 * m; // <---
    static constexpr double um = 1e-6 * m;
    static constexpr double s = 1.0;       // <---
    static constexpr double ms = 1e-3 * s;
    static constexpr double kg = 1000.0;
    static constexpr double g = 1e-3 * kg; // <---
    static constexpr double N = 1.0;       // <---
    static constexpr double J = N * m;
    static constexpr double kJ = 1e3 * J;
    static constexpr double W = J / s;
    static constexpr double kW = 1e3 * W;
    static constexpr double C = 1.0;       // <---
    static constexpr double Pa = N / ( m * m );
    static constexpr double MPa = 1e6 * Pa;
    static constexpr double GPa = 1e9 * Pa;
};

using TemperatureFunction = RealFunctionWithDerivative;

struct Material
{
    bool initialized = false;
    std::string name = "UninitializedMaterial";

    TemperatureFunction density = { };

    // Thermal parameters
    TemperatureFunction specificHeatCapacity = { };
    TemperatureFunction heatConductivity = { };

    double solidTemperature = std::numeric_limits<double>::max( );
    double liquidTemperature = std::numeric_limits<double>::max( );
    double latentHeatOfFusion = 0.0;
    double regularization = 1.0; // The higher the smoother

    //double emissivity;
    //double conductivity; // convectivity?

    TemperatureFunction thermalExpansionCoefficient = { };
    TemperatureFunction thermalExpansionCoefficientCooling = { };

    // Linear elastic parameters
    TemperatureFunction youngsModulus = { };
    TemperatureFunction poissonRatio = { };

    // Plastic parameters
    TemperatureFunction yieldStress = { };
    TemperatureFunction hardeningParameter = { };

    // beta = 0.0 -> isotropic hardening
    // beta = 1.0 -> kinematic hardening
    double plasticModelSelector = 0.0; // should be model parameter
};

enum class MaterialType : size_t 
{ 
    BasePlate = 0, 
    Structure = 1, 
    Powder    = 2, 
    Air       = 3 
};

struct Materials
{
    Material baseplate;
    Material structure;
    Material powder;
    Material air;
};

static constexpr const char* MaterialString[] = { "Base plate", "Structure", "Powder", "Air" };

inline auto makeIN625( )
{
    auto rhoT = std::vector<double>
    {
        22.0, 1290.0, 1350.0
    };

    auto rhoV = std::vector<double>
    {
        8440.0, 8000.0, 7500.0
    };

    auto cpT = std::vector<double>
    {
        21,  93, 204,  316,  427,  538,  649,  760,
        871, 982, 1093
    };

    auto cpV = std::vector<double>
    {
        410, 427, 456, 481, 511, 536, 565, 590,
        620, 645, 670
    };

    auto kT = std::vector<double>
    {
        21,  93, 204,  316,  427,  538,  649,  760,
        871, 982
    };

    auto kV = std::vector<double>
    {
        9.8, 10.1, 10.8, 12.5, 14.1, 15.7, 17.5, 19.0, 20.8, 
        22.8, 25.2
    };

    auto eT = std::vector { 93.0, 204.0, 316.0, 427.0, 538.0, 649.0, 760.0, 871.0, 982.0 };
    auto eV = std::vector { 12.8e-6, 13.1e-6, 13.3e-6, 13.7e-6, 14.0e-6, 14.8e-6, 15.3e-6, 15.8e-6, 16.2e-6 };

    auto syT = std::vector { 21.0, 93.0, 204.0, 316.0, 427.0, 538.0, 649.0, 760.0, 871.0, 1040.0, 1150.0 };
    auto syV = std::vector { 493.0, 479.0, 443.0, 430.0, 424.0, 423.0, 422.0, 415.0, 386.0, 31.0, 15.0 };

    auto ET = std::vector { 21.0, 93.0, 204.0, 316.0, 427.0, 538.0, 649.0, 760.0, 871.0 };
    auto EV = std::vector { 207.5, 204.1, 197.9, 191.7, 185.5, 178.6, 170.3, 160.6,  147.5 };
    auto nuV = std::vector { 0.278, 0.280, 0.286, 0.290, 0.295, 0.305, 0.321, 0.340, 0.336 };

    auto applyUnits = []( auto& container, auto unit )
    {
        for( auto& value : container ) value *= unit;
    };

    applyUnits( rhoV, Units::kg / ( Units::m * Units::m * Units::m ) );
    applyUnits( cpV, Units::J / ( Units::kg * Units::C ) );
    applyUnits( kV, Units::W / ( Units::m * Units::C ) );
    applyUnits( eV, 1.0 / Units::C );
    applyUnits( syV, Units::MPa );
    applyUnits( EV, Units::GPa );

    auto hardening = []( double ) noexcept -> std::array<double, 2>
    {
        return { 0.0, 0.0 };
    };

    constexpr auto Constant = interpolation::Extrapolate::Constant;

    return Material
    {
        .initialized = true,
        .name = "IN625",
        .density = interpolation::makeLinearInterpolation( rhoT, rhoV, Constant ),
        .specificHeatCapacity = interpolation::makeLinearInterpolation( cpT, cpV, Constant ),
        .heatConductivity = interpolation::makeLinearInterpolation( kT, kV, Constant ),
        .solidTemperature = 1290.0 * Units::C,
        .liquidTemperature = 1350.0 * Units::C,
        .latentHeatOfFusion = 2.8e5 * Units::J / Units::kg,
        .thermalExpansionCoefficient = interpolation::makeLinearInterpolation( eT, eV, Constant ),
        .youngsModulus = interpolation::makeLinearInterpolation( ET, EV, Constant ),
        .poissonRatio = interpolation::makeLinearInterpolation( ET, nuV, Constant ),
        .yieldStress = interpolation::makeLinearInterpolation( syT, syV, Constant ),
        .hardeningParameter = hardening,
        .plasticModelSelector = 0.5
    };
}

inline auto makeIN718( )
{
    auto Tm = 1250.0;

    auto rhoT = std::vector<double> { 0.0 };
    auto rhoV = std::vector<double> { 8170.0 };

    auto cpT = std::vector<double> { 0.0, Tm };
    auto cpV = std::vector<double> { 425.0, 425.0 + 189.65e-3 * Tm };

    auto kT = std::vector<double> { 0.0, Tm };
    auto kV = std::vector<double> { 9.94, 9.94 + 13.9e-3 * Tm };

    auto applyUnits = []( auto& container, auto unit )
    {
        for( auto& value : container ) value *= unit;
    };

    applyUnits( rhoV, Units::kg / ( Units::m * Units::m * Units::m ) );
    applyUnits( cpV, Units::J / ( Units::kg * Units::C ) );
    applyUnits( kV, Units::W / ( Units::m * Units::C ) );

    constexpr auto Constant = interpolation::Extrapolate::Constant;

    return Material
    {
        .initialized = true,
        .name = "IN718",
        .density = interpolation::makeLinearInterpolation( rhoT, rhoV, Constant ),
        .specificHeatCapacity = interpolation::makeLinearInterpolation( cpT, cpV, Constant ),
        .heatConductivity = interpolation::makeLinearInterpolation( kT, kV, Constant ),
        .solidTemperature = 1250.0 * Units::C,
        .liquidTemperature = 1335.0 * Units::C,
        .latentHeatOfFusion = 2.1e5 * Units::J / Units::kg,
        .thermalExpansionCoefficient = nullptr,
        .youngsModulus = nullptr,
        .poissonRatio = nullptr,
        .yieldStress = nullptr,
        .hardeningParameter = nullptr,
        .plasticModelSelector = 0.5
    };
}

inline auto makeSS316L( )
{
    auto rhoT = std::vector<double>
    {
        26.85,   126.85,  226.85,  326.85,  426.85,  526.85,  626.85,  726.85,
        826.85,  926.85,  1026.85, 1126.85, 1226.85, 1326.85, 1426.85, 1526.85,
        1626.85, 1726.85, 1826.85, 1926.85, 2026.85, 2126.85, 2226.85, 2326.85,
        2426.85, 2526.85, 2626.85, 2726.85
    };

    auto rhoV = std::vector<double>
    {
        7954, 7910, 7864, 7818, 7771, 7723, 7674, 7624,
        7574, 7523, 7471, 7419, 7365, 7311, 6979, 6920,
        6857, 6791, 6721, 6648, 6571, 6490, 6406, 6318,
        6229, 6131, 6032, 5930
    };

    auto cpT = std::vector<double>
    {
        26,  126, 226,  326,  426,  526,  626,  726,
        826, 926, 1026, 1126, 1226, 1326, 1426, 1526
    };

    auto cpV = std::vector<double>
    {
        498, 512, 525, 538, 551, 565, 578, 591,
        605, 618, 631, 644, 658, 671, 769, 769
    };

    auto kT = std::vector<double>
    {
        -0.15,   19.85,   26.85,   76.85,  126.85, 226.85,  326.85,  426.85,
        526.85,  626.85,  726.85,  826.85, 926.85, 1026.85, 1126.85, 1226.85,
        1326.85, 1370.85, 1398.85, 1426.85
    };

    auto kV = std::vector<double>
    {
        12.97, 13.31, 13.44, 14.32, 15.16, 16.8, 18.36, 19.87,
        21.39, 22.79, 24.06, 25.46, 26.74, 28.02, 29.32, 30.61,
        31.86, 32.41, 26.9,  27.24
    };

    auto eT = std::vector { -0.15,   19.85,   26.85,   76.85,  126.85, 226.85,  326.85,  426.85, 
        526.85,  626.85,  726.85,  826.85, 926.85, 1026.85, 1126.85, 1226.85,
        1326.85 };
    auto eV = std::vector { 14.6e-6, 14.8e-6, 15.2e-6, 15.6e-6, 16.3e-6, 16.9e-6, 17.4e-6, 17.9e-6, 18.3e-6,
        18.7e-6, 19.0e-6, 19.3e-6, 19.5e-6, 19.6e-6, 19.8e-6, 19.9e-8 };

    auto syT = std::vector { 100.0, 300.0, 816.0, 1040.0, 1150.0 };
    auto syV = std::vector { 225.0, 168.0, 115.0, 31.0, 15.0 };
    auto hardening = std::vector { 2091.0, 1577.0, 708.0, 405.0, 265.0 };

    auto ET = std::vector { 20.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0 };
    auto EV = std::vector { 195.0, 191.0, 186.0, 180.0, 173.0, 164.0, 155.0, 144.0, 131.0, 117.0, 100.0, 81.0, 51.0 };
    auto nuV = std::vector { 0.35, 0.26, 0.275, 0.315, 0.33, 0.3, 0.32, 0.31, 0.24, 0.24, 0.24, 0.24, 0.24 };

    auto applyUnits = []( auto& container, auto unit )
        {
            for( auto& value : container ) value *= unit;
        };

    applyUnits( rhoV, Units::kg / ( Units::m * Units::m * Units::m ) );
    applyUnits( cpV, Units::J / ( Units::kg * Units::C ) );
    applyUnits( kV, Units::W / ( Units::m * Units::C ) );
    applyUnits( eV, 1.0 / Units::C );
    applyUnits( syV, Units::MPa );
    applyUnits( EV, Units::GPa );
    applyUnits( hardening, Units::MPa );

    constexpr auto Constant = interpolation::Extrapolate::Constant;

    return Material
    {
        .initialized = true,
        .name = "SS316L",
        .density = interpolation::makeLinearInterpolation( rhoT, rhoV, Constant ),
        .specificHeatCapacity = interpolation::makeLinearInterpolation( cpT, cpV, Constant ),
        .heatConductivity = interpolation::makeLinearInterpolation( kT, kV, Constant ),
        .solidTemperature = 1375.0 * Units::C,
        .liquidTemperature = 1400.0 * Units::C,
        .latentHeatOfFusion = 2.8e5 * Units::J / Units::kg,
        .thermalExpansionCoefficient = interpolation::makeLinearInterpolation( eT, eV, Constant ),
        .youngsModulus = interpolation::makeLinearInterpolation( ET, EV, Constant ),
        .poissonRatio = interpolation::makeLinearInterpolation( ET, nuV, Constant ),
        .yieldStress = interpolation::makeLinearInterpolation( syT, syV, Constant ),
        .hardeningParameter = interpolation::makeLinearInterpolation( syT, hardening, Constant ),
        .plasticModelSelector = 0.5
    };
}

inline auto parseCSV( std::filesystem::path file, 
                      std::string separator = "," )
{
    auto fstream = std::ifstream { file };
    auto data = std::vector<std::vector<std::string>> { };
    auto irow = size_t { 0 };

    MLHP_CHECK( fstream.is_open( ), "Unable to open file " + file.string( ) + "." );

    auto appendLine = [&]( auto&& line )
    {
        auto entries = std::vector<std::string> { };
        auto icolumn = size_t { 0 };

        auto appendColumn = [&]( auto begin, auto end )
        {
            auto sub = line.substr( begin, end - begin );

            if( !sub.empty( ) )
            {
                if( irow == 0 ) 
                {
                    data.push_back( { std::move( sub ) } );
                }
                else
                {
                    MLHP_CHECK( icolumn < data.size( ), "Too many columns in row " +
                        std::to_string( irow ) + " of data file " + file.string( ) + "." );

                    data[icolumn].push_back( std::move( sub ) );
                }

                icolumn += 1;
            }
        };
        
        auto index0 = size_t { 0 };
        auto index1 = line.find( separator, index0 );
        
        while( index1 != std::string::npos )
        {
            appendColumn( index0, index1 );

            index0 = index1 + 1;
            index1 = line.find( separator, index0 );
        }

        appendColumn( index0, line.size( ) );

        if( icolumn > 0 )
        {
            MLHP_CHECK( icolumn == data.size( ), "Too few columns in row " +
                std::to_string( irow ) + " of data file " + file.string( ) + "." );

            irow += 1;
        }
    };
    
    auto line = std::string { };

    while( std::getline( fstream, line ) )
    {
        appendLine( line );
    }

    fstream.close( );

    return data;
}

namespace detail 
{

inline auto parseTemperatureData( std::filesystem::path file, 
                                  std::string separator = "," )
{
    auto columns = parseCSV( file, separator );

    MLHP_CHECK( columns.size( ) == 2, "Too many columns in input file " + file.string( ) + ".");

    auto convertColumn = []( auto&& column )
    {
        auto converted = std::vector<double> { };

        for( size_t i = 1; i < column.size( ); ++i )
        {
            converted.push_back( std::stod( column[i] ) );
        }

        return converted;
    };

    return std::array { convertColumn( std::move( columns[0] ) ), 
                        convertColumn( std::move( columns[1] ) ) };
}

inline auto createTemperatureFunction( const std::string& name,
                                       std::vector<double>&& T, 
                                       std::vector<double>&& V,
                                       bool constantExtrapolation,
                                       double scaling )
{
    MLHP_CHECK( !T.empty( ), "No data point given for material " + name + "." );

    MLHP_CHECK( T.size( ) == V.size( ), "Inconsistent number of data "
        "points for parameter " + name + "." );

    for( auto& value : V )
    {
        value *= scaling;
    }

    auto extrapolate = constantExtrapolation ? 
        interpolation::Extrapolate::Constant : 
        interpolation::Extrapolate::Linear;

    return interpolation::makeLinearInterpolation( T, V, extrapolate );
}

struct ReadMaterial : Units
{
    static auto read( std::istream& istream, std::filesystem::path parentpath )
    {
        auto json = nlohmann::json::parse( istream );
        auto material = Material { .initialized = true, .name = "JsonMaterial" };
        auto input = json;//[key];

        if( input.contains( "name" ) )
        {
            material.name = input["name"];
        }

        auto readParameterFunction = [&]( std::string name, double unit ) -> TemperatureFunction
        {
            if( !input.contains( name ) )
            {
                return { };
            }

            if( auto field = input[name]; field.is_number( ) )
            {
                auto number = field.get<double>( );

                return [number]( auto ) noexcept { return std::array { number, 0.0 }; };
            }
            else if( field.is_string( ) )
            {
                auto datafile = field.get<std::filesystem::path>( );

                if( !std::filesystem::exists( datafile ) )
                {
                    datafile = parentpath / field.get<std::filesystem::path>( );
                }

                if( !std::filesystem::exists( datafile ) )
                {
                    datafile = parentpath / material.name / field.get<std::filesystem::path>( );
                }

                MLHP_CHECK( std::filesystem::exists( datafile ), "Unable to read data file " + 
                    field.get<std::string>( ) + " for parameter " + name + ".");

                auto [T, V] = detail::parseTemperatureData( datafile );

                return detail::createTemperatureFunction( name, std::move( T ), std::move( V ), true, unit );
            }
            else if( field.contains( "temperatures" ) )
            {
                MLHP_CHECK( field.contains( "values" ), "Parameter " + name + " has temperatures but no values." );
                
                auto constantExtrapolation = true;

                if( field.contains( "extrapolation" ) )
                {
                    auto extrapolation = field["extrapolation"];

                    constantExtrapolation = extrapolation == "constant";

                    MLHP_CHECK( extrapolation == "constant" || extrapolation == "linear",
                        "Invalid extrapolation \"" + std::string { extrapolation } + "\" "
                        "for parameter " + name + ". Must be \"constant\" or \"linear\"." );
                }

                return detail::createTemperatureFunction( name, 
                    field["temperatures"].get<std::vector<double>>( ), 
                    field["values"].get<std::vector<double>>( ),
                    constantExtrapolation, unit );
            }

            MLHP_THROW( "Could not read " + name + " data." );
        };

        auto readParameterConstant = [&]( std::string name, double unit ) -> double
        {
            MLHP_CHECK( input.contains( name ), "Could not find " + name + " parameter." );
            MLHP_CHECK( input[name].is_number( ), "Invalid format for parameter constant " + name + "." );

            return input[name].get<double>( ) * unit;
        };

        material.density              = readParameterFunction( "density", kg / ( m * m * m ) );
        material.specificHeatCapacity = readParameterFunction( "specificHeatCapacity", J / ( kg * C ) );
        material.heatConductivity     = readParameterFunction( "heatConductivity", W / ( m * C ) );
        material.solidTemperature     = readParameterConstant( "solidTemperature", C );
        material.liquidTemperature    = readParameterConstant( "liquidTemperature", C );
        material.latentHeatOfFusion   = readParameterConstant( "latentHeatOfFusion", J / kg );
        material.thermalExpansionCoefficient = readParameterFunction( "thermalExpansionCoefficient", 1.0 );
        material.thermalExpansionCoefficientCooling = readParameterFunction( "thermalExpansionCoefficientCooling", 1.0 );
        material.youngsModulus        = readParameterFunction( "youngsModulus", Units::GPa );
        material.poissonRatio         = readParameterFunction( "poissonRatio", 1.0 );
        material.yieldStress          = readParameterFunction( "yieldStress", Units::MPa );
        material.hardeningParameter   = readParameterFunction( "hardening", Units::MPa );
        material.plasticModelSelector = 0.0;

        return material;
    }
};

} // detail

inline auto readMaterialString( std::string json )
{
    auto sstream = std::stringstream { std::move( json ) };

    return detail::ReadMaterial::read( sstream, std::filesystem::path { "." } );
}

inline auto readMaterialFile( std::filesystem::path file )
{    
    auto fstream = std::ifstream { file };
    
    MLHP_CHECK( fstream.is_open( ), "Unable to open file " + file.string( ) + "." );

    auto material = detail::ReadMaterial::read( fstream, file.parent_path( ) );

    fstream.close( );

    return material;
}

inline auto makePowder( const Material& material )
{
    auto solid = std::make_shared<Material>( material );

    return Material
    {
        .initialized                 = true,
        .name                        = material.name + "Powder",
        .density                     = [=]( auto T ) { return 0.5 * solid->density( T ); },
        .specificHeatCapacity        = [=]( auto T ) { return solid->specificHeatCapacity( T ); },
        .heatConductivity            = [=]( auto T ) { return 0.1 * solid->heatConductivity( T ); },
        .solidTemperature            = solid->solidTemperature,
        .liquidTemperature           = solid->liquidTemperature,
        .latentHeatOfFusion          = solid->latentHeatOfFusion,
        .thermalExpansionCoefficient = [=]( auto ) noexcept { return std::array { 0.0, 0.0 }; },
        .youngsModulus               = [=]( auto T ) { return 1e-12 * solid->youngsModulus( T ); },
        .poissonRatio                = [=]( auto ) noexcept { return std::array { 0.2, 0.0 }; },
        .yieldStress                 = [=]( auto ) noexcept { return std::array { 1.0e50, 0.0 }; },
        .hardeningParameter          = [=]( auto ) noexcept { return std::array { 0.0, 0.0 }; },
        .plasticModelSelector        = 0.0
    };
}

inline auto makeAir( auto material = makeIN625( ) )
{
    auto solid = std::make_shared<Material>( material );
    double alpha = 1e-4;

    return Material
    {
        .initialized                 = true,
        .name                        = material.name + "Air",
        .density                     = [=]( auto T ) { return alpha * solid->density( T );  },
        .specificHeatCapacity        = [=]( auto T ) { return solid->specificHeatCapacity( T ); },
        .heatConductivity            = [=]( auto T ) { return alpha * solid->heatConductivity( T ); },
        .solidTemperature            = solid->solidTemperature,
        .liquidTemperature           = solid->liquidTemperature,
        .latentHeatOfFusion          = 0.0,
        .thermalExpansionCoefficient = [=]( auto ) { return std::array { 0.0, 0.0 }; },
        .youngsModulus               = [=]( auto T ) { return alpha * solid->youngsModulus( T ); },
        .poissonRatio                = [=]( auto ) { return std::array { 0.0, 0.0 }; },
        .yieldStress                 = [=]( auto ) { return std::array { 1e50, 0.0 }; },
        .hardeningParameter          = [=]( auto ) { return std::array { 0.0, 0.0 }; },
        .plasticModelSelector        = 0.0
    };
}

// Returns [fpc, dfpc/dT, ddfpc/ddT]
inline auto regularizedStepFunction( double Ts, double Tl, double T, double S )
{
    double Tmid = ( Tl + Ts ) / 2.0;
    double Tstd = ( Tl - Ts ) / 2.0 * S;
    double xi = ( T - Tmid ) / Tstd;

    if( std::abs( xi ) < 5.0 )
    {
        auto tanhXi = std::tanh( xi );

        double fpc_d0 = 0.5 * ( tanhXi + 1.0 );
        double fpc_d1 = ( 1.0 - tanhXi * tanhXi ) / ( 2.0 * Tstd );
        double fpc_d2 = ( tanhXi * tanhXi - 1.0 ) * tanhXi / ( Tstd * Tstd );

        return std::array { fpc_d0, fpc_d1, fpc_d2 };
    }
    else
    {
        return std::array { xi > 0.0 ? 1.0 : 0.0, 0.0, 0.0 };
    }
}

inline auto evaluatePhaseTransition( const Material& material, double T )
{
    auto [f, df, ddf] = regularizedStepFunction( material.solidTemperature, 
        material.liquidTemperature, T, material.regularization );

    auto L = material.latentHeatOfFusion;
    auto rho = material.density( T )[0];
    
    return std::array { f * L * rho, df * L * rho, ddf * L * rho };
}

} // namespace mlhp

#endif // MLHPBF_MATERIALS_HPP
