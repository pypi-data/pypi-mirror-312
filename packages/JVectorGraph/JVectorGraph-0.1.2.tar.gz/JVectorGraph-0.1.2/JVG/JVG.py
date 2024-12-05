import webbrowser
import os
import urllib.parse
import http.server
import socketserver
import threading
from matplotlib.figure import Figure
import pkg_resources
import matplotlib.pyplot as plt
from matplotlib import rc
rc("svg", fonttype='path')
import time




class mpl_editor:
    
    def __init__(self, figure:Figure):
        
        self.figure = figure
        def get_package_directory():
            return pkg_resources.resource_filename(__name__, '')
        
        self._package_path = get_package_directory()
        self._cwd = os.getcwd()

        
        

    def save_tmp(self):
        self.figure.savefig(os.path.join(self._package_path, 'tmp.svg'), format='svg', bbox_inches='tight', transparent=True)

        
    
    def run_server(self):

        # Start the HTTP server
        socketserver.TCPServer.allow_reuse_address = True
        handler = http.server.SimpleHTTPRequestHandler
        handler.directory = self._package_path
        httpd = socketserver.TCPServer(("", 8005), handler)
        httpd.serve_forever()
    
       
        
    def open_in_browser(self):
        
        file_path = 'vecedit.html'
        argument = 'tmp.svg'

        file_path = file_path.replace("\\", "/")
        argument = argument.replace("\\", "/")


        url_with_argument = f"http://localhost:8005/{os.path.basename(file_path)}?graph={urllib.parse.quote(argument)}"

        webbrowser.open(url_with_argument)
    
    def del_tmp(self):
        
        try:
            if os.path.exists(os.path.join(self._package_path, 'tmp.svg')):
                os.remove(os.path.join(self._package_path, 'tmp.svg'))
        except:
            pass
    
    
    def edit(self):
        
        self.save_tmp()
            
        os.chdir(self._package_path)
        server_thread = threading.Thread(target=self.run_server, daemon=True)
        server_thread.start()
        time.sleep(1)
        
        self.open_in_browser()
            
            
        os.chdir(self._cwd)
        
        time.sleep(2)

        self.del_tmp()
        
        