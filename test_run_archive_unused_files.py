import tempfile
import os
import subprocess
from test_fixture_archive_unused_files import setup_test_fixture_archive_unused_files

def run_script_in_fixture(script_path, archive=False, exclude_args=None):
    with tempfile.TemporaryDirectory() as tmpdir:
        setup_test_fixture_archive_unused_files(tmpdir)
        cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            cmd = ['python3', script_path]
            if archive:
                cmd.append('--archive')
            if exclude_args:
                cmd.extend(exclude_args)
            result = subprocess.run(cmd, capture_output=True, text=True)
            print('STDOUT:')
            print(result.stdout)
            print('STDERR:')
            print(result.stderr)
            # List files in archive dir for verification
            archive_dir = os.path.join(tmpdir, 'archive')
            print('Archive dir contents:', os.listdir(archive_dir))
        finally:
            os.chdir(cwd)

if __name__ == '__main__':
    # Example: run without exclusions
    run_script_in_fixture('../archive_unused_files.py')
    # Example: run with --archive
    run_script_in_fixture('../archive_unused_files.py', archive=True)
    # Example: run with exclusions
    run_script_in_fixture('../archive_unused_files.py', exclude_args=['--exclude-dir', './modules', '--exclude-file', './modules/unused1.adoc'])
