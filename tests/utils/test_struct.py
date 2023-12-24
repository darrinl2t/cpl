# -*- coding: utf-8 -*-

"""
caelus.utils.struct Tests
"""

import pytest
from caelus.utils.struct import Struct, merge

def test_access():
    """Test basic key/attribute access patterns"""
    obj = Struct(a=1, b=2, c=3)
    obj.abc = 10
    obj["xyz"] = 20
    assert obj.a == 1
    assert obj.xyz == 20
    assert obj["abc"] == 10
    with pytest.raises(AttributeError):
        _ = obj.ijk

def test_merge_update():
    """Test dictionary merging"""
    base = Struct(
        LESModel="oneEqEddy",
        delta="bananas",
        printCoeffs="on",
        cubeRootVolCoeffs={
            "deltaCoeff": 1.0,
        },)
    prandtl_coeffs = Struct(
        delta="cubeRootVol",
        smoothCoeffs=dict(
            delta="cubeRootVol",
            maxDeltaRatio=1.1
        ),)

    base.merge(prandtl_coeffs)
    assert base.delta == "cubeRootVol"
    assert "smoothCoeffs" in base

test_yaml = """
caelus:

  caelus_cml:
    default: latest

    versions:
      - version: v7.04
        path: ~/Caelus/caelus-7.04/

      - version: v6.10
        path: ~/Caelus/caelus-6.10/

      - version: v6.04
        path: ~/Caelus/caelus-6.04/
"""

# pylint: disable=line-too-long
yaml_out_string = '{caelus: {caelus_cml: {default: latest, versions: [{version: v7.04, path: ~/Caelus/caelus-7.04/},\n        {version: v6.10, path: ~/Caelus/caelus-6.10/}, {version: v6.04, path: ~/Caelus/caelus-6.04/}]}}}\n'

def test_yaml_parse():
    """Test loading of YAML data"""
    obj = Struct.from_yaml(test_yaml)
    cml_info = obj.caelus.caelus_cml
    assert cml_info.default == "latest"
    assert cml_info.versions[0].version == "v7.04"

def test_yaml_output():
    """Test writing YAML data"""
    obj = Struct.from_yaml(test_yaml)
    out = obj.to_yaml(default_flow_style=True)
    assert out == yaml_out_string

def test_yaml_load(tmpdir):
    yfile = tmpdir.join("test.yaml")
    yfile.write(test_yaml)
    obj = Struct.load_yaml(str(yfile))
    assert("caelus" in obj)

def test_merge():
    obj1 = Struct.from_yaml(test_yaml)
    obj2 = Struct.from_yaml(test_yaml)
    merge(obj1, obj2)


def test_get_set():
    obj = Struct.from_yaml(test_yaml)
    assert(obj.pget("caelus.caelus_cml.default") == 'latest')
    obj.pset("caelus.caelus_cml.default", 'v6.10')
    obj.pset("caelus.p1.p2.p3", 10)
    assert(
        obj.pget("caelus.p1.p2.p3") == 10)
