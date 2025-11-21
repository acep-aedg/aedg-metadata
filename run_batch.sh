#!/bin/bash

# each is different so cannot loop simply with names

# raw tables
# aedg_metadata generate lookup_fuelcode_2023-11-08 -d raw/dowl --bbox none --time none --data-dictionary raw_dowl_data_dictionary.csv --save
# aedg_metadata generate lookup_primemover_2023-11-08 -d raw/dowl --bbox none --time none --data-dictionary raw_dowl_data_dictionary.csv --save
# aedg_metadata generate lookup_plants_2025-03-10 -d raw/dowl --bbox infer --time none --data-dictionary raw_dowl_data_dictionary.csv --save
# aedg_metadata generate lookup_salesreport_2025-03-03 -d raw/dowl --bbox infer --time none --data-dictionary raw_dowl_data_dictionary.csv --save
# aedg_metadata generate lookup_interties_2024-02-23 -d raw/dowl --bbox none --time specify --data-dictionary raw_dowl_data_dictionary.csv --save
# aedg_metadata generate lookup_grids_2025-04-17 -d raw/dowl --bbox none --time specify --data-dictionary raw_dowl_data_dictionary.csv --save
# aedg_metadata generate lookup_operator_2025-03-07 -d raw/dowl --bbox none --time none --data-dictionary raw_dowl_data_dictionary.csv --save
# aedg_metadata generate lookup_communities_2024-02-23 -d raw/dowl --bbox infer --time none --data-dictionary raw_dowl_data_dictionary.csv --save

# normalized tables:
# final	boroughs.geojson
#aedg_metadata generate capacity -d final --bbox infer --time specify --save
# final	communities.geojson
# final	communities_grids.csv
# final	communities_legislative_districts.csv
# final	communities_reporting_entities.csv
# final	communities_school_districts.csv
# final	electric_rates.csv
# final	employment.csv
# final	fuel_prices.csv
# final	grids.csv
# final	house_districts.geojson
#aedg_metadata generate monthly_generation -d final --bbox infer --time specify --save
# final	populations.csv
# final	populations_ages_sexes.csv
# final	regional_corporations.geojson
# final	reporting_entities.csv
# final	senate_districts.geojson
# final	taxes.csv
#aedg_metadata generate transportation -d final --bbox infer --time specify --save
# final	village_corporations.geojson
#aedg_metadata generate yearly_generation -d final --bbox infer --time specify --save

# denormalized tables for the data explorer
aedg_metadata generate public_capacity -d public --bbox infer --time specify --save
aedg_metadata generate public_communities -d public --bbox infer -t none --save
# aedg_metadata generate public_employment -d public --bbox infer -t specify --save



aedg_metadata generate data/public_fuel_prices/public_fuel_prices.csv --bbox infer -t specify --save



aedg_metadata generate public_monthly_generation -d public --bbox infer --save
# aedg_metadata generate public_rates -d public --bbox infer -t none --save  # change this!!
# aedg_metadata generate public_populations_ages_sexes -d public --bbox infer -t specify --save
# aedg_metadata generate public_taxes -d public --bbox infer -t specify --save
# aedg_metadata generate public_transportation -d public --bbox infer -t specify --save
aedg_metadata generate public_yearly_generation -d public --bbox infer --save

# Gather keywords/topics together into registry file
# python src/aedg_metadata/scripts/keywords_to_registry.py
