import subprocess
import os
import atexit
import tempfile
import tarfile
import shutil
import boto3
import mimetypes

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    setup()
    # Output Git version to Log
    os_command("git --version")
    shutil.copyfile('hugo', '/tmp/hugo')
    os.chmod('/tmp/hugo', 0555)
    # Output Hugo version to Log
    os_command("/tmp/hugo version")
    # Get repository path from user enviornmental variables
    GIT_REPO = os.environ['GIT_REPO']
    os_command("git clone --recurse-submodules " + GIT_REPO + " /tmp/blog")
    os.chdir("/tmp/blog")
    os_command('/tmp/hugo')
    S3_BUCKET = os.environ['S3_BUCKET']
    for root, dirs, files in os.walk('/tmp/blog/public/'):
        for file in files:
            filepath = os.path.join(root, file)
            mimetype = mimetypes.guess_type(filepath)
            data = open(filepath, 'rb')
            s3.Bucket(S3_BUCKET).put_object(Key=filepath[17:], Body=data, ContentType=mimetype[0])
    print("Upload complete")


def os_command(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE) 
    output, error = process.communicate()
    print(output)

def setup(target_directory=None,
          update_env=True):

    if not target_directory:
        target_directory = tempfile.mkdtemp()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    tar = tarfile.open(os.path.join(dir_path, 'git-2.14.0.tar'))
    tar.extractall(target_directory)
    git_path = os.path.join(target_directory, 'git')

    bin_path = os.path.join(git_path, 'bin')

    template_dir = os.path.join(
        git_path,
        'share',
        'git-core',
        'templates'
    )

    exec_path = os.path.join(
        git_path,
        'libexec',
        'git-core'
    )

    if update_env:
        os.environ['PATH'] = bin_path + ':' + os.environ['PATH']
        os.environ['GIT_TEMPLATE_DIR'] = template_dir
        os.environ['GIT_EXEC_PATH'] = exec_path

    atexit.register(teardown, target_directory)

def teardown(git_dir):
    shutil.rmtree(git_dir)