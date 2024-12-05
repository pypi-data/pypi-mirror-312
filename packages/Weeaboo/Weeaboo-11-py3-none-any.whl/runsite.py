'Website entrypoint.'
from aridity.config import ConfigCtrl
from lagoon import mod_wsgi_express
from pathlib import Path
import os

def main():
    cc = ConfigCtrl()
    cc.load('/site/deploy/LOADME.arid')
    config = cc.node
    stat = Path(config.img.root).stat()
    os.setgid(stat.st_gid)
    os.setuid(stat.st_uid)
    del os.environ['HOME']
    mod_wsgi_express.start_server.__log_to_terminal.__application_type.module[exec]('--include-file', '/site/deploy/httpd.conf', '--document-root', config.htdocs.root, 'weeaboo.wsgi')

if '__main__' == __name__:
    main()
