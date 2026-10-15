import json, re, html, sys
B = "https://oneillstyres.com.au"
stores = [
 ("belmont","Belmont","3 Herbert St","Belmont","2280","+61249454945","ChIJUT1R790ic2sRBtAcSOyp2Do",("07:30","17:00"),("08:00","11:30")),
 ("beresfield","Beresfield TME","2 Babilla Cl","Beresfield","2322","+61249660444","ChIJJ6tn6-VAc2sRX0xVCGpsU4Y",("07:00","17:00"),("07:30","11:30")),
 ("broadmeadow","Broadmeadow","4 Newton St","Broadmeadow","2292","+61240480108","ChIJe1NrzL8Vc2sR_i-Q3Sa9Tv0",("07:30","17:00"),("08:00","12:00")),
 ("cessnock","Cessnock","256 Maitland Rd","Cessnock","2325","+61249901455","ChIJla38nO40c2sRYiH7itsBNRA",("07:30","17:00"),("08:00","11:30")),
 ("gateshead","Gateshead","1 Navin Cl","Gateshead","2290","+61249433711","ChIJl87sCXs9c2sRWMRP-lAldcg",("07:30","17:00"),("08:00","11:30")),
 ("kurri-kurri","Kurri Kurri","249 Lang St","Kurri Kurri","2327","+61249375288","ChIJGR8f_cU3c2sRZpaMIv3yCNo",("07:30","17:00"),("08:00","11:30")),
 ("morisset","Morisset","36 Gateway Blvd","Morisset","2264","+61249704321","ChIJ56Bc_zMoc2sREeYl_lwClG0",("07:30","17:00"),("08:00","11:30")),
 ("warners-bay","Warners Bay","183 Macquarie Rd","Warners Bay","2282","+61249567577","ChIJAUGelLI9c2sR0d9kZBawfKE",("07:30","17:00"),("08:00","11:30")),
]
ALT = {"broadmeadow": "Broadmeadow Tyres Newcastle", "morisset": "Morisset Batteries"}  # former trading names
org_id = B + "/#organization"
graph = [{
  "@type": "AutomotiveBusiness", "@id": org_id,
  "name": "O'Neills Tyre & Autocare", "url": B + "/",
  "logo": B + "/media/logo/default/oneills_logo_1.jpg",
  "email": "info@oneillstyres.com.au", "foundingDate": "1961",
  "slogan": "If you've got wheels, you need O'Neills",
  "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in ["Newcastle", "Lake Macquarie", "Hunter Region"]],
  "sameAs": ["https://www.facebook.com/ONeillsTyreAutocare/", "https://x.com/oneillstyres", "https://www.linkedin.com/company/o-neills-tyre-autocare/"],
  "subOrganization": [{"@id": f"{B}/location-{s[0]}#store"} for s in stores],
}, {
  "@type": "WebSite", "@id": B + "/#website", "url": B + "/", "name": "O'Neills Tyre & Autocare",
  "inLanguage": "en-AU", "publisher": {"@id": org_id},
  "potentialAction": {"@type": "SearchAction", "target": {"@type": "EntryPoint", "urlTemplate": B + "/catalogsearch/result/?q={search_term_string}"}, "query-input": "required name=search_term_string"},
}]
for slug, name, street, loc, pc, tel, pid, wk, sat in stores:
  graph.append({
    "@type": ["TireShop", "AutoRepair"], "@id": f"{B}/location-{slug}#store",
    "name": f"O'Neills Tyre & Autocare {name}", "url": f"{B}/location-{slug}",
    "telephone": tel, "image": B + "/media/wysiwyg/meetanshi/images/New.webp",
    **({"alternateName": ALT[slug]} if slug in ALT else {}),
    "parentOrganization": {"@id": org_id},
    "address": {"@type": "PostalAddress", "streetAddress": street, "addressLocality": loc, "addressRegion": "NSW", "postalCode": pc, "addressCountry": "AU"},
    "hasMap": f"https://www.google.com/maps/place/?q=place_id:{pid}",
    "openingHoursSpecification": [
      {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": wk[0], "closes": wk[1]},
      {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": sat[0], "closes": sat[1]},
    ],
    "paymentAccepted": "Cash, Credit Card, EFTPOS, Afterpay, Zip, Humm", "currenciesAccepted": "AUD", "priceRange": "$$",
  })

# FAQ is read from the homepage markup so the schema always matches the visible text
src = open(sys.argv[1]).read()
def clean(s):
  return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()
faq = [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}}
       for q, a in re.findall(r'<summary[^>]*>(.*?)<svg.*?</summary>\s*<p[^>]*>(.*?)</p>', src, re.S)]
graph.append({"@type": "FAQPage", "@id": B + "/#faq", "mainEntity": faq})

out = ('<!-- Homepage structured data. Output in <head> (or before </body>) on the homepage only.\n'
       '     No aggregateRating: Google does not allow self-serving or third-party aggregated review markup. -->\n'
       '<script type="application/ld+json">\n'
       + json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
       + '\n</script>\n')
open(sys.argv[2], "w").write(out)
print(len(graph), "nodes,", len(faq), "faqs:", [f["name"][:40] for f in faq])
