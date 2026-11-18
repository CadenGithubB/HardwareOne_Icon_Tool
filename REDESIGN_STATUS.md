# Icon redesign — completed October 21, 2026

All 87 standard icons were redrawn through the GitHub Pages editor using computer-controlled Line/Eraser strokes. Names and cells are unchanged. `redesign.mjs` holds the final pixel plans, including centered warning/info marks and a rotationally symmetric refresh pair.

Final deliverables: `~/Documents/Codex/2026-10-21/https-github-com-cadengithubb-hardwareone-icon/outputs/hardwareone-icons.zip`

Unpacked deliverables and importable PNG/JSON: the sibling `outputs/hardwareone-icons/` directory. Import `assets/iconsheet.png` together with `iconsheet.json`; leave color inversion off.

Validation: all 87 exported tiles exactly match the plans. All C++ LSB-first 128-byte bitmap arrays and all embedded PNGs decode to the same pixels. Original names and positions retained. Firmware build/hardware testing was outside this artwork task. Approved default assets pushed to main in commit e431b0c on October 21, 2026.

The browser editor does not preserve unsaved artwork across an app restart. Always export before stopping. Repository defaults, sheet, registry, and C++ exports now contain the approved replacement set. The sheet regeneration script reads the browser defaults.

Follow-up refinements: directional arrowheads taper in even pixel steps; file_json uses a semicolon; file_image has a second dot lower on the right; search uses four-pixel flat circle extrema without single-pixel nubs. Re-exported through the editor and verified all 87 icons again.

Publication: commit e431b0c pushed to origin/main at user request. GitHub Pages deployment started: https://github.com/CadenGithubB/HardwareOne_Icon_Tool/actions/runs/39606054592

October 22 expansion: all 85 requests drawn (83 new names, memory/notify_cli revised), 170 editor icons total. Source in scripts/icon-designs.mjs; saved editor PNG matches all plans. Defaults, sheet, manifest, optimized C++ synchronized. Browser export checked against optimized C++; regeneration and six firmware build/lookup variants passed. Portable integrator tested against a nested generator with reserved cells. Expansion remains local for review; no October 22 push performed. Firmware checkout remains unchanged.

Final October 22 revision: removed fingerprint, guardrail, hourglass, bolt, calendar, stopwatch, branch and model at user request. Final set 162 (75 additions, 2 revisions); 77 requests completed. All final corrected pixels match the editor export. New strokes align to 2px coverage for 16px readability. Installer removes rejected reserved slots and compacts the nested sheet. Final six host firmware variants and installed-generator tests passed. All changes remain uncommitted and unpushed at user request.

Style rebuild after user review: replaced free-form round-cap expansion strokes with square-ended integer-grid geometry; explicit symmetry constraints for chips, bug, display, microphone, etc. All 14 page/file icons now use expanded 24x28 frame at (4,2). file_video is a large camera-in-page symbol. Re-imported into the editor and byte/pixel-verified its PNG export. Symmetry/page-frame and all firmware integration tests pass. Revised delivery: outputs/hardwareone-icons-refined.zip. All work remains uncommitted/unpushed.
