import logging

from modules.base_module import BaseModule

log = logging.getLogger(__name__)

import subprocess
import os
import shlex
from datetime import date
from datetime import datetime

def scp(src, remote, destination, args=''):
    cmd = 'scp {0} {3} {1}:{2}'.format(src, remote, destination, args)
    log.debug('Executing command \'{0}\''.format(cmd))
    rc = subprocess.call(cmd.split())
    return rc

def ssh(remote, cmd, args=''):
    cmd = 'ssh -x {2} {0} {1}'.format(remote, cmd, args)
    log.debug('Executing command \'{0}\''.format(cmd))
    print cmd.split()
    rc = subprocess.call(shlex.split(cmd))
    return rc


class CopyToWebModule(BaseModule):
    def __init__(self):
        super(CopyToWebModule, self).__init__()
        self.arg_group.add_argument('--www', nargs='+', type='str2kvstr', action='setting', help='')

    def __call__(self, config):
        remote_host = 'sieber@ekplx77.physik.uni-karlsruhe.de' 
        remote_basedir = 'public_html/private/plots/'


        if (ssh(remote_host, args='-oNumberOfPasswordPrompts=0 -o ConnectTimeout=5', cmd='echo Connection succeded.') == 0):
            log.debug('Passwordless ssh is working. Continue with copying stuff.')
            folder_name = date.today().isoformat()

            output_file = config['output_path']
            current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            remote_filename = '{0}_{1}{2}'.format(os.path.splitext(config['output_path'])[0], current_datetime, os.path.splitext(config['output_path'])[1])
            log.debug('Try to create folder {0} on remote host.'.format(os.path.join(remote_basedir, folder_name)))
            ssh(remote_host, 'mkdir -p {0}'.format(os.path.join(remote_basedir, folder_name)))
            log.debug('Copying the output file.')
            scp(os.path.join(config['output_prefix'], config['output_path']), remote_host, os.path.join(remote_basedir, folder_name, remote_filename))
            scp(os.path.join(config['output_prefix'], config['output_path'].replace('.png', '.json')), remote_host, os.path.join(remote_basedir, folder_name, remote_filename.replace('.png','.json')))
            scp(os.path.join(config['output_prefix'], config['output_path'].replace('.png', '.pdf')), remote_host, os.path.join(remote_basedir, folder_name, remote_filename.replace('.png','.pdf')))
            log.debug('Calling the gallery preparation file.')
            ssh(remote_host, '\'{0}/prep_gallery.py {1}\''.format(remote_basedir, os.path.join(remote_basedir, folder_name)))
        else:
            log.error('Passwordless ssh is not working. Omitting the plot backup.')

