# Preparation verification

Prepared 2026-10-18 from the supplied project README and Pi backup. Only the output folder was modified. During initial preparation, no hardware scripts, API requests, installation commands, Git initialization, commits, remotes, or pushes were run. The owner subsequently authorized an initial commit and publication to the PiRobot GitHub repository. The MIT License was added following the owner’s explicit selection.

## Checks performed

- Compiled all 12 Python source texts in memory with Python `compile()`; no module imports, GPIO execution, or bytecode files were needed.
- Parsed imports with AST: both local modules resolve within the root folder; direct third-party imports are represented in requirements, with ONNX runtime explicitly listed for the selected backend.
- Checked local Markdown links, named layout files, and all nine documented diagnostic commands against actual files.
- Executed only the missing-key startup path in robot.py, test_gemini.py, and test_vision.py with the variable removed. Each exits with the expected clear error before third-party or hardware imports. No hardware/API work occurs on this path.
- Scanned every output file, including hidden files, for the actual embedded source credentials and patterns for API tokens, private keys, SSH public keys, personal paths, email addresses, local network addresses, and the source machine username. No matching credential/private-data findings remained. Values were never included in scan reports. This is a targeted static scan, not a guarantee against every possible secret format.
- Compared SHA-256 hashes of all 514 original files against the pre-copy baseline; originals and backup are unchanged.
- Used Git's untracked-file enumeration and ignore checker with disposable metadata outside the output folder. Reviewed the exact candidate list and tested ignored credential/environment/cache/log/media paths while keeping documentation and demo images visible. No `.git` directory or index was created in the output during those preparation checks; repository initialization was authorized later for publication.

## Candidate contents

The commit candidate is exactly these 26 files (24 text files and two JPEG photos):

```text
.env.example
.gitignore
LICENSE
README.md
config/README.md
config/environment.env.example
docs/configuration.md
docs/hardware.md
docs/images/fruit-box-front.jpg
docs/images/fruit-box-interior.jpg
docs/power.md
docs/verification.md
docs/wiring.md
eye_lib.py
expressions.py
requirements.txt
robot.py
test_arm_positions.py
test_camera.py
test_eyes.py
test_gemini.py
test_oled.py
test_servos.py
test_tts.py
test_vision.py
test_wakeword.py
```

## Still requires the Pi / owner decisions

No dependency installation, supported Python/ARM wheel resolution, real third-party imports, model download/inference, live Gemini availability or billing check, microphone/speaker routing, OLED/camera operation, servo motion, sensor/motor operation, power measurement, or end-to-end robot test was performed. Runtime resource limits and wake-word reliability need confirmation. The old README's hardware descriptions are historical reports, not new test results.

The owner confirms audio, camera, and servos are working, and that the robot uses wired outlet power with no batteries installed. These are owner-reported functional results, separate from the static preparation checks above. The owner reports that nothing has been pushed; no public credential exposure is established. The prepared folder contains no embedded API keys or copied private machine configuration.

The project uses MIT; third-party code/model terms remain separate. The owner confirms wall outlet → USB power brick → USB cable → Pi. Document the adapter rating, servo power and common grounds, and safe servo travel. Confirm intended Gemini model/account access, audio indexes, and compatible dependencies for new installations. This sanitized copy has not been run on the Pi; electrical measurements and end-to-end validation of this copy remain outstanding.

## Documentation media review

- Added owner-supplied front and interior prototype photos under `docs/images/`; both were visually reviewed for private information.
- Removed JPEG metadata segments from the published copies; confirmed no EXIF metadata remains and decoded image pixels exactly match the original photos. Originals in Downloads were not modified.
- Verified both README image paths and image integrity. Images use explicit display widths, with the interior photo in an expandable section.
- The terminal demo is an explicitly labeled historical text excerpt, transcribed from the original screenshot. Its private shell prompt is omitted. Neither the original identifying screenshot nor an AI-edited rendition is included in the repository.
- Historical Cosmo references in the demo preserve the actual recorded wording; current code and project naming remain fruit_box. The old Enter trigger and generated wheel dialogue are identified as historical behavior and character dialogue respectively.
