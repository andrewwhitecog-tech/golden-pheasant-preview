# Golden Pheasant Painting preview

This folder is the standalone static preview for Golden Pheasant Painting. It is intentionally
dependency-free: the homepage, estimator, service story, gallery placeholders, and contact surface
all live in index.html, with the permissioned brand image in logo.png.

## Open it

Double-click index.html, or serve this folder locally:

    C:\Python314\python.exe -m http.server 8765

Then open http://127.0.0.1:8765/ in a browser.

The current public preview is:

    https://andrewwhitecog-tech.github.io/golden-pheasant-preview/

That preview URL is the current canonical URL in the HTML, sitemap, robots file, and social-card
metadata. Change all four together if the site later moves to a verified business domain.

## Current status

- Responsive single-page portfolio concept separating cleaning-only inquiries from future licensed
  painting and construction services.
- Creator case study, brand story, and compliance-first design principles.
- Six clearly labeled gallery placeholders; no stock photography is presented as completed work.
- Scope-builder interface demo runs entirely in the browser, produces no price, and transmits no
  customer data.
- The cleaning-only inquiry form uses the computer's email application; it has no hidden database
  or tracker.
- Search, Open Graph, Twitter-card, favicon, web-manifest, robots, sitemap, and truthful
  CreativeWork metadata are included without an address, hours, license number, ratings, reviews,
  or testimonials.
- The PORTFOLIO CONCEPT ribbon stays visible until licensing, insurance, domain, contact, and
  pricing claims are re-verified for launch.

## Verify it

Run the dependency-free static checks and an ephemeral local HTTP smoke test:

    C:\Python314\python.exe tools\verify_static_site.py --http-smoke

The verifier checks public root assets, internal links and fragments, JSON-LD, manifest JSON,
sitemap XML, the canonical URL, clickable phone/email actions, the noindex state, and the required
concept/no-license/mailto disclosures. It also rejects stale contractor claims such as
"Insured + Bonded," "CCB # pending," and HousePainter schema. It does not contact customers or
submit the placeholder form.

The business contact details already in the preview came from the existing permissioned project
history. Do not add a home address or personal-only credentials to the public site.

## Add project photography

1. Obtain the customer's permission to publish each project.
2. Remove faces, house numbers, license plates, mail, and location metadata.
3. Export a web-sized JPG or WebP under 1600 pixels on the long edge.
4. Save it in a new assets/projects folder and replace one gallery placeholder with a figure,
   image, and honest caption.
5. Keep before-and-after images paired and label any color correction.

## Before publishing

- Confirm the business name, public phone, public email, service area, and legal entity.
- Replace all pending licensing language with verified wording or remove it.
- Approve estimator ranges and the assessment policy before restoring any public pricing tool.
- Connect the form to a privacy-respecting provider or keep the explicit email handoff.
- Test keyboard navigation, mobile layout, estimator behavior, and every link.
- Replace the PORTFOLIO CONCEPT state only after every launch gate in
  BUSINESS_LAUNCH_READINESS.md is independently verified.

BUSINESS_LAUNCH_READINESS.md is the dated operator checklist for moving from the current concept
to a real painting contractor business. It separates safe preparation from paid, account, and
public-launch actions that require owner confirmation.

EMAIL_SETUP_RUNBOOK.md is an unpublished operator note for the future business domain. Nothing in
this folder requires that domain to exist, and this handoff does not publish or deploy the site.
