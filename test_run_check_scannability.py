import tempfile
import os
import subprocess
from test_fixture_check_scannability import setup_test_fixture_check_scannability

def run_script_in_fixture(script_path, extra_args=None):
    with tempfile.TemporaryDirectory() as tmpdir:
        setup_test_fixture_check_scannability(tmpdir)
        cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            cmd = ['python3', script_path]
            if extra_args:
                cmd.extend(extra_args)
            result = subprocess.run(cmd, capture_output=True, text=True)
            print('STDOUT:')
            print(result.stdout)
            print('STDERR:')
            print(result.stderr)
            # List files in tmpdir for verification
            print('Test dir contents:', os.listdir(tmpdir))
        finally:
            os.chdir(cwd)

if __name__ == '__main__':
    # Example: run with default settings
    run_script_in_fixture('../check_scannability.py')
    # Example: run with custom limits
    run_script_in_fixture('../check_scannability.py', extra_args=['--max-sentence-length', '10', '--max-paragraph-sentences', '3'])
