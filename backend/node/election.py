# election.py

import httpx
import os

from node.cluster import NODES, SELF


async def get_alive_nodes(include_self=True):
    alive_nodes = []
    for node in NODES:
        if node==SELF and not include_self:
            continue
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(f"{node}/health")
                if res.json()["status"] == "alive":
                    alive_nodes.append(node)
        except:
            continue

    return alive_nodes


async def elect_new_master():

    alive_nodes = await get_alive_nodes()
    new_master = alive_nodes[0]

    for node in NODES:
        if node == SELF:
            continue
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.post(f"{node}/set_master", json={"master": new_master})
        except:
            continue

    return new_master
