"""
Metagenome Assembly (jgi_metaAssembly) pipeline, version 0.2.0.

Source: https://github.com/kbaseincubator/metaAssembly
WDL MD5s below are for the `drop-sam-bam-outputs` branch of that repo, based on commit
5e11066d7c9d47022fa6948dbc8637b172f59488 (the v0.1.0 pin).
TODO: replace with the final upstream commit hash once the branch is pushed / merged.

Changes from v0.1.0:
  * The WDL no longer generates the read mapping BAM (`sr_bam`) or SAM.gz (`sr_samgz`).
    `read_mapping_pairs` now runs bbmap for coverage stats only (no sort / index / reformat),
    and `finish_asm` no longer rewrites either file.
  * The bbcms error corrected reads FASTQ (`sr_bbcms_fq`) is still generated, since it's the
    assembler's input, but is no longer uploaded.

All three were the largest outputs, roughly input sized, and their uploads from NERSC failed on
large inputs.

Inputs are identical to v0.1.0 and the input models are shared with that version - see the
v0.1.0 module docstring for input details.
"""

from pathlib import Path

import semver

from cdmtaskservice.pipelines.definition import PipelineDefinition
from cdmtaskservice.pipelines.metaassembly.v0_1_0 import MetaAssemblyInput

_WORKFLOW = "jgi_metaAssembly"


_NERSC_WDL_PATH = Path(
    "/global/cfs/cdirs/kbase/cdm_task_service/pipelines/metaassembly/0.2.0/metaAssembly/"
)


_FILE_MD5S = {
    "jgi_assembly.wdl": "d268039220dcc628f42f2eb628624be2",
    "shortReads_assembly.wdl": "0fc40b6bb465bafb5fa32643a36bbd12",
    "make_interleaved_reads.wdl": "5a70ad09514da5845af6ba79af1856f4",
}


_OUTPUT_KEYS = frozenset({
    f"{_WORKFLOW}.sr_contig",
    f"{_WORKFLOW}.sr_scaffold",
    f"{_WORKFLOW}.sr_agp",
    f"{_WORKFLOW}.sr_covstats",
    f"{_WORKFLOW}.sr_asminfo",
    f"{_WORKFLOW}.stats",
})


_DESCRIPTION = (
    "Metagenome assembly of Illumina short reads: error correction via BBTools (bbcms), "
    "assembly via metaSPAdes, and coverage statistics from mapping reads back to the "
    "assembly via bbmap."
)

_DOC_URLS = [
    "https://github.com/kbaseincubator/metaAssembly",
    "https://docs.microbiomedata.org/workflows/chapters/4_Metagenome_Assembly/",
]


def init() -> PipelineDefinition:
    """ Build the PipelineDefinition for Metagenome Assembly (jgi_metaAssembly), version 0.2.0. """
    return PipelineDefinition(
        name="metaassembly",
        version=semver.Version(0, 2, 0),
        description=_DESCRIPTION,
        input_model=MetaAssemblyInput,
        nersc_path=_NERSC_WDL_PATH,
        main_wdl="jgi_assembly.wdl",
        file_md5s=_FILE_MD5S,
        output_keys=_OUTPUT_KEYS,
        doc_urls=_DOC_URLS,
    )
