# ENA Genome Notes Workflow

## Introduction

Credit attibution can sometimes be an issue when submitting data to the archives. In many cases,
not every contributor to the production of data gets credited with their work. To this end, we
have created a workflow to produce a micropublication based on any assembly accession.

This micropublication will be populated based on available information from INSDC and by running
some QC steps (BUSCO) and written in markdown format (`.md`). From here, you can tweak the text
to include additional information or authors.

## Preparation
If you will be running the pipeline in local mode, you will need to install the requirements
of this workflow manually first:
```
pip install -r requirements.txt
```

If running in Docker or Singularity, the required containers will be automatically pulled at runtime, so there is no preparation necessary.

## Running

```
cd ena-genome-notes
nextflow run . --accession GCA_030926885.1 -profile <profile name>
```

