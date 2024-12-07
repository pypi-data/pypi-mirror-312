# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DocumentCountParams"]


class DocumentCountParams(TypedDict, total=False):
    classification_facet: Annotated[List[str], PropertyInfo(alias="classificationFacet")]
    """
    **Classification facet**: Filters results based on hierarchical categories. Each
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
    """

    query: str
    """**Search query**: Retrieves the count of documents matching the criteria.

    - Terms are **implicitly ANDed** (e.g., `hund biss` only matches documents
      containing both terms).
    - Supports **exact phrases** (e.g., `"hund spazieren"`) and **proximity
      searches** (e.g., `"hund biss"~10`).
    - **Excludes terms** with `-term` (e.g., `beschattung -besonnung`).
    - **Prefix search** with `term*` for terms with at least 3 characters.
    - **Synonym expansion and translations** with lower relevance ranking.

    For advanced operators and tips, see
    [Justement Search Tips](https://justement.ch/en/search).
    """
