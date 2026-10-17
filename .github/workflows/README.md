# BlinkTask — personal portfolio & digital services

Custom-coded, static-first portfolio for Akhilesh Kumar. Built with plain HTML, CSS and JavaScript to keep the site lightweight and avoid paid themes, frameworks, font APIs, databases and API keys.

## Preview locally

Open `index.html` directly, or run a local server from this folder:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Publish to GitHub Pages (free for this static site)

1. Upload the contents of this project to the root of the `main` branch of [`iamalrboy/blinktask`](https://github.com/iamalrboy/blinktask).
2. In GitHub, open **Settings → Pages** and choose **GitHub Actions** as the build and deployment source.
3. The included `.github/workflows/pages.yml` deploys the static site when a commit is pushed to `main` or when manually run from the Actions tab.
4. Check **Actions** for a successful deployment. The preview URL appears in the Pages settings and deployment job.
5. Connect `blinktask.in` only after the GitHub Pages preview works. Add the custom domain in Pages settings, then configure the exact DNS records GitHub shows at your domain provider. Do not guess or overwrite existing DNS records. Enable HTTPS when it becomes available.

## Site pages

- `index.html` — homepage, services, work, about, process and contact
- `services.html` — service overview
- `resume.html` — résumé draft with print/save-to-PDF option
- `works/` — four evidence-conscious project/design case-study drafts
- `privacy.html`, `accessibility.html` — draft supporting pages
- `robots.txt`, `sitemap.xml`, `.nojekyll` — basic publishing and discovery files

## Before public launch

- Confirm public name, education/course wording and contact email.
- Replace concept illustrations with real project evidence where available.
- Verify project status, personal contribution, certificates, dates and claims.
- Remove services not ready to deliver.
- Review privacy/accessibility copy against actual hosting and data practices.
- Test mobile layout, keyboard navigation, reduced motion and major browsers.
- Once the custom domain is connected, update `sitemap.xml` and canonical/social metadata with the final production URLs.

## Scope and limitations

This is a static frontend, not a deployed site or full platform. There is no backend, secure admin, booking database, contact-form endpoint, email-sending service, analytics or AI assistant. The contact CTA uses `mailto:` and depends on the visitor's email app. Do not present planned features as live. The project visuals are illustrative concepts, not evidence of completed products or client work.
