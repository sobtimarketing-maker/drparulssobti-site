# The Smile Journal: a 60-post story, published every alternate day.
# Order matters: each post builds on the one before it, basic to advanced.
# Edit titles or summaries here, then run `python3 build.py`.

START_DATE = "2026-10-21"  # first post; every later post is 2 days after the previous one

CHAPTERS = [
    ("I", "The Language of a Smile", "Foundations: what a smile is made of and how a dentist reads it."),
    ("II", "Small Changes, Big Difference", "Gentle cosmetic treatments that brighten and refine without heavy work."),
    ("III", "Porcelain and Precision", "Veneers, crowns and replacing teeth so they look like they grew there."),
    ("IV", "The Frame: Gums, Alignment and Bite", "Why gums, tooth position and the bite decide how a smile looks."),
    ("V", "The Digital Smile", "The technology that lets us plan, preview and place work precisely."),
    ("VI", "Beyond Teeth: Facial Harmony", "Bringing lips, skin and facial proportions into the design."),
]

# (chapter, title, one-line summary, kind)  kind: "topic" or "doctor" (posts about Dr Parul)
POSTS = [
    # Chapter I
    ("I", "What is smile designing, really?", "A plain introduction to planning a smile around a face, not just fixing teeth.", "topic"),
    ("I", "Meet Dr Parul Sharma Sobti", "Why smiles became her life's work, and how she approaches every patient.", "doctor"),
    ("I", "The anatomy of a smile", "Teeth, gums, lips and face: the four layers every smile design considers.", "topic"),
    ("I", "The golden proportion and your front teeth", "Why the widths of your front six teeth follow a pattern, and when to ignore it.", "topic"),
    ("I", "Smile line, lip line and buccal corridors", "The words your dentist uses when they study your smile, explained.", "topic"),
    ("I", "Tooth colour explained", "Shade guides, value, chroma and translucency, and why white is not one colour.", "topic"),
    ("I", "Why teeth stain", "Tea, coffee, tobacco, age, medicines and genetics: surface stains versus deep ones.", "topic"),
    ("I", "Healthy first", "Why every cosmetic plan starts with clean teeth and healthy gums.", "topic"),
    ("I", "Your first smile consultation", "What happens, step by step, from photographs to the treatment plan.", "topic"),
    ("I", "A day in Dr Parul's clinic", "Behind the scenes of a working day at the clinic.", "doctor"),
    # Chapter II
    ("II", "Scaling and polishing", "The simplest way to brighten a smile, and why it comes before anything else.", "topic"),
    ("II", "Teeth whitening: in-clinic or at home?", "How each method works, how long it takes and what results to expect.", "topic"),
    ("II", "Does whitening damage enamel?", "Sensitivity, safety and the myths around bleaching, answered.", "topic"),
    ("II", "Composite bonding", "Repairing chips, worn edges and small gaps in a single visit.", "topic"),
    ("II", "Enamel contouring", "Small reshaping that evens out edges without drilling deep.", "topic"),
    ("II", "Closing small gaps without braces", "Options for a diastema and when braces are still the better choice.", "topic"),
    ("II", "White spots and fluorosis", "Why they appear and how micro-abrasion, infiltration and bonding help.", "topic"),
    ("II", "Replacing old silver fillings", "Tooth-coloured fillings and when replacement is worth it.", "topic"),
    ("II", "How long do cosmetic results last?", "A realistic care guide for whitening, bonding and polish.", "topic"),
    ("II", "Conservative first: Dr Parul's philosophy", "Why she always tries the least invasive option before the bigger ones.", "doctor"),
    # Chapter III
    ("III", "Veneers 101", "What veneers are, what they fix and who they suit.", "topic"),
    ("III", "Porcelain or composite veneers?", "An honest comparison of cost, look, durability and repair.", "topic"),
    ("III", "No-prep and minimal-prep veneers", "When veneers can be placed with little or no tooth reduction.", "topic"),
    ("III", "The veneer journey", "From wax-up and trial smile to final bonding, visit by visit.", "topic"),
    ("III", "Choosing your veneer shade", "Natural, bright or Hollywood white, and how to decide.", "topic"),
    ("III", "Crowns for aesthetics", "Zirconia, lithium disilicate and metal-ceramic crowns explained.", "topic"),
    ("III", "Metal-free dentistry", "Why all-ceramic work looks more natural, especially near the gums.", "topic"),
    ("III", "Replacing a missing front tooth", "Implant, bridge or bonded bridge: how to choose.", "topic"),
    ("III", "Caring for veneers and crowns", "Daily habits, night guards and check-ups that protect your investment.", "topic"),
    ("III", "Case story: a veneer transformation", "One patient's journey from first visit to final smile, with their consent.", "doctor"),
    # Chapter IV
    ("IV", "Pink aesthetics", "Why the gums matter as much as the teeth in a beautiful smile.", "topic"),
    ("IV", "The gummy smile", "What causes it and the range of treatments available.", "topic"),
    ("IV", "Laser gum contouring", "Reshaping the gum line gently, with quick healing.", "topic"),
    ("IV", "Uneven gum lines and crown lengthening", "Making short teeth look their true length.", "topic"),
    ("IV", "Clear aligners", "How invisible orthodontics moves teeth, and what wearing them is like.", "topic"),
    ("IV", "Aligners or braces for adults?", "Comfort, speed, cost and which cases suit each.", "topic"),
    ("IV", "Your bite and your smile", "How jaw alignment and tooth wear change the way a smile looks.", "topic"),
    ("IV", "Black triangles between teeth", "Why they appear after gum recession and how to fill them.", "topic"),
    ("IV", "Combining treatments", "When alignment, gum work and veneers are planned as one sequence.", "topic"),
    ("IV", "How Dr Parul plans a smile makeover", "Her step-by-step planning method for multi-stage cases.", "doctor"),
    # Chapter V
    ("V", "Digital Smile Design", "Seeing your new smile on screen before any treatment begins.", "topic"),
    ("V", "Smile photography and video", "Why we photograph and film your smile, and what we measure.", "topic"),
    ("V", "Intraoral scanning", "A 3D scan in minutes in place of messy impression trays.", "topic"),
    ("V", "Mock-ups and 3D printing", "Test-driving your new smile in your own mouth.", "topic"),
    ("V", "3D imaging with CBCT", "How 3D X-rays make implant and bone planning precise.", "topic"),
    ("V", "Dental microscopes", "Magnification that makes fine margins and root canals more accurate.", "topic"),
    ("V", "Lasers in cosmetic dentistry", "Where lasers help, from gums to whitening, and where they do not.", "topic"),
    ("V", "CAD/CAM restorations", "Designing and milling crowns and veneers by computer.", "topic"),
    ("V", "Guided implant surgery", "Planning implants digitally and placing them through a surgical guide.", "topic"),
    ("V", "Inside our technology suite", "A tour of the equipment at the clinic and why Dr Parul chose each piece.", "doctor"),
    # Chapter VI
    ("VI", "Dento-facial aesthetics", "Why the face and the smile are designed together.", "topic"),
    ("VI", "Lips and the smile", "Lip proportions, lip support and how teeth shape the lips.", "topic"),
    ("VI", "Anti-wrinkle injections", "What dentists know about the muscles of the face, and how it helps.", "topic"),
    ("VI", "Dermal fillers for lips and smile lines", "Restoring volume and balance around the mouth.", "topic"),
    ("VI", "Treating a gummy smile with injections", "A non-surgical option for an over-active upper lip.", "topic"),
    ("VI", "Facial profile and full-mouth rehabilitation", "How rebuilding worn teeth can restore the lower face.", "topic"),
    ("VI", "Ageing around the mouth", "Volume loss, thinning lips and what can be done at each stage.", "topic"),
    ("VI", "Safety in facial aesthetics", "Training, products and setting realistic expectations.", "topic"),
    ("VI", "The complete makeover", "Planning teeth, gums, lips and face as one design.", "topic"),
    ("VI", "Dr Parul's vision for aesthetic dentistry", "Where the field is heading and what it means for her patients.", "doctor"),
]
