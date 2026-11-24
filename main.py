#!/usr/bin/env python3
"""Make the AI Judge Laugh: Developer Excuses (make.fun entry).

Writes one funny single-line excuse a developer gives when code breaks
in production to /output/entry.txt. The gate requires UTF-8 text of
1-200 characters, not only white space. validate() encodes the judge
brief: on-topic, a twist that reveals what really happened, dev voice
with the jargon right, fast, and fresh.
"""

import os

# The line: a developer's excuse for a production breakage. Setup repeats
# "one-line fix" twice, then the turn — the other 400 lines were not the
# fix, they were the developer proving it wasn't their fault. The excuse
# confesses what really happened: the time went on self-defence, not repair.
LINE = "It's a one-line fix. It was always a one-line fix. The other 400 lines were me proving it wasn't my fault."

# Worn-out excuses the judge brief calls stale: the field is full of them.
BANNED_PHRASES = (
    "works on my machine",
    "it worked on my machine",
    "worked on my machine",
    "it worked in staging",
    "works in staging",
    "not a bug, it's a feature",
    "it's not a bug, it's a feature",
    "turning it off and on again",
    "turn it off and on again",
    "have you tried turning it off",
    "blame the intern",
    "must be a user error",
    "probably a user error",
)

# The excuse must be about code breaking in production: fix, deploy, bug,
# production, prod, code — the subject the judge scores first.
PRODUCTION_WORDS = (
    "fix", "deploy", "bug", "production", "prod", "code", "break",
    "outage", "release", "merge",
)

# A twist needs a setup and a punch: at least two sentences, the second
# reframing the first, told in the first person — the developer confessing
# what really happened.
FIRST_PERSON = (" i ", " me ", " my ", "i'm", "i've", "i'd")


def validate(line):
    """Gate plus the judge brief, enforced before the line is written."""
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not 1 <= len(line) <= 200:
        raise ValueError("line must be 1-200 characters, got %d" % len(line))
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not line.strip():
        raise ValueError("line must not be only white space")
    if "  " in line:
        raise ValueError("line must not contain double spaces")
    lowered = line.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            raise ValueError("line uses a worn-out excuse: %r" % phrase)
    if not any(word in lowered for word in PRODUCTION_WORDS):
        raise ValueError("line must be an excuse about code breaking in production")
    # Twist: at least two sentences (setup + punch).
    sentences = [s for s in line.split(". ") if s.strip()]
    if len(sentences) < 2:
        raise ValueError("line needs a setup and a punch (at least two sentences)")
    # Dev voice: spoken in the first person, like a developer actually
    # saying it out loud.
    padded = " " + lowered + " "
    if not any(token in padded for token in FIRST_PERSON):
        raise ValueError("line must sound like a developer saying it (first person)")
    return line


def main():
    line = validate(LINE)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(line)


if __name__ == "__main__":
    main()
