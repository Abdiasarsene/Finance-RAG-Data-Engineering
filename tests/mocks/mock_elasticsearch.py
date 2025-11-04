# ====== MOCK ELASTISEARCH ======
class MockElasticsearch:
    # Set up
    def __init__(self):
        self.index = {}

    # Index doc
    def index_doc(self, index_name, doc_id, document):
        if index_name not in self.index:
            self.index[index_name] = {}
        self.index[index_name][doc_id] = document

    # Search
    def search(self, index_name, query):
        if index_name not in self.index:
            return []
        results = []
        for doc_id, doc in self.index[index_name].items():
            if any(q.lower() in str(doc).lower() for q in query.split()):
                results.append({"_id": doc_id, "_source": doc})
        return results