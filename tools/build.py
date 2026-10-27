import sys, pathlib, re
H = pathlib.Path(sys.argv[1])
r = lambda p: (H / p).read_text()

# ---------- 1. index.html: single-file preview (CDN Tailwind + Alpine), published on GitHub Pages ----------
head = """<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tyres &amp; Car Servicing Newcastle | O'Neills Tyre &amp; Autocare</title>
<meta name="description" content="Family owned since 1961. Buy tyres online or book a service at 8 O'Neills stores across Newcastle, Lake Macquarie and the Hunter.">
<link rel="canonical" href="https://oneillstyres.com.au/">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_AU">
<meta property="og:site_name" content="O'Neills Tyre &amp; Autocare">
<meta property="og:title" content="Tyres &amp; Car Servicing Newcastle | O'Neills Tyre &amp; Autocare">
<meta property="og:description" content="Family owned since 1961. Buy tyres online or book a service at 8 O'Neills stores across Newcastle, Lake Macquarie and the Hunter.">
<meta property="og:url" content="https://oneillstyres.com.au/">
<meta property="og:image" content="https://oneillstyres.com.au/media/wysiwyg/meetanshi/images/New.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<!-- PREVIEW ONLY: Tailwind Play CDN. In Hyvä the classes compile from the theme build. -->
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<script>
tailwind.config = {
  theme: { extend: {
    colors: {
      brand: {50:'#EEF4FC',100:'#D9E6F8',200:'#B3CDF0',300:'#82ACE4',400:'#4F86D3',500:'#2A6CC4',600:'#1A5FB4',700:'#154D93',800:'#123F77',900:'#0F335F'},
      navy: {700:'#1A2D42',800:'#0F1D2E',900:'#0A1628'}
    },
    fontFamily: { sans: ['Inter','ui-sans-serif','system-ui','sans-serif'], display: ['"Space Grotesk"','Inter','ui-sans-serif','sans-serif'] }
  } }
};
</script>
<style>[x-cloak]{display:none!important}</style>
""" + r("schema/home-jsonld.html") + """</head>
<body class="bg-white font-sans text-slate-700 antialiased">
"""
body = r("src/icons.html") + r("src/header.html") + r("src/home-content.html") + r("src/footer.html")
# PREVIEW ONLY: sample review cards (clearly labelled, not real reviews) inlined so they also show when index.html is
# opened straight from the folder (a fetch of a local file is blocked there). The Hyvä template keeps data-endpoint="".
body = body.replace('x-data="ohReviews" data-endpoint=""', 'x-data="ohReviews" data-endpoint="" data-json="oh-reviews-preview"', 1)
body += '<script type="application/json" id="oh-reviews-preview">' + r("data/preview-reviews.json").replace("</", "<\\/") + '</script>\n'
tail = "<script>\n" + r("js/oneills-home.js") + "</script>\n" + \
       '<!-- PREVIEW ONLY: Alpine is already loaded by Hyvä. -->\n<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.8/dist/cdn.min.js"></script>\n</body>\n</html>\n'
(H / "index.html").write_text(head + body + tail)

# ---------- 2. Hyvä template + layout ----------
MEDIA_BASE = '/media/wysiwyg/oneills-home/'  # upload homepage/assets/* here
content = r("src/home-content.html").replace('"assets/', '"' + MEDIA_BASE).replace(', assets/', ', ' + MEDIA_BASE)
content = re.sub(r'^<!--.*?-->\n', '', content, count=1, flags=re.S)  # drop the file header comment
# Hyvä's page layout already renders <main id="maincontent">, so the template must not output another.
content = re.sub(r'<main id="maincontent" class="([^"]*)">', r'<div class="\1">', content, count=1)
content = content.replace('</main>', '</div>')
content = content.replace('data-combinations=""',
    'data-combinations="<?= $escaper->escapeHtmlAttr((string) $block->getData(\'tyre_size_combinations\')) ?>"')

phtml = """<?php
/**
 * O'Neills Tyre & Autocare homepage.
 * Generated from homepage/src/home-content.html and homepage/js/oneills-home.js. Edit those, then regenerate.
 *
 * Requirements:
 *  - The icon sprite (homepage/src/icons.html) is output once sitewide, e.g. at the top of header.phtml.
 *  - Brand Tailwind tokens (homepage/tailwind) are in the theme config, and this folder is in Tailwind `content`.
 *  - `tyre_size_combinations`: pass the same JSON the live tyre size form uses in data-combinations
 *    (array of {width_val, width_label, profile_val, profile_label, rim_val, rim_label}).
 *
 * @var \\Magento\\Framework\\View\\Element\\Template $block
 * @var \\Magento\\Framework\\Escaper $escaper
 * @var \\Hyva\\Theme\\ViewModel\\HyvaCsp $hyvaCsp
 */
declare(strict_types=1);
?>
""" + content + "\n<script>\n" + r("js/oneills-home.js") + "</script>\n<?php $hyvaCsp->registerInlineScript() ?>\n\n" + r("schema/home-jsonld.html")

out = H / "hyva" / "Magento_Cms" / "templates" / "home"
out.mkdir(parents=True, exist_ok=True)
(out / "homepage.phtml").write_text(phtml)

layout = H / "hyva" / "Magento_Cms" / "layout"
layout.mkdir(parents=True, exist_ok=True)
(layout / "cms_index_index.xml").write_text("""<?xml version="1.0"?>
<!--
  Homepage layout for the Hyvä child theme: app/design/frontend/<Vendor>/<theme>/Magento_Cms/layout/cms_index_index.xml
  Leave the homepage CMS page content empty; title and meta description stay in the CMS page settings.
-->
<page xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="urn:magento:framework:View/Layout/etc/page_configuration.xsd">
    <body>
        <referenceContainer name="content">
            <block class="Magento\\Framework\\View\\Element\\Template"
                   name="oneills.homepage"
                   template="Magento_Cms::home/homepage.phtml"
                   before="-">
                <!-- Dev: replace with the block/view model that already outputs the tyre size combinations JSON -->
                <arguments>
                    <argument name="tyre_size_combinations" xsi:type="string"></argument>
                </arguments>
            </block>
        </referenceContainer>
    </body>
</page>
""")
print("built index.html", (H / "index.html").stat().st_size, "bytes; hyva/ template", (out / "homepage.phtml").stat().st_size, "bytes")
