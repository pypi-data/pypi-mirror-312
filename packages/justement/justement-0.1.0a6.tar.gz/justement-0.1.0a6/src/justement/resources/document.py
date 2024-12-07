# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ..types import (
    Language,
    document_by_id_params,
    document_count_params,
    document_by_ref_params,
    document_search_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncJustementPagination, AsyncJustementPagination
from .._base_client import AsyncPaginator, make_request_options
from ..types.snippet import Snippet
from ..types.document import Document
from ..types.language import Language
from ..types.document_count_response import DocumentCountResponse

__all__ = ["DocumentResource", "AsyncDocumentResource"]


class DocumentResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DocumentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/justement-api/justement-python#accessing-raw-response-data-eg-headers
        """
        return DocumentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocumentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/justement-api/justement-python#with_streaming_response
        """
        return DocumentResourceWithStreamingResponse(self)

    def by_id(
        self,
        *,
        doc_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Document:
        """
        Retrieve a document by its document identifier.

        The docId is returned by the `search` endpoint as part of the result snippets.
        The response includes the full document content and metadata.

        Args:
          doc_id: The `docId` of the document that should be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/document",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"doc_id": doc_id}, document_by_id_params.DocumentByIDParams),
            ),
            cast_to=Document,
        )

    def by_ref(
        self,
        *,
        doc_ref: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Document:
        """
        Retrieve a document using its standard legal reference.

        This endpoint accepts Swiss legal references in their standard citation format
        and returns the corresponding document if found.

        Args:
          doc_ref: The legal reference of the document.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/documentByRef",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"doc_ref": doc_ref}, document_by_ref_params.DocumentByRefParams),
            ),
            cast_to=Document,
        )

    def count(
        self,
        *,
        classification_facet: List[str] | NotGiven = NOT_GIVEN,
        query: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentCountResponse:
        """
        Count the number of documents matching the search criteria.

        Args:
          classification_facet: **Classification facet**: Filters results based on hierarchical categories. Each
              element in the list represents a level in the hierarchy:

              - `["Staatsrecht", "Grundrecht"]`: filters to Staatsrecht (Public Law) and
                Grundrecht (Fundamental Rights).
              - `["Privatrecht", "Zivilrecht", "Vertragsrecht"]`: filters to Privatrecht
                (Private Law), Zivilrecht (Civil Law), and Vertragsrecht (Contract Law).
              - `["Strafrecht", "Straftaten"]`: filters to Strafrecht (Criminal Law) and
                Straftaten (Offenses).

              See the full classification hierarchy:

              ```plaintext
              Staatsrecht
              ├── Abgaberecht & öffentliche Finanzen
              ├── Bau- & Planungsrecht
              ├── Bürger- & Ausländerrecht
              ├── Energie/Verkehr/Medien
              │   └── Verkehr
              ├── Grundrecht
              ├── Gesundheit & soziale Sicherheit
              ├── Öffentliches Dienstverhältnis
              ├── Ökologisches Gleichgewicht
              ├── Politische Rechte
              ├── Rechtshilfe & Auslieferung
              ├── Schuldbetreibungs- & Konkursrecht
              ├── Sozialversicherungsrecht
              │   ├── AHV
              │   ├── ALV
              │   ├── BV
              │   ├── EL
              │   ├── IV
              │   ├── KV
              │   └── UV
              ├── Unterrichtswesen & Berufsausbildung
              ├── Verfahren
              │   ├── Strafprozess
              │   ├── Zivilprozess
              │   └── Zuständigkeitsfragen
              └── Verfahrensrecht

              Privatrecht
              ├── Immaterialgüter-, Wettbewerbs- & Kartellrecht
              ├── Obligationen- & Handelsrecht
              │   ├── Gesellschaftsrecht
              │   ├── Haftpflichtrecht
              │   ├── Obligationsrecht (allgemein)
              │   └── Vertragsrecht
              └── Zivilrecht
                 ├── Erbrecht
                 ├── Familienrecht
                 ├── Personenrecht
                 └── Sachenrecht

              Strafrecht
              ├── Straf- & Massnahmenvollzug
              ├── Straftaten
              └── Strafrecht (allgemein)
              ```

          query: **Search query**: Retrieves the count of documents matching the criteria.

              - Terms are **implicitly ANDed** (e.g., `hund biss` only matches documents
                containing both terms).
              - Supports **exact phrases** (e.g., `"hund spazieren"`) and **proximity
                searches** (e.g., `"hund biss"~10`).
              - **Excludes terms** with `-term` (e.g., `beschattung -besonnung`).
              - **Prefix search** with `term*` for terms with at least 3 characters.
              - **Synonym expansion and translations** with lower relevance ranking.

              For advanced operators and tips, see
              [Justement Search Tips](https://justement.ch/en/search).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/count",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "classification_facet": classification_facet,
                        "query": query,
                    },
                    document_count_params.DocumentCountParams,
                ),
            ),
            cast_to=int,
        )

    def search(
        self,
        *,
        classification_facet: List[str] | NotGiven = NOT_GIVEN,
        language: Language | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        query: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncJustementPagination[Snippet]:
        """
        Search Justement and receive a result page with up to 10 snippets of matching
        documents, ranked by relevance.

        Args:
          classification_facet: **Classification facet**: Filters results based on hierarchical categories. Each
              element in the list represents a level in the hierarchy:

              - `["Staatsrecht", "Grundrecht"]`: filters to Staatsrecht (Public Law) and
                Grundrecht (Fundamental Rights).
              - `["Privatrecht", "Zivilrecht", "Vertragsrecht"]`: filters to Privatrecht
                (Private Law), Zivilrecht (Civil Law), and Vertragsrecht (Contract Law).
              - `["Strafrecht", "Straftaten"]`: filters to Strafrecht (Criminal Law) and
                Straftaten (Offenses).

              See the full classification hierarchy:

              ```plaintext
              Staatsrecht
              ├── Abgaberecht & öffentliche Finanzen
              ├── Bau- & Planungsrecht
              ├── Bürger- & Ausländerrecht
              ├── Energie/Verkehr/Medien
              │   └── Verkehr
              ├── Grundrecht
              ├── Gesundheit & soziale Sicherheit
              ├── Öffentliches Dienstverhältnis
              ├── Ökologisches Gleichgewicht
              ├── Politische Rechte
              ├── Rechtshilfe & Auslieferung
              ├── Schuldbetreibungs- & Konkursrecht
              ├── Sozialversicherungsrecht
              │   ├── AHV
              │   ├── ALV
              │   ├── BV
              │   ├── EL
              │   ├── IV
              │   ├── KV
              │   └── UV
              ├── Unterrichtswesen & Berufsausbildung
              ├── Verfahren
              │   ├── Strafprozess
              │   ├── Zivilprozess
              │   └── Zuständigkeitsfragen
              └── Verfahrensrecht

              Privatrecht
              ├── Immaterialgüter-, Wettbewerbs- & Kartellrecht
              ├── Obligationen- & Handelsrecht
              │   ├── Gesellschaftsrecht
              │   ├── Haftpflichtrecht
              │   ├── Obligationsrecht (allgemein)
              │   └── Vertragsrecht
              └── Zivilrecht
                 ├── Erbrecht
                 ├── Familienrecht
                 ├── Personenrecht
                 └── Sachenrecht

              Strafrecht
              ├── Straf- & Massnahmenvollzug
              ├── Straftaten
              └── Strafrecht (allgemein)
              ```

          language: Preferred language for snippets.

          page: Result page (1-based). Maximum page is total results / 10 rounded up.

          query: **Search query**: Retrieves the count of documents matching the criteria.

              - Terms are **implicitly ANDed** (e.g., `hund biss` only matches documents
                containing both terms).
              - Supports **exact phrases** (e.g., `"hund spazieren"`) and **proximity
                searches** (e.g., `"hund biss"~10`).
              - **Excludes terms** with `-term` (e.g., `beschattung -besonnung`).
              - **Prefix search** with `term*` for terms with at least 3 characters.
              - **Synonym expansion and translations** with lower relevance ranking.

              For advanced operators and tips, see
              [Justement Search Tips](https://justement.ch/en/search).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/search",
            page=SyncJustementPagination[Snippet],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "classification_facet": classification_facet,
                        "language": language,
                        "page": page,
                        "query": query,
                    },
                    document_search_params.DocumentSearchParams,
                ),
            ),
            model=Snippet,
        )


class AsyncDocumentResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDocumentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/justement-api/justement-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDocumentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocumentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/justement-api/justement-python#with_streaming_response
        """
        return AsyncDocumentResourceWithStreamingResponse(self)

    async def by_id(
        self,
        *,
        doc_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Document:
        """
        Retrieve a document by its document identifier.

        The docId is returned by the `search` endpoint as part of the result snippets.
        The response includes the full document content and metadata.

        Args:
          doc_id: The `docId` of the document that should be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/document",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"doc_id": doc_id}, document_by_id_params.DocumentByIDParams),
            ),
            cast_to=Document,
        )

    async def by_ref(
        self,
        *,
        doc_ref: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Document:
        """
        Retrieve a document using its standard legal reference.

        This endpoint accepts Swiss legal references in their standard citation format
        and returns the corresponding document if found.

        Args:
          doc_ref: The legal reference of the document.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/documentByRef",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"doc_ref": doc_ref}, document_by_ref_params.DocumentByRefParams),
            ),
            cast_to=Document,
        )

    async def count(
        self,
        *,
        classification_facet: List[str] | NotGiven = NOT_GIVEN,
        query: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentCountResponse:
        """
        Count the number of documents matching the search criteria.

        Args:
          classification_facet: **Classification facet**: Filters results based on hierarchical categories. Each
              element in the list represents a level in the hierarchy:

              - `["Staatsrecht", "Grundrecht"]`: filters to Staatsrecht (Public Law) and
                Grundrecht (Fundamental Rights).
              - `["Privatrecht", "Zivilrecht", "Vertragsrecht"]`: filters to Privatrecht
                (Private Law), Zivilrecht (Civil Law), and Vertragsrecht (Contract Law).
              - `["Strafrecht", "Straftaten"]`: filters to Strafrecht (Criminal Law) and
                Straftaten (Offenses).

              See the full classification hierarchy:

              ```plaintext
              Staatsrecht
              ├── Abgaberecht & öffentliche Finanzen
              ├── Bau- & Planungsrecht
              ├── Bürger- & Ausländerrecht
              ├── Energie/Verkehr/Medien
              │   └── Verkehr
              ├── Grundrecht
              ├── Gesundheit & soziale Sicherheit
              ├── Öffentliches Dienstverhältnis
              ├── Ökologisches Gleichgewicht
              ├── Politische Rechte
              ├── Rechtshilfe & Auslieferung
              ├── Schuldbetreibungs- & Konkursrecht
              ├── Sozialversicherungsrecht
              │   ├── AHV
              │   ├── ALV
              │   ├── BV
              │   ├── EL
              │   ├── IV
              │   ├── KV
              │   └── UV
              ├── Unterrichtswesen & Berufsausbildung
              ├── Verfahren
              │   ├── Strafprozess
              │   ├── Zivilprozess
              │   └── Zuständigkeitsfragen
              └── Verfahrensrecht

              Privatrecht
              ├── Immaterialgüter-, Wettbewerbs- & Kartellrecht
              ├── Obligationen- & Handelsrecht
              │   ├── Gesellschaftsrecht
              │   ├── Haftpflichtrecht
              │   ├── Obligationsrecht (allgemein)
              │   └── Vertragsrecht
              └── Zivilrecht
                 ├── Erbrecht
                 ├── Familienrecht
                 ├── Personenrecht
                 └── Sachenrecht

              Strafrecht
              ├── Straf- & Massnahmenvollzug
              ├── Straftaten
              └── Strafrecht (allgemein)
              ```

          query: **Search query**: Retrieves the count of documents matching the criteria.

              - Terms are **implicitly ANDed** (e.g., `hund biss` only matches documents
                containing both terms).
              - Supports **exact phrases** (e.g., `"hund spazieren"`) and **proximity
                searches** (e.g., `"hund biss"~10`).
              - **Excludes terms** with `-term` (e.g., `beschattung -besonnung`).
              - **Prefix search** with `term*` for terms with at least 3 characters.
              - **Synonym expansion and translations** with lower relevance ranking.

              For advanced operators and tips, see
              [Justement Search Tips](https://justement.ch/en/search).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/count",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "classification_facet": classification_facet,
                        "query": query,
                    },
                    document_count_params.DocumentCountParams,
                ),
            ),
            cast_to=int,
        )

    def search(
        self,
        *,
        classification_facet: List[str] | NotGiven = NOT_GIVEN,
        language: Language | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        query: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Snippet, AsyncJustementPagination[Snippet]]:
        """
        Search Justement and receive a result page with up to 10 snippets of matching
        documents, ranked by relevance.

        Args:
          classification_facet: **Classification facet**: Filters results based on hierarchical categories. Each
              element in the list represents a level in the hierarchy:

              - `["Staatsrecht", "Grundrecht"]`: filters to Staatsrecht (Public Law) and
                Grundrecht (Fundamental Rights).
              - `["Privatrecht", "Zivilrecht", "Vertragsrecht"]`: filters to Privatrecht
                (Private Law), Zivilrecht (Civil Law), and Vertragsrecht (Contract Law).
              - `["Strafrecht", "Straftaten"]`: filters to Strafrecht (Criminal Law) and
                Straftaten (Offenses).

              See the full classification hierarchy:

              ```plaintext
              Staatsrecht
              ├── Abgaberecht & öffentliche Finanzen
              ├── Bau- & Planungsrecht
              ├── Bürger- & Ausländerrecht
              ├── Energie/Verkehr/Medien
              │   └── Verkehr
              ├── Grundrecht
              ├── Gesundheit & soziale Sicherheit
              ├── Öffentliches Dienstverhältnis
              ├── Ökologisches Gleichgewicht
              ├── Politische Rechte
              ├── Rechtshilfe & Auslieferung
              ├── Schuldbetreibungs- & Konkursrecht
              ├── Sozialversicherungsrecht
              │   ├── AHV
              │   ├── ALV
              │   ├── BV
              │   ├── EL
              │   ├── IV
              │   ├── KV
              │   └── UV
              ├── Unterrichtswesen & Berufsausbildung
              ├── Verfahren
              │   ├── Strafprozess
              │   ├── Zivilprozess
              │   └── Zuständigkeitsfragen
              └── Verfahrensrecht

              Privatrecht
              ├── Immaterialgüter-, Wettbewerbs- & Kartellrecht
              ├── Obligationen- & Handelsrecht
              │   ├── Gesellschaftsrecht
              │   ├── Haftpflichtrecht
              │   ├── Obligationsrecht (allgemein)
              │   └── Vertragsrecht
              └── Zivilrecht
                 ├── Erbrecht
                 ├── Familienrecht
                 ├── Personenrecht
                 └── Sachenrecht

              Strafrecht
              ├── Straf- & Massnahmenvollzug
              ├── Straftaten
              └── Strafrecht (allgemein)
              ```

          language: Preferred language for snippets.

          page: Result page (1-based). Maximum page is total results / 10 rounded up.

          query: **Search query**: Retrieves the count of documents matching the criteria.

              - Terms are **implicitly ANDed** (e.g., `hund biss` only matches documents
                containing both terms).
              - Supports **exact phrases** (e.g., `"hund spazieren"`) and **proximity
                searches** (e.g., `"hund biss"~10`).
              - **Excludes terms** with `-term` (e.g., `beschattung -besonnung`).
              - **Prefix search** with `term*` for terms with at least 3 characters.
              - **Synonym expansion and translations** with lower relevance ranking.

              For advanced operators and tips, see
              [Justement Search Tips](https://justement.ch/en/search).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/search",
            page=AsyncJustementPagination[Snippet],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "classification_facet": classification_facet,
                        "language": language,
                        "page": page,
                        "query": query,
                    },
                    document_search_params.DocumentSearchParams,
                ),
            ),
            model=Snippet,
        )


class DocumentResourceWithRawResponse:
    def __init__(self, document: DocumentResource) -> None:
        self._document = document

        self.by_id = to_raw_response_wrapper(
            document.by_id,
        )
        self.by_ref = to_raw_response_wrapper(
            document.by_ref,
        )
        self.count = to_raw_response_wrapper(
            document.count,
        )
        self.search = to_raw_response_wrapper(
            document.search,
        )


class AsyncDocumentResourceWithRawResponse:
    def __init__(self, document: AsyncDocumentResource) -> None:
        self._document = document

        self.by_id = async_to_raw_response_wrapper(
            document.by_id,
        )
        self.by_ref = async_to_raw_response_wrapper(
            document.by_ref,
        )
        self.count = async_to_raw_response_wrapper(
            document.count,
        )
        self.search = async_to_raw_response_wrapper(
            document.search,
        )


class DocumentResourceWithStreamingResponse:
    def __init__(self, document: DocumentResource) -> None:
        self._document = document

        self.by_id = to_streamed_response_wrapper(
            document.by_id,
        )
        self.by_ref = to_streamed_response_wrapper(
            document.by_ref,
        )
        self.count = to_streamed_response_wrapper(
            document.count,
        )
        self.search = to_streamed_response_wrapper(
            document.search,
        )


class AsyncDocumentResourceWithStreamingResponse:
    def __init__(self, document: AsyncDocumentResource) -> None:
        self._document = document

        self.by_id = async_to_streamed_response_wrapper(
            document.by_id,
        )
        self.by_ref = async_to_streamed_response_wrapper(
            document.by_ref,
        )
        self.count = async_to_streamed_response_wrapper(
            document.count,
        )
        self.search = async_to_streamed_response_wrapper(
            document.search,
        )
