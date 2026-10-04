#!/usr/bin/env python3
"""One-off generator for the four static Grid9 pages. Output is plain HTML
(no build step needed on the server); this script is just a convenience so
the shared header/footer isn't copy-pasted by hand four times. Safe to delete
after the pages are generated, or keep to regenerate after edits."""
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "support@hagedornworks.se"
UPDATED = "4 October 2026"

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Grid9 Sudoku</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="{css}">
</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="brand" href="{home}">Grid9 Sudoku</a>
    <nav class="site">
      <a href="{p}privacy/"{c_privacy}>Privacy</a>
      <a href="{p}terms/"{c_terms}>Terms</a>
      <a href="{p}support/"{c_support}>Support</a>
    </nav>
  </div>
</header>
<main>
<div class="wrap">
{body}
</div>
</main>
<footer class="site">
  <div class="wrap">
    <p>&copy; 2026 Joachim Hagedorn &middot; <a href="mailto:{email}">{email}</a></p>
  </div>
</footer>
</body>
</html>
"""


def page(path, key, title, description, body, depth):
    # depth = number of directory levels below the site root (landing=1, subpages=2)
    prefix = "./" if depth == 1 else "../"
    html = TEMPLATE.format(
        title=title,
        description=description,
        css="../" * depth + "assets/site.css",
        home="./" if depth == 1 else "../",
        p=prefix,
        c_privacy=' aria-current="page"' if key == "privacy" else "",
        c_terms=' aria-current="page"' if key == "terms" else "",
        c_support=' aria-current="page"' if key == "support" else "",
        body=body,
        email=EMAIL,
    )
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


# ---------------------------------------------------------------- landing
LANDING = f"""
<h1>Grid9 Sudoku</h1>
<p class="meta">A sudoku app that teaches you the techniques, not just the grid.</p>
<p>Grid9 is developed by Joachim Hagedorn. Reading about a technique is always free. Grid9 Premium unlocks practising techniques on real puzzles, the full step-by-step hint walkthroughs, and entering your own puzzles.</p>
<div class="card">
  <p><a href="privacy/">Privacy Policy</a></p>
  <p><a href="terms/">Terms of Use</a></p>
  <p><a href="support/">Support</a></p>
</div>
"""

# ---------------------------------------------------------------- privacy
PRIVACY = f"""
<h1>Privacy Policy</h1>
<p class="meta">Grid9 Sudoku &middot; Last updated {UPDATED}</p>

<div class="card">
  <p><strong>In short:</strong> Grid9 has no accounts, no advertising and no analytics or tracking. Your puzzle progress and settings stay on your device. The only information that leaves your device relates to buying and verifying a Grid9 Premium subscription, and is handled by Apple and RevenueCat.</p>
</div>

<h2>1. Who is responsible</h2>
<p>The controller of personal data described in this policy is:</p>
<p>Joachim Hagedorn<br>Sweden<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>

<h2>2. What stays on your device</h2>
<p>Puzzle progress, statistics, your own notes and candidates, the theme you chose and other app settings are stored locally on your device by the app. This information is not sent to me or to any server I operate. If you delete the app, this information is deleted with it.</p>

<h2>3. What is not collected</h2>
<ul>
  <li>Grid9 has no user accounts or log-in, and I do not ask for your name, e-mail address or phone number in the app.</li>
  <li>Grid9 contains no advertising and no third-party analytics or tracking tools.</li>
  <li>Grid9 does not use the advertising identifier (IDFA) and does not track you across other companies' apps or websites.</li>
</ul>
<p>This describes the app as of the date above. If this changes, this policy will be updated before the change is released.</p>

<h2>4. Subscriptions: Apple and RevenueCat</h2>
<p>Grid9 Premium is an auto-renewing subscription. Two third parties are involved:</p>
<ul>
  <li><strong>Apple</strong> processes the payment, manages the subscription and any free trial, and issues the receipt. I never receive your card or payment details. Apple's handling of your data is described in <a href="https://www.apple.com/legal/privacy/">Apple's Privacy Policy</a>.</li>
  <li><strong>RevenueCat, Inc.</strong> provides the service that verifies Apple's purchase information and tells the app whether your subscription is active. RevenueCat acts on my behalf as a data processor. It receives an anonymous identifier generated for your installation, the purchase and subscription information from Apple (for example which product, and when it starts and ends), and technical information needed to provide the service, such as IP address (used to determine your country), device type, operating system version, app version and language settings. See <a href="https://www.revenuecat.com/privacy">RevenueCat's Privacy Policy</a> for details, including how it handles transfers of data outside the EU/EEA.</li>
</ul>
<p>Neither Apple nor RevenueCat is given your puzzle progress or in-app activity by the app, and I do not sell personal data.</p>

<h2>5. Why this data is used, and on what legal basis</h2>
<table>
  <tr><th>Purpose</th><th>Legal basis (GDPR)</th></tr>
  <tr><td>Verifying that you have an active subscription and unlocking Premium features</td><td>Performance of the contract with you (Art. 6(1)(b))</td></tr>
  <tr><td>Keeping the subscription service secure and preventing misuse, and answering support requests</td><td>Legitimate interest (Art. 6(1)(f))</td></tr>
</table>

<h2>6. How long data is kept</h2>
<p>Data stored in the app stays on your device until you delete it or the app. Purchase and subscription records held by RevenueCat are kept for as long as needed to provide the service and to meet legal obligations, such as accounting rules. E-mail you send to support is kept for as long as needed to handle your request.</p>

<h2>7. Children</h2>
<p>Grid9 is not directed at children under 13, and I do not knowingly collect personal data from them.</p>

<h2>8. Your rights</h2>
<p>Under the GDPR you can request access to, correction of, or deletion of personal data about you, ask me to restrict its use or object to it, and request a copy in a portable format. Because the app has no accounts, I may need some information from you, such as your anonymous App User ID or purchase details, to find the right records. To use your rights, e-mail <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p>You also have the right to lodge a complaint with the Swedish supervisory authority, Integritetsskyddsmyndigheten (IMY), <a href="https://www.imy.se">imy.se</a>, or with the authority in your own country.</p>

<h2>9. Changes to this policy</h2>
<p>If this policy changes, the new version is published on this page with a new "last updated" date.</p>

<h2>10. Contact</h2>
<p>Questions about privacy: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
"""

# ---------------------------------------------------------------- terms
TERMS = f"""
<h1>Terms of Use</h1>
<p class="meta">Grid9 Sudoku &middot; Last updated {UPDATED}</p>

<div class="card">
  <p>These terms apply between you and Joachim Hagedorn ("I", "me"), the developer of Grid9 Sudoku ("the app"). In addition, <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Apple's Standard License Agreement (EULA)</a> applies to your use of the app. If the two conflict, the mandatory consumer rights described in section 9 prevail.</p>
</div>

<h2>1. The app</h2>
<p>Grid9 is a sudoku app that teaches solving techniques. Reading the explanation of any technique, playing puzzles, using candidates and auto-fill, and viewing statistics are free. Some features require a Grid9 Premium subscription (section 2).</p>

<h2>2. Grid9 Premium subscription</h2>
<p>Grid9 Premium unlocks:</p>
<ul>
  <li>practising every technique on real puzzles,</li>
  <li>the full hint walkthroughs (Where, Which cell, Why, Apply) and the step-by-step mode,</li>
  <li>entering and solving your own puzzles.</li>
</ul>

<table>
  <tr><th>Subscription</th><th>Length</th><th>Price (Sweden)</th></tr>
  <tr><td>Grid9 Premium Monthly</td><td>1 month</td><td>39 SEK</td></tr>
  <tr><td>Grid9 Premium Yearly</td><td>1 year</td><td>249 SEK</td></tr>
</table>
<p>The price you pay in other countries is shown in the App Store before you confirm the purchase, and may include local taxes.</p>

<h3>Free trial</h3>
<p>New subscribers who are eligible get a 14-day free trial. Apple decides eligibility based on your Apple ID. You can cancel during the trial and will not be charged. Any unused part of a free trial is forfeited when you buy a subscription.</p>

<h3>Payment and renewal</h3>
<ul>
  <li>Payment is charged to your Apple ID account at confirmation of purchase, or when the free trial ends.</li>
  <li>The subscription renews automatically for the same length unless you cancel at least 24 hours before the end of the current period.</li>
  <li>Your account is charged for renewal within 24 hours before the end of the current period.</li>
</ul>

<h3>Cancelling and managing</h3>
<p>You manage and cancel your subscription in your device's settings: <em>Settings &rarr; your name &rarr; Subscriptions &rarr; Grid9</em>. Cancelling is not done inside the app, and deleting the app does not cancel the subscription. After cancelling you keep Premium until the end of the period you have already paid for.</p>

<h3>Refunds and billing problems</h3>
<p>Payments and refunds are handled by Apple. To request a refund, use <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>. I cannot issue refunds for App Store purchases myself.</p>

<h3>Restoring a purchase</h3>
<p>If you reinstall the app or use a new device with the same Apple ID, choose <em>Restore purchases</em> in the Premium screen to get your subscription back.</p>

<h2>3. Licence</h2>
<p>You get a personal, non-exclusive, non-transferable licence to use the app on devices you own or control, in accordance with these terms and Apple's EULA. The app, its code, puzzle collection, texts, diagrams and the Grid9 name and logo remain my property. You may not copy, modify, reverse engineer or redistribute them, except as the law allows.</p>

<h2>4. Acceptable use</h2>
<p>Do not misuse the app, try to bypass the subscription, or interfere with its operation.</p>

<h2>5. Availability and changes</h2>
<p>I work to keep the app working and correct, but I do not promise that it will always be available or free from errors. I may update, change or discontinue features. Where a change significantly affects what you have paid for, I will tell you in good time.</p>

<h2>6. Your puzzle data</h2>
<p>Puzzle progress and settings are stored on your device (see the <a href="../privacy/">Privacy Policy</a>). Deleting the app deletes this data, and I cannot restore it for you.</p>

<h2>7. Disclaimer and limitation of liability</h2>
<p>The app is provided "as is". To the extent permitted by law, I am not liable for indirect or consequential loss, such as lost data or lost profit. Nothing in these terms limits liability that cannot be limited by law, including liability for intent or gross negligence.</p>

<h2>8. Changes to these terms</h2>
<p>I may update these terms. The current version is always on this page with its "last updated" date. For changes to the subscription terms, Apple's rules for price and term changes also apply.</p>

<h2>9. Consumer rights and governing law</h2>
<p>Swedish law applies. If you are a consumer in the EU/EEA, you keep the mandatory consumer rights of the country where you live, and nothing in these terms takes them away.</p>

<h2>10. Contact</h2>
<p>Joachim Hagedorn<br>Sweden<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
"""

# ---------------------------------------------------------------- support
SUPPORT = f"""
<h1>Support</h1>
<p class="meta">Grid9 Sudoku</p>

<div class="card">
  <p>Questions, problems or feedback? E-mail <a href="mailto:{EMAIL}">{EMAIL}</a>. I usually reply within 2 working days.</p>
  <p>If you are reporting a problem, it helps to include your device model, iOS version and the app version (shown in the App Store listing or in TestFlight).</p>
</div>

<h2>Frequently asked questions</h2>

<h3>How do I cancel my subscription?</h3>
<p>Open <em>Settings &rarr; your name &rarr; Subscriptions &rarr; Grid9</em> on your iPhone or iPad and choose <em>Cancel Subscription</em>. Cancelling is done in iOS settings, not in the app. You keep Premium until the end of the period you have paid for.</p>

<h3>I was charged but the app does not show Premium</h3>
<p>Open the Premium screen and tap <em>Restore purchases</em>. If that does not help, e-mail me and I will look into it.</p>

<h3>I reinstalled the app or got a new phone</h3>
<p>Tap <em>Restore purchases</em> to get Premium back. Puzzle progress and statistics are stored only on the device and cannot be transferred automatically, because Grid9 has no accounts.</p>

<h3>I want a refund</h3>
<p>Refunds for App Store purchases are handled by Apple: <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</p>

<h3>What data do you keep about me?</h3>
<p>Almost none, since there are no accounts and no analytics. See the <a href="../privacy/">Privacy Policy</a>. To ask about or delete data tied to your subscription, e-mail me.</p>

<h3>I found a puzzle that seems wrong, or a hint that doesn't make sense</h3>
<p>Please e-mail me with a short description, and if possible a screenshot. Corrections to the hint explanations are very welcome.</p>

<h2>More</h2>
<p><a href="../privacy/">Privacy Policy</a> &middot; <a href="../terms/">Terms of Use</a></p>
"""

page("grid9/index.html", "home", "Grid9 Sudoku", "Grid9 Sudoku — a sudoku app that teaches the techniques.", LANDING, 1)
page("grid9/privacy/index.html", "privacy", "Privacy Policy", "How Grid9 Sudoku handles your data.", PRIVACY, 2)
page("grid9/terms/index.html", "terms", "Terms of Use", "Terms of use and subscription terms for Grid9 Sudoku.", TERMS, 2)
page("grid9/support/index.html", "support", "Support", "Support and frequently asked questions for Grid9 Sudoku.", SUPPORT, 2)

# ------------------------------------------------- site root + Pages files
ROOT_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hagedorn Works</title>
<meta name="description" content="Apps by Joachim Hagedorn.">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="brand" href="./">Hagedorn Works</a>
  </div>
</header>
<main>
<div class="wrap">
<h1>Hagedorn Works</h1>
<p class="meta">Apps by Joachim Hagedorn.</p>
<div class="card">
  <p><a href="grid9/">Grid9 Sudoku</a> &mdash; a sudoku app that teaches you the techniques, not just the grid.</p>
</div>
</div>
</main>
<footer class="site">
  <div class="wrap">
    <p>&copy; 2026 Joachim Hagedorn &middot; <a href="mailto:%s">%s</a></p>
  </div>
</footer>
</body>
</html>
""" % (EMAIL, EMAIL)

(ROOT / "index.html").write_text(ROOT_PAGE, encoding="utf-8")
(ROOT / "CNAME").write_text("hagedornworks.se\n", encoding="utf-8")
(ROOT / ".nojekyll").write_text("", encoding="utf-8")
print("wrote index.html, CNAME, .nojekyll")
