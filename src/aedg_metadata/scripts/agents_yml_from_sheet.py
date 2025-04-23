""" To get agent information from a Google Sheet, where it is easier to edit, and convert to yml.

During the metadata blitz, we crowd-sourced the organizations from which AEDG derives its data.
To avoid changing formats or copy pasting all the fields, this script was written to transfer info
from the Google Sheet we populated into the YAML file in the registry.

I expect to only use this script once, and to maintain the YAML file as the source of truth going forward
ELD
4/22/2025
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml


def hack_fix(filename: Path) -> None:
    """Fix yaml file so it can be read back in like a normal file.
    I do not understand why, but writing the YAML file is sticking in a "|" that
    causes it to be read in as a big long string, not a YAML file. So strip
    out that one line.
    """

    with Path.open(filename) as f:
        lines = f.readlines()
    with Path.open(filename, "w") as f:
        for line in lines:
            if not line.strip().startswith("|"):
                f.write(line)

def main() -> None:
    """ Grab the data and write it out with some contextual notes."""

    prologue = \
    """# Schema Descriptions for agents (organizations) in the context of AEDG
#
#  code (string): code used in configurations
#  name (string): the title of the organization
#  home_page (string): URL where can find more information on the organization
#  description (string): a mission statement or description of the organization to give context
#  These fields will be used in various OEMetadata contexts
#
    """

    agent_file = Path(__file__).parents[3] / "src" / "registry" / "agents.yml"
    google_sheet_id = "1he4-_HxtL-pnppv3LfCiA6VwtXdJlwa0pr6-rv55Qvg"  # must be readable to anyone with a link
    google_sheet_name = "Agents"
    url = f"https://docs.google.com/spreadsheets/d/{google_sheet_id}/gviz/tq?tqx=out:csv&sheet={google_sheet_name}"
    print(f"Processing: {google_sheet_name}")  # noqa: T201

    agents = pd.read_csv(url)
    agents = agents.drop(columns=['license?', 'notes'])
    agents = agents.set_index('code')

    dict_agents = agents.to_dict(orient='index')
    yaml_agents = yaml.dump(dict_agents, sort_keys=False)

    print('Writing to', agent_file)  # noqa: T201
    with Path.open(agent_file, 'w') as file:
        file.write(prologue)
        yaml.dump(yaml_agents, file, width=120, default_flow_style=False, default_style='|')

    hack_fix(agent_file)

    # test
    with (agent_file).open() as stream:
        read_agents = yaml.safe_load(stream)

    print("ACEP's description read from 'agents.yml':")  # noqa: T201
    print(read_agents['acep']['description'])  # noqa: T201

if __name__ == "__main__":

    main()
