#!/usr/bin/env python3
"""Generator for the static Grid9 pages (legal pages + marketing pages). Output is plain HTML
(no build step needed on the server); this script is just a convenience so
the shared header/footer isn't copy-pasted by hand four times. Safe to delete
after the pages are generated, or keep to regenerate after edits."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "support@hagedornworks.se"
UPDATED = "12 October 2026"

APP = "Grid9 Sudoku"   # app name is not final: change here only

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<link rel="stylesheet" href="{css}">
</head>
<body class="{body_class}">
<header class="site">
  <div class="wrap">
    <a class="brand" href="{home}" aria-label="Grid9 Sudoku, home"><span class="wm" aria-hidden="true">GRID<b>9</b></span><span class="brand-sub" aria-hidden="true">Sudoku</span></a>
    <nav class="site">
      <a href="{p}how-it-works/"{c_how}>How it works</a>
      <a href="{p}learn/"{c_learn}>Learn</a>
      <a href="{p}features/"{c_features}>Features</a>
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
    <p>&copy; 2026 Joachim Hagedorn &middot; <a href="{p}privacy/"{c_privacy}>Privacy</a> &middot; <a href="{p}terms/"{c_terms}>Terms</a> &middot; <a href="mailto:{email}">{email}</a></p>
  </div>
</footer>
</body>
</html>
"""


# --- media helpers ---------------------------------------------------------
# A page asks for an image/loop by name. If assets/img/<name>.(webp|png|jpg)
# (or assets/video/<name>.mp4) exists it is used, otherwise a visible
# placeholder is rendered, so the site can be built before the media exists.
# assets/img/README.md lists every name the pages currently ask for.
REQUESTED_MEDIA = []


def _find(kind_dir, name, exts):
    for e in exts:
        f = ROOT / "assets" / kind_dir / (name + "." + e)
        if f.exists():
            return f.name
    return None


def shot(depth, name, alt, caption=""):
    REQUESTED_MEDIA.append(("image", name, alt))
    base = "../" * depth + "assets/img/"
    found = _find("img", name, ("webp", "png", "jpg"))
    full = _find("img", name + "-full", ("webp", "png", "jpg"))
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    if found:
        img = f'<img src="{base}{found}" alt="{alt}" loading="lazy">'
        if full:
            img = f'<a class="zoom" href="{base}{full}" target="_blank" rel="noopener" title="Click to enlarge">{img}</a>'
            cap = f"<figcaption>{caption} <span class=\"zoomhint\">Click to enlarge.</span></figcaption>" if caption else cap
        return f'<figure class="shot">{img}{cap}</figure>'
    return (f'<figure class="shot ph"><div class="ph-inner"><span>Screenshot</span>'
            f'<b>{name}</b><small>{alt}</small></div>{cap}</figure>')


def detail(depth, name, alt, caption=""):
    """Close-up crop with yellow rings, shown in the text column; click to open full size."""
    REQUESTED_MEDIA.append(("image", name, alt))
    base = "../" * depth + "assets/img/"
    found = _find("img", name, ("webp", "png", "jpg"))
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    if not found:
        return (f'<figure class="shot ph detail"><div class="ph-inner"><span>Close-up</span>'
                f'<b>{name}</b><small>{alt}</small></div>{cap}</figure>')
    return (f'<figure class="detail"><a class="zoom" href="{base}{found}" target="_blank" rel="noopener" title="Click to enlarge">'
            f'<img src="{base}{found}" alt="{alt}" loading="lazy"></a>{cap}</figure>')


def loop(depth, name, alt, caption=""):
    REQUESTED_MEDIA.append(("video", name, alt))
    base = "../" * depth + "assets/video/"
    found = _find("video", name, ("mp4",))
    poster = _find("img", name, ("webp", "png", "jpg"))
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    if found:
        pst = f' poster="{"../" * depth}assets/img/{poster}"' if poster else ""
        return (f'<figure class="shot"><video autoplay muted loop playsinline preload="metadata"{pst} '
                f'aria-label="{alt}"><source src="{base}{found}" type="video/mp4"></video>{cap}</figure>')
    return (f'<figure class="shot ph"><div class="ph-inner"><span>Short screen recording</span>'
            f'<b>{name}</b><small>{alt}</small></div>{cap}</figure>')


def page(path, key, title, description, body, depth, wide=False, bare=False, noindex=False, band=False):
    # depth = number of directory levels below the site root (landing=1, subpages=2)
    prefix = "./" if depth == 1 else "../" * (depth - 1)
    cur = ' aria-current="page"'
    html = TEMPLATE.format(
        title=title,
        description=description,
        css="../" * depth + "assets/site.css",
        home="./" if depth == 1 else "../" * (depth - 1),
        p=prefix,
        app=APP,
        body_class="marketing" if wide else "legal",
        c_how=cur if key == "how" else "",
        c_learn=cur if key == "learn" else "",
        c_features=cur if key == "features" else "",
        c_privacy=cur if key == "privacy" else "",
        c_terms=cur if key == "terms" else "",
        c_support=cur if key == "support" else "",
        body=body,
        email=EMAIL,
    )
    if band:
        m = re.match(r'\s*<h1>(.*?)</h1>\s*<p class="lead">(.*?)</p>\s*', body, re.S)
        if m:
            rest = body[m.end():]
            media = ""
            mm = re.match(r'<div class="hero-media">(.*?)</div>\s*', rest, re.S)
            if mm:
                media = f'<div class="dhero-media">{mm.group(1)}</div>'
                rest = rest[mm.end():]
            hero = (f'<section class="dhero dband{" has-media" if media else ""}"><div class="wrap dwrap">'
                    f'<h1>{m.group(1)}</h1><p class="dlead">{m.group(2)}</p>{media}</div></section>')
            html = html.replace('<div class="wrap">\n' + body + '\n</div>\n</main>',
                                hero + '\n<div class="wrap dafter">\n' + rest + '\n</div>\n</main>')
    if bare:
        html = html.replace('<div class="wrap">\n' + body + '\n</div>\n</main>', body + '\n</main>')
    if noindex:
        html = html.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


# ---------------------------------------------------------------- privacy
PRIVACY = f"""
<h1>Privacy Policy</h1>
<p class="meta">Grid9 Sudoku &middot; Last updated {UPDATED}</p>

<div class="card">
  <p><strong>In short:</strong> Grid9 has no accounts, no advertising and no analytics or tracking. Your puzzle progress and settings stay on your device. The only information that leaves your device relates to buying and verifying a Grid9 Premium subscription, and is handled by Apple and RevenueCat.</p>
</div>

<h2>1. Who is responsible</h2>
<p>The controller of personal data described in this policy is:</p>
<p>Joachim Hagedorn<br>Friedrichstr. 155<br>10117 Berlin<br>Germany<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>

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
<p>Joachim Hagedorn<br>Friedrichstr. 155<br>10117 Berlin<br>Germany<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
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




# ================================================================ marketing
SOON = '<span class="btn disabled" aria-disabled="true">Coming soon to the App Store</span>'


HOW_STEPS = [
    dict(
        n="1", title="Your notes, or automatic ones",
        img="cands", alt="A cell showing amber Snyder notes next to a cell showing grey automatic candidates",
        text="""
<p>Grid9 has two kinds of candidates, and you can use either or both.</p>
<ul>
<li><strong>Your own notes (amber).</strong> Tap a number in the grey <em>Notes</em> row to note it (the blue <em>Digits</em> row below places the number itself). These are Snyder-style marks: you only write a number where it has at most two or three places left in a row, column or box. They work completely on their own &mdash; you never have to touch the automatic fill.</li>
<li><strong>Automatic candidates (grey).</strong> <em>Fill auto</em> adds every number that is still legal in each cell, based on the values already placed.</li>
</ul>
<p class="note">Good to know: Fill auto never removes candidates using a technique. To eliminate with a technique, you run it from the strategy panel &mdash; that is where the learning happens.</p>
""",
        example="A cell where your notes say <b>1, 7</b> but automatic candidates would show <b>1, 3, 7, 8, 9</b>.",
    ),
    dict(
        n="2", title="See what is available",
        img="overview", alt="The strategy panel listing Naked Single 5, Hidden Single 2, Naked Pair 1",
        text="""
<p>Tap <em>Hint</em> and a panel slides up from the bottom, with the grid still visible above it. It lists only the techniques that have a hit <em>right now</em>, with a count.</p>
<p>That makes the list an answer to &ldquo;what can I do here?&rdquo; &mdash; you see that a Naked Pair exists, and how many Naked Singles, without being told where.</p>
""",
        example="<b>Naked Single</b> 5 &middot; <b>Hidden Single</b> 2 &middot; <b>Naked Pair</b> 1",
    ),
    dict(
        n="3", title="Help in doses",
        img="ladder", alt="The step ladder with Where?, Which cells?, Why? and an Apply button",
        text="""
<p>Choose a technique and its detail view opens with a step ladder. Each step gives a bit more help, and you decide how far to go before solving the rest yourself.</p>
<ul>
<li><strong>Where?</strong> The mildest hint: where to start looking. Try it yourself before going further.</li>
<li><strong>Which cells?</strong> Shows exactly which cells the technique involves.</li>
<li><strong>Why?</strong> The full reasoning &mdash; why the pattern works and what it lets you remove.</li>
<li><strong>Apply</strong> carries out the move for you.</li>
</ul>
<p><em>Next hit</em> is something different: it jumps to the next occurrence of the same technique on the board, if there is more than one.</p>
""",
        example="",
    ),
    dict(
        n="4", title="Reading the highlights",
        img="xwing", alt="A pattern outlined with solid frames and an eliminated candidate with a dashed frame and strikethrough",
        text="""
<p>Hints are drawn so that shape carries the meaning, not just colour:</p>
<ul>
<li>A <strong>solid outline</strong> marks the evidence &mdash; the cells that form the pattern.</li>
<li>A <strong>dashed outline with a struck-through digit</strong> marks what can be eliminated.</li>
<li>A <strong>bold digit</strong> is the number that matters in the pattern.</li>
<li>For techniques where geometry is the argument (X-Wing, wings, chains) <strong>lines between cells</strong> show the shape.</li>
</ul>
<p>The same language is used for every technique, so once you can read one hint you can read them all.</p>
""",
        example="",
    ),
    dict(
        n="5", title="Practise a technique",
        img="practice", alt="The practice view with Explanation and Step by step buttons above the step ladder",
        text="""
<p>Open the technique library, choose a technique, and Grid9 gives you a puzzle where it is needed. Two extra buttons appear above the step ladder:</p>
<ul>
<li><strong>Explanation</strong> &mdash; the full write-up of the technique, with diagrams. Reading it is always free.</li>
<li><strong>Step by step</strong> &mdash; walks the exact reasoning chain one link at a time, forwards or backwards, instead of only showing the end result. Lost the thread? Step back and watch it again.</li>
</ul>
""",
        example="",
        video="practice",
    ),
    dict(
        n="6", title="Faster input, your own puzzles, your progress",
        img="stats", alt="The statistics view with last puzzle, streaks and personal bests",
        text="""
<ul>
<li><strong>Multi-select.</strong> Drag across several cells to select them at once. Type a number or candidate and it is applied to all of them.</li>
<li><strong>Enter your own.</strong> Paste in a puzzle from a newspaper, a book or another app, to practise a specific problem or find out where you got stuck. Found in the menu.</li>
<li><strong>Statistics.</strong> Every solve is tracked automatically: time, mistakes and hints used; which techniques you found yourself versus used a hint for; personal bests and a day streak.</li>
</ul>
""",
        example="",
    ),
]


def how_it_works():
    d = 2
    out = ['<h1>How it works</h1>',
           '<p class="lead">Six short steps from the first note to the last technique. Everything below is how the app behaves today.</p>']
    for st in HOW_STEPS:
        media = loop(d, st["video"], st["alt"]) if st.get("video") else shot(d, st["img"], st["alt"])
        ex = f'<p class="example"><span>Example</span> {st["example"]}</p>' if st["example"] else ""
        out.append(f"""
<section class="step">
  <div class="step-text">
    <p class="step-n">Step {st["n"]}</p>
    <h2>{st["title"]}</h2>
    {st["text"]}
    {ex}
  </div>
  {media}
</section>""")
    out.append(f"""
<section class="cta">
  <h2>Want to try it?</h2>
  <p>{SOON}</p>
  <p><a href="../learn/">Read the step-by-step guides &rarr;</a> &middot; <a href="../features/">See the full feature list &rarr;</a></p>
</section>""")
    return "\n".join(out)


FEATURE_GROUPS = [
    ("Learn", [
        ("Two dozen techniques", "From Naked and Hidden Singles through pairs, triples and quads, to X-Wing, Swordfish, Jellyfish, wings, Skyscraper, XY-Chains and Unique Rectangles."),
        ("Hints in steps", "Where? &rarr; Which cells? &rarr; Why? &rarr; Apply. Ask for only as much as you need."),
        ("Practice mode", "Pick a technique and solve a puzzle that needs it, with a badge showing which technique you are practising."),
        ("Written explanations", "Every technique has a full explanation with diagrams. Reading is always free."),
        ("Step by step", "Follow a reasoning chain one link at a time, forwards or backwards."),
        ("One highlight language", "Solid outline for evidence, dashed outline and strikethrough for eliminations &mdash; the same for every technique."),
    ]),
    ("Play", [
        ("Five difficulty levels", "Easy, Medium, Hard, Expert and Master, from a large bank of puzzles graded by the techniques they require."),
        ("Your own notes or automatic", "Snyder-style notes in amber, automatic candidates in grey. Use either or both."),
        ("Enter your own puzzle", "Type or paste in a puzzle from anywhere and get the same hints and tools."),
        ("Multi-select", "Drag across cells and enter a number or candidate in all of them at once."),
        ("Undo and redo", "Take a move back, or forward again."),
        ("Mistake checking", "Wrong numbers are counted, so you can see how clean a solve was."),
    ]),
    ("Comfort", [
        ("Larger numbers", "One setting makes both digits and candidates bigger, for easier reading."),
        ("Row, column and box highlighting", "Switch on a gentle highlight of the selected cell&rsquo;s peers, or off for a clean grid."),
        ("Light and dark", "Follows your device, or choose one."),
        ("Works offline", "Puzzles, hints and explanations all run on your device."),
    ]),
    ("Progress and privacy", [
        ("Statistics", "Time, mistakes, hints used, and which techniques you found yourself versus with a hint."),
        ("Personal bests and streaks", "Tracked automatically, no set-up."),
        ("No account, no ads, no tracking", "Your progress stays on your device. Only subscription purchases involve Apple and RevenueCat &mdash; see the <a href=\"../privacy/\">Privacy Policy</a>."),
    ]),
]


def features():
    d = 2
    out = ['<h1>Features</h1>',
           '<p class="lead">What is in the app, in one place.</p>']
    for title, items in FEATURE_GROUPS:
        cards = "\n".join(f'<div class="card"><h3>{t}</h3><p>{x}</p></div>' for t, x in items)
        out.append(f'<h2>{title}</h2>\n<div class="grid3">\n{cards}\n</div>')
    out.append(f"""
<h2 id="free-vs-premium">Free and Premium</h2>
<p>Grid9 is free to download and play. Premium is an auto-renewing subscription (monthly or yearly) that unlocks the deeper learning tools. Eligible new subscribers get a free trial. Prices are shown in the app in your local currency before you subscribe, and you can cancel any time in your iPhone&rsquo;s settings.</p>
<table class="compare">
<thead><tr><th></th><th>Free</th><th>Premium</th></tr></thead>
<tbody>
<tr><th scope="row">Play puzzles, notes, undo/redo, statistics</th><td>&#10003;</td><td>&#10003;</td></tr>
<tr><th scope="row">Read the explanation of every technique</th><td>&#10003;</td><td>&#10003;</td></tr>
<tr><th scope="row">Hint overview: which techniques have a hit, and how many</th><td>&#10003;</td><td>&#10003;</td></tr>
<tr><th scope="row">Larger numbers, highlighting, light/dark</th><td>&#10003;</td><td>&#10003;</td></tr>
<tr><th scope="row">Full hint walkthroughs (Where, Which cells, Why, Apply)</th><td></td><td>&#10003;</td></tr>
<tr><th scope="row">Practise a technique on real puzzles, with Step by step</th><td></td><td>&#10003;</td></tr>
<tr><th scope="row">Enter and solve your own puzzles</th><td></td><td>&#10003;</td></tr>
</tbody>
</table>
<p class="fine">Subscription details are in the <a href="../terms/">Terms of Use</a>.</p>
<section class="cta">
  <p>{SOON}</p>
</section>""")
    return "\n".join(out)


# ================================================================ learn (tutorials)
# Five written guides under /grid9/learn/. They expand the three tours that are built into
# the app (gear menu: "Tour - app features / solving routine / learning a strategy") and add
# two more (custom puzzles, statistics). Text is first person where the guide describes a
# personal workflow (solving routine, learning a strategy), neutral elsewhere.

PREMIUM = '<span class="pill" title="Needs Grid9 Premium">Premium</span>'


def tcell(cands=(), kind="auto"):
    """A small illustration of one cell's candidates (kind: auto = grey, snyder = amber)."""
    digits = "".join(
        f'<i class="{kind if d in cands else "off"}">{d if d in cands else ""}</i>' for d in range(1, 10)
    )
    return f'<span class="tcell {kind}">{digits}</span>'


def cellrow(items):
    """items: list of (cands, kind, caption) or the string '->' for an arrow."""
    out = []
    for it in items:
        if it == "->":
            out.append('<span class="arrow" aria-hidden="true">&rarr;</span>')
        else:
            cands, kind, cap = it
            out.append(f'<span class="cellfig">{tcell(cands, kind)}<small>{cap}</small></span>')
    return '<div class="cellrow">' + "".join(out) + "</div>"


def ladder(rungs, active=None, apply=False):
    parts = []
    for r in rungs:
        cls = "rung on" if r == active else "rung"
        parts.append(f'<span class="{cls}">{r}</span>')
    if apply:
        parts.append('<span class="rung apply">Apply</span>')
    return '<div class="ladder">' + '<span class="arrow" aria-hidden="true">&rarr;</span>'.join(parts) + "</div>"



# Close-up crops (yellow rings) shown inside the text of a step, keyed by step title.
DETAILS = {
    "Start simple: scan the digits": [
        ("d-notes-rows", "Close-up of the grey Notes row and the blue Digits row", "Grey row: tap a digit to note it. Blue row: tap a digit to place it."),
        ("d-amber", "Close-up of one cell with two amber notes", "Amber marks are your own notes, here the digit 3 noted in two cells of a box."),
    ],
    "Check the overview": [
        ("d-overview", "Close-up of the hint overview with the counts ringed", "The ringed numbers are how many places each technique has right now."),
    ],
    "Take only as much help as you need": [
        ("d-ladder", "Close-up of the step ladder rungs and the Apply button", "The rungs reveal a little more each time. Apply, at the bottom, makes the move."),
    ],
    "Pick one you do not know": [
        ("d-picker", "Close-up of the Practice technique list", "Techniques are grouped by difficulty. Tap one to practise it."),
    ],
    "Read it before you hunt": [
        ("d-explanation", "Close-up of the core rule of an Explanation page", "The core rule comes first, in a sentence or two."),
        ("d-explanation-diagram", "Close-up of the diagram on an Explanation page", "Then a small diagram that shows the pattern."),
    ],
    "Try it for real": [
        ("d-xwing", "Close-up of the Which lines step for X-Wing", "Each rung narrows it down. Here: which two lines form the X-Wing."),
    ],
    "Walk it through again": [
        ("d-buttons", "Close-up of the Explanation and Step by step buttons", "The two buttons above the ladder in practice mode."),
        ("d-stepbystep", "Close-up of the Step by step panel", "One link of the chain at a time."),
    ],
    "Mark it yourself, then check": [
        ("d-guess", "Close-up of a practice grid with the cells I guessed marked in teal", "The teal cells are my guess. The ladder tells me if I was right."),
    ],
    "Two kinds of candidates": [
        ("d-notes-rows", "Close-up of the grey Notes row and the blue Digits row", "Grey row: tap a digit to note it. Blue row: tap a digit to place it. Clear auto removes the automatic candidates."),
        ("d-amber", "Close-up of one cell with two amber notes", "Amber marks are your own notes."),
    ],
    "The Info box and Show candidates": [
        ("d-info", "Close-up of the Info box with Show candidates ringed", "Show candidates, ringed, reveals what the row, column and box rules allow."),
    ],
    "The hint panel: see what is available": [
        ("d-overview", "Close-up of the hint overview with the counts ringed", "The ringed numbers are how many places each technique has right now."),
    ],
    "The step ladder: help in doses": [
        ("d-ladder", "Close-up of the step ladder rungs and the Apply button", "Rungs reveal a little more each time. Apply makes the move."),
    ],
    "Practice mode and Step by step": [
        ("d-buttons", "Close-up of the Explanation and Step by step buttons", "Explanation and Step by step sit above the ladder in practice mode."),
        ("d-stepbystep", "Close-up of the Step by step panel", "One link of the chain at a time."),
    ],
    "The gear menu": [
        ("d-menu", "Close-up of the gear menu", "The gear menu, in the dark theme."),
    ],
    "Comfortable to read": [
        ("d-larger", "Close-up of the grid with larger numbers", "Larger numbers, here in the light theme."),
    ],
    "Mistakes and solved puzzles": [
        ("d-solved", "Close-up of the solved screen", "Time, mistakes, hints and techniques used."),
    ],
    "Start entering": [
        ("d-custom-menu", "Gear menu with Enter custom puzzle ringed", "Enter custom puzzle, in the gear menu."),
        ("d-custom-entry", "The grid in manual entry mode with its banner", "The banner reminds you that you are in manual entry mode."),
    ],
    "Skip the empty cells": [
        ("d-custom-buttons", "Close-up of the Skip and Done entering buttons", "Skip and Done entering replace Fill auto and Hint while you enter."),
    ],
    "Last puzzle": [
        ("d-stats-last", "Close-up of the Last puzzle card", "The Last puzzle card. The ringed line lists what you peeked at."),
    ],
    "Solved and streaks": [
        ("d-stats-streak", "Close-up of the Solved, Day streak and Best streak counters", "Solved, Day streak and Best streak."),
    ],
    "Recent puzzles and personal bests": [
        ("d-stats-recent", "Close-up of Recent puzzles and Personal best", "Recent puzzles on top, your personal best per level below."),
    ],
    "Techniques: found, peeked, or via hint": [
        ("d-stats-tech", "Close-up of the Techniques list with three numbers per technique", "Three numbers per technique: self-found / peeked / via hint."),
    ],
}


def lstep(n, title, body, media="", premium=False, tip="", extra=""):
    label = f'Step {n}' if n is not None else "Note"
    pill = f" {PREMIUM}" if premium else ""
    tip_html = f'<p class="note">{tip}</p>' if tip else ""
    if not extra:
        extra = "".join(detail(3, nm, alt, cap) for nm, alt, cap in DETAILS.get(title, []))
    cls = "step" if media else "step solo"
    return f"""
<section class="{cls}">
  <div class="step-text">
    <p class="step-n">{label}{pill}</p>
    <h2>{title}</h2>
    {body}
    {extra}
    {tip_html}
  </div>
  {media}
</section>"""


def learn_nav(prev=None, nxt=None):
    bits = []
    if prev:
        bits.append(f'<a href="../{prev[0]}/">&larr; {prev[1]}</a>')
    bits.append('<a href="../">All guides</a>')
    if nxt:
        bits.append(f'<a href="../{nxt[0]}/">{nxt[1]} &rarr;</a>')
    return '<p class="learn-nav">' + " ".join(bits) + "</p>"


LEARN_PAGES = [
    ("solving-routine", "Solving routine", "How I work through a puzzle, tool by tool, in the order that works for me."),
    ("learning-a-strategy", "Learning a strategy", "How to pick up one unfamiliar technique on purpose, using practice mode."),
    ("app-features", "App features", "Every part of the screen and the menu, and what it does."),
    ("custom-puzzles", "Custom puzzles", "Type in a puzzle from paper or another app and use every tool on it."),
    ("statistics", "Statistics", "What the app tracks, what the numbers mean, and where they live."),
]
_order = [p[0] for p in LEARN_PAGES]
_title = {p[0]: p[1] for p in LEARN_PAGES}


def _nav_for(slug):
    i = _order.index(slug)
    prev = (_order[i - 1], _title[_order[i - 1]]) if i > 0 else None
    nxt = (_order[i + 1], _title[_order[i + 1]]) if i < len(_order) - 1 else None
    return learn_nav(prev, nxt)


def _tail(slug):
    if slug in ("solving-routine", "learning-a-strategy", "app-features"):
        blurb = "This guide is also built into the app, under the gear menu. Reading is always free."
    elif slug == "custom-puzzles":
        blurb = "Entering your own puzzle is part of Grid9 Premium, with a free trial for new subscribers."
    else:
        blurb = "Statistics are free for everyone, from your first solved puzzle."
    return f"""
{_nav_for(slug)}
<section class="cta">
  <h2>Try it yourself</h2>
  <p>{blurb}</p>
  <p>{SOON}</p>
</section>"""


# ---------------------------------------------------------------- learn index
def learn_index():
    cards = []
    for i, (slug, t, blurb) in enumerate(LEARN_PAGES, 1):
        prem = {"solving-routine": "Free, with Premium for the hint steps",
                "learning-a-strategy": "Reading is free, practice needs Premium",
                "app-features": "Free, with Premium marked where it applies",
                "custom-puzzles": "Premium",
                "statistics": "Free"}[slug]
        cards.append(f"""<a class="card guide" href="{slug}/">
  <p class="step-n">Guide {i}</p>
  <h3>{t}</h3>
  <p>{blurb}</p>
  <p class="fine">{prem}</p>
</a>""")
    return f"""
<h1>Learn Grid9</h1>
<p class="lead">Five short guides, from the first notes to your own statistics. Each one shows the real screens and says clearly what is free and what needs Premium.</p>
<div class="grid3 guides">
{chr(10).join(cards)}
</div>
<div class="card">
  <p><strong>Where to start?</strong> If you want the quick overview of what the buttons do, begin with <a href="app-features/">App features</a>. If you want to see how it all fits together while you solve, read the <a href="solving-routine/">Solving routine</a>. The techniques themselves are explained technique by technique inside the app, and <a href="learning-a-strategy/">Learning a strategy</a> shows how to use that.</p>
  <p>The first three guides are also built into the app: open the gear menu and choose one of the three <em>Tour</em> entries.</p>
</div>
<section class="cta">
  <p>{SOON}</p>
</section>
"""


# ---------------------------------------------------------------- 1. solving routine
def solving_routine():
    d = 3
    s = []
    s.append(f"""
<h1>Solving routine</h1>
<p class="lead">How I work through a puzzle with Grid9: which tool I reach for first, when I ask for help, and how the whole thing turns into a loop. It is one way to solve, not the only one.</p>
<div class="hero-media">{loop(d, "main-play", "A full puzzle being worked through: notes, hint overview, step ladder and Apply")}</div>
<div class="card">
  <p><strong>Free and Premium.</strong> Everything about notes, Fill auto and the hint overview is free. The steps of the hint ladder (Where, Which cells, Why, Apply) are marked {PREMIUM}.</p>
</div>""")

    s.append(lstep(None, "There is no single way",
        """<p>This is the order I personally switch between marking candidates myself, checking the hint overview and running Fill auto. If you already have your own rhythm, or like a different mix of the app&rsquo;s tools, that is just as correct. Take what works for you and skip what does not.</p>
<p>Every step below leans on something the app already does. The guide only shows the order I use them in.</p>"""))

    s.append(lstep(1, "Start simple: scan the digits",
        """<p>I go through the digits 1 to 9, one at a time. For each digit I scan box by box, and wherever only one or two cells could still take it, I pencil it in with Snyder notation: the amber notes you tap in with the grey <em>Notes</em> row.</p>
<p>If only <strong>one</strong> cell is left for the digit, that is a Single, and I place the number straight away instead of noting it. With <strong>three or more</strong> places left it is too early to bother writing it down.</p>
<p class="example"><span>Example</span> The 3 can only go in two cells of this box, so both get an amber 3.</p>""",
        media=shot(d, "cands", "The grid with amber Snyder notes next to grey automatic candidates", "Amber notes are mine. Grey ones come from Fill auto.")))

    s.append(lstep(2, "Scan again",
        """<p>Then I go through 1 to 9 a second time. The placements from the first pass almost always free up new cells: a digit that had three possible places before often has one or two now.</p>
<p>This is the point where the board really starts to open up, and I still have not filled in a single full candidate list.</p>"""))

    s.append(lstep(3, "Look for patterns in the notes",
        """<p>With numbers placed and a few Snyder notes in the grid, I look for rows, columns and boxes that already show a Hidden Single, a Hidden Pair or even a Box/Line Reduction. Often they are visible without ever filling in every candidate.</p>
<p>These techniques read from the same row, column and box logic that Fill auto uses. You just do not need the full picture to spot them.</p>""",
        tip="Snyder notes work completely on their own. You never have to touch Fill auto at all if you prefer to reason it out yourself."))

    s.append(lstep(4, "Check the overview",
        """<p>Now I open the hint panel, but only for a quick look at the overview, not the detail view. It lists the techniques that have a hit in the position right now, with a count. If a Naked Single or a Hidden Single is on the list, it should be one I could already find myself, since neither needs a full candidate fill.</p>
<p>The overview answers &ldquo;what can I do here?&rdquo; without giving the move away. Just glance at it, there is no need to tap into a technique yet.</p>""",
        media=shot(d, "overview", "The hints panel listing Hidden Single, Naked Quad, Pointing Pair and X-Wing with counts", "The overview lists every technique that has a hit right now.")))

    s.append(lstep(5, "Take only as much help as you need",
        """<p>If I still cannot find it, that is what hints are for. I start with the smallest one. Still stuck? I take the next. There is no shame in it, that is exactly what the step ladder is for: as much or as little help as you need.</p>
""" + ladder(["Where?", "Which cells?", "Why?"], apply=True) + """
<ul>
<li><strong>Where?</strong> Points out where to start looking. Try to find it yourself before going further.</li>
<li><strong>Which cells?</strong> Shows exactly which cells the technique involves.</li>
<li><strong>Why?</strong> The reasoning: why the pattern works and what it lets you remove.</li>
<li><strong>Apply</strong> carries out the move for you.</li>
</ul>
<p><em>Next hit</em> does something different: it jumps to the next place on the board where the same technique applies, if there is more than one.</p>""",
        media=shot(d, "ladder", "The step ladder with Where, Which cells, Why and the Apply button", "The ladder: each rung gives a bit more."),
        premium=True))

    s.append(lstep(6, "Go deeper when needed",
        """<p>Once the easy passes are used up, I run <em>Fill auto</em> and look at every candidate at once. That is when I hunt for the tougher patterns, such as a Hidden Pair or a Naked Triple, and cross off every candidate I can find a reason to remove.</p>
<p>Fill auto only computes what the raw row, column and box rules allow. It never eliminates through a technique on its own. Finding those eliminations is still my job, or the hint ladder&rsquo;s.</p>"""))

    s.append(lstep(7, "Reduce the noise",
        """<p>With every candidate filled in, the board gets crowded fast. When I have finished cross-referencing I switch Fill auto back off. The grid looks clean again, but my own eliminations are still remembered underneath.</p>
""" + cellrow([([1, 3, 7, 8, 9], "auto", "Auto on<br>the 5 is already crossed off"), "->", ([], "auto", "Auto off<br>clean, the 5 stays gone"), "->", ([1, 3, 7, 8, 9], "auto", "Auto on again<br>still no 5")]) + """
<p>Fill auto is a toggle, not a one-way door. Turn it on when you need the full picture and off when you do not. It never forgets what you or a technique has already ruled out.</p>"""))

    loop_stages = ["Scan", "Solve", "Look for patterns", "Check the overview", "Ask for help", "Go deeper", "Clean up", "Repeat"]
    flow = '<ol class="flow">' + "".join(f"<li>{x}</li>" for x in loop_stages) + "</ol>"
    s.append(lstep(8, "Repeat the cycle",
        """<p>This was never really 1 to 8 and done. It is a loop. The grid changes with every move, and my approach changes with it.</p>
""" + flow + """
<p>The same handful of tools, cycled through in whatever order the puzzle asks for, until it is solved.</p>"""))

    s.append(lstep(9, "It works on paper puzzles too",
        """<p>Say you are stuck on a puzzle from a magazine or a puzzle book, with nowhere else to turn. Enter it through <em>Enter custom puzzle</em> in the gear menu, and the whole routine above is yours to use on it: notes, Fill auto and the hint ladder, exactly as if it had started in the app.</p>
<p>Same tools, same routine, different starting point. <a href="../custom-puzzles/">Read how entering a puzzle works &rarr;</a></p>""",
        premium=True))

    s.append(f"""
<h2>The routine on one screen</h2>
<div class="card">
<ol>
<li>Scan digits 1 to 9, box by box. Place Singles, note digits with one or two places left.</li>
<li>Scan again. The first pass has opened new cells.</li>
<li>Look for Hidden Singles, Hidden Pairs and Box/Line Reductions in the notes.</li>
<li>Glance at the hint overview. Find the Singles yourself.</li>
<li>Still stuck? Climb the ladder one rung at a time.</li>
<li>Run Fill auto and hunt for pairs, triples and other eliminations.</li>
<li>Turn Fill auto off to clean up. Your eliminations stay.</li>
<li>Go round again.</li>
</ol>
</div>""")
    s.append(_tail("solving-routine"))
    return "\n".join(s)


# ---------------------------------------------------------------- 2. learning a strategy
def learning_strategy():
    d = 3
    s = []
    s.append(f"""
<h1>Learning a strategy</h1>
<p class="lead">How I pick up one technique I do not know yet: read it, think it through, find it on a real puzzle, walk through why it works, and then try to spot it myself.</p>
<div class="hero-media">{loop(d, "practice", "Practice mode: choosing a technique, the hint ladder and Step by step")}</div>
<div class="card">
  <p><strong>Free and Premium.</strong> Reading the explanation of any technique is free. Practising a technique on puzzles built for it, and the Step by step mode, need {PREMIUM}.</p>
</div>""")

    s.append(lstep(None, "Not a checklist to clear",
        """<p>Most of what you will ever use, such as Hidden Pair, Naked Triple or Pointing Pair, you will start to notice on your own just by solving puzzles with the <a href="../solving-routine/">Solving routine</a>. This guide is for the techniques that do not click that way: a way to sit down deliberately with <em>one</em> unfamiliar pattern and learn it.</p>
<p>There is no progress bar, nothing to unlock and no level to reach. Pick a technique because you are curious about it, go at your own pace and stop the moment it clicks, or whenever you have had enough for today.</p>"""))

    s.append(lstep(1, "Pick one you do not know",
        """<p>I open the gear menu and choose <em>Practice technique&hellip;</em>. It lists every technique Grid9 knows, grouped by how advanced it is. I pick one I do not reliably spot myself yet.</p>
<p>Swordfish is a good example for this guide: three rows, three columns, one digit. It is genuinely hard to see until you have looked at a few.</p>""",
        media=shot(d, "practice-picker", "The Practice technique menu listing techniques grouped as Easy, Medium and Hard", "The technique list, grouped by difficulty."),
        premium=True))

    s.append(lstep(2, "Read it before you hunt",
        """<p>Before I go looking for the pattern on a real board, I open <em>Explanation</em>, the small &ldquo;i&rdquo; next to the hint. It is worth reading properly: what the pattern looks like, why it works and what it lets you eliminate. Each explanation starts with a short core rule and has a diagram.</p>
<p>Hunting for something you do not understand yet is just guessing with extra steps.</p>""",
        media=shot(d, "explanation", "An Explanation page with a core rule, a diagram and the reasoning", "Explanation: the core rule, a diagram and the why."),
        tip="Reading the explanation of any technique is free."))

    s.append(lstep(3, "Sit with it first",
        """<p>Then I stop and actually think it through, sometimes with paper and a pencil, tracing the logic by hand: which candidates, which rows and columns, and why they lock together the way they do.</p>
<p>I do not rush to a puzzle. Skipping ahead to &ldquo;just show me an example&rdquo; skips the part that makes a pattern stick.</p>"""))

    s.append(lstep(4, "Try it for real",
        """<p>Only then do I bring it to a real puzzle. Grid9 gives me one where the technique is needed, with a badge showing which technique I am practising. I open the hint ladder and walk it down one rung at a time. Fish techniques such as Swordfish get an extra rung, <em>Which lines?</em>, before the hint narrows down to exact cells.</p>
""" + ladder(["Where?", "Which lines?", "Which cells?", "Why?"], active="Why?", apply=True) + """
<p>At each rung I try to actually look for the pattern myself before I tap through to the next one.</p>""",
        media=shot(d, "xwing", "The hint ladder for X-Wing with Where, Which lines, Which cells and Why", "X-Wing in practice mode, with the highlighted pattern and its reasoning."),
        premium=True))

    s.append(lstep(5, "Walk it through again",
        """<p>Once I have reached <em>Why?</em>, or even after I have applied the move, I tap <em>Step by step</em>. It is more pedagogical than the ladder: it walks the whole reasoning chain one link at a time, forwards and backwards. That is worth doing even when I already know the answer.</p>
<p>Lost the thread? Step back and watch the link again. Seeing <em>why</em> it is true is different from seeing <em>that</em> it is true.</p>""",
        media=shot(d, "stepbystep", "The Step by step panel explaining an X-Wing one link at a time", "Step by step shows one link of the chain at a time."),
        premium=True))

    s.append(lstep(6, "Do it again, a few times",
        """<p>Then I do it again: <em>Practice technique&hellip;</em> once more, same technique, a few more puzzles, until the shape stops feeling like a lucky find and starts to look familiar.</p>
<p>Some techniques take two puzzles to click and others take five. There is no fixed number, and no way to get it wrong by taking longer.</p>""",
        premium=True))

    s.append(lstep(7, "Mark it yourself, then check",
        """<p>Eventually I flip it around. Before opening any hint, I tap the cells I think form the pattern. Practice mode remembers every tap as a soft highlight, with no commitment and easy to undo. Then I walk the hint ladder and see whether I was right.</p>
<p>Some puzzles hide more than one occurrence of the same technique. Two separate Swordfish in one grid is not unusual. I mark what I found, check it, and then go looking for a second one before I move on.</p>""",
        media=shot(d, "practice-guess", "A practice puzzle where the cells I think form the pattern are marked in teal", "My guess is marked on the grid, the ladder then shows if it was right."),
        premium=True))

    s.append(lstep(8, "One day you will just see it",
        """<p>There is no test at the end and nothing that marks a technique as done. You will know it worked the same way everything else in Grid9 works: mid-game, on some ordinary puzzle, you will just see it.</p>
<p>That is the point. Not finishing a guide, but folding one more pattern into how you already play, back in the regular <a href="../solving-routine/">Solving routine</a>.</p>"""))

    s.append(_tail("learning-a-strategy"))
    return "\n".join(s)


# ---------------------------------------------------------------- 3. app features
def app_features():
    d = 3
    s = []
    s.append(f"""
<h1>App features</h1>
<p class="lead">A walk through the screen and the menu: what each part does, and which parts need Premium. You do not need to read it in order, every section stands on its own.</p>
<div class="hero-media">{loop(d, "candidates", "Switching between automatic candidates and your own notes")}</div>""")

    s.append(lstep(1, "Two kinds of candidates",
        """<p>Grid9 has two kinds of candidates, and understanding the difference is the key to playing efficiently.</p>
<ul>
<li><strong>Snyder notes (amber)</strong> are your own. Tap a number in the grey <em>Notes</em> row to note it (the blue <em>Digits</em> row below places the number itself). The idea, from Snyder notation, is to note a digit only when it has at most two or three possible places left in a row, column or box. That way the notes show patterns instead of drowning them.</li>
<li><strong>Auto candidates (grey)</strong> are every number that is still legal in a cell. <em>Fill auto</em> adds them, and the button changes to <em>Clear auto</em> to remove them.</li>
</ul>
""" + cellrow([([1, 7], "snyder", "Snyder<br>my own notes"), ([1, 3, 7, 8, 9], "auto", "Auto<br>everything still legal")]) + """
<p class="note">Fill auto never removes candidates using a technique. It only computes what is possible from the numbers already placed. To eliminate with a technique you run it from the hint panel, which is where the learning happens. Your amber notes are never cleared by Fill auto or by running a technique, only by you or by <em>Clear all candidates</em> in the menu.</p>""",
        media=shot(d, "cands", "The grid showing amber notes and grey automatic candidates", "Amber and grey candidates side by side.")))

    s.append(lstep(2, "The Info box and Show candidates",
        """<p>When you select an empty cell, the Info box under the grid says whether there are conflicts and which cell you are on. Its <em>Show candidates</em> checkbox lists exactly which numbers are still possible in that cell, a quick way to double-check your own reasoning.</p>
<p>That list only looks at the raw row, column and box rules. It does not know what you have crossed out or what a technique has eliminated, so after you have applied a technique it can list more numbers than there are open candidates in the cell.</p>"""))

    s.append(lstep(3, "The hint panel: see what is available",
        """<p>Tap <em>Hint</em> and a panel slides up from the bottom with the grid still visible above it. It lists every technique that has a hit in the current position, with a count, for example Naked Single 5, Hidden Single 2, Naked Pair 1.</p>
<p>It tells you what exists without telling you where. This overview is free.</p>""",
        media=shot(d, "overview", "The hints panel with a list of techniques and how many hits each has", "The overview lists only what is available right now.")))

    s.append(lstep(4, "The step ladder: help in doses",
        """<p>Tap a technique and its detail view opens with a step ladder. This is the heart of the app: each step gives a bit more help, and you decide how far to go before solving the rest yourself.</p>
""" + ladder(["Where?", "Which cells?", "Why?"], apply=True) + """
<p>Two different ways to move around: the ladder gives different <em>amounts</em> of help for the same hit, and <em>Apply</em> carries the move out. <em>Next hit</em> does something else: it jumps to the next occurrence of the same technique on the board, if there is more than one.</p>
<p>Hints are drawn the same way for every technique. A <strong>solid outline</strong> marks the pattern, a <strong>dashed outline with a struck-through digit</strong> marks what can be removed, and for geometric techniques such as X-Wing, <strong>lines between cells</strong> show the shape.</p>""",
        media=shot(d, "ladder", "The step ladder for Empty Rectangle", "Where, Which cells, Why and Apply."),
        premium=True))

    s.append(lstep(5, "Practice mode and Step by step",
        """<p>Choose <em>Practice technique&hellip;</em> in the gear menu and Grid9 gives you a puzzle where that technique is needed. Two buttons appear above the ladder:</p>
<ul>
<li><strong>Explanation</strong> is the full write-up of the technique with diagrams. Reading it is free.</li>
<li><strong>Step by step</strong> walks the exact reasoning chain one link at a time, forwards or backwards, instead of only showing the end result.</li>
</ul>
<p>For a full guide to using it, see <a href="../learning-a-strategy/">Learning a strategy</a>.</p>""",
        media=shot(d, "stepbystep", "Practice mode with the Explanation and Step by step buttons above the hint ladder", "Explanation and Step by step in practice mode."),
        premium=True))

    s.append(lstep(6, "Multi-select",
        """<p>Drag a finger across several cells to select them all at once. Whatever number or candidate you then type is applied to every selected cell at the same time. It speeds up writing the same note into a row or a box.</p>"""))

    s.append(lstep(7, "The gear menu",
        """<p>Everything else lives in the gear menu in the top corner.</p>
<ul>
<li><strong>Practice technique&hellip;</strong> opens the technique list, where you choose what to practise (Premium).</li>
<li><strong>Enter custom puzzle</strong> lets you type in your own (Premium). See <a href="../custom-puzzles/">Custom puzzles</a>.</li>
<li><strong>Reset puzzle</strong> takes the puzzle back to its starting position.</li>
<li><strong>Theme</strong> chooses System, Light or Dark.</li>
<li><strong>Check conflicts</strong> finds numbers that clash in a row, column or box.</li>
<li><strong>Check against solution</strong> marks every number you placed that differs from the puzzle&rsquo;s solution, and says how many are wrong.</li>
<li><strong>Clear all candidates</strong> removes all notes and automatic candidates.</li>
<li><strong>Show conflicts immediately</strong> highlights clashes as you type instead of when you ask.</li>
<li><strong>Highlight row/column/box</strong> tints the selected cell&rsquo;s row, column and box. Turn it off for a cleaner grid.</li>
<li><strong>Larger numbers</strong> makes both digits and candidates bigger.</li>
<li><strong>Statistics</strong> opens your statistics. See <a href="../statistics/">Statistics</a>.</li>
<li><strong>Tour</strong> entries open the three guides built into the app.</li>
</ul>""",
        media=shot(d, "menu-dark", "The gear menu with Game and Settings sections and the three Tour entries", "The gear menu.")))

    s.append(lstep(8, "Comfortable to read",
        """<p>Light and dark themes follow your device or can be forced either way. <em>Larger numbers</em> scales up both the digits and the candidates, for easier reading in a dim room or without glasses. Both can be switched at any time without losing your position.</p>""",
        media=shot(d, "larger", "The grid with larger numbers enabled in the light theme", "Larger numbers in the light theme.")))

    s.append(lstep(9, "Mistakes and solved puzzles",
        """<p>A wrong number is counted against the puzzle&rsquo;s solution, so at the end you can see how clean the solve was. When the last cell is filled correctly the grid plays a short animation and shows time, mistakes, hints used and the techniques used. All of it goes into your <a href="../statistics/">statistics</a>.</p>""",
        media=shot(d, "solved", "The puzzle solved screen with time, mistakes, hints and techniques used", "The solved screen.")))

    s.append(_tail("app-features"))
    return "\n".join(s)


# ---------------------------------------------------------------- 4. custom puzzles
def custom_puzzles():
    d = 3
    s = []
    s.append(f"""
<h1>Custom puzzles</h1>
<p class="lead">Type in a puzzle from a magazine, a book or another app, and use every Grid9 tool on it: notes, Fill auto, the hint ladder and the technique explanations.</p>
<div class="hero-media">{loop(d, "custom", "Entering a puzzle, then solving it with Fill auto and the hint ladder")}</div>
<div class="card">
  <p><strong>Premium.</strong> Entering your own puzzle is a {PREMIUM} feature. Everything you do on it afterwards works exactly as on a built-in puzzle.</p>
</div>""")

    s.append(lstep(1, "When it is useful",
        """<p>The common case is being stuck on a paper puzzle with nowhere else to turn. It is also a good way to practise a specific position, to find out where you went wrong in a half-finished grid, or to see which techniques a puzzle from another source really needs.</p>""",
        media=shot(d, "paper", "A paper sudoku next to the app on a phone", "From paper to the app."),
        premium=True))

    s.append(lstep(2, "Start entering",
        """<p>Open the gear menu and choose <em>Enter custom puzzle</em>. The board is cleared, the cursor starts in the top-left cell (R1C1), and a line above the grid reminds you that you are in manual entry mode.</p>
<p>Fill in the given numbers with the number pad, starting at R1C1. After each number the cursor moves on to the next cell by itself, so you can read the puzzle row by row.</p>"""))

    s.append(lstep(3, "Skip the empty cells",
        """<p>Where the puzzle has an empty cell, press <em>Skip</em> to move on without entering anything. <em>Skip</em> and <em>Done entering</em> take the place of the Fill auto and Hint buttons while you are entering, since candidates and hints mean nothing until the puzzle is complete.</p>"""))

    s.append(lstep(4, "Done entering: the puzzle is checked",
        """<p>When all the givens are in, press <em>Done entering</em>. Before it lets you start, Grid9 checks two things:</p>
<ul>
<li><strong>No conflicts.</strong> If the same number appears twice in a row, column or box, the app lists the cells that clash and you stay in entry mode to fix them.</li>
<li><strong>Exactly one solution.</strong> A proper sudoku has one and only one solution. If your grid has none, or more than one, the app says so and does not start.</li>
</ul>
<p>The solution is needed so that hints, Check against solution and the mistake count all work. A typo is very often caught by one of these two checks. Not always, though: if a wrong digit happens to produce another valid puzzle, the app cannot know. So compare against the original once before you start.</p>""",
        premium=True))

    s.append(lstep(5, "Solve it like any other puzzle",
        """<p>After the check the numbers you entered are the puzzle&rsquo;s givens and the grid is a normal puzzle. Use your own notes or Fill auto, ask the hint panel what is available and climb the ladder as far as you like. See the <a href="../solving-routine/">Solving routine</a> for the way I do it.</p>
<p>Mistakes are counted against the solution the app found, as in any other puzzle.</p>""",
        media=shot(d, "ladder", "The step ladder on a puzzle", "The same hint ladder, on your puzzle."),
        premium=True))

    s.append(lstep(None, "Good to know",
        """<ul>
<li>Entering a new puzzle replaces the one you are on.</li>
<li><em>Reset puzzle</em> in the gear menu takes you back to the numbers you entered, so you can try a different route.</li>
</ul>"""))

    s.append(_tail("custom-puzzles"))
    return "\n".join(s)


# ---------------------------------------------------------------- 5. statistics
def statistics():
    d = 3
    s = []
    s.append(f"""
<h1>Statistics</h1>
<p class="lead">Every solved puzzle is tracked automatically, with no setup. Open the gear menu and choose <em>Statistics</em> to see how you are really solving.</p>
<div class="hero-media">{loop(d, "statistics", "Opening the statistics view and scrolling through it")}</div>
<div class="card">
  <p><strong>Free.</strong> Statistics are available to everyone. They stay on your device, see the end of this page.</p>
</div>""")

    s.append(lstep(1, "Last puzzle",
        """<p>At the top is a summary of the last puzzle you solved: the difficulty, the date, the time, the number of mistakes and the number of hints you used. Below it is a line starting with <em>Peeked at</em>, which lists the techniques whose pattern you looked at in the hint panel without applying them, with a count for each.</p>""",
        media=shot(d, "stats", "The Statistics view with last puzzle, solved count, streaks and personal bests", "The Statistics view.")))

    s.append(lstep(2, "Solved and streaks",
        """<p>Three counters sit under it. <strong>Solved</strong> is the number of puzzles you have finished. <strong>Day streak</strong> is the number of days in a row on which you solved at least one puzzle. <strong>Best streak</strong> is your longest run so far.</p>
<p>Solving several puzzles on the same day does not add to the streak. Missing a whole day starts it again from one.</p>"""))

    s.append(lstep(3, "Recent puzzles and personal bests",
        """<p><em>Recent puzzles</em> lists your latest solves with difficulty, date, time, mistakes and hints. Under <em>Personal best</em> you see your fastest time at each difficulty level. Tap a level for details, including which techniques you used on puzzles at that level.</p>
<p>The app keeps your 200 most recent solves.</p>"""))

    s.append(lstep(4, "Techniques: found, peeked, or via hint",
        """<p>This is the part I find most useful. For every technique, three numbers are shown in this order:</p>
<ol>
<li><strong>Self-found:</strong> how many times you used the technique yourself, without a hint.</li>
<li><strong>Peeked:</strong> how many times the hint panel showed you the pattern and you did not apply it.</li>
<li><strong>Via hint:</strong> how many times you applied it with the hint ladder.</li>
</ol>
<p>A technique with a high first number is one you have mastered. A technique with mostly peeks or hints is one worth practising, which is where <a href="../learning-a-strategy/">Learning a strategy</a> comes in.</p>
<p class="example"><span>Example</span> <b>Naked Single 81 / 33 / 32</b> means 81 found on your own, 33 peeks, and 32 applied through a hint.</p>"""))

    s.append(lstep(None, "Where your statistics live",
        """<p>Grid9 has no accounts, so statistics are stored only on your device. They are not sent anywhere, which is also why they cannot be moved automatically to a new phone, and why deleting the app deletes them. See the <a href="../../privacy/">Privacy Policy</a> for the full picture.</p>"""))

    s.append(_tail("statistics"))
    return "\n".join(s)



# ---------------------------------------------------------------- landing page
def landing():
    d = 1
    base = "../" * d + "assets/img/"
    tabs = [
        ("notes", "Notes", "Your own notes, your own pace",
         "A grey row for notes, a blue row for numbers. Mark only the digits that have two or three places left, the way Snyder notation works, and let the grid show you the patterns.",
         "cands"),
        ("hints", "Hints", "Know what to look for",
         "Tap Hint and the panel lists every technique that has a hit right now, with a count. It answers \u201cwhat can I do here?\u201d without giving the move away.",
         "overview"),
        ("ladder", "Step ladder", "Help in doses",
         "Where? Which cells? Why? Apply. Take only as much help as you need, and see the reasoning drawn on the grid.",
         "ladder"),
        ("practice", "Practice", "One technique at a time",
         "Pick a technique, read how it works, then solve a puzzle that actually needs it. Two dozen techniques, from Naked Singles to Jellyfish.",
         "practice-picker"),
        ("stats", "Statistics", "See what you really know",
         "For every technique: how often you found it yourself, peeked at it, or took it from a hint. Stored on your device only.",
         "stats"),
    ]
    pills = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}">{n}</button>'
        for i, (k, n, *_r) in enumerate(tabs))
    panels = "".join(
        f'''<div class="dpanel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " data-later"}>
  <div class="dpanel-text"><h3>{h}</h3><p>{body}</p></div>
  <a class="zoom" href="{base}{img}-full.webp" target="_blank" rel="noopener"><img class="dphone" src="{base}{img}.webp" alt="{h}" loading="lazy"></a>
</div>'''
        for i, (k, n, h, body, img) in enumerate(tabs))
    guides = "".join(
        f'<a class="dguide" href="learn/{s}/"><span class="step-n">Guide {i}</span><strong>{t}</strong><span>{b}</span></a>'
        for i, (s, t, b) in enumerate(LEARN_PAGES, 1))
    video = loop(d, "main-play", "A hint walking through a technique on the sudoku grid")
    return f"""
<section class="dhero">
  <div class="wrap dwrap">
    <p class="dkicker">A sudoku app that teaches</p>
    <h1>Learn <em>why</em> a move works,<br>not just where it goes.</h1>
    <p class="dlead">Ask for help in small doses, see the reasoning drawn on the grid, and practise one technique at a time on puzzles built for it.</p>
    <p class="dcta">{SOON}</p>
    <p class="dfine">For iPhone and iPad &middot; No account, no ads, no tracking</p>
    <div class="dhero-media">{video}</div>
  </div>
</section>

<section class="dsec">
  <div class="wrap dwrap">
    <div class="grid3 dcards">
      <div class="card"><h3>Help in doses</h3><p>Start with <em>Where?</em>, the mildest nudge. Only ask for <em>Which cells?</em> and <em>Why?</em> if you still need them.</p></div>
      <div class="card"><h3>See the reasoning</h3><p>A solid outline for the pattern, a dashed one and a struck-through digit for what can go. Step by step walks a chain one link at a time.</p></div>
      <div class="card"><h3>Practise one technique</h3><p>Read how it works, then solve a puzzle that needs it. From Naked Singles to Jellyfish.</p></div>
    </div>
  </div>
</section>

<section class="dsec dtabs" id="tour">
  <div class="wrap dwrap">
    <h2 class="dcenter">Everything in one place</h2>
    <div class="dpills" role="tablist" aria-label="Features">{pills}</div>
    <div class="dpanels">{panels}</div>
  </div>
</section>

<section class="dsec">
  <div class="wrap dwrap">
    <h2 class="dcenter">Light, dark, and easy to read</h2>
    <p class="dlead dcenter">It follows your phone, or you choose. Bigger numbers, highlighted rows, columns and boxes, all optional. Free for everyone.</p>
    <div class="dpair">
      <figure><img src="{base}overview.webp" alt="Grid9 in the dark theme" loading="lazy"><figcaption>Dark</figcaption></figure>
      <figure><img src="{base}larger.webp" alt="Grid9 in the light theme with larger numbers" loading="lazy"><figcaption>Light, with larger numbers</figcaption></figure>
    </div>
  </div>
</section>

<section class="dsec">
  <div class="wrap dwrap">
    <h2 class="dcenter">Learn Grid9</h2>
    <p class="dlead dcenter">Five short guides, with the real screens and a clear note on what is free and what needs Premium.</p>
    <div class="dguides">{guides}</div>
  </div>
</section>

<section class="dsec">
  <div class="wrap dwrap">
    <div class="dstory">
      <p class="dkicker">From the developer</p>
      <h2>Why I made Grid9</h2>
      <p>&ldquo;I thought of an app that could help you, but in levels: a small first nudge in the right direction. If that is not enough, you can get one more hint.&rdquo;</p>
      <p class="fine">&mdash; Joachim Hagedorn</p>
      <p><a href="why/">Read the story &rarr;</a></p>
    </div>
  </div>
</section>

<section class="dsec dfinal">
  <div class="wrap dwrap">
    <h2>Try it yourself</h2>
    <p>{SOON}</p>
    <p class="dfine">Free to play. Premium unlocks the hint steps, practice runs and custom puzzles, with a free trial for new subscribers.</p>
  </div>
</section>

<script>
(function () {{
  var tabs = document.querySelectorAll('.dpills [role=tab]');
  var panels = document.querySelectorAll('.dpanel');
  if (!tabs.length) return;
  document.documentElement.classList.add('js');
  function show(i) {{
    tabs.forEach(function (t, j) {{ t.setAttribute('aria-selected', j === i ? 'true' : 'false'); }});
    panels.forEach(function (p, j) {{ p.hidden = j !== i; }});
  }}
  tabs.forEach(function (t, i) {{ t.addEventListener('click', function () {{ show(i); }}); }});
  show(0);
}})();
</script>
"""


# ---------------------------------------------------------------- why I made Grid9
def why_page():
    return """
<h1>Why I made Grid9</h1>
<p class="lead">A few words from the developer.</p>

<div class="story">
<p class="hook">Sometimes I open the hint overview and see a Hidden Single. I go back to the puzzle, cannot find it, and think the app must be wrong. Then I ask for one more hint, see exactly where I missed it, and I am amazed at myself. Once you know it is there, it is easy to see.</p>
<p class="hook">That moment is why I made Grid9.</p>

<h2>Getting stuck</h2>
<p>I have always loved sudoku: the feeling when you start to read the puzzle, see the patterns, and see the logic of why it can only be that one digit. The feeling when you start to build a strategy &mdash; if this one is a 2, then that one cannot be a 2 &mdash; and the reasoning grows on several levels.</p>
<p>But you always reach a point where you get stuck. You know there is a solution, but you cannot see it. You look and look, you try different strategies, and you do not find the key, the breakthrough, as I call it, that more or less unlocks the whole puzzle.</p>

<h2>Pencil, paper and a phone</h2>
<p>I like solving sudoku best with a pencil and a book or a magazine, writing out the candidates and planning a strategy. A few years ago I started travelling for work, and like so many others I sat there with my phone. Of course I had downloaded a sudoku app, but it was either full of ads or hard to navigate, especially when it came to getting candidates into the puzzle.</p>
<p>I had also tried to learn new techniques by reading tutorials on how the different strategies work. But as usual it is hard to turn theory into practice. Even when you have understood the principle, you do not find the pattern in the puzzle when you are actually trying to solve it.</p>
<p>That was when I thought of an app that could help you, but in levels: a small first nudge in the right direction. If that is not enough, you can get one more hint.</p>

<h2>Practising what I read</h2>
<p>After reading about the different techniques, I realised that I wanted to try them, but on a puzzle where that technique was available right then. That is why I created Practice technique: you can read about a technique and then try it on a prepared puzzle.</p>
<p>At first I found it hard to get it right, even though the puzzle was prepared for the technique. I simply did not see the patterns. Frustrated, I added a Step by step guide to walk me through it. I always try to solve the puzzle myself first. When I cannot find the solution, I use Step by step to understand what I missed.</p>

<h2>How I use it myself</h2>
<p>I often look at just the hint overview, to see how many strategies are available. Most of the time I am stuck on something, and I can see that there is usually not just one possibility but several.</p>

<h2>And on paper</h2>
<p>I have solved many sudoku on paper, and I wanted the same chance to get help and to improve as I have in the app. That is why I added a mode where you can enter your own puzzle, the one you got stuck on.</p>
<p>I hope this app gives you many enjoyable moments.</p>
<p class="signoff">&mdash; Joachim Hagedorn</p>
</div>

<section class="cta">
  <h2>See how it works</h2>
  <p><a href="../how-it-works/">How it works</a> &middot; <a href="../learn/">Learn Grid9</a></p>
  <p>""" + SOON + """</p>
</section>
"""


# ---- page list -----------------------------------------------------------
page("grid9/index.html", "home", f"{APP} — learn why a move works", "A sudoku app that teaches you the solving techniques: help in small doses, reasoning drawn on the grid, and practice one technique at a time.", landing(), 1, wide=True, bare=True)
page("grid9/how-it-works/index.html", "how", f"How it works — {APP}", "How Grid9 teaches sudoku techniques: notes, the strategy panel, hints in doses, highlights, practice mode and statistics.", how_it_works(), 2, wide=True, band=True)
page("grid9/features/index.html", "features", f"Features — {APP}", "Everything in Grid9 Sudoku: two dozen techniques, step-by-step hints, practice mode, larger numbers, themes, statistics, and what is free versus Premium.", features(), 2, wide=True, band=True)
page("grid9/privacy/index.html", "privacy", f"Privacy Policy — {APP}", "How Grid9 Sudoku handles your data.", PRIVACY, 2)
page("grid9/terms/index.html", "terms", f"Terms of Use — {APP}", "Terms of use and subscription terms for Grid9 Sudoku.", TERMS, 2)
page("grid9/support/index.html", "support", f"Support — {APP}", "Support and frequently asked questions for Grid9 Sudoku.", SUPPORT, 2)

page("grid9/why/index.html", "why", f"Why I made Grid9 — {APP}", "A few words from the developer on why Grid9 Sudoku exists: pencil and paper, the moment you get stuck, and an app that helps in small steps.", why_page(), 2, wide=True, band=True)
page("grid9/learn/index.html", "learn", f"Learn Grid9 — guides — {APP}", "Five short guides to Grid9 Sudoku: solving routine, learning a technique, app features, custom puzzles and statistics.", learn_index(), 2, wide=True, band=True)
page("grid9/learn/solving-routine/index.html", "learn", f"Solving routine — {APP}", "A personal sudoku solving routine with Grid9: scan, note, check the hint overview, ask for help in steps and clean up, as a loop.", solving_routine(), 3, wide=True, band=True)
page("grid9/learn/learning-a-strategy/index.html", "learn", f"Learning a strategy — {APP}", "How to learn one new sudoku technique on purpose: read the explanation, think it through, practise on real puzzles, use Step by step and mark the pattern yourself.", learning_strategy(), 3, wide=True, band=True)
page("grid9/learn/app-features/index.html", "learn", f"App features — {APP}", "A walk through the Grid9 screen and menu: Snyder notes and auto candidates, the hint panel, the step ladder, practice mode, multi-select and settings.", app_features(), 3, wide=True, band=True)
page("grid9/learn/custom-puzzles/index.html", "learn", f"Custom puzzles — {APP}", "How to type in a sudoku from paper or another app and use Grid9's notes, Fill auto and hint ladder on it.", custom_puzzles(), 3, wide=True, band=True)
page("grid9/learn/statistics/index.html", "learn", f"Statistics — {APP}", "What Grid9 tracks for every solve: time, mistakes, hints, streaks, personal bests and which techniques you found yourself, peeked at, or used via a hint.", statistics(), 3, wide=True, band=True)

# Which media do the pages currently ask for? -> assets/img/README.md
_seen, _lines = set(), []
for kind, name, alt in REQUESTED_MEDIA:
    if (kind, name) in _seen:
        continue
    _seen.add((kind, name))
    _lines.append(f"| {name} | {'screen recording (.mp4)' if kind == 'video' else 'screenshot (.png/.webp)'} | {alt} |")
(ROOT / "assets" / "img").mkdir(parents=True, exist_ok=True)
(ROOT / "assets" / "img" / "README.md").write_text(
    "# Media the pages ask for\n\nGenerated by build_pages.py. Put a file with the given base name in `assets/img/` "
    "(screenshots) or `assets/video/` (recordings, mp4) and re-run the script; until then a placeholder is shown.\n\n"
    "| Name | Type | What it should show |\n|---|---|---|\n" + "\n".join(_lines) + "\n", encoding="utf-8")
print("media requested:", len(_lines))


# ------------------------------------------------- site root + Pages files
ROOT_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hagedorn Works</title>
<meta name="description" content="Apps by Joachim Hagedorn. Grid9 Sudoku: a sudoku app that teaches you the techniques, not just the grid.">
<link rel="stylesheet" href="assets/site.css">
</head>
<body class="marketing">
<header class="site">
  <div class="wrap">
    <a class="brand plain" href="./">Hagedorn Works</a>
    <nav class="site">
      <a href="grid9/">Grid9 Sudoku</a>
      <a href="grid9/support/">Support</a>
    </nav>
  </div>
</header>
<main>
<section class="dhero dband">
  <div class="wrap dwrap">
    <p class="dkicker">Apps</p>
    <h1>Hagedorn Works</h1>
    <p class="dlead">Apps by Joachim Hagedorn.</p>
  </div>
</section>
<div class="wrap dafter">
  <a class="dapp" href="grid9/">
    <div class="dapp-text">
      <p class="dwm" aria-label="Grid9">GRID<b>9</b></p>
      <h2>Learn <em>why</em> a move works, not just where it goes.</h2>
      <p>A sudoku app that teaches you the solving techniques. Ask for help in small doses, see the reasoning on the grid, and practise one technique at a time.</p>
      <p><span class="btn">See Grid9 Sudoku &rarr;</span></p>
      <p class="dfine">For iPhone and iPad &middot; Coming soon to the App Store</p>
    </div>
    <img class="dapp-img" src="assets/img/overview.webp" alt="Grid9 Sudoku showing the hint overview with the techniques that have a hit" loading="lazy">
  </a>
</div>
</main>
<footer class="site">
  <div class="wrap">
    <p>&copy; 2026 Joachim Hagedorn &middot; <a href="grid9/privacy/">Privacy</a> &middot; <a href="grid9/terms/">Terms</a> &middot; <a href="mailto:%s">%s</a></p>
  </div>
</footer>
</body>
</html>
""" % (EMAIL, EMAIL)

(ROOT / "index.html").write_text(ROOT_PAGE, encoding="utf-8")
(ROOT / "CNAME").write_text("hagedornworks.se\n", encoding="utf-8")
(ROOT / ".nojekyll").write_text("", encoding="utf-8")
print("wrote index.html, CNAME, .nojekyll")
