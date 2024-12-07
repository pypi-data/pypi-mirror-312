# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Snippet"]


class Snippet(BaseModel):
    doc_id: str = FieldInfo(alias="docId")

    document_url: str = FieldInfo(alias="documentUrl")

    language: str

    name: str

    snippet: str

    source: str

    year: int
