# Golden Pheasant email — runbook (waiting on domain purchase)

**Target address:** andrew@goldenpheasantpc.com (already on the card back + website)
**Domain to buy:** goldenpheasantpc.com (verified available 2026-07-15)

## Step 1 — Andre buys the domain (~$10-12/yr)
Cheapest/simplest registrars: Cloudflare Registrar (at-cost, requires free CF account first),
Porkbun, or DreamHost (existing account, panel.dreamhost.com → Domains → Register).
**Buying it at Cloudflare directly is best** — Step 2 then needs zero nameserver changes.

## Step 2 — Free email forwarding (Cloudflare Email Routing)
1. Cloudflare dashboard → the goldenpheasantpc.com zone → **Email → Email Routing → Enable**.
2. Create address `andrew@goldenpheasantpc.com` → forward to `andrew.white.cog@gmail.com`.
3. Verify the Gmail address when the confirmation mail arrives.
4. Cloudflare auto-adds the MX + SPF records. Done — inbound works.

## Step 3 — Send AS the business address from Gmail
1. Gmail → Settings → Accounts → "Send mail as" → Add another email address.
2. Name: Golden Pheasant Property Care; Email: andrew@goldenpheasantpc.com; untick "alias".
3. SMTP server: use Gmail's own (smtp.gmail.com, port 587, andrew.white.cog@gmail.com +
   an app password — GMAIL_APP_PASSWORD pattern already used by JOB_SEARCH tools).
4. Confirm the verification code (arrives via the forwarding set up in Step 2).
5. Optional: set as default From for replies.

## Step 4 — After email is live
- Update DNS: point apex/www at the preview site (GitHub Pages: A 185.199.108-111.153 + CNAME
  andrewwhitecog-tech.github.io) so goldenpheasantpc.com serves the real site.
- Re-verify the card back + site (already show the address, nothing to change).
- Add DKIM later if deliverability matters (Cloudflare Email Routing handles inbound only;
  outbound goes through Gmail's SMTP which is fine for a solo operator).
