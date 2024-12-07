# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .snippet import Snippet
from .._models import BaseModel

__all__ = ["Snippets"]


class Snippets(BaseModel):
    result_count: int = FieldInfo(alias="resultCount")

    results: Optional[List[Snippet]] = None
