import os
import shutil
import subprocess as sp
import tempfile
import unittest


class FullRunTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

        self.reads_fp = os.path.abspath(".tests/data/reads/")
        self.db_fp = os.path.abspath(".tests/data/db/")

        self.project_dir = os.path.join(self.temp_dir, "project/")

        sp.check_output(
            ["sunbeam", "init", "--data_fp", self.reads_fp, self.project_dir]
        )

        self.config_fp = os.path.join(self.project_dir, "sunbeam_config.yml")

        config_str = f"sbx_kraken: {{kraken_db_fp: {self.db_fp}}}"

        sp.check_output(
            [
                "sunbeam",
                "config",
                "modify",
                "-i",
                "-s",
                f"{config_str}",
                f"{self.config_fp}",
            ]
        )

        self.output_fp = os.path.join(self.project_dir, "sunbeam_output")
        # shutil.copytree(".tests/data/sunbeam_output", self.output_fp)

        self.all_samples_fp = os.path.join(
            self.output_fp, "classify/kraken/all_samples.tsv"
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_full_run(self):
        # Run the test job.
        sp.check_output(
            [
                "sunbeam",
                "run",
                "--profile",
                self.project_dir,
                "all_classify",
                "--directory",
                self.temp_dir,
            ]
        )

        # Check output
        self.assertTrue(os.path.exists(self.all_samples_fp))
        import sys
        sys.stderr("HERE")
        print("THERE")
        with open(self.all_samples_fp) as f:
            lines = f.readlines()
            sys.stderr(f"{len(lines)}")
            sys.stderr(f"{lines[0]}\n{lines[1]}\n{lines[2]}")
        self.assertTrue(False)

