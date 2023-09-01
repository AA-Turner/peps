from __future__ import annotations

from pathlib import Path
from typing import Any

from docutils import nodes
from docutils.frontend import OptionParser

from sphinx.builders.html import logger, StandaloneHTMLBuilder
from sphinx.errors import ThemeError
from sphinx.util.osutil import relative_uri
from sphinx.writers.html import HTMLWriter

from sphinx.builders.dirhtml import DirectoryHTMLBuilder


class FileBuilder(StandaloneHTMLBuilder):
    copysource = False  # Prevent unneeded source copying - we link direct to GitHub
    search = False  # Disable search

    # Things we don't use but that need to exist:
    indexer = None
    relations = {}
    _script_files = _css_files = []
    globalcontext = {"script_files": [], "css_files": []}

    def prepare_writing(self, _doc_names: set[str]) -> None:
        self.docwriter = HTMLWriter(self)
        _opt_parser = OptionParser([self.docwriter], defaults=self.env.settings, read_config_files=True)
        self.docsettings = _opt_parser.get_default_values()
        self._orig_css_files = self._orig_js_files = []

    def get_doc_context(self, docname: str, body: str, _metatags: str) -> dict:
        """Collect items for the template context of a page."""
        try:
            title = self.env.longtitles[docname].astext()
        except KeyError:
            title = ""

        # local table of contents
        toc_tree = self.env.tocs[docname].deepcopy()
        if len(toc_tree) and len(toc_tree[0]) > 1:
            toc_tree = toc_tree[0][1]  # don't include document title
            del toc_tree[0]  # remove contents node
            for node in toc_tree.findall(nodes.reference):
                node["refuri"] = node["anchorname"] or '#'  # fix targets
            toc = self.render_partial(toc_tree)["fragment"]
        else:
            toc = ""  # PEPs with no sections -- 9, 210

        return {"title": title, "sourcename": f"{docname}.rst", "toc": toc, "body": body}

    def handle_page(self, pagename: str, addctx: dict,
                    templatename='', outfilename=None, event_arg=None) -> None:

        def pathto(
            otheruri: str,
            resource: bool = False,
            baseuri: str = self.get_target_uri(pagename).rsplit('#', 1)[0],
        ) -> str:
            if resource and '://' in otheruri:
                # allow non-local resources given by scheme
                return otheruri
            elif not resource:
                otheruri = self.get_target_uri(otheruri)
            uri = relative_uri(baseuri, otheruri) or '#'
            if uri == '#' and not self.allow_sharp_as_current_path:
                uri = baseuri
            return uri

        ctx = {
            **self.globalcontext.copy(),
            'pagename': pagename.removeprefix('peps/'),
            'pathto': pathto,
            **addctx,
        }

        try:
            output = self.templates.render("page.html", ctx)
        except Exception as exc:
            msg = f"An error happened in rendering the page {pagename}.\nReason: {exc!r}"
            raise ThemeError(msg) from exc

        outfilename = Path(self.get_outfilename(pagename.removeprefix('peps/')))
        outfilename.parent.mkdir(parents=True, exist_ok=True)
        try:
            outfilename.write_text(output, encoding='utf-8', errors='xmlcharrefreplace')
        except OSError as err:
            logger.warning("error writing file %s: %s", outfilename, err)


class DirectoryBuilder(FileBuilder):
    # sync all overwritten things from DirectoryHTMLBuilder
    name = DirectoryHTMLBuilder.name
    get_target_uri = DirectoryHTMLBuilder.get_target_uri
    get_outfilename = DirectoryHTMLBuilder.get_outfilename
