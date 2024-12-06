import os, sys
from pathlib import Path


def load_path():
    file = Path(__file__).resolve()
    parent, root = file.parent, file.parents[1]
    sys.path.append(str(root))

    # Additionally remove the current file's directory from sys.path
    try:
        sys.path.remove(str(parent))
    except ValueError:  # Already removed
        pass


# actually load all user-defined paths
load_path()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.biomodels_restful_api_client.constants as bmconstants
import src.biomodels_restful_api_client.services as bmservices
