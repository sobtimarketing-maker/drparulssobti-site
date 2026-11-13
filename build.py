"""Builds the Dr Parul Sharma Sobti website into ./site.

    python3 build.py              # full website (standalone HTML files)
    python3 build.py --preview D  # also writes an Artifact preview build into D

Content lives in content/blog_plan.py (the blog sequence) and content/posts/NN.html
(written posts). Anything wrapped in <span class="ph">...</span> is a placeholder
the clinic still has to confirm.
"""
import csv
import datetime as dt
import html
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "content"))
from blog_plan import CHAPTERS, POSTS, START_DATE  # noqa: E402  (content/blog_plan.py)
from price_pages import PRICE_PAGES, RAJOURI_FAQ  # noqa: E402  (content/price_pages.py)
from videos import V as VIDEOS, obj as video_obj, card as video_card, CSS as VIDEO_CSS, JS as VIDEO_JS  # noqa: E402

SITE = ROOT / "site"

# Sister sites. Replace "#" with the live addresses.
SITE_URL = "https://drparulssobti.com"
CLINIC_URL = "https://www.sobtidentalcare.com"
PUSHKAR_URL = "https://dentalimplantsdelhi.com"

CLINIC = "Dr Sobti's Dental Care"
PHONE = "+91 87449 85976"  # front desk, call (matches the Google profile)
PHONES = [PHONE]  # lead-calling numbers are never published
PHONE_LINK = f'<a href="tel:{PHONE.replace(" ", "")}">{PHONE}</a>'  # tappable on phones
WHATSAPP_NO = "+91 80767 77307"
WHATSAPP = "https://wa.me/918076777307"

# Google Ads tag: counts taps on call and WhatsApp links as conversions (account 202-776-6680).
ADS_TAG = r"""<!-- Google Ads: counts taps on call and WhatsApp links as conversions -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18553206533"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'AW-18553206533');
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a[href]');
  if (!a) return;
  var h = a.getAttribute('href') || '';
  if (h.indexOf('tel:') === 0) {
    gtag('event', 'conversion', {send_to: 'AW-18553206533/5EgMCLfk97EdEIXu7Y5F'});
  } else if (/wa\.me|whatsapp\.com/i.test(h)) {
    gtag('event', 'conversion', {send_to: 'AW-18553206533/ioPLCKWI-LEdEIXu7Y5F'});
  }
}, true);
</script>"""
INSTAGRAM = "https://www.instagram.com/sobtidentalcare/"
YOUTUBE = "https://www.youtube.com/@DrSobtiDental"
FACEBOOK = "https://www.facebook.com/sobtidentalcare"
GOOGLE_PROFILE = "https://maps.google.com/maps?cid=6577991291147149801"
GOOGLE_REVIEW = "https://search.google.com/local/writereview?placeid=ChIJf7C_p8MDDTkR6WFwRDq4SVs"
EMAIL = "sobticlinic@gmail.com"
HOURS = "Open 7 days, 10:00 am to 7:00 pm"
ADDRESS = "J 12/26, First Floor, Rajouri Garden (above Rajmandir), New Delhi 110027"
ADDRESS_2 = "WZ 168, Mangal Bazaar Road, Vishnu Garden, New Delhi 110018"
MAP_1 = "https://maps.google.com/maps?cid=6577991291147149801"
MAP_2 = "https://maps.google.com/maps?cid=4235763968755079234"
# Dr Parul's portrait, hosted in this repo. It used to be loaded from the old sobtidentalcare.com,
# which broke when that site was rebuilt. Until the file is added, pages show a clinic photo instead.
PORTRAIT_FILE = "assets/images/dr-parul-sharma-sobti.jpg"
HAS_PORTRAIT = (Path(__file__).parent / PORTRAIT_FILE).exists()
PORTRAIT_URL = f"https://drparulssobti.com/{PORTRAIT_FILE}" if HAS_PORTRAIT else "https://drparulssobti.com/assets/images/share.jpg"
PREVIEW = False

FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;"
         "1,9..144,500&family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700&display=swap")

NAV = [
    ("index.html", "Home"),
    ("about.html", "Dr Parul"),
    ("clinic.html", "The Clinic"),
    ("treatments.html", "Treatments"),
    ("technology.html", "Technology"),
    ("blog.html", "Smile Journal"),
    ("visit.html", "Visit"),
]


CURRENT = ' aria-current="page"'


def portrait(alt="Dr Parul Sharma Sobti"):
    if PREVIEW:
        return f'<div class="photo">{ph("Portrait from sobtidentalcare.com shows on the live site")}</div>'
    if HAS_PORTRAIT:
        return f'<img class="portrait" src="{PORTRAIT_FILE}" alt="{alt}" width="800" height="1000" loading="lazy">'
    return ('<img class="portrait" src="assets/images/clinic/clinic-reception-waiting.jpg" '
            'alt="Reception at Dr Sobti\'s Dental Care, Rajouri Garden" loading="lazy">')


# Patient reviews, word for word from Google and Practo (shortened only where marked "…").
# (name, treatment, words, source)
REVIEWS = [
    ("Divjot K.", "Consultation with Dr Parul", "Dr. Parul is incredibly patient and explains the condition in depth. She answers all questions thoroughly and spends ample time with patients to ensure they feel satisfied and well-informed, never rushing into procedures.", "rg"),
    ("Afran N.", "Front teeth veneers", "Best dental treatment is offered by them in the area with all the latest equipment one can imagine. State of the art clinic.I got my front teeth veneers done and very happy with my smile.", "vg"),
    ("Kamna S.", "Teeth polishing", "Had my teeth polishing done by Dr. Parul Sharma and had such a lovely experience! She was incredibly sweet, helpful, and made the whole process so comfortable. Really happy with the results.", "rg"),
    ("Avneet", "Consultation", "The doctor was extremely professional, patient, and took the time to listen to all my concerns carefully. The consultation was very detailed, and the treatment suggested was clearly explained.", "practo"),
    ("Debesh P.", "Root canal and zirconia caps", "Had a painless experience while getting my RCT treatment and zirconia caps from Dr Parul Sobti.Really appreciate her way of handling her patients.", "vg"),
    ("Navneet S.", "Re-root canal", "I came here with severe infection and tooth ache and received a really good and painless re- root canal treatment in the hands of Dr Parul Sobti. The clinic is very clean and has a peaceful ambiance and they have all the facilities available in house.", "rg"),
    ("Ivneet K.", "Scaling", "I recently had a scaling treatment done by Dr. Parul Sharma Sobti, and it was a wonderful experience. She is an excellent doctor, very professional and gentle.", "practo"),
    ("Sayan D.", "Front teeth cosmetic work", "Had my front teeth cosmetic work done by Dr. Parul and it was a great experience, satisfied.", "vg"),
    ("Nipun M.", "Treatment plan", "Dr. Parul explained me about my teeth anatomy and guided me transparently about my procedure. It was a nice and calming experience altogether and I feel much better now", "rg"),
]
REVIEW_SOURCES = {"rg": "Google, Rajouri Garden", "vg": "Google, Vishnu Garden clinic", "practo": "Practo"}
PRACTO = "https://www.practo.com/delhi/clinic/sobti-dental-clinic-vishnu-garden/reviews"


def review_cards(items):
    return '<div class="reviews">' + "".join(
        f'<figure class="review"><div class="stars" aria-label="5 out of 5 stars">★★★★★</div>'
        f'<blockquote>“{esc(t)}”</blockquote><figcaption><b>{esc(n)}</b>'
        f'<span class="label">{esc(w)} · {REVIEW_SOURCES[src]}</span></figcaption></figure>'
        for n, w, t, src in items) + "</div>"


def reviews_section(items):
    return f"""<section><div class="wrap">
  <div class="section-head"><span class="label">Patient reviews</span><h2>In our patients' words</h2>
  <p>From Google reviews of our Rajouri Garden and Vishnu Garden clinics, and patient stories on Practo.</p></div>
  {review_cards(items)}
  <p style="margin-top:28px"><a href="{GOOGLE_PROFILE}">Read all reviews on Google</a> · <a href="{PRACTO}">Patient stories on Practo</a></p>
</div></section>"""


def gallery(items, root=""):
    """items: (file in assets/images/clinic, caption)."""
    figs = "".join(
        f'<figure><img src="{root}assets/images/clinic/{f}" alt="{esc(c)}" loading="lazy" width="1200" height="900">'
        f'<figcaption>{c}</figcaption></figure>' for f, c in items)
    return f'<div class="gallery">{figs}</div>'


def ph(text):
    return f'<span class="ph">{text}</span>'


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- blog data
def today_ist():
    """Build date in India. BUILD_DATE=YYYY-MM-DD overrides it (for previews)."""
    if os.environ.get("BUILD_DATE"):
        return dt.date.fromisoformat(os.environ["BUILD_DATE"])
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=5, minutes=30)).date()


def approved_posts():
    """Post numbers Dr Parul has approved, one per line in content/approved.txt."""
    f = ROOT / "content" / "approved.txt"
    if not f.exists():
        return set()
    return {int(line.split("#")[0]) for line in f.read_text().splitlines() if line.split("#")[0].strip()}


def post_list():
    """A post goes live once it is written, approved and its publish date has arrived."""
    start = dt.date.fromisoformat(START_DATE)
    today = today_ist()
    approved = approved_posts()
    out = []
    for i, (ch, title, summary, kind) in enumerate(POSTS):
        n = i + 1
        body_file = ROOT / "content" / "posts" / f"{n:02d}.html"
        out.append({
            "n": n, "chapter": ch, "title": title, "summary": summary, "kind": kind,
            "date": start + dt.timedelta(days=2 * i),
            "slug": f"{n:02d}-" + "".join(c if c.isalnum() else "-" for c in title.lower()).strip("-").replace("--", "-"),
            "written": body_file.exists(),
            "approved": n in approved,
            "body": (body_file.read_text()
                     if body_file.exists() and n in approved and start + dt.timedelta(days=2 * i) <= today else None),
        })
    return out


def fmt_date(d):
    return d.strftime("%a %-d %b %Y")


# ---------------------------------------------------------------- structured data
def schema(extra=None):
    """JSON-LD on every page: Dr Parul, the Rajouri Garden clinic and this website, plus page-specific items."""
    def branch(id_, name, street, locality, pin, phone, maps):
        return {"@type": "Dentist", "@id": id_, "name": name, "url": CLINIC_URL, "telephone": phone,
                "image": f"{SITE_URL}/assets/images/clinic/clinic-reception-waiting.jpg", "priceRange": "₹₹",
                "address": {"@type": "PostalAddress", "streetAddress": street, "addressLocality": locality,
                            "addressRegion": "Delhi", "postalCode": pin, "addressCountry": "IN"},
                "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    "opens": "10:00", "closes": "19:00"}],
                "geo": {"@type": "GeoCoordinates", "latitude": 28.6407497, "longitude": 77.120662},
                "hasMap": maps, "sameAs": [GOOGLE_PROFILE, CLINIC_URL + "/", INSTAGRAM, FACEBOOK, YOUTUBE,
                                            "https://www.linkedin.com/company/sobti-dental-clinic/"]}
    graph = [
        branch(f"{SITE_URL}/#clinic", CLINIC, "J 12/26, First Floor, Rajouri Garden",
               "New Delhi", "110027", PHONE, GOOGLE_PROFILE),
        {"@type": "Person", "@id": f"{SITE_URL}/#drparul", "name": "Dr Parul Sharma Sobti",
         "jobTitle": "Cosmetic Dentist and Digital Smile Designer", "honorificSuffix": "BDS",
         "identifier": {"@type": "PropertyValue", "propertyID": "Dental Council registration", "value": "A-8604"},
         "image": PORTRAIT_URL, "url": SITE_URL + "/",
         "alumniOf": "SR Dental College, Maharshi Dayanand University, Rohtak",
         "memberOf": {"@type": "Organization", "name": "Indian Dental Association"},
         "knowsLanguage": ["English", "Hindi"],
         "knowsAbout": ["Smile design", "Digital Smile Design", "Cosmetic dentistry", "Veneers", "Teeth whitening",
                        "Composite bonding", "Gum contouring", "Facial aesthetics"],
         "worksFor": {"@id": f"{SITE_URL}/#clinic"},
         "sameAs": [CLINIC_URL, INSTAGRAM, FACEBOOK, YOUTUBE]},
        {"@type": "WebSite", "@id": f"{SITE_URL}/#website", "url": SITE_URL + "/", "name": "Dr Parul Sharma Sobti",
         "inLanguage": "en-IN", "publisher": {"@id": f"{SITE_URL}/#drparul"}},
    ]
    return {"@context": "https://schema.org", "@graph": graph + (extra or [])}


def post_schema(p):
    url = f'{SITE_URL}/blog/{p["slug"]}.html'
    return [
        {"@type": "BlogPosting", "@id": url + "#post", "headline": p["title"], "description": p["summary"],
         "datePublished": p["date"].isoformat(), "dateModified": p["date"].isoformat(),
         "author": {"@id": f"{SITE_URL}/#drparul"}, "publisher": {"@id": f"{SITE_URL}/#clinic"},
         "image": f"{SITE_URL}/assets/images/share.jpg", "mainEntityOfPage": url, "inLanguage": "en-IN",
         "isPartOf": {"@type": "Blog", "name": "Smile Journal", "url": f"{SITE_URL}/blog.html"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Smile Journal", "item": f"{SITE_URL}/blog.html"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]},
    ]


# ---------------------------------------------------------------- layout
def home_link(root=""):
    # Link to the folder, not index.html: Google treats /index.html as a duplicate of /
    # ("Alternative page with proper canonical tag" in Search Console).
    return root or "./"


def layout(title, desc, body, active, root="", preview_main=False, path="", og_type="website", ld=None):
    nav = "".join(
        f'<a href="{home_link(root) if href == "index.html" else root + href}"{CURRENT if href == active else ""}>{label}</a>'
        for href, label in NAV)
    head = f"""<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="canonical" href="{SITE_URL}/{path}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_IN">
<meta property="og:site_name" content="Dr Parul Sharma Sobti">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE_URL}/{path}">
<meta property="og:image" content="{SITE_URL}/assets/images/share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="1200">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE_URL}/assets/images/share.jpg">
<link rel="icon" href="{root}assets/images/favicon.png">
<link rel="apple-touch-icon" href="{root}assets/images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{root}assets/style.css">
<script type="application/ld+json">{json.dumps(schema(ld), ensure_ascii=False)}</script>"""
    page = f"""<header class="site-header"><div class="wrap">
  <a class="brand" href="{home_link(root)}"><b>Dr Parul Sharma Sobti</b><span>Smile Design · Aesthetic Dentistry</span></a>
  <nav class="nav" aria-label="Main">{nav}</nav>
  <a class="btn" href="{root}visit.html">Book a consultation</a>
</div></header>
<main>
{body}
</main>
{family(root)}
<footer class="site-footer"><div class="wrap">
  <div><b>Dr Parul Sharma Sobti</b> · BDS, Digital Smile Designer<br>{CLINIC} · {ADDRESS}</div>
  <div>Call {PHONE_LINK} · WhatsApp <a href="{WHATSAPP}">{WHATSAPP_NO}</a><br>{EMAIL}<br>{HOURS}</div>
  <div><a href="{GOOGLE_PROFILE}">Google reviews</a> · <a href="{GOOGLE_REVIEW}">Leave a review</a><br><a href="{INSTAGRAM}">Instagram</a> · <a href="{FACEBOOK}">Facebook</a> · <a href="{YOUTUBE}">YouTube</a> · <a href="https://www.linkedin.com/company/sobti-dental-clinic/">LinkedIn</a> · <a href="{root}videos.html">Videos</a></div>
  <div>© 2026 {CLINIC}<br>Our websites: <a href="https://www.sobtidentalcare.com/">sobtidentalcare.com</a> · <a href="https://dentalimplantsdelhi.com/">dentalimplantsdelhi.com</a></div>
</div></footer>"""
    if preview_main:
        return head + "\n" + page
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light">
{head}
{ADS_TAG}
</head>
<body>
{page}
</body>
</html>
"""


def family(root):
    return f"""<section class="family"><div class="wrap">
  <div class="section-head"><span class="label">The Sobti family of websites</span>
  <h2>One clinic, three doors</h2></div>
  <div class="grid three">
    <a class="card" href="{CLINIC_URL}"><span class="label">Clinic</span><h3>Dr Sobti&#39;s Dental Care</h3>
      <p class="muted">Appointments, general dentistry, timings and everything about the practice.</p></a>
    <a class="card" href="{PUSHKAR_URL}"><span class="label">Doctor</span><h3>Dr Pushkar Sobti</h3>
      <p class="muted">Implant surgeon: digital implantology and full-mouth rehabilitation.</p></a>
    <div class="card here"><span class="label">You are here</span><h3>Dr Parul Sharma Sobti</h3>
      <p class="muted">Smile design, dental and facial aesthetics, and the Smile Journal.</p></div>
  </div>
</div></section>"""


def shade_strip():
    shades = [("B1", "--enamel-1"), ("A1", "--enamel-1"), ("B2", "--enamel-2"), ("A2", "--enamel-2"),
              ("C1", "--enamel-3"), ("A3", "--enamel-3"), ("A3.5", "--enamel-4"), ("B3", "--enamel-4")]
    return '<div class="shades" aria-hidden="true">' + "".join(
        f'<span style="background:var({v})">{s}</span>' for s, v in shades) + "</div>"


# ---------------------------------------------------------------- pages
def page_home(posts):
    live = [p for p in posts if p["body"]]
    upcoming = live[-3:][::-1] if live else posts[:3]

    def card(p):
        inner = (f'<div class="card"><span class="label">Post {p["n"]:02d} · {fmt_date(p["date"])}</span>'
                 f'<h3>{esc(p["title"])}</h3><p class="muted">{esc(p["summary"])}</p></div>')
        return f'<a href="blog/{p["slug"]}.html">{inner}</a>' if p["body"] else f"<div>{inner}</div>"
    cards = "".join(card(p) for p in upcoming)
    return f"""<section class="hero"><div class="wrap">
  <div class="hero-copy">
    <span class="label">Smile design · Dental &amp; facial aesthetics</span>
    <h1>Smiles designed around <em>your face</em>, not a catalogue.</h1>
    <p>Dr Parul Sharma Sobti plans every smile from the face inwards: proportion, colour, gums and lips, before a single tooth is touched.</p>
    <div class="hero-actions"><a class="btn" href="visit.html">Book a smile consultation</a>
    <a class="btn ghost" href="blog.html">Read the Smile Journal</a></div>
  </div>
  <figure class="proportion" style="margin:0">
    <img src="assets/images/smile-golden-proportion.jpg" width="1200" height="814"
      alt="A smile with the upper front teeth measured in golden proportion: canine 0.62, lateral incisor 1.0, central incisor 1.62">
    <figcaption class="label">Golden proportion · central 1.62 : lateral 1.0 : canine 0.62, as seen from the front</figcaption></figure>
</div></section>

<section><div class="wrap split">
  {portrait()}
  <div class="prose">
    <span class="label">Meet the doctor</span>
    <h2>Dr Parul Sharma Sobti</h2>
    <p>Dr Parul is a cosmetic dentist and Digital Smile Designer, in practice since 2009 with more than 500 successful smile designs. At {CLINIC} in Rajouri Garden, New Delhi, rated 5 stars by more than 200 patients on Google, she leads smile design and dental aesthetics alongside implant surgeon Dr Pushkar Sobti.</p>
    <p>Her approach is simple: get the mouth healthy, try the gentlest option first, and show patients their new smile before making anything permanent.</p>
    <p>Patients mention the same thing again and again: she gives them time, listens, and makes sure they are comfortable, children included.</p>
    <p><a href="about.html">Read Dr Parul's story →</a></p>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="label">What we do</span><h2>Three layers of a beautiful smile</h2>
  <p>Teeth, gums and face are planned together and treated in the right order.</p></div>
  <div class="grid three">
    <div class="card"><span class="label">Smile designing</span><h3>Planned before it's made</h3>
      <p class="muted">Digital smile design, photographs and a trial smile in your mouth so you approve the result first.</p></div>
    <div class="card"><span class="label">Dental cosmetics</span><h3>Whitening to veneers</h3>
      <p class="muted">Whitening, bonding, contouring, veneers, ceramic crowns, gum contouring and clear aligners.</p></div>
    <div class="card"><span class="label">Facial aesthetics</span><h3>The frame around the smile</h3>
      <p class="muted">Lip balance, smile lines and facial harmony, planned by a dentist who knows the muscles of the face.</p></div>
  </div>
  <p style="margin-top:28px"><a href="treatments.html">See all treatments →</a></p>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="label">Smile Journal · a new post every other day</span>
  <h2>A 60-part story, from first principles to full makeovers</h2>
  <p>Six chapters that move from the basics of a smile to digital design and facial harmony. Start at post one and read in order.</p></div>
  <div class="next-up">{cards}</div>
  <p style="margin-top:28px"><a href="blog.html">See the full series →</a></p>
</div></section>

<section><div class="wrap split">
  <div class="prose">
    <span class="label">Technology</span>
    <h2>Precision you can see</h2>
    <p>3D imaging, scanning, digital design and in-house milling mean your smile is planned, previewed and made under one roof.</p>
    {shade_strip()}
    <p><a href="technology.html">Tour our technology →</a></p>
  </div>
  <dl class="facts">
    <div><dt>Imaging</dt><dd>MyRay X5 CBCT 3D scanner</dd></div>
    <div><dt>Scanning</dt><dd>Three intraoral scanners (Medit i900, i500, Upcera)</dd></div>
    <div><dt>Design</dt><dd>exocad smile design, exoplan implant planning</dd></div>
    <div><dt>Making</dt><dd>3D printer and three in-house milling machines</dd></div>
    <div><dt>Precision</dt><dd>Operating microscope, piezosurgery, ISQ meter</dd></div>
  </dl>
</div>
<div class="wrap" style="margin-top:40px">{gallery([
    ("clinic-treatment-room-blue.jpg", "Microscope operatory"),
    ("lab-veneers-on-model.jpg", "Veneers made in our lab"),
    ("lab-smile-design-mock-up.jpg", "Smile design mock-up"),
])}</div></section>

{reviews_section(REVIEWS[:6])}

<section class="cta-band"><div class="wrap">
  <h2>Thinking about changing your smile? Start with a conversation.</h2>
  <a class="btn" href="visit.html">Book a consultation</a>
</div></section>"""


def page_about():
    return f"""<section class="page-hero"><div class="wrap">
  <span class="label">About</span>
  <h1>Dr Parul Sharma Sobti</h1>
  <p>BDS, Digital Smile Designer and cosmetic dentist, in practice since 2009 with more than 500 successful smile designs, at {CLINIC}, New Delhi.</p>
</div></section>

<section><div class="wrap split">
  {portrait()}
  <div class="prose">
    <h2>Her approach</h2>
    <p>Dr Parul believes a smile should suit the face it belongs to. Every plan starts with listening: what the patient wants to change, what they want to keep, and how they want to feel when they smile.</p>
    <ul>
      <li><strong>Healthy before beautiful.</strong> Gum and tooth health come first.</li>
      <li><strong>Least invasive first.</strong> Whitening, bonding and contouring before veneers or crowns, wherever they can do the job.</li>
      <li><strong>Show before doing.</strong> Patients see a preview on screen or as a trial smile before anything is permanent.</li>
      <li><strong>Face and smile together.</strong> Teeth, gums, lips and facial proportions are designed as one.</li>
    </ul>
    <blockquote class="pull">“Your natural beauty begins with a confident smile.”</blockquote>
  </div>
</div></section>

<section><div class="wrap split">
  <div class="prose"><h2>Qualifications</h2>
  <p class="muted">Registered dental surgeon and member of the Indian Dental Association.</p></div>
  <dl class="facts">
    <div><dt>Degree</dt><dd>Bachelor of Dental Surgery (BDS), SR Dental College, Maharshi Dayanand University, Rohtak</dd></div>
    <div><dt>Focus</dt><dd>Digital Smile Design, cosmetic dentistry and dental aesthetics</dd></div>
    <div><dt>In practice</dt><dd>Since 2009</dd></div>
    <div><dt>Smile designs</dt><dd>500+ successful cases</dd></div>
    <div><dt>Membership</dt><dd>Indian Dental Association (IDA)</dd></div>
    <div><dt>Registration</dt><dd class="mono">A-8604</dd></div>
    <div><dt>Practice</dt><dd>{CLINIC}, Rajouri Garden and Vishnu Garden, New Delhi</dd></div>
  </dl>
</div></section>

<section><div class="wrap split">
  <figure class="solo wide"><img src="assets/images/dr-pushkar-and-dr-parul-sobti.jpg" alt="Dr Parul Sharma Sobti with Dr Pushkar Sobti at Dr Sobti's Dental Care" loading="lazy" width="1440" height="1200">
    <figcaption>Dr Parul with Dr Pushkar Sobti</figcaption></figure>
  <div class="prose"><span class="label">Working together</span><h2>Two dentists, one plan</h2>
  <p>Dr Parul works alongside implant surgeon Dr Pushkar Sobti. When a smile needs both cosmetic work and implants, they plan it together, so the new teeth look right in your face as well as fitting the implants.</p>
  <p><a href="{PUSHKAR_URL}/">Dr Pushkar's implant website →</a></p></div>
</div></section>"""


def page_clinic():
    steps = [
        ("Consultation", "We listen, examine your teeth and gums, and photograph your smile."),
        ("Plan", "Dr Parul designs your smile digitally and explains the options, costs and number of visits."),
        ("Preview", "You see the planned result on screen or as a temporary trial smile."),
        ("Treatment", "Health treatment first, then cosmetic work in the agreed order."),
        ("Aftercare", "Review visits, maintenance and a care plan so your result lasts."),
    ]
    rows = "".join(f'<div><dt>Step {i}</dt><dd><b>{a}.</b> {b}</dd></div>' for i, (a, b) in enumerate(steps, 1))
    return f"""<section class="page-hero"><div class="wrap">
  <span class="label">The clinic</span>
  <h1>Dr Sobti&#39;s Dental Care</h1>
  <p>A family practice in West Delhi since 1982, when Dr Rajesh Sobti opened the Vishnu Garden clinic. Today it is run by Dr Parul Sharma Sobti and Dr Pushkar Sobti. Known for dental implants and cosmetic dentistry, rated 5 stars from more than 200 Google reviews across our two clinics, and trusted by patients from more than 20 countries.</p>
</div></section>

<section><div class="wrap split">
  <div class="grid">
    <div class="card"><span class="label">Dr Parul Sharma Sobti</span><h3>BDS · Digital Smile Designer</h3>
      <p class="muted">Smile design, cosmetic dentistry and dental aesthetics. In practice since 2009, 500+ smile designs.</p></div>
    <div class="card"><span class="label"><a href="{PUSHKAR_URL}">Dr Pushkar Sobti</a></span><h3>BDS, MDS, PG in Oral Implantology (UCAM) · Implantologist</h3>
      <p class="muted">In practice since 2009, more than 5,000 implants and 500 full arches. Guided surgery, zygomatic and pterygoid implants, full-mouth rehabilitation.</p></div>
  </div>
  <dl class="facts">
    <div><dt>Head clinic</dt><dd>{ADDRESS} · <a href="{MAP_1}">Map</a></dd></div>
    <div><dt>Also at</dt><dd>{ADDRESS_2} · <a href="{MAP_2}">Map</a></dd></div>
    <div><dt>Hours</dt><dd>{HOURS}</dd></div>
    <div><dt>Established</dt><dd>2009</dd></div>
    <div><dt>Team</dt><dd>12 people and growing · 1 implant surgery suite and 2 general dentistry chairs</dd></div>
    <div><dt>Appointments</dt><dd>Call {PHONE_LINK} · WhatsApp <a href="{WHATSAPP}">{WHATSAPP_NO}</a></dd></div>
    <div><dt>Email</dt><dd>{EMAIL}</dd></div>
    <div><dt>Main website</dt><dd><a href="{CLINIC_URL}">sobtidentalcare.com</a></dd></div>
  </dl>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="label">Inside the clinic</span><h2>Rajouri Garden, New Delhi</h2></div>
  {gallery([
    ("clinic-reception-waiting.jpg", "Reception and waiting area"),
    ("clinic-treatment-room.jpg", "Treatment room"),
    ("clinic-treatment-room-blue.jpg", "Microscope operatory"),
    ("clinic-treatment-room-2.jpg", "Second treatment room"),
    ("clinic-treatment-room-3.jpg", "Treatment room, wide view"),
    ("clinic-lounge-certificates.jpg", "Patient lounge"),
    ("clinic-lounge-sofa.jpg", "Waiting lounge"),
    ("clinic-cbct-scanner.jpg", "CBCT 3D scanner"),
    ("clinic-dental-lab.jpg", "In-house lab"),
  ])}
</div></section>

<section><div class="wrap split">
  <div class="prose"><span class="label">Your visit</span><h2>How treatment works here</h2>
  <p>Every smile project follows the same five steps, whether it is one crown or a full makeover.</p></div>
  <dl class="facts">{rows}</dl>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="label">Safety</span><h2>Sterilisation and hygiene</h2>
  <p>Strict hygiene, sterilisation and infection-control protocols for every patient.</p></div>
  <div class="grid three">
    <div class="card"><h3>Class B autoclave</h3><p class="muted">Instruments are cleaned, pouched and sterilised in a hospital-grade Class B autoclave for every patient.</p></div>
    <div class="card"><h3>Single-use items</h3><p class="muted">Needles, gloves, masks, suction tips and bibs are used once and discarded.</p></div>
    <div class="card"><h3>Surface disinfection</h3><p class="muted">The chair and surfaces are disinfected between every appointment.</p></div>
  </div>
  <figure class="solo"><img src="assets/images/clinic/clinic-class-b-autoclave.jpg" alt="Class B autoclave at the clinic" loading="lazy" width="900" height="1200">
    <figcaption>Our Class B autoclave</figcaption></figure>
</div></section>"""


TREATMENTS = [
    ("Smile designing", "Planning the whole smile around your face.", [
        ("Digital Smile Design (DSD)", "Photographs and video analysed on screen to plan tooth shape, size and position.", "1–2 visits"),
        ("Trial smile (mock-up)", "A temporary version of your new smile placed over your teeth so you can see and feel it.", "1 visit"),
        ("Smile makeover", "A combined plan that may include whitening, gum shaping, veneers and alignment.", "Planned case by case"),
    ]),
    ("Cosmetic dentistry", "Brightening and reshaping teeth.", [
        ("Teeth whitening", "In-clinic and take-home whitening for natural teeth.", "1 visit / 2 weeks at home"),
        ("Composite bonding", "Tooth-coloured resin to repair chips, worn edges and small gaps.", "1 visit"),
        ("Porcelain veneers", "Thin ceramic shells that change colour, shape and length.", "2–3 visits"),
        ("Composite veneers", "Veneers sculpted directly in resin, quicker and easily repaired.", "1–2 visits"),
        ("Enamel contouring", "Light reshaping of edges to even out the smile.", "1 visit"),
        ("Tooth-coloured fillings", "Replacing dark or silver fillings with natural-looking materials.", "1 visit"),
    ]),
    ("Crowns, bridges & implants", "Restoring and replacing teeth so they look natural.", [
        ("Ceramic crowns", "Metal-free zirconia and lithium disilicate crowns.", "2 visits"),
        ("Crowns and bridges", "Fixed replacements for damaged or missing teeth.", "2–3 visits"),
        ("Single tooth implant", "Guided placement with an Osstem implant, custom abutment and zirconia crown, with a 3-year warranty. From ₹35,000.", "Over 3–6 months"),
        ("Immediate implants and same-day teeth", "An implant placed when the tooth is removed, with fixed teeth the same day where suitable.", "1 visit to start"),
        ("Zygomatic and pterygoid implants", "Fixed teeth for people told they lack the bone for regular implants, without bone grafting.", "Planned case by case"),
        ("Bone grafting, sinus lift and PRF", "Rebuilding bone and speeding healing using your own growth factors.", "With implant treatment"),
        ("Full-mouth rehabilitation", "Rebuilding a worn, broken or missing set of teeth to restore bite, function and the lower face.", "Planned case by case"),
        ("All-on-4 / All-on-X", "A full fixed set of teeth on four to six implants for people missing most or all teeth.", "Planned case by case"),
        ("Dentures", "Complete and partial dentures, made to look natural.", "3–5 visits"),
    ]),
    ("Gums & alignment", "The frame of the smile.", [
        ("Gum contouring", "Reshaping uneven or excess gum for a balanced gum line.", "1 visit"),
        ("Gummy smile treatment", "Gum, lip or bone procedures depending on the cause.", "Varies"),
        ("Clear aligners", "Removable, nearly invisible trays that straighten teeth.", "6–18 months"),
        ("Braces", "Fixed orthodontic braces for children and adults.", "12–24 months"),
    ]),
    ("Facial aesthetics", "Balancing the face around the smile.", [
        ("Anti-wrinkle injections", "Softening frown lines, crow's feet and an over-active upper lip.", "1 visit"),
        ("Dermal fillers", "Lip enhancement and smile-line softening with hyaluronic acid fillers.", "1 visit"),
    ]),
    ("General dentistry", "The healthy foundation for every smile.", [
        ("Scaling and polishing", "Professional cleaning to remove stains, plaque and tartar.", "1 visit"),
        ("Root canal treatment", "Single-sitting root canal treatment where suitable, under magnification.", "1–2 visits"),
        ("Extractions", "Routine and surgical removal, including impacted wisdom teeth.", "1 visit"),
        ("Fillings", "Treatment of decay with tooth-coloured materials.", "1 visit"),
        ("Children's dentistry", "Gentle check-ups, fillings and prevention for children.", "1 visit"),
        ("Conscious sedation", "Sedation for anxious patients during treatment.", "With treatment"),
    ]),
]


def page_treatments():
    groups = []
    for name, sub, items in TREATMENTS:
        rows = "".join(f'<div class="titem"><h3>{t}</h3><span class="mono">{v}</span><p>{d}</p></div>' for t, d, v in items)
        groups.append(f'<div class="tgroup"><div><h2>{name}</h2><p class="muted">{sub}</p></div><div class="tlist">{rows}</div></div>')
    return f"""<section class="page-hero"><div class="wrap">
  <span class="label">Treatments</span>
  <h1>What we do</h1>
  <p>From a single whitening session to a full smile and facial makeover. Visit counts are typical and depend on your case. Prices: <a href="veneers.html">veneers</a>, <a href="dental-crown-cost-delhi.html">crowns and caps</a>, <a href="braces-cost-delhi.html">braces</a>, <a href="clear-aligners-cost-delhi.html">clear aligners</a>, <a href="root-canal-cost-delhi.html">root canal</a>, <a href="teeth-whitening-cost-delhi.html">whitening</a> and <a href="teeth-cleaning-cost-delhi.html">cleaning</a>.</p>
</div></section>
<section><div class="wrap treatments">{''.join(groups)}</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="label">From our lab</span><h2>Made on the same floor as the clinic</h2>
  <p>Veneers, crowns, mock-ups and aligners are designed and made at Titanium Arts Dental Studio, the clinic's own lab.</p></div>
  {gallery([
    ("lab-veneers-on-model.jpg", "Veneers on the patient's model"),
    ("lab-smile-design-mock-up.jpg", "Smile design mock-up on a printed model"),
    ("lab-zirconia-bridge.jpg", "Zirconia bridge, milled in-house"),
    ("lab-clear-aligner.jpg", "Clear aligner"),
    ("lab-front-teeth-bridge.jpg", "Front teeth bridge, hand-finished"),
    ("lab-crowns-on-printed-model.jpg", "Crowns on a 3D-printed model"),
  ])}
</div></section>
{reviews_section(REVIEWS[3:])}"""


VENEER_FAQ = [
    ("How much do veneers cost in Delhi?",
     "At Dr Sobti's Dental Care in Rajouri Garden, veneers start from ₹10,000 per tooth. The final cost depends on the material and how many teeth are included, and you get a written estimate after your consultation."),
    ("How does veneers cost in India compare with Delhi?",
     "Prices across India range widely, mainly because of the material and the lab. Porcelain made in a good lab costs more than composite. We quote per tooth, from ₹10,000, with the material written on your estimate."),
    ("What does a smile makeover cost?",
     "Smile makeover cost in India varies more than almost any other treatment, because it depends on what the plan includes. Some makeovers are whitening and a few bonded edges; others need veneers on 8 to 10 teeth. Dr Parul gives you a written estimate after the smile design, before any treatment."),
    ("How many teeth need veneers?",
     "It depends on how much of your smile shows. Many people only need the front teeth that are visible when they smile. The smile design shows exactly which teeth to include before anything is done."),
    ("Porcelain or composite veneers: which is better?",
     "Porcelain veneers keep their colour and shine longer and take 2 to 3 visits. Composite veneers are sculpted directly in resin in 1 to 2 visits and are easier to repair. Dr Parul will explain which suits your teeth and budget."),
    ("Can I see the result before getting veneers?",
     "Yes. Your new smile is designed on your own photos and scans, and a trial smile (mock-up) can be placed over your teeth so you can see and feel it before any permanent work."),
]


def page_veneers():
    faq = "".join(f'<div class="titem"><h3>{q}</h3><p>{a}</p></div>' for q, a in VENEER_FAQ)
    return f"""<section class="page-hero"><div class="wrap">
  <span class="label">Treatments · Veneers</span>
  <h1>Veneers in Delhi</h1>
  <p>Porcelain and composite veneers with Dr Parul Sharma Sobti at {CLINIC}, Rajouri Garden. Veneers start from ₹10,000 per tooth.</p>
</div></section>

<section><div class="wrap split">
  <div class="prose">
    <h2>What veneers can change</h2>
    <p>A veneer is a thin layer bonded to the front of a tooth. It can change the colour, shape and length of a tooth, close small gaps, and cover chips or stains that whitening cannot lift.</p>
    <p>Dr Parul works on the principle of least invasive first. If whitening, bonding or a little reshaping can give you the smile you want, she will tell you so before suggesting veneers.</p>
    <h2>Porcelain or composite</h2>
    <ul>
      <li>Porcelain veneers are thin ceramic shells. They hold their colour and shine for many years and take 2 to 3 visits.</li>
      <li>Composite veneers are sculpted directly on the tooth in resin. They take 1 to 2 visits, cost less and are easy to repair.</li>
    </ul>
    <p>Glass-ceramic veneers are milled in the clinic's own lab, which keeps the fit precise and the waiting time short.</p>
    <h2>How it works</h2>
    <ul>
      <li>Consultation: photographs, a look at your teeth and gums, and what you want to change.</li>
      <li>Smile design: your new smile is planned on screen around your face.</li>
      <li>Trial smile: a temporary version over your own teeth, so you can see and feel it first.</li>
      <li>Veneers: prepared and fitted only once you have agreed the design.</li>
    </ul>
  </div>
  <dl class="facts">
    <div><dt>Price</dt><dd>From ₹10,000 per tooth</dd></div>
    <div><dt>Porcelain</dt><dd>2–3 visits</dd></div>
    <div><dt>Composite</dt><dd>1–2 visits</dd></div>
    <div><dt>Where</dt><dd>{CLINIC}, {ADDRESS} · <a href="{MAP_1}">Map</a></dd></div>
    <div><dt>Call</dt><dd>{PHONE_LINK} · WhatsApp <a href="{WHATSAPP}">{WHATSAPP_NO}</a></dd></div>
    <div><dt>Hours</dt><dd>{HOURS}</dd></div>
  </dl>
</div></section>

{video_block(PAGE_VIDEOS["veneers"])}
<section><div class="wrap treatments"><div class="tgroup"><div><h2>Questions</h2>
<p class="muted">Ask anything else on WhatsApp.</p></div><div class="tlist">{faq}</div></div></div></section>
<section><div class="wrap"><p><a class="btn" href="visit.html">Book a smile consultation</a> <a href="treatments.html">See all treatments</a></p></div></section>"""


def veneers_schema():
    url = f"{SITE_URL}/veneers.html"
    return [
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in VENEER_FAQ]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Treatments", "item": f"{SITE_URL}/treatments.html"},
            {"@type": "ListItem", "position": 3, "name": "Veneers", "item": url}]},
    ] + video_ld(PAGE_VIDEOS["veneers"], "veneers.html")


def _paras(blocks):
    out = []
    for b in blocks:
        out.append("<ul>" + "".join(f"<li>{x}</li>" for x in b) + "</ul>" if isinstance(b, list) else f"<p>{b}</p>")
    return "".join(out)


def faq_html(faq):
    return "".join(f'<div class="titem"><h3>{q}</h3><p>{a}</p></div>' for q, a in faq)


def page_schema(slug, name, faq):
    url = f"{SITE_URL}/{slug}.html"
    return [
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re_tags(a))}} for q, a in faq]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Treatments", "item": f"{SITE_URL}/treatments.html"},
            {"@type": "ListItem", "position": 3, "name": name, "item": url}]},
    ] + video_ld(PAGE_VIDEOS.get(slug, []), f"{slug}.html")


def re_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


def page_price(pg):
    prices = "".join(f'<div class="titem"><h3>{i}</h3><span class="mono">{v}</span></div>' for i, v in pg["prices"])
    body = "".join(f"<h2>{h}</h2>{_paras(b)}" for h, b in pg["sections"])
    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in pg["facts"])
    return f"""<section class="page-hero"><div class="wrap">
  <span class="label">{pg["label"]}</span>
  <h1>{pg["h1"]}</h1>
  <p>{pg["intro"]}</p>
</div></section>

<section><div class="wrap treatments"><div class="tgroup"><div><h2>Prices</h2>
<p class="muted">Starting prices, updated November 2026. You get the full cost in writing before treatment starts.</p></div><div class="tlist">{prices}</div></div></div></section>

<section><div class="wrap split">
  <div class="prose">{body}</div>
  <dl class="facts">
    {facts}
    <div><dt>Where</dt><dd>{CLINIC}, {ADDRESS} · <a href="{MAP_1}">Map</a></dd></div>
    <div><dt>Call</dt><dd>{PHONE_LINK} · WhatsApp <a href="{WHATSAPP}">{WHATSAPP_NO}</a></dd></div>
    <div><dt>Hours</dt><dd>{HOURS}</dd></div>
    <div><dt>Pay by</dt><dd>UPI, card or cash</dd></div>
  </dl>
</div></section>

{video_block(PAGE_VIDEOS.get(pg["slug"], []))}
<section><div class="wrap treatments"><div class="tgroup"><div><h2>Questions</h2>
<p class="muted">Ask anything else on WhatsApp.</p></div><div class="tlist">{faq_html(pg["faq"])}</div></div></div></section>
<section><div class="wrap"><p><a class="btn" href="visit.html">{pg["cta"]}</a> <a href="treatments.html">See all treatments</a></p></div></section>"""


def page_rajouri():
    links = "".join(f'<li><a href="{p["slug"]}.html">{p["name"]}</a>: {p["prices"][0][1].lower()}</li>' for p in PRICE_PAGES)
    return f"""<section class="page-hero"><div class="wrap">
  <span class="label">Rajouri Garden, West Delhi</span>
  <h1>Treatment prices, timings and directions</h1>
  <p>Dr Parul sees patients at <a href="{CLINIC_URL}/">{CLINIC}, our clinic in Rajouri Garden</a>, above Rajmandir in Rajouri Garden Extension. Dr Pushkar Sobti and Dr Parul Sharma Sobti have been in practice since 2009, and the Rajouri Garden clinic opened in 2024. Below are starting prices and how to reach us.</p>
</div></section>

<section><div class="wrap split">
  <div class="prose">
    <h2>Your dentists</h2>
    <ul>
      <li><strong>Dr Pushkar Sobti</strong> (BDS, MDS, PG in Oral Implantology) is an implantologist who has placed more than 5,000 implants, from single teeth to <a href="{PUSHKAR_URL}/">All-on-4 and full mouth implants</a>.</li>
      <li><strong><a href="about.html">Dr Parul Sharma Sobti</a></strong> (BDS) focuses on smile design and cosmetic dentistry: veneers, whitening, bonding and smile makeovers.</li>
    </ul>
    <h2>Treatments and starting prices</h2>
    <ul>
      {links}
      <li><a href="veneers.html">Veneers</a>: from ₹10,000 per tooth</li>
      <li>Tooth-coloured fillings: from ₹2,500</li>
      <li>Wisdom tooth removal: from ₹10,000</li>
      <li><a href="{PUSHKAR_URL}/dental-implant-cost-delhi/">Dental implants</a>: from ₹35,000</li>
      <li>Children's dentistry, dentures and all general treatments, priced after a check-up</li>
    </ul>
    <p>Everything is planned with digital tools: a CBCT scanner, intraoral 3D scanners, a dental microscope and an in-house lab. See <a href="technology.html">our technology</a>.</p>
    <h2>Getting here</h2>
    <p>The clinic is on the first floor of J-12/26, Block J, Rajouri Garden Extension, above Rajmandir and near Geetanjali Salon. It is about 1.5 km from Rajouri Garden metro station. Parking is available, and there is a lift.</p>
    <p>Patients come from across Delhi and NCR, including Tagore Garden, Subhash Nagar, Tilak Nagar, Janakpuri, Punjabi Bagh and Ramesh Nagar, as well as from other states. We also regularly treat international patients from the UK, Europe, the US, Canada, Australia, New Zealand, Hong Kong, Japan, Singapore, the UAE, Saudi Arabia and Africa.</p>
  </div>
  <dl class="facts">
    <div><dt>Address</dt><dd>{CLINIC}, {ADDRESS} · <a href="{MAP_1}">Map</a></dd></div>
    <div><dt>Landmark</dt><dd>Above Rajmandir, near Geetanjali Salon</dd></div>
    <div><dt>Metro</dt><dd>About 1.5 km from Rajouri Garden</dd></div>
    <div><dt>Hours</dt><dd>{HOURS}</dd></div>
    <div><dt>Call</dt><dd>{PHONE_LINK} · WhatsApp <a href="{WHATSAPP}">{WHATSAPP_NO}</a></dd></div>
    <div><dt>Languages</dt><dd>Hindi and English</dd></div>
    <div><dt>Pay by</dt><dd>UPI, card or cash</dd></div>
    <div><dt>Access</dt><dd>Parking and lift</dd></div>
  </dl>
</div></section>

<section><div class="wrap treatments"><div class="tgroup"><div><h2>Questions</h2>
<p class="muted">Ask anything else on WhatsApp.</p></div><div class="tlist">{faq_html(RAJOURI_FAQ)}</div></div></div></section>
<section><div class="wrap"><p><a class="btn" href="visit.html">Book a visit</a> <a href="treatments.html">See all treatments</a></p></div></section>"""


def rajouri_schema():
    url = f"{SITE_URL}/dentist-rajouri-garden.html"
    return [
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in RAJOURI_FAQ]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Prices, timings and directions", "item": url}]},
    ]


TECH = [
    ("MyRay X5 CBCT", "3D X-ray of bone, nerves and sinuses for safe, precise implant planning.", "Imaging"),
    ("Medit i900, Medit i500 and Upcera scanners", "Three intraoral 3D scanners: digital impressions in minutes, no trays.", "Scanning"),
    ("exocad Smile Design", "Your new smile designed on your own photos and scans before treatment.", "Planning"),
    ("exoplan and Blue Sky Bio", "Implant planning software to position every implant in 3D before surgery.", "Planning"),
    ("3D printer", "Surgical guides, study models, mock-ups and temporary teeth printed in-house.", "Fabrication"),
    ("Roland dry mill", "Zirconia crowns and bridges milled in-house.", "Fabrication"),
    ("Upcera wet mill", "Glass-ceramic veneers and crowns, and PMMA temporaries.", "Fabrication"),
    ("Kelkar wet mill", "Titanium components for implant restorations.", "Fabrication"),
    ("Dental microscope and loupes", "One operating microscope and three sets of loupes for magnified precision.", "Precision"),
    ("Piezosurgery unit", "Ultrasonic bone surgery that spares soft tissue for gentler implant and graft work.", "Surgery"),
    ("Implant motors with torque control", "Three units that place implants at exactly the planned force.", "Surgery"),
    ("ISQ stability meter", "Measures implant stability so teeth are loaded only when the implant is ready.", "Surgery"),
    ("PRF centrifuge", "Prepares growth factors from your own blood to speed healing.", "Healing"),
    ("Conscious sedation", "Calm, relaxed treatment for anxious patients.", "Comfort"),
    ("Class B autoclave", "Hospital-grade sterilisation for every instrument.", "Safety"),
]


def page_technology():
    rows = "".join(
        f'<tr><td><b>{n}</b></td><td>{d}</td><td class="mono muted">{c}</td></tr>'
        for n, d, c in TECH)
    return f"""<section class="page-hero"><div class="wrap">
  <span class="label">Technology</span>
  <h1>How advanced we are, and why it matters to you</h1>
  <p>Technology is only useful if it makes treatment more accurate, more comfortable or more predictable. Here is what we use and what it does for you.</p>
</div></section>
<section><div class="wrap">
  {gallery([
    ("clinic-cbct-scanner.jpg", "MyRay CBCT 3D scanner"),
    ("clinic-treatment-room-blue.jpg", "Operating microscope"),
    ("clinic-dental-lab.jpg", "3D printers and Kelkar mill in our lab"),
  ])}
  <div class="table-wrap" style="margin-top:40px"><table>
    <thead><tr><th>Equipment</th><th>What it does for you</th><th>Area</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</div></section>
<section><div class="wrap split">
  <div class="prose"><span class="label">Spotlight</span><h2>From scan to smile, digitally</h2>
  <p>A typical smile makeover here starts with an intraoral scan and photographs. Dr Parul designs the new smile in exocad, a mock-up is 3D printed so you can try it in your mouth, and the final veneers or crowns are milled in-house from zirconia or glass ceramic. For implants, a CBCT scan shows the bone in 3D, Dr Pushkar plans each implant in exoplan, and it is placed through a printed surgical guide.</p></div>
  <div class="prose"><p>Posts 41 to 50 of the Smile Journal explain each of these technologies in detail.</p>
  <p><a href="blog.html">See the Smile Journal →</a></p></div>
</div></section>"""


def page_blog(posts):
    chapters = []
    for num, name, desc in CHAPTERS:
        items = []
        for p in [p for p in posts if p["chapter"] == num]:
            title = (f'<a href="blog/{p["slug"]}.html">{esc(p["title"])}</a>' if p["body"]
                     else f'<span class="title">{esc(p["title"])}</span>')
            tag = '<span class="doc">Dr Parul</span>' if p["kind"] == "doctor" else ""
            items.append(f'<li><span class="n">{p["n"]:02d}</span><span class="t">{title}{tag}<small>{esc(p["summary"])}</small></span>'
                         f'<span class="d">{fmt_date(p["date"])}</span></li>')
        chapters.append(f'<div class="chapter"><div class="chapter-head"><span class="num">{num}</span><h2>{name}</h2><p>{desc}</p></div>'
                        f'<ol class="posts">{"".join(items)}</ol></div>')
    first, last = posts[0]["date"], posts[-1]["date"]
    return f"""<section class="page-hero"><div class="wrap">
  <span class="label">Smile Journal · every other day · {fmt_date(first)} to {fmt_date(last)}</span>
  <h1>The story of a smile, in 60 parts</h1>
  <p>Each post builds on the one before, moving from the basics of a smile to digital design and full facial harmony. Posts marked Dr Parul tell her own story and the clinic's.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">{''.join(chapters)}</div></section>"""


def page_post(p, posts):
    ch = next(c for c in CHAPTERS if c[0] == p["chapter"])
    prev_p = posts[p["n"] - 2] if p["n"] > 1 else None
    next_p = posts[p["n"]] if p["n"] < len(posts) else None

    def link(q, cls, label):
        if not q:
            return "<div></div>"
        inner = f'<span class="label">{label}</span><b>{esc(q["title"])}</b>'
        if q["body"]:
            return f'<a class="{cls}" href="{q["slug"]}.html">{inner}</a>'
        return f'<div class="{cls}">{inner}<span class="muted mono">{fmt_date(q["date"])}</span></div>'

    words = len(p["body"].split())
    pct = round(p["n"] / len(posts) * 100)
    return f"""<article class="article"><div class="wrap">
  <header>
    <span class="label">Chapter {ch[0]} · {ch[1]} · Post {p["n"]:02d} of {len(posts)}</span>
    <h1>{esc(p["title"])}</h1>
    <span class="mono muted">{fmt_date(p["date"])} · {max(2, round(words / 220))} min read · By Dr Parul Sharma Sobti</span>
    <div class="progress" aria-label="Series progress {pct}%"><i style="width:{pct}%"></i></div>
  </header>
  <div class="article-body">{p["body"]}</div>
  <nav class="article-nav" aria-label="Series">{link(prev_p, "prev", "← Previous")}{link(next_p, "next", "Next in the story →")}</nav>
  <p style="margin-top:28px"><a href="../blog.html">All 60 posts</a></p>
</div></article>"""


def page_visit():
    return f"""<section class="page-hero"><div class="wrap">
  <span class="label">Visit</span>
  <h1>Book a smile consultation</h1>
  <p>The first visit is a conversation: we look at your teeth, gums and face, photograph your smile and talk through what is possible.</p>
</div></section>
<section><div class="wrap split">
  <dl class="facts">
    <div><dt>WhatsApp</dt><dd><a href="{WHATSAPP}">{WHATSAPP_NO}</a></dd></div>
    <div><dt>Call</dt><dd class="mono">{"<br>".join(f'<a href="tel:{p.replace(" ", "")}">{p}</a>' for p in PHONES)}</dd></div>
    <div><dt>Email</dt><dd>{EMAIL}</dd></div>
    <div><dt>Head clinic</dt><dd>{CLINIC}, {ADDRESS} · <a href="{MAP_1}">Map</a> · <a href="dentist-rajouri-garden.html">Directions, timings and prices</a></dd></div>
    <div><dt>Also at</dt><dd>{ADDRESS_2} · <a href="{MAP_2}">Map</a></dd></div>
    <div><dt>Hours</dt><dd>{HOURS}</dd></div>
    <div><dt>Book online</dt><dd><a href="https://www.sobtidentalcare.com/booking.html">sobtidentalcare.com/booking</a></dd></div>
    <div><dt>International</dt><dd>Patients from more than 20 countries. Medical visa invitation letters, paid airport pickup and nearby hotels can be arranged. Full-arch treatment usually needs about 15 days in Delhi.</dd></div>
    <div><dt>Bring</dt><dd>Any previous X-rays, a list of medicines, and photos of smiles you like.</dd></div>
  </dl>
  <div class="prose"><h2>What to expect</h2>
  <ul><li>About 30 to 45 minutes with Dr Parul.</li><li>Examination, smile photographs and, if needed, an X-ray.</li>
  <li>A clear explanation of options, number of visits and costs.</li><li>No treatment starts until you have seen and agreed the plan.</li></ul>
  </div>
</div></section>"""


# ---------------------------------------------------------------- videos (YouTube @DrSobtiDental)
VIDEO_SECTIONS = [
    ("Smile makeovers and veneers", "Smile designing, composite veneers and same-day teeth, from the first design to the final smile.",
     ["oAl3H6l39Es", "s3GXnZ2gkUk", "2_e0jS8wVsg", "6PXXzwvCBco", "etx9YUTW_kg", "t2iKVdDL8D0", "1SivMyXkBa0", "VBxecBKQiYo", "6zl3kROUoso"]),
    ("Crowns made in our own lab", "Crowns and bridges designed on screen and milled in the clinic.",
     ["fvKcdFYR3R8", "nkUCoO-IgKk"]),
    ("Comfortable treatment", "Root canals, wisdom teeth and laughing gas for nervous patients.",
     ["kPXjCugNphI", "a3YGzvm1YsU", "kQDuNdLutes"]),
    ("Children", "Gentle treatment for children, in the words of the children and their parents.",
     ["K6o1xrWnsJ4", "HMKI76NpUCw", "4pk7Kov41sQ"]),
    ("Gums and cleaning", "Air polishing and gentler gum treatment.",
     ["Q4XgYfekrpw", "Vu4W2Kl_Mvs"]),
    ("Inside the clinic", "A look around Dr Sobti's Dental Care in Rajouri Garden, where Dr Parul sees her patients.",
     ["lDd7hbX0E9k", "thmGh27-57I", "VL64ySkZs60"]),
]
VIDEO_FAQ = [
    ("Can composite veneers fix a smile after a root canal?",
     "Often, yes. If a treated tooth looks darker or the shape no longer matches, composite veneers can reshape and recolour it with very little drilling. A very dark tooth may need a crown or porcelain veneer instead."),
    ("Can a crown be made the same day?",
     "In many cases, yes. The tooth is scanned, the crown is designed on screen with you, then milled and finished in the clinic's own lab, so a single crown can often be fitted in about 2 hours."),
    ("Is laughing gas safe for nervous patients and children?",
     "Nitrous oxide (laughing gas) is a mild sedative breathed through a small nose mask. It helps you relax while you stay awake, and its effect wears off within minutes after the mask is removed."),
    ("Are root canals painful?",
     "With local anaesthesia, a root canal should feel much like a filling. Most of the pain people remember comes from the infection before treatment, not from the treatment itself."),
    ("What is dental air polishing?",
     "Air polishing removes stains and plaque with a fine jet of air, water and a gentle powder. It is quicker and more comfortable than scraping alone and is often added to a scaling and cleaning visit."),
]
PAGE_VIDEOS = {
    "veneers": ["s3GXnZ2gkUk", "oAl3H6l39Es", "6PXXzwvCBco"],
    "dental-crown-cost-delhi": ["2_e0jS8wVsg", "fvKcdFYR3R8"],
    "root-canal-cost-delhi": ["kPXjCugNphI", "K6o1xrWnsJ4"],
    "teeth-cleaning-cost-delhi": ["Q4XgYfekrpw", "Vu4W2Kl_Mvs"],
}


def video_grid(ids):
    return '<div class="yt-grid">' + "".join(video_card(VIDEOS[i], esc) for i in ids) + "</div>"


def video_block(ids):
    if not ids:
        return ""
    return f"""<section><div class="wrap"><div class="section-head"><span class="label">On video</span><h2>See it from our clinic</h2></div>
{video_grid(ids)}
<p style="margin-top:20px"><a href="videos.html">All videos</a> · <a href="{YOUTUBE}">YouTube channel</a></p></div></section>
{VIDEO_JS}"""


def video_ld(ids, page):
    return [dict(video_obj(VIDEOS[i], f"{SITE_URL}/{page}"), publisher={"@id": f"{SITE_URL}/#clinic"}) for i in ids]


def page_videos():
    secs = "".join(f"""<section><div class="wrap"><div class="section-head"><span class="label">Videos</span><h2>{esc(h)}</h2><p>{esc(intro)}</p></div>
{video_grid(ids)}</div></section>""" for h, intro, ids in VIDEO_SECTIONS)
    return f"""<section class="page-hero"><div class="wrap">
  <span class="label">Videos</span>
  <h1>Smile makeover and cosmetic dentistry videos</h1>
  <p>Real cases and patient stories from {CLINIC}, Rajouri Garden, New Delhi: smile designing, composite veneers, same-day crowns, gentle treatment for children and nervous patients. Tap a video to play it here, or watch more on our <a href="{YOUTUBE}">YouTube channel</a>.</p>
</div></section>
{secs}
<section><div class="wrap treatments"><div class="tgroup"><div><h2>Quick answers</h2>
<p class="muted">Ask anything else on WhatsApp.</p></div><div class="tlist">{faq_html(VIDEO_FAQ)}</div></div></div></section>
<section><div class="wrap"><p><a class="btn" href="visit.html">Book a smile consultation</a> <a href="treatments.html">See all treatments</a> · Implant videos: <a href="{PUSHKAR_URL}/videos/">Dr Pushkar Sobti</a> · Clinic videos: <a href="https://www.sobtidentalcare.com/videos.html">sobtidentalcare.com</a></p></div></section>
{VIDEO_JS}"""


def videos_schema():
    url = f"{SITE_URL}/videos.html"
    ids = [i for _, _, l in VIDEO_SECTIONS for i in l]
    return [{"@type": "CollectionPage", "@id": url, "url": url, "name": "Smile makeover and cosmetic dentistry videos",
             "about": {"@id": f"{SITE_URL}/#clinic"}, "inLanguage": "en-IN"},
            {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in VIDEO_FAQ]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": "Videos", "item": url}]}] + video_ld(ids, "videos.html")


# ---------------------------------------------------------------- build
def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def build(out, preview=False):
    global PREVIEW
    PREVIEW = preview
    posts = post_list()
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    shutil.copy(ROOT / "assets" / "style.css", out / "assets" / "style.css")
    shutil.copytree(ROOT / "assets" / "images", out / "assets" / "images")
    pages = [
        ("index.html", "Cosmetic Dentist in Rajouri Garden, Delhi | Dr Parul Sharma Sobti", "Dr Parul Sharma Sobti is a cosmetic dentist in Rajouri Garden, New Delhi. Veneers, whitening, bonding and smile makeovers planned around your face. 500+ smile designs.", page_home(posts)),
        ("about.html", "About Dr Parul Sharma Sobti, Cosmetic Dentist in Delhi", "Dr Parul Sharma Sobti (BDS), Digital Smile Designer at Dr Sobti's Dental Care, Rajouri Garden: her training, approach and 500+ smile designs since 2009.", page_about()),
        ("clinic.html", "Dr Sobti's Dental Care, Rajouri Garden, Delhi", "Inside Dr Sobti's Dental Care in Rajouri Garden, New Delhi: the team, your first visit, hygiene and sterilisation standards.", page_clinic()),
        ("treatments.html", "Veneers, Teeth Whitening & Smile Makeover in Delhi | Dr Parul", "Smile design, veneers, teeth whitening, composite bonding, gum contouring, aligners and facial aesthetics with Dr Parul Sharma Sobti in Rajouri Garden, Delhi.", page_treatments()),
        ("technology.html", "Digital Smile Design & Dental Technology in Delhi | Dr Parul", "Digital Smile Design, dental microscopes, CBCT and digital X-rays at Dr Sobti's Dental Care, Rajouri Garden, Delhi, and how they make cosmetic work precise.", page_technology()),
        ("blog.html", "Smile Journal: Cosmetic Dentistry Blog | Dr Parul Sharma Sobti", "A 60-part blog on smile design by Delhi cosmetic dentist Dr Parul Sharma Sobti, from the basics of a smile to veneers, aligners and facial harmony.", page_blog(posts)),
        ("visit.html", "Book a Smile Consultation in Rajouri Garden | Dr Parul Sobti", "Book a smile consultation with Dr Parul Sharma Sobti at Dr Sobti's Dental Care, Rajouri Garden, New Delhi. Open 7 days, 10 am to 7 pm. WhatsApp +91 80767 77307.", page_visit()),
    ]
    for name, title, desc, body in pages:
        write(out / name, layout(title, desc, body, name, preview_main=(preview and name == "index.html"), path="" if name == "index.html" else name))
    write(out / "veneers.html", layout(
        "Veneers in Delhi: Cost from ₹10,000 per Tooth | Dr Parul Sobti",
        "Porcelain and composite veneers in Rajouri Garden, Delhi, from ₹10,000 per tooth. Smile design and a trial smile before anything is permanent, with Dr Parul Sharma Sobti.",
        page_veneers(), "treatments.html", path="veneers.html", ld=veneers_schema()))
    for pg in PRICE_PAGES:
        write(out / f'{pg["slug"]}.html', layout(pg["title"], pg["desc"], page_price(pg), "treatments.html",
                                                 path=f'{pg["slug"]}.html', ld=page_schema(pg["slug"], pg["name"], pg["faq"])))
    write(out / "videos.html", layout(
        "Smile Makeover & Cosmetic Dentistry Videos, Delhi | Dr Parul Sobti",
        "Videos from Dr Sobti's Dental Care, Rajouri Garden: smile designing, composite veneers, same-day crowns, root canals, laughing gas and children's dentistry.",
        page_videos(), "treatments.html", path="videos.html", ld=videos_schema()))
    write(out / "dentist-rajouri-garden.html", layout(
        "Treatment Prices, Timings and Directions, Rajouri Garden Clinic | Dr Parul Sobti",
        "Starting prices for veneers, whitening, crowns, braces, aligners and root canal at Dr Sobti's Dental Care, above Rajmandir. Open 7 days, 10 am to 7 pm. Parking and directions.",
        page_rajouri(), "visit.html", path="dentist-rajouri-garden.html", ld=rajouri_schema()))
    for p in posts:
        if p["body"]:
            write(out / "blog" / f'{p["slug"]}.html',
                  layout(f'{p["title"]} | Dr Parul Sharma Sobti', post_description(p), page_post(p, posts),
                         "blog.html", root="../", path=f'blog/{p["slug"]}.html', og_type="article", ld=post_schema(p)))
    write_sitemap(out, posts)
    write_llms(out, posts)
    # Google Search Console ownership file. Keep it, or the site loses verification.
    write(out / "google92cb67c4e945410f.html", "google-site-verification: google92cb67c4e945410f.html")
    return posts


def post_description(p):
    """Search snippet for a post: its summary plus who wrote it and where, about 150 characters."""
    tail = " By Dr Parul Sharma Sobti, cosmetic dentist in Rajouri Garden, Delhi."
    return p["summary"] + (tail if len(p["summary"]) + len(tail) <= 165 else "")


def write_sitemap(out, posts):
    """sitemap.xml and robots.txt, so Google finds every new post the day it goes live."""
    today = today_ist().isoformat()
    urls = [(SITE_URL + "/", today)] + [(f"{SITE_URL}/{n}", today) for n in
            ("about.html", "clinic.html", "treatments.html", "veneers.html", "technology.html", "blog.html", "visit.html",
             "dentist-rajouri-garden.html", "videos.html") + tuple(f'{p["slug"]}.html' for p in PRICE_PAGES)]
    urls += [(f'{SITE_URL}/blog/{p["slug"]}.html', p["date"].isoformat()) for p in posts if p["body"]]
    write(out / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")
    ai_bots = ["OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "Perplexity-User", "ClaudeBot",
               "Claude-SearchBot", "Claude-User", "Google-Extended", "Applebot-Extended", "Bingbot"]
    write(out / "robots.txt", "User-agent: *\nAllow: /\n\n# AI search and answer engines: welcome to read and cite this site\n"
          + "".join(f"User-agent: {b}\n" for b in ai_bots) + f"Allow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")


def write_llms(out, posts):
    """llms.txt: a plain fact sheet that AI search tools (ChatGPT, Perplexity, Gemini) can read and quote."""
    prices = "\n".join(f'- {pg["h1"]}: ' + "; ".join(f"{re_tags(i)}: {re_tags(v)}" for i, v in pg["prices"])
                       + f' ({SITE_URL}/{pg["slug"]}.html)' for pg in PRICE_PAGES)
    pages = "\n".join(f"- [{t}]({SITE_URL}/{u})" for t, u in [
        ("Home", ""), ("About Dr Parul Sharma Sobti", "about.html"), ("The clinic", "clinic.html"),
        ("All treatments", "treatments.html"), ("Veneers in Delhi", "veneers.html"), ("Technology", "technology.html"),
        ("Dentist in Rajouri Garden: prices, timings and directions", "dentist-rajouri-garden.html"),
        ("Visit and book", "visit.html"), ("Smile Journal blog", "blog.html"),
        ("Videos: smile makeovers, veneers, same-day crowns, children and nervous patients", "videos.html")]
        + [(pg["h1"], f'{pg["slug"]}.html') for pg in PRICE_PAGES])
    live = "\n".join(f'- [{p["title"]}]({SITE_URL}/blog/{p["slug"]}.html)' for p in posts if p["body"])
    write(out / "llms.txt", f"""# Dr Parul Sharma Sobti, cosmetic dentist in Rajouri Garden, Delhi

> Dr Parul Sharma Sobti (BDS, SR Dental College, Rohtak; member of the Indian Dental Association) is a cosmetic dentist and digital smile designer at {CLINIC}, J 12/26, First Floor, Rajouri Garden, New Delhi 110027. She leads veneers, teeth whitening, smile makeovers, aligners and braces, root canals, crowns and cleanings at the clinic. Implants at the same clinic are done by Dr Pushkar Sobti ({PUSHKAR_URL}/).

## Key facts
- Clinic: {CLINIC}, J 12/26, First Floor, Rajouri Garden, New Delhi 110027, India (above Rajmandir; nearest metro Rajouri Garden, Blue and Pink lines)
- Clinic website: {CLINIC_URL}/ · Google profile: {GOOGLE_PROFILE}
- Timings: {HOURS}, including Sundays
- Call {PHONE}; WhatsApp {WHATSAPP_NO}; {EMAIL}
- Consultation: free first opinion on WhatsApp; in-clinic consultation INR 700
- Veneers from INR 10,000 per tooth; smile makeover priced case by case after a digital smile design
- Languages: English, Hindi. Not on the CGHS panel.
- Profiles: {INSTAGRAM} · {FACEBOOK} · {YOUTUBE}

## Starting prices (November 2026)
{prices}

## Pages
{pages}

## Smile Journal posts
{live}
""")


def export_calendar(posts):
    names = {c[0]: c[1] for c in CHAPTERS}
    with open(ROOT / "blog-calendar.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["post", "publish_date", "chapter", "chapter_name", "title", "summary", "type", "status"])
        for p in posts:
            w.writerow([p["n"], p["date"].isoformat(), p["chapter"], names[p["chapter"]], p["title"], p["summary"],
                        "About Dr Parul" if p["kind"] == "doctor" else "Topic", "Live" if p["body"] else ("Approved" if p["approved"] else "Awaiting approval" if p["written"] else "Planned")])


if __name__ == "__main__":
    posts = build(SITE)
    export_calendar(posts)
    if "--preview" in sys.argv:
        build(Path(sys.argv[sys.argv.index("--preview") + 1]), preview=True)
    print(f"Built {SITE} with {sum(1 for p in posts if p['body'])} live posts of {len(posts)}")
