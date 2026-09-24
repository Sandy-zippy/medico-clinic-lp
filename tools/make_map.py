# Builds assets/map.svg: real BC + Alberta outlines (click_that_hood canada.geojson) + the 4 Medico offices.
# Projection: equirectangular with cos(mid-lat) x-scaling. Good enough at province scale, no distortion games.
import json, math, pathlib
here = pathlib.Path(__file__).parent
d = json.load(open(here / "canada.geojson"))
PROV = {f["properties"]["name"]: f["geometry"] for f in d["features"]}
# source: medicoconstruction.com/contact-us/ (verified 24 Sep 2026). Coordinates are the city centres.
OFFICES = [("Surrey", 49.19, -122.85, "r"), ("Victoria", 48.43, -123.37, "l"),
           ("Calgary", 51.05, -114.07, "l"), ("Edmonton", 53.54, -113.30, "l")]
LON0, LON1, LAT0, LAT1 = -134.2, -109.7, 48.1, 60.1
W = 900; k = math.cos(math.radians(54))
H = round(W * (LAT1 - LAT0) / ((LON1 - LON0) * k))
def xy(lon, lat): return ((lon - LON0) / (LON1 - LON0) * W, (LAT1 - lat) / (LAT1 - LAT0) * H)
def rings(g):
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    for p in polys:
        yield p[0]
def path(g, minlen=6):
    out = []
    for r in rings(g):
        pts = [xy(*c[:2]) for c in r]
        # drop tiny islets and thin every ring so the file stays small
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        if max(xs) - min(xs) < minlen and max(ys) - min(ys) < minlen: continue
        keep = [pts[0]]
        for p in pts[1:]:
            if abs(p[0] - keep[-1][0]) + abs(p[1] - keep[-1][1]) > 1.2: keep.append(p)
        out.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in keep) + "Z")
    return "".join(out)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Map of British Columbia and Alberta with Medico offices in Surrey, Victoria, Calgary and Sherwood Park">']
svg.append(f'<path class="m-bc" d="{path(PROV["British Columbia"])}"/>')
svg.append(f'<path class="m-ab" d="{path(PROV["Alberta"])}"/>')
bx, by = xy(-124.5, 55.2); ax, ay = xy(-115.2, 56.2)
svg.append(f'<text class="m-prov" x="{bx:.0f}" y="{by:.0f}">BRITISH COLUMBIA</text><text class="m-prov" x="{ax:.0f}" y="{ay:.0f}" text-anchor="middle">ALBERTA</text>')
for name, lat, lon, side in OFFICES:
    x, y = xy(lon, lat)
    tx, anchor = (x - 22, "end") if side == "l" else (x + 22, "start")
    svg.append(f'<g class="m-pin"><circle class="m-halo" cx="{x:.1f}" cy="{y:.1f}" r="18"/><circle class="m-dot" cx="{x:.1f}" cy="{y:.1f}" r="8"/>'
               f'<text x="{tx:.1f}" y="{y+9:.1f}" text-anchor="{anchor}">{name}</text></g>')
svg.append("</svg>")
out = here.parent / "assets" / "map.svg"
out.write_text("".join(svg)); print(out, W, H, out.stat().st_size, "bytes")
