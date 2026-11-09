"""S3-B: ending 'The shadow of FINAL (29)'. Save shown on screen, then it never ends."""
from s3_endings import (PANELS_HEAD, LINES_HEAD, p_crawl, p_save29, p_shadow, p_black, shake, make_overlay)

PANELS = PANELS_HEAD + [(12.5, 13.2, p_crawl), (13.2, 13.5, p_save29),
                        (13.5, 14.7, p_shadow), (14.7, 15.0, p_black)]
LINES = LINES_HEAD
overlay = make_overlay(LINES)
