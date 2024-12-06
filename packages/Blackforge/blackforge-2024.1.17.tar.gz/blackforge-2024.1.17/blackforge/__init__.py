"""
d34d0s' BLACKFORGE

[ game development framework ]
"""

import blackforge.app as app

import blackforge.input as input
import blackforge.events as events

import blackforge.gfx as gfx
import blackforge.asset as asset
import blackforge.resource as resource

import blackforge.world as world
import blackforge.entity as entity
import blackforge.object as object

import blackforge.AI as AI

import os, platform, blackforge.version as ver
if "BLACKFORGE_NO_PROMT" not in os.environ:
    print(
        f"BlackForge {ver.BLACKFORGE_YEAR}.{ver.BLACKFORGE_MINOR}.{ver.BLACKFORGE_PATCH} | Random Quote Here..."
    )