import socket
import os
from opendm import log

PROGRESS_BROADCAST_PORT = 6367 #ODMR
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
    log.ODM_WARNING("Cannot create UDP socket, progress reporting will be disabled.")
    sock = None

class Broadcaster:
    def __init__(self, port):
        self.port = port
        self.project_name = "<unnamed>"
        self.pid = os.getpid()

    def set_project_name(self, project_name):
        self.project_name = project_name

    def send_update(self, global_progress, stage_progress, stage):
        """
        Update any listener on the pipeline progress (in percentage terms)
        """
        if not sock:
            return

        UDP_IP = "127.0.0.1"

        if global_progress > 100:
            log.ODM_WARNING("Global progress is > 100, please contact the developers.")
            global_progress = 100

        try:
            sock.sendto("PGUP/{}/{}/{}/{}/{}".format(self.pid, self.project_name, float(global_progress), float(stage_progress), stage).encode('utf-8'), (UDP_IP, self.port))
        except:
            log.ODM_WARNING("Failed to broadcast progress update on UDP port %s" % str(self.port))

progressbc = Broadcaster(PROGRESS_BROADCAST_PORT)