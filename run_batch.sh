#!/bin/bash

# each is different so cannot loop simply with names

# raw tables
# raw/dowl	lookup_communities_2024-02-23.csv
# raw/dowl	lookup_grids_2025-04-17.csv
# raw/dowl	lookup_interties_2024-02-23.csv
# raw/dowl	lookup_operator_2025-03-07.csv
# raw/dowl	lookup_plants_2025-03-10.csv
# raw/dowl	lookup_salesreport_2025-03-03.csv

# normalized tables:
# final	boroughs.geojson
aedg_metadata generate capacity -d final --bbox infer --time specify --save
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
aedg_metadata generate monthly_generation -d final --bbox infer --time specify --save
# final	populations.csv
# final	populations_ages_sexes.csv
# final	regional_corporations.geojson
# final	reporting_entities.csv
# final	senate_districts.geojson
# final	taxes.csv
aedg_metadata generate transportation -d final --bbox infer --time specify --save
# final	village_corporations.geojson
aedg_metadata generate yearly_generation -d final --bbox infer --time specify --save

# denormalized tables for the data explorer
aedg_metadata generate public_communities_monthly_generation -d public --bbox infer --save
aedg_metadata generate public_communities_yearly_generation -d public --bbox infer --save
# pause till file exists
# aedg_metadata generate public_communities_transportation -d public --bbox infer -t specify --save
