# Research: Room-level phone localization from its own speaker and mic (ultrasonic chirps, no beacons)
Budget: Standard, 11 searches and 3 page reads used. One of those reads (the arXiv PDF) failed to parse, so I read the same paper through its ar5iv HTML copy.

## Claim tested
No prior work localizes a phone at room level using only its built-in speaker and microphone (active ultrasonic probing), with no installed beacons.

## What would falsify it (stated before searching)
A paper, patent, or product where an unmodified phone emits sound, records the echo or reverberation, and infers which room it is in, with no external hardware.

## Closest existing work
| Source (dated) | Type | Mechanism | How close | Gap vs. the claim |
|---|---|---|---|---|
| [Song, Gu, Tan, "Deep Room Recognition Using Inaudible Echos", IMWUT 2018](https://ar5iv.arxiv.org/html/1809.00531) (read directly) | Peer-reviewed paper | A 2 ms 20 kHz chirp every 100 ms, recorded in a 19.5–20.5 kHz band. A CNN classifies the echo spectrogram. | **Essentially identical.** | Classification runs on a cloud GPU. It needs per-room training. It was tested on one phone model, a Samsung S7. |
| RoomSense, Rossi et al., AH 2013 (not read; described only via the 2018 paper) | Paper | MLS wideband probe, MFCC features, SVM classifier. | Same idea, earlier. | The probe covers a wide spectrum, including audible frequencies, so it is not ultrasonic. The 2018 authors call it the only prior active acoustic room-recognition system. |
| [EchoTag, Tung & Shin, MobiCom 2015](https://old.sigmobile.org/mobicom/2015/papers/p525-tungA.pdf) (seen only through search summaries) | Paper | Speaker emits sound and the mic reads reflections, giving a fingerprint for a spot. | Same sensing, but it tags positions at about 1 cm resolution, not rooms. | Requires the phone to be stationary. It is reportedly sensitive to environment changes. |
| [EchoLoc, NTU](https://www.ntu.edu.sg/scale/research-capabilities/research-highlights/infrastructure-free-smartphone-indoor-localization-using-room-acoustic-responses) (project page, not read in depth) | Research prototype, with a tech-licensing page | 15–20 kHz chirps and a cloud DNN. | Same mechanism, finer granularity. Reported 95% recall in a large public space and sub-meter error in an office. | These are the team's own claims. |
| [Echoic-feature SLAM, SenSys 2022](https://deepai.org/publication/indoor-smartphone-slam-with-learned-echoic-location-features) (search summary) | Paper | Near-inaudible chirps plus IMU, with learned echo features for loop closure. | Adjacent. | It is a SLAM system, not a room classifier. |
| [US11567195B2, Sonitor, priority 2018-01-29, granted 2023-01-31, listed active](https://patents.google.com/patent/US11567195) (read; claims not read) | Granted patent | The phone's own speaker and mic capture a room response trace, which is compared to a modeled trace to find location. | **The Summary describes exactly this.** | I could not read the claims, and the description also covers fixed-transmitter embodiments. Whether claim 1 needs external transmitters is unconfirmed. |
| US9209909 (search summary only) | Patent | A mobile unit emits a signal and uses the direct-path-to-echo delay. | Adjacent. | Gives ranging to a reflector, not room identity. |
| Smart-device radar location tagging, US12210086 (a patent whose title, and no more, appeared in search results) | Patent | Location tagging by smart-device radar. | Unverified. | Not read. |

## Strongest counter-evidence
The claim is false as stated.

- **Academic layer:** Song et al. 2018 reports 99.7% accuracy over 22 rooms and 97.7% over 50 rooms. Both figures come from a source I read directly. They use only the phone's speaker and mic, with no infrastructure.
- **Patent layer:** Sonitor's US11567195B2 covers phone-only room-response matching, and Google Patents lists it as active.
- **Products layer:** I found no shipped phone-only product doing this. The only commercial hit was an unrelated Bang & Olufsen "RoomSense" speaker-calibration feature.

## Verdict
**Killed** for a claim of general novelty, with high confidence. The mechanism has published prior art from 2013 and 2018, plus a granted patent. A narrower claim might survive. The papers' own limitations point to the gaps:
- **Robustness to ambient music.** In the 2018 paper, music in every room dropped accuracy from 100% to 81%.
- **Phone orientation.** Leave-one-orientation-out accuracy was 64%.
- **Crowded spaces.** The crowded-museum test reached 89%, against 99% when quiet.
- **Cross-device generalization.** The 2018 paper did not address it in the portion I read.
- **On-device inference.** The prior systems classify in the cloud.
- **Training-free operation.** The prior systems need a labeled walk through each room.

## Open questions
- What does US11567195B2 claim? If you plan to build on this, a freedom-to-operate check against the claims is needed.
- Did any 2023–2026 work address cross-device robustness or on-device inference? My two searches for recent work returned only 2018–2022 papers, so I can't say. Nothing in the results rules such work out.
- RoomSense, EchoTag and EchoLoc were not read in full. Their descriptions above are single-sourced from search summaries.
- I did not check Espacenet, WIPO or CPC-class searches. The patent coverage is shallow.
- Did the 2018 paper test furniture changes or time drift? Its results were cut off in my read.

## Sources
**Papers**
- [Deep Room Recognition Using Inaudible Echos (2018)](https://ar5iv.arxiv.org/html/1809.00531)
- [EchoTag (2015)](https://old.sigmobile.org/mobicom/2015/papers/p525-tungA.pdf)
- [Indoor Smartphone SLAM with Learned Echoic Location Features (2022)](https://deepai.org/publication/indoor-smartphone-slam-with-learned-echoic-location-features)
- [RoomSense, ETH record (2013, metadata only)](https://www.research-collection.ethz.ch/items/56f55356-efe6-469b-85d0-cfa7cbd8d294)

**Patents**
- [US11567195B2](https://patents.google.com/patent/US11567195)
- [US9829577, Active indoor location sensing](https://patents.google.com/patent/US9829577)
- [US9209909](https://patents.justia.com/patent/9209909)

**Other (weaker)**
- [NTU EchoLoc research highlight](https://www.ntu.edu.sg/scale/research-capabilities/research-highlights/infrastructure-free-smartphone-indoor-localization-using-room-acoustic-responses)