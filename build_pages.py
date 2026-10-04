#!/usr/bin/env python3
"""Generator for the static Grid9 pages (legal pages + marketing pages). Output is plain HTML
(no build step needed on the server); this script is just a convenience so
the shared header/footer isn't copy-pasted by hand four times. Safe to delete
after the pages are generated, or keep to regenerate after edits."""
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "support@hagedornworks.se"
UPDATED = "4 October 2026"

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
    <a class="brand" href="{home}">{app}</a>
    <nav class="site">
      <a href="{p}how-it-works/"{c_how}>How it works</a>
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
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    if found:
        return f'<figure class="shot"><img src="{base}{found}" alt="{alt}" loading="lazy">{cap}</figure>'
    return (f'<figure class="shot ph"><div class="ph-inner"><span>Screenshot</span>'
            f'<b>{name}</b><small>{alt}</small></div>{cap}</figure>')


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


def page(path, key, title, description, body, depth, wide=False):
    # depth = number of directory levels below the site root (landing=1, subpages=2)
    prefix = "./" if depth == 1 else "../"
    cur = ' aria-current="page"'
    html = TEMPLATE.format(
        title=title,
        description=description,
        css="../" * depth + "assets/site.css",
        home="./" if depth == 1 else "../",
        p=prefix,
        app=APP,
        body_class="marketing" if wide else "legal",
        c_how=cur if key == "how" else "",
        c_features=cur if key == "features" else "",
        c_privacy=cur if key == "privacy" else "",
        c_terms=cur if key == "terms" else "",
        c_support=cur if key == "support" else "",
        body=body,
        email=EMAIL,
    )
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




# ================================================================ marketing
SOON = '<span class="btn disabled" aria-disabled="true">Coming soon to the App Store</span>'


def landing():
    d = 1
    return f"""
<section class="hero">
  <div class="hero-text">
    <h1>Learn <em>why</em> a move works &mdash; not just where it goes.</h1>
    <p class="lead">{APP} is a sudoku app that teaches you the solving techniques. Ask for help in small doses, see the reasoning on the grid, and practise one technique at a time on puzzles built for it.</p>
    <p>{SOON}</p>
    <p class="fine">For iPhone and iPad. No account, no ads, no tracking.</p>
  </div>
  {loop(d, "hero", "A hint walking through a technique on the sudoku grid")}
</section>

<section class="grid3">
  <div class="card">
    <h3>Help in doses</h3>
    <p>Stuck? Start with <em>Where?</em> &mdash; the mildest nudge. Only ask for <em>Which cells?</em> and <em>Why?</em> if you still need them. You decide how much to be told.</p>
  </div>
  <div class="card">
    <h3>See the reasoning</h3>
    <p>Every hint is drawn on the grid: a solid outline for the pattern, a dashed outline and a struck-through digit for what can be removed. Step-by-step mode walks a chain one link at a time.</p>
  </div>
  <div class="card">
    <h3>Practise one technique</h3>
    <p>Pick a technique from the library, read how it works, then solve a puzzle that actually needs it. Two dozen techniques, from Naked Singles to Jellyfish.</p>
  </div>
</section>

<section class="split">
  {shot(d, "landing-strategy-panel", "The strategy panel listing techniques that have a hit right now")}
  <div>
    <h2>Know what to look for</h2>
    <p>Tap Hint and the strategy panel lists every technique that has a hit in the current position, with how many. It is the answer to &ldquo;what can I do here?&rdquo; &mdash; without giving the move away.</p>
    <p><a href="how-it-works/">See how it works &rarr;</a></p>
  </div>
</section>

<section class="split flip">
  <div>
    <h2>Comfortable to play</h2>
    <p>Larger numbers for easier reading, optional row/column/box highlighting, light and dark themes, undo and redo, and your own notes or automatic candidates &mdash; whichever way you like to work.</p>
    <p><a href="features/">All features &rarr;</a></p>
  </div>
  {shot(d, "landing-large-numbers", "The grid with larger numbers enabled")}
</section>

<section class="cta">
  <h2>Reading is always free</h2>
  <p>Playing puzzles and reading about every technique costs nothing. Premium adds practising techniques on real puzzles, the full hint walkthroughs and entering your own puzzles &mdash; with a free trial for new subscribers.</p>
  <p>{SOON}</p>
</section>
"""


HOW_STEPS = [
    dict(
        n="1", title="Your notes, or automatic ones",
        img="how-notes", alt="A cell showing amber Snyder notes next to a cell showing grey automatic candidates",
        text="""
<p>Grid9 has two kinds of candidates, and you can use either or both.</p>
<ul>
<li><strong>Your own notes (amber).</strong> Press a number in the <em>Cand</em> column to note it. These are Snyder-style marks: you only write a number where it has at most two or three places left in a row, column or box. They work completely on their own &mdash; you never have to touch the automatic fill.</li>
<li><strong>Automatic candidates (grey).</strong> <em>Fill auto</em> adds every number that is still legal in each cell, based on the values already placed.</li>
</ul>
<p class="note">Good to know: Fill auto never removes candidates using a technique. To eliminate with a technique, you run it from the strategy panel &mdash; that is where the learning happens.</p>
""",
        example="A cell where your notes say <b>1, 7</b> but automatic candidates would show <b>1, 3, 7, 8, 9</b>.",
    ),
    dict(
        n="2", title="See what is available",
        img="how-panel", alt="The strategy panel listing Naked Single 5, Hidden Single 2, Naked Pair 1",
        text="""
<p>Tap <em>Hint</em> and a panel slides up from the bottom, with the grid still visible above it. It lists only the techniques that have a hit <em>right now</em>, with a count.</p>
<p>That makes the list an answer to &ldquo;what can I do here?&rdquo; &mdash; you see that a Naked Pair exists, and how many Naked Singles, without being told where.</p>
""",
        example="<b>Naked Single</b> 5 &middot; <b>Hidden Single</b> 2 &middot; <b>Naked Pair</b> 1",
    ),
    dict(
        n="3", title="Help in doses",
        img="how-ladder", alt="The step ladder with Where?, Which cells?, Why? and an Apply button",
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
        video="how-ladder",
    ),
    dict(
        n="4", title="Reading the highlights",
        img="how-highlights", alt="A pattern outlined with solid frames and an eliminated candidate with a dashed frame and strikethrough",
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
        img="how-practice", alt="The practice view with Explanation and Step by step buttons above the step ladder",
        text="""
<p>Open the technique library, choose a technique, and Grid9 gives you a puzzle where it is needed. Two extra buttons appear above the step ladder:</p>
<ul>
<li><strong>Explanation</strong> &mdash; the full write-up of the technique, with diagrams. Reading it is always free.</li>
<li><strong>Step by step</strong> &mdash; walks the exact reasoning chain one link at a time, forwards or backwards, instead of only showing the end result. Lost the thread? Step back and watch it again.</li>
</ul>
""",
        example="",
        video="how-practice",
    ),
    dict(
        n="6", title="Faster input, your own puzzles, your progress",
        img="how-more", alt="Dragging across several cells to select them, and the statistics view",
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
  <p><a href="../features/">See the full feature list &rarr;</a></p>
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


# ---- page list -----------------------------------------------------------
page("grid9/index.html", "home", f"{APP} — learn why a move works", "A sudoku app that teaches you the solving techniques: help in small doses, reasoning drawn on the grid, and practice one technique at a time.", landing(), 1, wide=True)
page("grid9/how-it-works/index.html", "how", f"How it works — {APP}", "How Grid9 teaches sudoku techniques: notes, the strategy panel, hints in doses, highlights, practice mode and statistics.", how_it_works(), 2, wide=True)
page("grid9/features/index.html", "features", f"Features — {APP}", "Everything in Grid9 Sudoku: two dozen techniques, step-by-step hints, practice mode, larger numbers, themes, statistics, and what is free versus Premium.", features(), 2, wide=True)
page("grid9/privacy/index.html", "privacy", f"Privacy Policy — {APP}", "How Grid9 Sudoku handles your data.", PRIVACY, 2)
page("grid9/terms/index.html", "terms", f"Terms of Use — {APP}", "Terms of use and subscription terms for Grid9 Sudoku.", TERMS, 2)
page("grid9/support/index.html", "support", f"Support — {APP}", "Support and frequently asked questions for Grid9 Sudoku.", SUPPORT, 2)

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
