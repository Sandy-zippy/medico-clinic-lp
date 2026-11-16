"""Google Ads keyword pages: one page per keyword theme at /g/<slug>/ (Sandy, 16 Nov 2026: "keep Facebook landing
pages different, keep Google's landing pages different per keyword"). Facebook stays on / with its ?a= angles.

Each page is index.html with the searched words written into the HTML itself (title, description, eyebrow, h1, lead),
so Google's landing-page check reads them without running JS. Claims only from the live page: no-cost site
assessment, 100+ clinics built, one team, licensed and insured, CSA Z8000 (surgical only). Run from the repo root:
    python3 tools/gpages.py        # writes g/<slug>/index.html and g/pages.json (keyword -> URL map)
"""
import html, json, os, re

S = "Medico Construction &amp; Design"
# slug, variant (photo + clinic type), title head, eyebrow, h1, lead, keywords (ad group keywords routed here)
PAGES = [
 ("medical-construction", "medical", "Medical Construction in BC", "Medical construction | British Columbia",
  "Medical construction by a team that builds only healthcare spaces.",
  "Medico is a medical construction company in BC. Site planning, permit drawings, construction and handover for clinics run under one team.",
  ["medical construction", "healthcare construction", "healthcare construction company", "medical facility contractor"]),
 ("build-a-medical-clinic", "medical", "Build a Medical Clinic in BC", "Build a medical clinic | British Columbia",
  "Build a medical clinic with a team that specializes in healthcare.",
  "Planning to build a medical clinic? Medico takes you from the space and the layout to permits, construction and opening day.",
  ["build a medical clinic"]),
 ("medical-clinic-construction", "medical", "Medical Clinic Construction in BC", "Medical clinic construction | British Columbia",
  "Medical clinic construction by builders who only do healthcare.",
  "Medico are medical clinic builders and contractors in BC. 100+ clinics built, from exam rooms to reception.",
  ["medical clinic construction", "medical clinic contractor", "medical office contractors", "medical clinic builders",
   "clinic construction company", "clinic construction", "clinic builders", "clinic builder"]),
 ("medical-office-construction", "medical", "Medical Office Construction in BC", "Medical office construction | British Columbia",
  "Medical office construction and build out, by one healthcare team.",
  "Medico handles medical office construction, build out and clinic fit out in BC, from permit drawings to handover.",
  ["medical office construction", "medical office build out", "clinic build out", "clinic fit out"]),
 ("clinic-design-build", "medical", "Clinic Design Build in BC", "Clinic design build | British Columbia",
  "Clinic design build: one team designs it and builds it.",
  "Medico is a medical design build firm. Your clinic layout, permit drawings and construction are planned by the same team.",
  ["clinic design build", "medical design build", "medical office design build", "design build medical office",
   "medical clinic building design"]),
 ("medical-clinic-renovation", "medical", "Medical Clinic Renovation in BC", "Medical clinic renovation | British Columbia",
  "Medical clinic renovation by a healthcare renovation contractor.",
  "Medico renovates medical clinics and medical offices in BC, planned around your patients so the work fits your clinic.",
  ["medical clinic renovation", "medical office renovation", "clinic renovation", "clinic renovation contractor"]),
 ("surgical-clinic-construction", "surgical", "Surgical Clinic Construction in BC", "Surgical clinic construction | British Columbia",
  "Surgical clinic construction with a contractor that designs to CSA Z8000.",
  "Medico builds surgical clinics, surgical suites and minor procedure rooms in BC, planned with applicable CSA Z8000 considerations.",
  ["surgical suite construction", "private surgical clinic construction", "minor procedure room construction",
   "surgical facility construction", "surgical clinic construction", "surgical centre construction", "surgery center construction"]),
 ("fertility-clinic-construction", "surgical", "Fertility Clinic Construction in BC", "Fertility clinic construction | British Columbia",
  "Fertility clinic construction, embryology lab included.",
  "Medico builds fertility clinics and embryology labs in BC, with procedure and lab spaces planned before construction starts.",
  ["fertility clinic construction", "embryology lab construction"]),
 ("healthcare-facility-construction", "surgical", "Healthcare Facility Construction in BC", "Healthcare facility construction | British Columbia",
  "Healthcare facility construction by a contractor that designs to CSA Z8000.",
  "Medico is a healthcare contractor in BC for medical facility construction, planned with applicable CSA Z8000 considerations.",
  ["healthcare facility construction", "medical facility construction", "healthcare contractor", "healthcare general contractor",
   "z8000 construction", "csa z8000 contractor"]),
 ("long-term-care-construction", "surgical", "Long Term Care Construction in BC", "Long term care construction | British Columbia",
  "Long term care and ambulatory care construction.",
  "Medico builds long term care and ambulatory care spaces in BC, planned with applicable CSA Z8000 considerations.",
  ["long term care construction", "ambulatory care construction"]),
 ("specialty-clinic-construction", "surgical", "Imaging, Dialysis + Specialty Clinic Construction in BC", "Specialty clinic construction | British Columbia",
  "Imaging, dialysis, endoscopy and cancer clinic construction.",
  "Medico builds diagnostic imaging, dialysis, endoscopy and cancer clinics in BC, planned with applicable CSA Z8000 considerations.",
  ["imaging clinic construction", "diagnostic imaging construction", "dialysis clinic construction",
   "endoscopy clinic construction", "cancer clinic construction"]),
 ("compounding-pharmacy-construction", "compounding", "Compounding Pharmacy Construction in BC", "Compounding pharmacy construction | British Columbia",
  "Compounding pharmacy construction, cleanroom included.",
  "Medico builds compounding pharmacies, sterile compounding rooms and pharmacy cleanrooms in BC, planned around NAPRA compounding room needs.",
  ["compounding pharmacy construction", "compounding pharmacy renovation", "compounding pharmacy design build",
   "compounding room construction", "compounding lab construction", "sterile compounding room", "pharmacy cleanroom",
   "pharmacy clean room", "napra compounding room"]),
 ("pharmacy-construction", "pharmacy", "Pharmacy Construction in BC", "Pharmacy construction | British Columbia",
  "Pharmacy construction and renovation by a healthcare builder.",
  "Medico handles pharmacy construction, pharmacy renovation and build out in BC, with dispensary and storage planned first.",
  ["pharmacy construction", "pharmacy renovation", "pharmacy build out"]),
 ("physiotherapy-clinic-construction", "physio", "Physiotherapy Clinic Construction in BC", "Physiotherapy clinic construction | British Columbia",
  "Physiotherapy clinic construction and renovation.",
  "Medico builds and renovates physio and chiropractic clinics in BC, with treatment rooms and gym space planned around your patients.",
  ["physiotherapy clinic construction", "physiotherapy clinic renovation", "physio clinic construction",
   "physio clinic renovation", "chiropractic clinic construction"]),
 ("vet-clinic-construction", "vet", "Vet Clinic Construction in BC", "Vet clinic construction | British Columbia",
  "Vet clinic and animal hospital construction.",
  "Medico builds and renovates veterinary clinics and animal hospitals in BC, with exam rooms, kennels and surgery planned first.",
  ["vet clinic construction", "veterinary clinic construction", "veterinary hospital construction", "animal hospital construction",
   "vet clinic renovation", "veterinary clinic renovation"]),
 ("dental-construction", "dental", "Dental Construction in BC", "Dental construction | British Columbia",
  "Dental construction by contractors who build only healthcare.",
  "Medico is a dental construction company in BC. Dental contractors and builders for operatories, sterilization and reception.",
  ["dental construction", "dental contractors", "dental construction companies", "dental general contractor",
   "dental clinic builders", "dental office builders", "dental office contractor"]),
 ("dental-clinic-construction", "dental", "Dental Clinic Construction in BC", "Dental clinic construction | British Columbia",
  "Dental clinic construction with a team that specializes in healthcare.",
  "Building a dental office? Medico handles dental clinic construction in BC, from the layout to permits and handover.",
  ["dental clinic construction", "dental office construction", "dental clinic building", "building a dental office",
   "dental practice construction"]),
 ("dental-office-build-out", "dental", "Dental Office Build Out in BC", "Dental office build out | British Columbia",
  "Dental office build out, turnkey from layout to handover.",
  "Medico handles dental office build outs and dental tenant improvements in BC, designed and built by one team.",
  ["dental office build out", "turnkey dental office", "dental tenant improvement", "dental office design build"]),
 ("dental-office-renovation", "dental", "Dental Office Renovation in BC", "Dental office renovation | British Columbia",
  "Dental office renovation planned around your patients.",
  "Medico handles dental office and dental clinic renovation in BC, staged so the work fits around your practice.",
  ["dental office renovation", "dental clinic renovation", "dental renovation"]),
 ("dental-office-design", "dental", "Dental Office Design in BC", "Dental office design | British Columbia",
  "Dental office design and dental clinic interior design.",
  "Medico designs dental offices and dental clinic interiors in BC: operatory layout, sterilization flow and reception, then builds them.",
  ["dental office design", "dental clinic design", "dental clinic interior design", "dental office interior design",
   "dental office layout", "dental operatory design", "dental clinic architect"]),
 ("medical-office-design", "medical", "Medical Office Design in BC", "Medical office design | British Columbia",
  "Medical office design and clinic interior design.",
  "Medico handles clinic design in BC: medical office layout and medical office interior design, then construction by the same team.",
  ["clinic design", "medical office design", "medical office interior design", "medical clinic design",
   "medical clinic interior design", "medical clinic design layout"]),
 ("specialty-clinic-design", "surgical", "Procedure Room + Specialty Clinic Design in BC", "Procedure room design | British Columbia",
  "Procedure room design for specialty and fertility clinics.",
  "Medico designs procedure rooms, fertility clinics, IVF labs, hair transplant and men's health clinics in BC, then builds them.",
  ["procedure room design", "fertility clinic design", "ivf lab design", "hair transplant clinic design", "men's health clinic design"]),
 ("physiotherapy-clinic-design", "physio", "Physiotherapy Clinic Design in BC", "Physiotherapy clinic design | British Columbia",
  "Physiotherapy clinic design, then the build.",
  "Medico handles physio clinic design in BC: treatment rooms, gym space and reception laid out, then built by the same team.",
  ["physiotherapy clinic design", "physio clinic design"]),
 ("pharmacy-design", "pharmacy", "Pharmacy Design in BC", "Pharmacy design | British Columbia",
  "Pharmacy design, built by the same team.",
  "Medico handles pharmacy design in BC: dispensary, storage and counter flow laid out before construction starts.",
  ["pharmacy design"]),
 ("vet-clinic-design", "vet", "Vet Clinic Design in BC", "Vet clinic design | British Columbia",
  "Vet clinic and veterinary hospital design.",
  "Medico handles veterinary clinic design in BC: exam rooms, kennels and surgery laid out, then built by the same team.",
  ["vet clinic design", "veterinary clinic design", "veterinary hospital design"]),
 ("medico-construction", "medical", "Healthcare Builders in BC", "Medico Construction &amp; Design | British Columbia",
  "Medico Construction &amp; Design: healthcare builders in BC.",
  "Medico Construction &amp; Design builds medical, dental, pharmacy and veterinary clinics across BC. 100+ clinics built.",
  ["medico construction", "medico construction and design", "medico construction & design", "medico construction & design ltd",
   "medicoconstruction.com", "medical construction and design", "medico construction vancouver", "medico construction ltd",
   "medico construction bc"]),
]


def build():
    src = open("index.html").read()
    # Root-relative asset and page links so /g/<slug>/ resolves them.
    src = re.sub(r'((?:src|href|srcset)="|, |url\(["\']?)(assets/|styles\.css|app\.js|motion\.js|privacy\.html)', r"\1/\2", src)
    seen = {}
    for slug, v, title, eyebrow, h1, lead, kws in PAGES:
        for k in kws:
            assert k not in seen, (k, seen.get(k), slug)
            seen[k] = slug
        h1t = html.unescape(h1).lower()
        assert any(k in h1t for k in kws) or slug == "medico-construction", (slug, "h1 must carry a keyword")
        p = src
        p = re.sub(r"<title>.*?</title>", f"<title>{title} | {S}</title>", p, count=1)
        p = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{lead}">', p, count=1)
        p = p.replace("<html ", f'<html data-gv="{v}" data-gslug="{slug}" ', 1)
        p = re.sub(r'(data-v="eyebrow">)[^<]*(</p>)', rf"\g<1>{eyebrow}\2", p, count=1)
        p = re.sub(r'(data-v="h1">)[^<]*(</h1>)', rf"\g<1>{h1}\2", p, count=1)
        p = re.sub(r'(<p class="lead" data-in="3">)[^<]*(</p>)', rf"\g<1>{lead}\2", p, count=1)
        assert p.count(h1) == 1 and p.count(lead) == 2 and 'data-gv="' in p, slug
        os.makedirs(f"g/{slug}", exist_ok=True)
        open(f"g/{slug}/index.html", "w").write(p)
    json.dump({k: f"https://build.medicoconstruction.com/g/{s}/" for k, s in seen.items()}, open("g/pages.json", "w"), indent=1)
    print(len(PAGES), "pages,", len(seen), "keywords mapped")


if __name__ == "__main__":
    build()
