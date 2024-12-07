# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from justement import Justement, AsyncJustement
from tests.utils import assert_matches_type
from justement.types import (
    Snippet,
    Document,
    DocumentCountResponse,
)
from justement.pagination import SyncJustementPagination, AsyncJustementPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDocument:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_by_id(self, client: Justement) -> None:
        document = client.document.by_id(
            doc_id="docId",
        )
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    def test_raw_response_by_id(self, client: Justement) -> None:
        response = client.document.with_raw_response.by_id(
            doc_id="docId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    def test_streaming_response_by_id(self, client: Justement) -> None:
        with client.document.with_streaming_response.by_id(
            doc_id="docId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_by_ref(self, client: Justement) -> None:
        document = client.document.by_ref(
            doc_ref="docRef",
        )
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    def test_raw_response_by_ref(self, client: Justement) -> None:
        response = client.document.with_raw_response.by_ref(
            doc_ref="docRef",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    def test_streaming_response_by_ref(self, client: Justement) -> None:
        with client.document.with_streaming_response.by_ref(
            doc_ref="docRef",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_count(self, client: Justement) -> None:
        document = client.document.count()
        assert_matches_type(DocumentCountResponse, document, path=["response"])

    @parametrize
    def test_method_count_with_all_params(self, client: Justement) -> None:
        document = client.document.count(
            classification_facet=["string"],
            query="query",
        )
        assert_matches_type(DocumentCountResponse, document, path=["response"])

    @parametrize
    def test_raw_response_count(self, client: Justement) -> None:
        response = client.document.with_raw_response.count()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentCountResponse, document, path=["response"])

    @parametrize
    def test_streaming_response_count(self, client: Justement) -> None:
        with client.document.with_streaming_response.count() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentCountResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_search(self, client: Justement) -> None:
        document = client.document.search()
        assert_matches_type(SyncJustementPagination[Snippet], document, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: Justement) -> None:
        document = client.document.search(
            classification_facet=["string"],
            language="de",
            page=1,
            query="query",
        )
        assert_matches_type(SyncJustementPagination[Snippet], document, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: Justement) -> None:
        response = client.document.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(SyncJustementPagination[Snippet], document, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: Justement) -> None:
        with client.document.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(SyncJustementPagination[Snippet], document, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDocument:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_by_id(self, async_client: AsyncJustement) -> None:
        document = await async_client.document.by_id(
            doc_id="docId",
        )
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    async def test_raw_response_by_id(self, async_client: AsyncJustement) -> None:
        response = await async_client.document.with_raw_response.by_id(
            doc_id="docId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    async def test_streaming_response_by_id(self, async_client: AsyncJustement) -> None:
        async with async_client.document.with_streaming_response.by_id(
            doc_id="docId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_by_ref(self, async_client: AsyncJustement) -> None:
        document = await async_client.document.by_ref(
            doc_ref="docRef",
        )
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    async def test_raw_response_by_ref(self, async_client: AsyncJustement) -> None:
        response = await async_client.document.with_raw_response.by_ref(
            doc_ref="docRef",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    async def test_streaming_response_by_ref(self, async_client: AsyncJustement) -> None:
        async with async_client.document.with_streaming_response.by_ref(
            doc_ref="docRef",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_count(self, async_client: AsyncJustement) -> None:
        document = await async_client.document.count()
        assert_matches_type(DocumentCountResponse, document, path=["response"])

    @parametrize
    async def test_method_count_with_all_params(self, async_client: AsyncJustement) -> None:
        document = await async_client.document.count(
            classification_facet=["string"],
            query="query",
        )
        assert_matches_type(DocumentCountResponse, document, path=["response"])

    @parametrize
    async def test_raw_response_count(self, async_client: AsyncJustement) -> None:
        response = await async_client.document.with_raw_response.count()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentCountResponse, document, path=["response"])

    @parametrize
    async def test_streaming_response_count(self, async_client: AsyncJustement) -> None:
        async with async_client.document.with_streaming_response.count() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentCountResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_search(self, async_client: AsyncJustement) -> None:
        document = await async_client.document.search()
        assert_matches_type(AsyncJustementPagination[Snippet], document, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncJustement) -> None:
        document = await async_client.document.search(
            classification_facet=["string"],
            language="de",
            page=1,
            query="query",
        )
        assert_matches_type(AsyncJustementPagination[Snippet], document, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncJustement) -> None:
        response = await async_client.document.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(AsyncJustementPagination[Snippet], document, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncJustement) -> None:
        async with async_client.document.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(AsyncJustementPagination[Snippet], document, path=["response"])

        assert cast(Any, response.is_closed) is True
