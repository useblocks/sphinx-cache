import os
from pathlib import Path

import pytest


@pytest.mark.parametrize("test_app", [{"buildername": "html", "srcdir": "doc_test/doc_basic"}], indirect=True)
def test_restore_cache_done(test_app):
    """
    Test to check if the cache restore feature completes successfully
    :param test_app: Sphinx test app fixture
    :return:
    """
    import subprocess

    app = test_app

    src_dir = Path(app.srcdir)
    out_dir = Path(app.outdir)
    output = subprocess.run(["sphinx-build", "-b", "html", src_dir, out_dir], capture_output=True)
    # Restore cache skipped because `environment.pickle` is not in cache directory
    assert "⚠️ Skipped cache restore because we cannot find any cache to restore." in output.stdout.decode("utf-8")

    # Remove `environment.pickle` file from doctree directory
    os.remove(Path(app.doctreedir).joinpath("environment.pickle"))

    # Second sphinx_build
    output_2 = subprocess.run(["sphinx-build", "-b", "html", src_dir, out_dir], capture_output=True)
    # Restore cache was successful
    assert "✅ Restoring Done" in output_2.stdout.decode("utf-8")


@pytest.mark.parametrize("test_app", [{"buildername": "html", "srcdir": "doc_test/doc_basic"}], indirect=True)
def test_store_cache_done(test_app):
    """
    Test to check if the cache store feature completes successfully
    :param test_app: Sphinx test app fixture
    :return:
    """
    import subprocess

    app = test_app

    src_dir = Path(app.srcdir)
    out_dir = Path(app.outdir)
    output = subprocess.run(["sphinx-build", "-b", "html", src_dir, out_dir], capture_output=True)

    # Store cache was successful
    assert "✅ Storing Done" in output.stdout.decode("utf-8")

    # Second sphinx_build
    output_2 = subprocess.run(["sphinx-build", "-b", "html", src_dir, out_dir], capture_output=True)
    # Restore cache skipped because `environment.pickle` is in and .doctrees directory
    assert "⚠️ Skipped cache restore because we can use the found cache." in output_2.stdout.decode("utf-8")

    # Store cache was successful
    assert "✅ Storing Done" in output_2.stdout.decode("utf-8")
