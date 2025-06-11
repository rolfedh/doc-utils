import os
import sys
import tempfile
import pytest
from test_fixture_check_scannability import setup_test_fixture_check_scannability
import subprocess

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'check_scannability.py'))

def run_script(args, cwd):
    result = subprocess.run([sys.executable, SCRIPT] + args, cwd=cwd, capture_output=True, text=True)
    return result

def test_check_scannability_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        setup_test_fixture_check_scannability(tmpdir)
        result = run_script([], cwd=tmpdir)
        # Should flag the long sentence and long paragraph in test1.adoc
        assert 'too long' in result.stdout or 'too many sentences' in result.stdout
        # Should not flag test2.adoc
        assert 'test2.adoc' not in result.stderr

@pytest.mark.parametrize('args,should_flag', [
    (['--max-sentence-length', '10'], True),
    (['--max-paragraph-sentences', '3'], True),
])
def test_check_scannability_custom_limits(args, should_flag):
    with tempfile.TemporaryDirectory() as tmpdir:
        setup_test_fixture_check_scannability(tmpdir)
        result = run_script(args, cwd=tmpdir)
        if should_flag:
            assert 'too long' in result.stdout or 'too many sentences' in result.stdout
