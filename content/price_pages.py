"""Cosmetic treatment pages. Since 22 Nov 2026 (Dr) this site covers only smile design, cosmetics and veneers;
other treatment pages moved to www.sobtidentalcare.com and redirect there (MOVED in build.py).
No prices (as live on 22 Nov 2026): the front desk gives the cost on WhatsApp or a call after checking with the doctor.

Each page targets one search people in Delhi use, such as "root canal cost in Delhi".
build.py turns every entry into <slug>.html with FAQ and breadcrumb schema.
Fields: slug, title, desc, label, h1, intro, sections [(heading, [paragraph or list of bullets])],
facts [(label, value)], faq [(question, answer)], cta.
"""

PRICE_PAGES = [
    {
        "slug": "teeth-whitening-cost-delhi",
        "wa": "Teeth whitening",
        "name": "Teeth whitening",
        "title": "Teeth Whitening Cost in Delhi: In-Clinic and Take-Home | Dr Parul Sobti",
        "desc": "In-clinic and take-home teeth whitening planned by cosmetic dentist Dr Parul Sharma Sobti in Rajouri Garden, Delhi. Message or call to ask the cost for your teeth.",
        "label": "Treatments · Teeth whitening",
        "h1": "Teeth whitening cost in Delhi",
        "intro": "In-clinic and take-home whitening with Dr Parul Sharma Sobti at Dr Sobti's Dental Care, Rajouri Garden. In-clinic whitening is done in one visit.",
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
        "facts": [("In-clinic", "1 visit"), ("Take-home", "About 2 weeks"), ("Systems", "Pola Office and others")],
        "faq": [
            ("How much does teeth whitening cost in Delhi?",
             "It depends on your teeth and which method suits you. Send us a WhatsApp message on 80767 77307 or call 87449 85976. The front desk will check with the doctor and tell you the cost for your case."),
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
