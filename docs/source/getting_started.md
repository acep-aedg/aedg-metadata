# Getting started

On this page you can find important information about the project.

## About

We had to make metadata.  Lots of it.  To streamline it, there are some rules that restrict the applicability of this code to AEDG only. That isn't optimum, but it saves a lot of trouble as we are getting started. The rules are:

1. There is a single file stem that will be used for both the configuration YAML file and the output JSON metadata file. That stem must match that of the data file being described and is a required argument for `generate`. For instance,
   1. for the data file `capacity.csv`, the stem is `capacity`
   2. configurations file must be called `capacity.yml`
   3. the output metadata will be `capacity.json`
2. The directory structure that contain the input configuration files (`src/config/`) and output metadata files (`metadata/`) must repeat the structure of https://github.com/acep-aedg/aedg-data-pond/tree/main/data. This subdirectory is input as an option of `generate`. For instance:
   1. `capacity.csv` is in the subdirectory `final`
   2. the command is `aedg_metata generate capacity -d final`
   3. `generate` will look to `src/config/final/capacity.yml` for input
   4. `generate` will output `metadata/final/capacity.json`

## Example Usage

The CLI is set-up according to `typer's` [Building a Package](https://typer.tiangolo.com/tutorial/package/#try-your-cli-program) instructions
so the usage conforms to `aedg_metadata [OPTIONS] COMMAND [ARGS]...`

``` shell
% aedg_metadata generate --help
% aedg_metadata generate public_communities_monthly_generation -d public --bbox infer --sav
% aedg_metadata generate --help

 Usage: aedg_metadata generate [OPTIONS] CONFIG

 To call gen_meta.py.

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    config      TEXT  File stem of config file (req). [default: None] [required]                                                                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --directory  -d               TEXT                       Subdirectory of data/ where target file lives in the AEDG pond. [default: public]                                                                  │
│ --bbox       -b               [infer|calc|specify|none]  How the spatial bounding box should be determined. [default: infer]                                                                                │
│ --save           --no-save                               Write generated metadata to the file or else to the screen. [default: no-save]                                                                     │
│ --help                                                   Show this message and exit.                                                                                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Note: there is a practice call still hanging around as `aedg_metadata greet Name --count 5`. Don't let that bother you!
