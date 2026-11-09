"""S3-C: ending 'Role reversal'. Save shown on screen, then RUSH passes the trauma on."""
from s3_endings import (PANELS_HEAD, LINES_HEAD, p_slump, p_max_asks, shake, make_overlay)

PANELS = PANELS_HEAD + [(12.5, 13.2, p_slump), (13.2, 15.0, p_max_asks)]
LINES = LINES_HEAD + [
    (13.25, 14.15, "Where's the final?", 110, 360),
    (14.2, 15.0, "Downloads.", 330, 400),
]
overlay = make_overlay(LINES)
