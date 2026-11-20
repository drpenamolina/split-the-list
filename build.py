#!/usr/bin/env python3
"""Builds the public, standalone Split page (index.html) from the Apps Script sources.

The Apps Script project stays the single source: this inlines Rounds.html where Split.html
includes it and drops the "← My Beds" link. Outside Apps Script, Split turns off the
My Beds features on its own (GAS is false). Run: python3 build.py  (then commit and push).
"""
import pathlib, re, sys
here = pathlib.Path(__file__).resolve().parent
src = here.parent / "apps-script"
split = (src / "Split.html").read_text()
rounds = (src / "Rounds.html").read_text()
inc = "<?!= HtmlService.createHtmlOutputFromFile('Rounds').getContent() ?>"
assert split.count(inc) == 1, "Rounds include not found"
out = split.replace(inc, rounds)
out, n = re.subn(r'\s*<a class="back" href="<\?= url \?>"[^>]*>.*?</a>', "", out)
assert n == 1, "My Beds link not found"
left = re.findall(r"<\?.*?\?>", out)
if left: sys.exit("Unresolved Apps Script scriptlets: %s" % left)
(here / "index.html").write_text(out)
print("index.html written (%d KB)" % (len(out) // 1024))
