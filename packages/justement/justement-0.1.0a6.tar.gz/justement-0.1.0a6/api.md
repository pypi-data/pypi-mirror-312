# Document

Types:

```python
from justement.types import Decision, Document, Language, Snippet, Snippets, DocumentCountResponse
```

Methods:

- <code title="get /api/document">client.document.<a href="./src/justement/resources/document.py">by_id</a>(\*\*<a href="src/justement/types/document_by_id_params.py">params</a>) -> <a href="./src/justement/types/document.py">Document</a></code>
- <code title="get /api/documentByRef">client.document.<a href="./src/justement/resources/document.py">by_ref</a>(\*\*<a href="src/justement/types/document_by_ref_params.py">params</a>) -> <a href="./src/justement/types/document.py">Document</a></code>
- <code title="get /api/count">client.document.<a href="./src/justement/resources/document.py">count</a>(\*\*<a href="src/justement/types/document_count_params.py">params</a>) -> <a href="./src/justement/types/document_count_response.py">DocumentCountResponse</a></code>
- <code title="get /api/search">client.document.<a href="./src/justement/resources/document.py">search</a>(\*\*<a href="src/justement/types/document_search_params.py">params</a>) -> <a href="./src/justement/types/snippet.py">SyncJustementPagination[Snippet]</a></code>
