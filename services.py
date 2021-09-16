from __future__ import annotations

import model
from model import OrderLine
from repository import AbstractRepository
from typing import Optional
from datetime import date


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], repo: AbstractRepository, session):
    repo.add(model.Batch(ref, sku, qty, eta))
    session.commit()


def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref

def deallocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.deallocate(line, batches)
    session.commit()
    return batchref