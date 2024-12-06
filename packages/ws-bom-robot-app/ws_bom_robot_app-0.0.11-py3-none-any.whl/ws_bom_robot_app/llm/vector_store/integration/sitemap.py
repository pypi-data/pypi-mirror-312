import aiofiles
import aiofiles.os
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain_community.document_transformers import MarkdownifyTransformer as markdownify
from langchain_core.documents import Document
from bs4 import BeautifulSoup, Tag


class Sitemap(IntegrationStrategy):
    """_summary_
      Load a sitemap.xml file and extract text from the urls.
    Args:
        data (dict[str, str]):
        data["sitemapUrl"] (str): absolute/relative url of the sitemap.xml
        data["outputFormat"] (str): ["text", "html", "markdown"] default to "text"
        data["filterUrls"] list: list of regex pattern to filter urls ["https://www.example.com/en/products", "^.*products.*$"]
        data["includeOnlySelector"] : [".content", "#main-article", "article p"]
        data["excludeTag"] (str): default to ["script", "noscript", "style", "head", "header","nav","footer", "iframe"]
        data["excludeClass"] (str): ["class1", "class2"]
        data["excludeId"] (str): ["id1", "id2"]
    """
    def __init__(self, knowledgebase_path: str, data: dict[str, str]):
        super().__init__(knowledgebase_path, data)
        self.__sitemap_url = self.data.get("sitemapUrl")
        self.__filter_urls: list[str] = self.data.get("filterUrls",[]) # type: ignore
        self.__output_format: str = self.data.get("outputFormat", "text") # type: ignore
        self.__include_only_selectors: list[str] = self.data.get("includeOnlySelector", []) # type: ignore
        self.__exclude_tag: list[str] = self.data.get("excludeTag",[]) # type: ignore
        self.__exclude_class: list[str] = self.data.get("excludeClass",[]) # type: ignore
        self.__exclude_id: list[str] = self.data.get("excludeId",[]) # type: ignore
    def working_subdirectory(self) -> str: # type: ignore
        return ""
    def _extract(self, tag: Tag) -> str:
        return tag.get_text() if self.__output_format == "text" else tag.prettify()
    def _output(self, documents: list[Document]) -> list[Document]:
        return list(markdownify().transform_documents(documents)) if (self.__output_format == "markdown") else documents
    def _parse(self,content: BeautifulSoup) -> str:
        if self.__include_only_selectors:
            extracted = []
            for selector in self.__include_only_selectors:
                matching_elements = content.select(selector)
                for element in matching_elements:
                    extracted.append(self._extract(element))
            return '\n\n'.join(extracted)
        else:
            selectors: list[str] = ["script", "noscript", "style", "head", "header","nav","footer", "iframe"]
            selectors.extend(
                self.__exclude_tag
                + [f".{class_name}" for class_name in self.__exclude_class]
                + [f"#{id_name}" for id_name in self.__exclude_id]
                )
            for element in selectors:
                for _ in content.select(element):
                    _.decompose()
            return str(self._extract(content))
    async def load(self) -> list[Document]:
        def _is_local(url: str) -> bool:
            return not url.startswith("http")
        def _remap_if_local(url: str) -> str:
            return f"{self.knowledgebase_path}/{url}" if _is_local(url) else url

        if (self.__sitemap_url):
            _loader = SitemapLoader(
                web_path=_remap_if_local(self.__sitemap_url),
                filter_urls=self.__filter_urls,
                parsing_function=self._parse,
                is_local=_is_local(self.__sitemap_url)
            )
            _docs = self._output([document async for document in _loader.alazy_load()])
            if _is_local(self.__sitemap_url):
              await aiofiles.os.remove(_loader.web_path)
            return _docs
        return []
