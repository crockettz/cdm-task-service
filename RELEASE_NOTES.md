# CDM Task Service Release Notes

## Unreleased

* Added `metaassembly` pipeline version 0.2.0, which is now the default version. The WDL no
  longer generates the read mapping BAM or SAM.gz, and the bbcms corrected reads FASTQ is no
  longer uploaded. These were the three largest outputs, and their uploads failed on large
  inputs. Version 0.1.0 is still registered.

## 0.1.0-prototype1-6

* Initial prototype releases