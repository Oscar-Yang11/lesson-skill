# lesson-page

A [Claude Code](https://claude.com/claude-code) skill that turns "explain this to me" into a **lesson**: one self-contained web page that reads like a textbook chapter instead of a report.

Use it when you ask Claude to walk you through something it did, a method, a pipeline or a paper, and you want to come out able to retell it yourself, knowing why each step is done and where to check it.

## Why

An assistant's default explanation is a report: conclusions first, parallel sections, big tables, every number, a flow chart of ten boxes at the top. That is good for looking things up and bad for learning. The reader gets facts scattered like a web, cannot tell where each one comes from, and cannot supervise the work.

This skill makes Claude write for the reader's understanding instead:

| | Report (avoided) | Lesson (what you get) |
|---|---|---|
| Opening | Overview diagram, bullet list | One concrete scene and one question |
| Order | By step or module, in parallel | Each answer raises the next question |
| New ideas | All at once | One at a time, introduced when needed |
| Examples | A new one per section, or none | One real example carried through the whole page |
| Rules | Rule first | Example first, then the rule, then why |
| Details | All in the main text | Only what the main line needs; the rest is folded away |
| Ending | To-do list | A recap of the whole line, then the current status |

## What a lesson page looks like

- A single column of text with a progress rail that lists the section questions.
- An opening box: the question this lesson answers, up to three "after reading you can ...", reading time, prerequisites.
- Sections whose **titles are questions**. Each one starts by picking up the question the previous section ended with, shows a real example, states the rule, explains why, and closes with a short "so far" recap and the next question.
- Figures that carry the explanation, drawn from real data, each saying one thing, with what to look at marked on the figure.
- A source tag on every claim that could be doubted, collected in a table at the end. There are five kinds: *measured*, *decided by you*, *my judgement*, *literature*, *code*.
- "Think about it" questions with folded answers; prompts, pseudocode and large tables folded by default.
- A final recap diagram, which is useful only now that the reader knows every box in it.
- Self-contained HTML: inline styles, no external fonts or CDNs, light and dark themes.

## Contents

```
lesson-page/
├── SKILL.md                  the skill: what to decide before writing, the skeleton of a lesson, writing rules, the workflow
├── assets/template.html      page template with all styles inline
├── references/
│   ├── components.md         how to write each page component (goal box, section, figure, why / think / details, source tags)
│   ├── checklist.md          "be the reader once": checks to run on the screenshot before handing the page over
│   └── iterations.md         log format for user feedback, and lessons already folded back into the skill
└── scripts/shot.py           full-page screenshot, cut into parts, for the self-review step
```

The skill text is written in **Chinese** and produces Chinese pages by default. Claude follows it in any language; ask for another output language in your request if you want one.

## Install

Copy the `lesson-page` folder into your Claude Code skills directory:

```bash
git clone https://github.com/Oscar-Yang11/lesson-skill.git
cp -r lesson-skill/lesson-page ~/.claude/skills/
```

For a single project, copy it to `<project>/.claude/skills/` instead.

### Optional: the screenshot helper

The self-review step looks at a screenshot of the finished page, because overlapping labels, text running out of a box and truncated captions cannot be seen in the code. `scripts/shot.py` needs Playwright and Chromium:

```bash
pip install --target ~/.local/share/lesson-page/pw playwright
PYTHONPATH=~/.local/share/lesson-page/pw python -m playwright install chromium
```

If Chinese text shows up as boxes, install a CJK font (for example Noto Sans CJK SC) into `~/.fonts` and run `fc-cache -f`.

```bash
python ~/.claude/skills/lesson-page/scripts/shot.py <url or html file> <output dir> [width=1400]
```

## Use

Invoke it by name:

```
/lesson-page Walk me through how the labelling pipeline works, from one real example.
```

or just ask. The skill triggers on requests such as "explain this to me", "I did not follow", "show me the whole process", "walk me through", or when you say there is too much information and you have lost the thread.

What Claude then does:

1. Understands the material first, until it can tell the main line without notes.
2. Fixes three things before writing: where the reader starts, one main question with at most three "after reading you can ...", and the main line as a chain of 5 to 7 "question → answer → new question" links. Whatever is not on the chain is folded away, moved to a later lesson, or dropped.
3. Picks one real example and decides what each figure has to say before drawing it.
4. Writes the page from the template. Long topics become several lessons with an index page.
5. Takes a full-page screenshot, reads it as a reader would, and goes through the checklist.
6. Hands over the link in a few lines, without repeating the page in chat.
7. After your feedback, fixes the page and writes what generalises back into the skill.

Pages are written to `<project>/docs/lessons/<topic>/`, with figures generated by a script kept in the project so they can be regenerated.

## Adapting it

- `assets/template.html` holds every style; change colours, widths and fonts there.
- `references/iterations.md` is meant to grow: log what readers said about your lesson pages and move what generalises into `SKILL.md` or `components.md`.
- The five source kinds and the section skeleton are conventions of this skill, not requirements of Claude Code; edit `SKILL.md` to fit your own way of working.
