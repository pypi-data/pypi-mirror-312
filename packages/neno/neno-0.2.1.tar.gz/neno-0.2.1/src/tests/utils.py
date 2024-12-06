
CONFIG_TEMPLATE = """
host: "127.0.0.1"
port: %d
backends:
  dataBackend:
    filesystem:
      path: "%s/data"
  configBackend:
    filesystem:
      path: "%s/config"
"""

import tempfile, random, subprocess, os, shutil, time

class NenoTestInstance:
  def __init__(self):
    self.config_dir = tempfile.mkdtemp()
    self.backend_dir = self.config_dir
    self.config_path = f"{self.config_dir}/config.yaml"
    self.port_number = random.randint(20000, 60000)
    
  def __enter__(self):
    with open(self.config_path, "w") as f:
      f.write(CONFIG_TEMPLATE % (self.port_number, self.config_dir, self.config_dir))
    self.command = ["python", "-m", "neno", "serve", "--config-file", self.config_path]
    self.cwd = os.getcwd()
    print(f"Running neno with command: {' '.join(self.command)} (in working directory: {self.cwd})")
    self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # wait a bit for the process to start
    time.sleep(1)
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    # kill the process
    # remove the temporary directory
    print(f"Kill neno process (PID {self.process.pid})")
    self.process.kill()
    #shutil.rmtree(self.config_dir)

    
