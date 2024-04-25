import re
from re import Match

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page


# -----------------------------------------------------------------------------
# Hooks
# -----------------------------------------------------------------------------

url_pattern = r'<li class="md-select__item">[\n\s]*<a href="[^"]+'

def on_post_page(output: str, *, page: Page, config: MkDocsConfig):
    aval_langs = []
    for item in config.extra['alternate']:
        aval_langs.append(item['lang'])
    html = remove_langs(output, page.meta.get('ignore-langs'), aval_langs)
    def replace(match: Match):
        return match.group() + "/" + page.url
    return re.sub(url_pattern, replace, html, flags = re.M)

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

lang_selector_pattern = r'<div class="md-header__option">[\s\S]*?aria-label="Select language"[\s\S]*?(\s*</div>){3}'

def remove_langs(html: str, langs_to_remove: list, avaliable_langs = ["en"]):
    if langs_to_remove is None:
        return html
    aval_lang_num = len(avaliable_langs)
    for lang in avaliable_langs:
        if lang not in langs_to_remove: continue
        aval_lang_num -= 1
        if aval_lang_num <= 1:
            return re.sub(lang_selector_pattern, '', html, flags = re.M)
        select_item_pattern = r'<li class="md-select__item">[\n\s]*<a href=".*?"\s*hreflang="' + lang + r'"[\s\S]*?</li>'
        html = re.sub(select_item_pattern, '', html, flags = re.M)
    return html
