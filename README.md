# Dr Parul Sharma Sobti website

Static HTML/CSS site for drparulssobti.com, hosted free on GitHub Pages. `.github/workflows/deploy.yml` runs `python3 build.py` and publishes `site/` on every push to main and once a day at 00:10 India time, so each post goes live on its date without anyone pushing. (`netlify.toml` is the old Netlify setup and can be deleted once the domain points to GitHub Pages.)
A blog post goes live once its file exists in `content/posts/`, its number is in `content/approved.txt` (Dr Parul approves each post first), and its date in `content/blog_plan.py` has arrived (India time). Set `BUILD_DATE=YYYY-MM-DD` to preview a future date.

- `content/blog_plan.py`: the 60-post Smile Journal sequence (6 chapters, basic to advanced), start date and order.
- `content/posts/NN.html`: written post bodies. A post appears on the site once its file exists.
- `assets/style.css`: the design.
- `build.py`: run `python3 build.py` to regenerate `site/` and `blog-calendar.csv` locally.
- `blog-calendar.csv`: every post with its publish date (every alternate day from 21 Oct 2026).

Yellow ✎ chips on the site mark details the clinic still has to confirm (address, hours, phone, qualifications, photos, equipment).
Sister-site links (clinic site, Dr Pushkar Sobti) are set by `CLINIC_URL` and `PUSHKAR_URL` in `build.py`.
