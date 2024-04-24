import re
from re import Match

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page


# -----------------------------------------------------------------------------
# Hooks
# -----------------------------------------------------------------------------

url_pattern = r'<li class="md-select__item">[\n\s]*<a href=".*?"'

def on_post_page(output: str, *, page: Page, config: MkDocsConfig):
    aval_langs = []
    for item in config.extra['alternate']:
        aval_langs.append(item['lang'])
    html = remove_langs(output, get_ignored_langs(page.markdown), aval_langs)
    def replace(match: Match):
        return match.group() + "/" + page.url
    return re.sub(url_pattern, replace, html, flags = re.M)

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

key = "ignore-langs"
lang_pattern = r'<li class="md-select__item">[\n\s]*<a href=".*?"\s*hreflang="(.*?)"'
lang_selector_pattern = r'<div class="md-header__option">[\s\S]*?aria-label="Select language"[\s\S\n]*?(\s*</div>){3}'

def get_ignored_langs(markdown: str):
    def trim(s):
        return re.sub(r'^\s+|\s+$', '', s)
    match = re.search(r'^\s*<!--([\s\S]*?)-->', markdown)
    if match is None: return
    page_options = match.group(1)
    option_value = None
    while page_options != '':
        page_options = trim(page_options)
        current_key = re.match(r'^#\s*([\w-]+)\s*:', page_options)
        if current_key is None: return
        if current_key.group(1) == key:
            option_value = re.match(r'^#[^:;]+:([^;]*)(;|$)', page_options).group(1)
            break
        else:
            page_options = re.sub(r'^#[^;]+(;|$)', '', page_options)
    if option_value is None: return
    return re.split(r'\s*,\s*', trim(option_value))

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
