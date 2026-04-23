#!/bin/bash


# CSV example data
aedg_metadata generate \
    example_data/public_yearly_generation/public_yearly_generation.csv \
    ~/repos/aedg-etl-2024/data-sources \
    --bbox infer \
    -t specify

# GeoJSON example data
aedg_metadata generate \
    example_data/bulk_fuel/bulk_fuel.geojson \
    ~/repos/aedg-etl-2024/data-sources \
    -dd bulk_fuel_data_dictionary.csv \
    --bbox infer \
    -t specify

# Gather keywords/topics together into registry file
# python src/aedg_metadata/scripts/keywords_to_registry.py
