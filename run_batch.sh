#!/bin/bash

# Define an array of names
all_tags=(
    "public_communities_monthly_generation"
    "public_communities_yearly_generation"
    "public_communities_transportation"
)

# Loop through each name in the array and echo it
for tag in "${all_tags[@]}"; do
  echo ${tag}
  aedg_metadata generate ${tag} -d public --bbox infer --save
done
