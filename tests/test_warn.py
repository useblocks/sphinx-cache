from pathlib import Path

import pytest


@pytest.mark.parametrize("test_app", [{"buildername": "html", "srcdir": "doc_test/doc_basic"}], indirect=True)
def test_restore_cache_skipped_envpickle_404(test_app):
    """
    Test to check if the cache restore feature is skipped
    when `environment.pickle` is not in and cache directory
    :param test_app: Sphinx test app fixture
    :return:
    """
    import subprocess

    app = test_app

    src_dir = Path(app.srcdir)
    out_dir = Path(app.outdir)
    output = subprocess.run(["sphinx-build", "-b", "html", src_dir, out_dir], capture_output=True)
    # restore cache skipped because `environment.pickle` is not in cache directory
    assert (
        f"⚠️ Skipped cache restore - Reason: `environment.pickle` file not found in {app.config.cache_store_path}"
        in output.stdout.decode("utf-8")
    )

    # store cache was successful
    assert "✅ Storing Done" in output.stdout.decode("utf-8")


@pytest.mark.parametrize("test_app", [{"buildername": "html", "srcdir": "doc_test/doc_basic"}], indirect=True)
def test_restore_cache_skipped_envpickle_exist(test_app):
    """
    Test to check if the cache restore feature is skipped
    when `environment.pickle` is in and .doctrees directory
    :param test_app: Sphinx test app fixture
    :return:
    """
    import subprocess

    app = test_app

    src_dir = Path(app.srcdir)
    out_dir = Path(app.outdir)
    output = subprocess.run(["sphinx-build", "-b", "html", src_dir, out_dir], capture_output=True)
    # restore cache skipped because `environment.pickle` is not in and cache directory
    assert (
        f"⚠️ Skipped cache restore - Reason: `environment.pickle` file not found in {app.config.cache_store_path}"
        in output.stdout.decode("utf-8")
    )

    # store cache was successful
    assert "✅ Storing Done" in output.stdout.decode("utf-8")

    # Second sphinx_build
    output_2 = subprocess.run(["sphinx-build", "-b", "html", src_dir, out_dir], capture_output=True)
    # restore cache skipped because `environment.pickle` is in and .doctrees directory
    assert (
        f"⚠️ Skipped cache restore - Reason: `environment.pickle` file "
        f"exists already in {app.config.cache_doctree_path}" in output_2.stdout.decode("utf-8")
    )

    # store cache was successful
    assert "✅ Storing Done" in output_2.stdout.decode("utf-8")
