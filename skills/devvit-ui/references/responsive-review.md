# Responsive Review Matrix

## Simulator-first pass

Use Reddit's [UI Simulator](https://developers.reddit.com/docs/guides/tools/ui_simulator#best-practices) as the first responsive review pass:

1. Begin in mobile view and confirm every critical feature and action is accessible before widening the viewport.
2. Add layout density and secondary enhancements progressively in desktop and fullscreen views; do not make the mobile design a compressed desktop layout.
3. Prioritize essential content, optimize images and media, and prefer a single-column mobile hierarchy where it fits the surface's fixed-height contract. Split or paginate content instead of creating inline scrolling.
4. Keep primary actions within comfortable thumb reach. Verify touch-target size, spacing between controls, and readable text without zooming.
5. Use relative units for typography and adaptable spacing, while retaining fixed values only where the Devvit surface contract genuinely requires them.
6. Test light and dark themes, including contrast, focus indicators, disabled controls, validation, overlays, and image legibility. Devvit webviews receive the user's color-scheme preference, so implement `prefers-color-scheme` or the framework's equivalent rather than a simulator-only theme switch.
7. Test every new feature in mobile view again before considering its responsive work complete.

The simulator offers mobile, desktop, fullscreen, light, and dark checks. Its color-scheme toggle does not currently work in Safari; use a Chrome-based browser for that check. Simulator success does not prove native safe areas, on-screen keyboard behavior, surrounding feed gestures, device performance, or Reddit client effects, so finish with real-client playtests.

Review every major state, not only the initial screen:

| Surface | What to inspect |
| --- | --- |
| Inline `REGULAR` | 320px fixed post height, responsive width, Reddit page can still move |
| Inline `TALL` | 512px fixed post height, responsive width, CTA remains visible |
| Mobile expanded | complete layout at the 596px safe-height fixture, real-device safe areas, touch controls, no hidden footer |
| Short/landscape | compact chrome, playable center, reachable primary action |
| Desktop expanded | complete non-fullscreen modal at the 596px height fixture, responsive width, matched borders |
| Desktop fullscreen | optional enhancement only; no feature or control depends on it |
| Loading/error | same outer dimensions, no layout jump, retry remains reachable |
| Inline results/editor | fixed row or field capacity, visible pagination, no internal scrolling |
| Mobile keyboard | focused field, validation, and primary action visible; nonessential regions collapse; layout restores on dismissal |
| Feedback states | loading, success, validation, and error feedback do not change outer dimensions or push controls |
| Light and dark themes | sufficient contrast, visible focus and state styling, legible media and overlays |

At the exact width breakpoint, compare adjacent regions pixel-for-pixel. Header, main container, footer, and overlays should agree on max width, horizontal padding, side borders, and radii.

Test long localized labels, long usernames, empty, full, and over-capacity collections, first and last pagination states, software-keyboard appearance and dismissal, zoomed text, and focus traversal. Remove duplicated titles and challenge every paragraph that consumes scarce height. Trigger every loading, success, validation, and error state and confirm that no message insertion moves the layout or hides controls. Test repeated transient messages for overlap and stacking. With the keyboard present, exercise every field and confirm that its label, validation feedback, and relevant action remain visible. Confirm that each repeated-content region in an inline or intentionally fixed composition has an explicit maximum item count and that overflow data moves to another page. Resize width independently while holding each surface's height fixture constant. If inline content cannot fit, change hierarchy, density, or page size instead of clipping it, adding scrolling, or relying on fullscreen.
