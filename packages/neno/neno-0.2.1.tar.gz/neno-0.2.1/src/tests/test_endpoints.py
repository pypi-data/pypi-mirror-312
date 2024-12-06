import os, time
from utils import NenoTestInstance
from typer.testing import CliRunner

import sys
neno_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "neno"))
sys.path.append(neno_path)
print("Added neno path to sys.path:", neno_path)

from client import cliApp

tests_dir = os.path.dirname(__file__)

runner = CliRunner()

def test_show_help():
  with NenoTestInstance() as neno:
    result = runner.invoke(cliApp, ["--help"])
    assert "Usage" in result.stdout
    assert result.exit_code == 0

def test_delete_non_existing_endpoint():
  with NenoTestInstance() as neno:
    env={"NENO_SERVER_URL": f"http://127.0.0.1:{neno.port_number}"}
    result = runner.invoke(cliApp, ["delete", "endpoint", "/api/non-existing-endpoint"], env=env)
    assert "Failed to delete endpoint" in result.stdout
    assert result.exit_code != 0

def test_add_delete_endpoint():
  with NenoTestInstance() as neno:
    env={"NENO_SERVER_URL": f"http://127.0.0.1:{neno.port_number}"}
    endpoint_name = "test_add_endpoint"
    notebook_path = f"{tests_dir}/example-endpoint/test-notebook.ipynb"
    result = runner.invoke(cliApp, ["add", "endpoint", endpoint_name, "--notebook", notebook_path, "--output", "cell", "--keep-runs", "always"], env=env)
    if result.exit_code != 0:
      print(result.stdout)
    assert result.exit_code == 0
    assert f"Uploaded endpoint {endpoint_name}" in result.stdout

    time.sleep(1)

    # now delete the endpoint again
    result = runner.invoke(cliApp, ["delete", "endpoint", "/api/" + endpoint_name], env=env)
    assert result.exit_code == 0
    assert f"Deleted endpoint /api/{endpoint_name}" in result.stdout

