"""Cosmetic treatment pages. Since 22 Nov 2026 (Dr) this site covers only smile design, cosmetics and veneers;
other treatment pages moved to www.sobtidentalcare.com and redirect there (MOVED in build.py).
Prices (Dr, 22 Nov 2026): only basic starting prices ("from ₹...") already published; never exact costs, no new prices.
Exact cost is given after the patient is examined.

Each page targets one search people in Delhi use, such as "root canal cost in Delhi".
build.py turns every entry into <slug>.html with FAQ and breadcrumb schema.
Fields: slug, title, desc, label, h1, intro, sections [(heading, [paragraph or list of bullets])],
facts [(label, value)], faq [(question, answer)], cta.
"""

PRICE_PAGES = [
    {
        "slug": "smile-makeover-delhi",
        "wa": "Smile makeover",
        "name": "Smile makeover",
        "title": "Smile Makeover in Delhi: Smile Designing | Dr Parul Sobti",
        "desc": "Smile makeover and smile designing in Rajouri Garden, Delhi with Dr Parul Sharma Sobti. See your new smile on your own photos and try it before treatment starts.",
        "label": "Treatments · Smile makeover",
        "h1": "Smile makeover in Delhi",
        "intro": "Smile designing with Dr Parul Sharma Sobti at Dr Sobti's Dental Care, Rajouri Garden. Your new smile is planned on your own photos and scans, and you try it in your mouth before anything permanent is done.",
        "prices": [
            ("Smile makeover", "Planned case by case"),
            ("Veneers, where needed", "From ₹10,000 per tooth"),
            ("In-clinic whitening, where needed", "From ₹8,000 (depends on the case)"),
        ],
        "sections": [
            ("What a smile makeover is", [
                "A smile makeover is not one treatment. It is a plan for the teeth that show when you talk and smile, and it uses only what your teeth need.",
                ["<a href=\"teeth-whitening-cost-delhi.html\">Whitening</a>, when the shape is fine and only the colour bothers you.",
                 "Composite bonding or contouring for chips, worn edges and small gaps.",
                 "Porcelain or composite <a href=\"veneers.html\">veneers</a> when colour, shape and length all need to change.",
                 "Gum shaping when the gum line is uneven or the teeth look short.",
                 "Clear aligners first, when the teeth need to move before anything is added to them."],
                "Dr Parul works on the principle of least invasive first. If whitening and a little bonding will give you the smile you want, she will tell you so before suggesting veneers.",
            ]),
            ("How your smile is designed", [
                ["Photographs, a short video and a 3D scan of your teeth. There are no impression trays.",
                 "Dr Parul designs the new smile on screen, working out the shape, length and proportion of each tooth against your lips and face.",
                 "A mock-up of that design is 3D printed and placed over your own teeth, so you can see it in the mirror and feel it when you speak.",
                 "You ask for changes: longer, shorter, rounder, a shade less white. The design is adjusted until you are happy with it.",
                 "Only then is the final work done. Veneers and crowns are milled in our own lab, on the same floor as the clinic."],
                "Nothing permanent is done to your teeth until you have seen and approved the trial smile.",
            ]),
            ("How long it takes", [
                "It depends on the plan. Whitening is one visit, and bonding usually is too. Porcelain veneers take 2 to 3 visits, and because they are made in the clinic's own lab there is no long wait in between. If aligners are part of the plan, the teeth are moved first and the cosmetic work follows.",
            ]),
            ("Who asks for one", [
                "Most people who ask about a smile makeover have one of a few concerns: gaps, chipped or worn front teeth, teeth that have gone dark or stayed stained after whitening, old fillings that show, or teeth that look uneven in photos.",
                "Teeth and gums need to be healthy first, so any decay or gum problem is treated before the cosmetic work starts.",
            ]),
        ],
        "facts": [("Smile design", "1–2 visits"), ("Trial smile", "1 visit, before any permanent work"),
                  ("Veneers, where needed", "From ₹10,000 per tooth"), ("Dentist", "Dr Parul Sharma Sobti, BDS, Digital Smile Design")],
        "faq": [
            ("What does a smile makeover cost in Delhi?",
             "There is no single price, because a makeover can be whitening and a few bonded edges, or veneers on 8 to 10 teeth. At Dr Sobti's Dental Care in Rajouri Garden, veneers start from ₹10,000 per tooth and in-clinic whitening from ₹8,000. Dr Parul gives you a written estimate after the smile design, before any treatment."),
            ("What is the difference between smile designing and a smile makeover?",
             "Smile designing is the planning: your new smile is worked out on your photos and scans and shown to you as a trial smile. The smile makeover is the treatment that follows, using whitening, bonding, veneers, gum shaping or aligners as the plan needs."),
            ("Can I see my new smile before treatment?",
             "Yes. The design is placed over your own teeth as a mock-up, so you can see and feel it and ask for changes before any permanent work."),
            ("Will my teeth be cut down?",
             "Often very little, and sometimes not at all. Whitening, bonding and contouring leave the tooth almost untouched. Veneers usually need a thin layer of enamel removed. Dr Parul shows you what each option involves before you choose."),
            ("How long does a smile makeover last?",
             "It depends on the materials and on how you look after them. Porcelain keeps its colour and shine for many years. Composite may need polishing or small repairs over time. Whitening fades gradually and can be topped up."),
            ("Do you see smile makeover patients from other parts of Delhi?",
             "Yes. The clinic is in Rajouri Garden, about 1.5 km from Rajouri Garden metro station, and open 7 days from 10 am to 7 pm. Dr Parul sees patients by appointment, so message or call before you travel."),
        ],
        "cta": "Ask about a smile makeover",
    },

    {
        "slug": "teeth-whitening-cost-delhi",
        "wa": "Teeth whitening",
        "name": "Teeth whitening",
        "title": "Teeth Whitening Cost in Delhi: In-Clinic from ₹8,000 | Dr Parul Sobti",
        "desc": "Teeth whitening cost in Delhi: in-clinic whitening from ₹8,000 and take-home kits, planned by cosmetic dentist Dr Parul Sharma Sobti in Rajouri Garden.",
        "label": "Treatments · Teeth whitening",
        "h1": "Teeth whitening cost in Delhi",
        "intro": "In-clinic and take-home whitening with Dr Parul Sharma Sobti at Dr Sobti's Dental Care, Rajouri Garden. In-clinic whitening starts from ₹8,000; the final price depends on your case.",
        "prices": [
            ("In-clinic whitening", "From ₹8,000 (depends on the case)"),
            ("Take-home whitening kit", "Priced after a check-up"),
        ],
        "sections": [
            ("In-clinic or at home", [
                ["In-clinic whitening is done in one visit using professional systems such as Pola Office.",
                 "Take-home whitening uses custom trays and a gentle gel that you wear for about two weeks."],
                "How many shades lighter your teeth get, and how long it lasts, depends on your teeth and habits. Dr Parul will give you a realistic idea at the check-up.",
            ]),
            ("Whitening first", [
                "Dr Parul works on the principle of least invasive first. Whitening is often all a smile needs. If stains or chips don't respond, <a href=\"veneers.html\">veneers</a> are the next step.",
            ]),
        ],
        "facts": [("In-clinic", "From ₹8,000"), ("Take-home", "Priced after a check-up"), ("Visits", "1 visit / 2 weeks at home")],
        "faq": [
            ("How much does teeth whitening cost in Delhi?",
             "At Dr Sobti's Dental Care in Rajouri Garden, in-clinic whitening starts from ₹8,000, depending on your case. Take-home kits are priced after a check-up."),
            ("Where can I get teeth whitening in Delhi on a weekend?",
             "Our Rajouri Garden clinic is open 7 days, 10 am to 7 pm, so a whitening visit can be booked on a Saturday or Sunday. Call 80767 77307."),
            ("How many shades whiter will my teeth get?",
             "It depends on your teeth. Dr Parul will tell you what to expect after looking at them."),
            ("Does whitening work on crowns or fillings?",
             "No, whitening only lightens natural teeth. Crowns, veneers and fillings keep their colour."),
        ],
        "cta": "Book a whitening consultation",
    },

]

RAJOURI_FAQ = [
    ("Where is Dr Sobti's Dental Care in Rajouri Garden?",
     "First Floor, J-12/26, Block J, Rajouri Garden Extension, above Rajmandir and near Geetanjali Salon. It is about 1.5 km from Rajouri Garden metro station."),
    ("What are the clinic timings?",
     "Open 7 days a week, 10 am to 7 pm."),
    ("Is there parking?",
     "Yes, parking is available, and there is a lift to the first floor."),
    ("Which payment methods do you accept?",
     "UPI, cards and cash."),
    ("How do I choose a dentist for cosmetic or long treatments?",
     "Look at reviews, ask who will actually treat you, and ask for the price in writing before you start. At our clinic you see the same two doctors every visit, and the full cost is given in writing before treatment starts."),
    ("Do you see patients from other parts of West Delhi?",
     "Yes, most of our patients come from nearby West Delhi areas like Tagore Garden, Subhash Nagar, Tilak Nagar, Janakpuri and Punjabi Bagh. We are open 7 days and about 1.5 km from Rajouri Garden metro."),
]
