from langchain_chroma import Chroma
import config.config_data as config
class VectorStoryService(object):
    def __init__(self,embedding):

        self.embedding = embedding

        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.chroma_db_path
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})
