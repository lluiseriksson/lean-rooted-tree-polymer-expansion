#!/usr/bin/env python3
"""Validate the machine-readable proof dependency graph against theorem metadata."""
from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

from project_config import ROOT, load_project


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    project = load_project(root)
    graph = _load(root / "archive/proof-dag.json")
    manifest = _load(root / "archive/theorem-manifest.json")
    if graph.get("schema_version") != 1:
        errors.append("proof DAG schema_version must be 1")
    if graph.get("artifact") != project["artifact_title"]:
        errors.append("proof DAG artifact title differs from project.json")
    if graph.get("version") != project["version"]:
        errors.append("proof DAG version differs from project.json")

    nodes = graph.get("nodes") if isinstance(graph.get("nodes"), list) else []
    edges = graph.get("edges") if isinstance(graph.get("edges"), list) else []
    by_id: dict[str, dict[str, Any]] = {}
    by_name: dict[str, dict[str, Any]] = {}
    for node in nodes:
        if not isinstance(node, dict):
            errors.append("non-object node in proof DAG")
            continue
        node_id = node.get("id")
        qname = node.get("qualified_name")
        if not isinstance(node_id, str) or node_id in by_id:
            errors.append(f"duplicate or invalid proof DAG node id: {node_id!r}")
            continue
        if not isinstance(qname, str) or qname in by_name:
            errors.append(f"duplicate or invalid theorem name in proof DAG: {qname!r}")
        by_id[node_id] = node
        if isinstance(qname, str):
            by_name[qname] = node

    adjacency: dict[str, list[str]] = defaultdict(list)
    indegree = {node_id: 0 for node_id in by_id}
    seen_edges: set[tuple[str, str, str]] = set()
    for edge in edges:
        if not isinstance(edge, dict):
            errors.append("non-object edge in proof DAG")
            continue
        source, target, relation = edge.get("from"), edge.get("to"), edge.get("relation")
        key = (str(source), str(target), str(relation))
        if key in seen_edges:
            errors.append(f"duplicate proof DAG edge: {key}")
        seen_edges.add(key)
        if source not in by_id or target not in by_id:
            errors.append(f"proof DAG edge references unknown node: {source!r} -> {target!r}")
            continue
        if source == target:
            errors.append(f"proof DAG self-loop: {source}")
            continue
        adjacency[source].append(target)
        indegree[target] += 1

    queue = deque(sorted(node_id for node_id, degree in indegree.items() if degree == 0))
    visited: list[str] = []
    while queue:
        node_id = queue.popleft()
        visited.append(node_id)
        for target in adjacency[node_id]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if len(visited) != len(by_id):
        errors.append("proof DAG contains a directed cycle")

    endpoints = manifest.get("endpoints", [])
    expected_public = {
        endpoint.get("qualified_public_name"): endpoint
        for endpoint in endpoints
        if isinstance(endpoint, dict)
    }
    actual_public = {
        node.get("qualified_name"): node
        for node in nodes
        if isinstance(node, dict) and node.get("kind") == "public-endpoint"
    }
    if set(actual_public) != set(expected_public):
        errors.append("proof DAG public endpoint set differs from theorem manifest")

    for endpoint in endpoints:
        if not isinstance(endpoint, dict):
            continue
        upstream_name = endpoint.get("upstream_name")
        public_name = endpoint.get("qualified_public_name")
        source_node = by_name.get(str(upstream_name))
        public_node = by_name.get(str(public_name))
        if source_node is None:
            errors.append(f"proof DAG missing upstream theorem: {upstream_name}")
            continue
        if public_node is None:
            errors.append(f"proof DAG missing public endpoint: {public_name}")
            continue
        if source_node.get("source") != endpoint.get("source"):
            errors.append(f"proof DAG source path mismatch for {upstream_name}")
        if source_node.get("source_blob_sha") != endpoint.get("source_blob_sha"):
            errors.append(f"proof DAG source blob mismatch for {upstream_name}")
        if public_node["id"] not in adjacency[source_node["id"]]:
            errors.append(f"proof DAG lacks direct re-export edge for {public_name}")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        raise SystemExit("Proof DAG audit failed:\n" + "\n".join(f"- {e}" for e in errors))
    graph = _load(ROOT / "archive/proof-dag.json")
    print(f"proof DAG audit: OK ({len(graph['nodes'])} nodes; {len(graph['edges'])} edges)")


if __name__ == "__main__":
    main()
