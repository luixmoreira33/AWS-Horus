import pytest
from collector.collector import Edge

def test_edge_defaults():
    e = Edge(source_arn="arn:aws:lambda:us-east-1:123:function:test", target_arn="arn:aws:iam::123:role/test")
    assert e.evidence_level == "DECLARADA"
    assert e.category == "IAM/AUTORIZAÇÃO"
    assert e.first_seen is not None

def test_edge_custom():
    e = Edge(
        source_arn="a",
        target_arn="b",
        category="REDE",
        mechanism="security-group-rule",
        ports=[443],
        protocol="tcp",
        evidence_level="PERMITIDA",
        risk="medium"
    )
    assert e.ports == [443]
    assert e.evidence_level == "PERMITIDA"
