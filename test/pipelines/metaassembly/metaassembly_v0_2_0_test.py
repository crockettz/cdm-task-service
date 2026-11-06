# Input model behavior is shared with v0.1.0 and tested in metaassembly_v0_1_0_test.py.

from pathlib import Path

import semver

from cdmtaskservice import models
from cdmtaskservice.pipelines.metaassembly import v0_2_0
from cdmtaskservice.pipelines.metaassembly.v0_1_0 import (
    MetaAssemblyFiles, MetaAssemblyInput, MetaAssemblyParams, ReadMode,
)

_F1 = models.S3File(file="bucket/reads_1.fastq.gz")
_F2 = models.S3File(file="bucket/reads_2.fastq.gz")


def test_init():
    p = v0_2_0.init()

    assert p.name == "metaassembly"
    assert p.version == semver.Version.parse("0.2.0")
    assert p.description == (
        "Metagenome assembly of Illumina short reads: error correction via BBTools (bbcms), "
        "assembly via metaSPAdes, and coverage statistics from mapping reads back to the "
        "assembly via bbmap."
    )
    assert p.input_model is MetaAssemblyInput
    assert p.nersc_path == Path(
        "/global/cfs/cdirs/kbase/cdm_task_service/pipelines/metaassembly/0.2.0/metaAssembly/"
    )
    assert p.main_wdl == "jgi_assembly.wdl"
    assert dict(p.file_md5s) == {
        "jgi_assembly.wdl": "d268039220dcc628f42f2eb628624be2",
        "shortReads_assembly.wdl": "0fc40b6bb465bafb5fa32643a36bbd12",
        "make_interleaved_reads.wdl": "5a70ad09514da5845af6ba79af1856f4",
    }
    assert p.output_keys == {
        "jgi_metaAssembly.sr_contig",
        "jgi_metaAssembly.sr_scaffold",
        "jgi_metaAssembly.sr_agp",
        "jgi_metaAssembly.sr_covstats",
        "jgi_metaAssembly.sr_asminfo",
        "jgi_metaAssembly.stats",
    }
    assert p.doc_urls == [
        "https://github.com/kbaseincubator/metaAssembly",
        "https://docs.microbiomedata.org/workflows/chapters/4_Metagenome_Assembly/",
    ]


def test_init_validate_input_then_get_input_json_paired():
    p = v0_2_0.init()
    inp = MetaAssemblyInput(
        input=MetaAssemblyParams(read_mode=ReadMode.PAIRED, output_prefix="proj-xyz"),
        files=MetaAssemblyFiles(input_file=_F1, input_file2=_F2),
    )
    locs = {
        _F1.file: Path("/scratch/cache/aa/reads_1.fastq.gz"),
        _F2.file: Path("/scratch/cache/bb/reads_2.fastq.gz"),
    }

    run = p.validate_input(inp).get_input_json(locs)

    assert run == {
        "jgi_metaAssembly.proj": "proj-xyz",
        "jgi_metaAssembly.shortRead": True,
        "jgi_metaAssembly.threads": "16",
        "jgi_metaAssembly.input_files": [
            "/scratch/cache/aa/reads_1.fastq.gz",
            "/scratch/cache/bb/reads_2.fastq.gz",
        ],
    }
