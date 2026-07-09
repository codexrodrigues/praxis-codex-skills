# Screenshot Review Checklist

Use this before finalizing visual UI work.

## Required Captures

Capture at least:

- desktop viewport representative of the target user
- narrow/mobile or tablet-width viewport when the surface can be resized
- open overlay/dropdown/menu state when the change affects overlays
- empty, selected, invalid, or busy state when relevant
- long-content or high-volume state when the component supports repeated items
- readonly or permission-limited state when relevant

If any capture is not feasible, state why.

Use only official repo routes, ports, origins, scripts, and browser validation flows. If they are not discoverable, do not improvise a replacement; report the gap and use static review.

## Review Questions

Ask these from the screenshot, not from code intent:

1. What does the eye see first?
2. Is that the correct primary task or state?
3. Can the selected entity be identified immediately?
4. Can the primary action be identified immediately?
5. Are secondary actions quieter but still discoverable?
6. Are labels, values, helper text, and errors visually distinct?
7. Are there unnecessary boxes, borders, or nested panels?
8. Is any overlay clipped or visually detached from its trigger?
9. Does spacing express grouping without needing extra dividers?
10. Does the narrow viewport preserve task flow?
11. Can the selected object be identified by name, type, and status?
12. Are dirty, invalid, saving/applying, readonly, and permission states visible when relevant?
13. Would a keyboard user know where focus is and what happens next?
14. Are compact controls stranded in wide empty rows?
15. Do full-width fields deserve their width because of content length, preview, or workflow importance?
16. Do row breaks and column spans reflect related editing tasks?
17. For each awkward row, what is the intended redistribution: full-width, paired medium fields, compact cluster, dependent inline group, or advanced section?
18. Does the first viewport give the largest meaningful region to the primary work surface?
19. Does the selected entity remain visible while editing long inspectors or details?
20. Do equivalent inline chip affordances, especially clear/close icon buttons, use consistent target size, background treatment, icon color, hover/focus state, and theme contrast across selected fields?
21. For inline chips with more than one suffix action, do clear, dropdown/toggle, and decorative icons have reserved space without overlap, redundant affordances, or unnecessary width?
22. When an inline component computes its own width, is any host shell, filter bar, grid minimum, or global Material override forcing a wider visual size than the component needs?

## Iteration Rule

If the screenshot still looks crude, do not finish. List the top three defects, name the concrete redistribution or primitive replacement for each layout defect, fix the highest-impact one first, then recapture.

Stop only when remaining defects are either out of scope, blocked by a canonical dependency, or explicitly accepted as follow-up debt.

## Final Evidence

Report:

- route and official origin/port used
- viewport sizes
- states captured
- browser/screenshot tool used
- build/spec/e2e validation run
- validation skipped and exact reason
- visual defects fixed
- residual visual risk
