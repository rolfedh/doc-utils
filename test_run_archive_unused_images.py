import tempfile
import os
import subprocess
from test_fixture_archive_unused_images import setup_test_fixture

def run_script_in_fixture(script_path, archive=False, exclude_args=None):
    with tempfile.TemporaryDirectory() as tmpdir:
        setup_test_fixture(tmpdir)
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
    run_script_in_fixture('../archive_unused_images.py')
    # Example: run with --archive
    run_script_in_fixture('../archive_unused_images.py', archive=True)
    # Example: run with exclusions
    run_script_in_fixture('../archive_unused_images.py', exclude_args=['--exclude-dir', './images', '--exclude-file', './images/unused1.png'])
