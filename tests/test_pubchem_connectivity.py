import time
import urllib.request
import urllib.parse
import urllib.error
import json
import pytest


def test_pubchem_smiles_resolves():
    smiles = urllib.parse.quote("c1ccncc1")  # pyridine
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/JSON"
    last_err = None
    for attempt in range(10):
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read())
            assert data["IdentifierList"]["CID"][0] > 0  # any CID at all
            assert data["IdentifierList"]["CID"][0] == 1049  # the actual CID
            return
        except urllib.error.URLError as exc:
            last_err = exc
            is_server_busy = isinstance(exc, urllib.error.HTTPError) and exc.code == 503
            is_timeout = isinstance(exc, TimeoutError) or not isinstance(exc, urllib.error.HTTPError)
            if not is_server_busy and not is_timeout:
                raise
            time.sleep(10 ** attempt)
    pytest.fail(f"PubChem unreachable after retries: {last_err}")
