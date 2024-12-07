# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DocumentByIDParams"]


class DocumentByIDParams(TypedDict, total=False):
    doc_id: Required[Annotated[str, PropertyInfo(alias="docId")]]
    """The `docId` of the document that should be returned."""
