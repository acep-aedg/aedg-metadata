""" To make a single list of used keywords and topics and put it in the registry.

I started using keywords while developing demo metadata files and then kept going
without sticking to a proscribed list or standard vocabulary. These words are intended
to supplement the other text in the metadata file rather than summarize them. But
there are now so many of them that we'd like to make a central list to see what they
are.

The list will be written as a CSV in the registry directory in case we want to use
this as the beginning of a standard vocabulary.

ELD
5/9/2025
"""
from __future__ import annotations

import json
from pathlib import Path


def main() -> None:

    input_dir = Path(__file__).parents[3] / "metadata"
    output_dir  = Path(__file__).parents[3] / "src" / "registry"
    keywords: list[str] = []
    topics: list[str] = []

    print('\nGathering keywords from:')  # noqa: T201
    for type in input_dir.iterdir():
        subdir = input_dir / type
        for file_path in subdir.iterdir():
            if file_path.is_file() and file_path.suffix == '.json':
                print(file_path)  # noqa: T201
                with file_path.open(encoding="UTF-8") as source:
                    package = json.load(source)
                for resource in package['resources']:
                    keywords = keywords + resource['keywords']
                    topics = topics + resource['topics']

    # clean those lists up
    keywords = list(set(keywords))
    keywords.sort()
    topics = list(set(topics))
    topics.sort()
    #print(keywords)
    #print(topics)

    # write rough CSV file
    with Path.open(output_dir / 'active_keywords.csv', 'w') as file:
        file.write('attribute,word_or_phrase\n')
        for word in keywords:
            file.write(f'keyword,{word}\n')
        for word in topics:
            file.write(f'topic,{word}\n')


if __name__ == "__main__":

    main()
