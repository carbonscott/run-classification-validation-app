# Experiment cxi101365424 - Logbook Analysis

**Total runs with logbook entries**: 39

## Run-by-Run Activities

### Run 1
**Duration**: 38.5 seconds
**Total entries**: 12 (4 unique)
**Activities**:
- DARK
- Confirmed MR2L0 and MR1L0 are at common trajectory with XCS
- Requested bypass link node 40, card 3, channel 9 and card 2, channel 7 for SC2 in air/He
- Bypass expiring Saturday evening, 6:30 PM

**Run classification**: calibration_run
**Confidence**: high
**Key evidence**: DARK measurement and bypass configuration for SC2

### Run 2
**Duration**: 3.0 minutes
**Total entries**: 30 (10 unique)
**Activities**:
- DARK
- Beam on DG1 YAG before repointing
- Beam on DG1 YAG after repointing -25 micron in Y, -30 in X
- Z motor positions at which YAG is in focus
- Beam on IP YAG with old crosshairs, pointing came back to nearly identical place!
- Pointing on YAG with new crosshairs
- Beam going through JF at full T (note pedestal: still warming up)
- Zyla with grating, showing XCS monochromator
- KB2 mirror positions, trying to reproduce values from commissioning
- WFS recording. Offset in focus position very similar to commissioning but note that the focus position has been changed (likely change on the side of software)

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: Multiple beam pointing activities, YAG focus, KB2 mirror positioning, and WFS recording

### Run 3
**Duration**: 2.4 minutes
**Total entries**: 12 (4 unique)
**Activities**:
- WFS recording
- Sarah and Gabby need another 10 min for first sample, will try quick wire scan to confirm focus
- Motor settings for scanning samples
- Not seeing clear enough signal on WFS for 1e-3 T wire scan. Taking new peds

**Run classification**: alignment_run
**Confidence**: medium
**Key evidence**: WFS recording and wire scan for focus confirmation

### Run 4
**Duration**: 2.4 minutes
**Total entries**: 21 (7 unique)
**Activities**:
- DARK
- Fluence significantly lower, due to multiplexing with XCS. Need to use 1e-3 T to see anything on Zyla
- Water leak in Klystron, 10 - 15 min estimated downtime
- AUX settings for wire scan: set SM and SF to NO_ALARM. Set back to MINOR when done and ready to continue with sample scan
- Motor settings wire scan
- ACR put in a different station, pulse energy came back very nicely, no tuning needed
- Pointing on DG1 YAG still looks good

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: Motor settings for wire scan and beam pointing verification on DG1 YAG

### Run 5
**Duration**: 3.8 minutes
**Total entries**: 12 (4 unique)
**Activities**:
- Vertical knife edge scan upstream, 5 mm, 1e-3 T RE(bp.daq_dscan([],x.sam_y,-0.01,0.010,101,events=10,record=True))
- Vertical wire scan, 10 mm upstream. Seeing strange wire artifcats, so took a bit more distance. 5e-3 T used to be able to see anything on the Zyla RE(bp.daq_dscan([],x.sam_y,-0.01,0.010,101,events=10,...
- 10 mm upstream may not have been 10 mm, not getting the wire back into focus
- May have been closer to 7 mm

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: Vertical knife edge scan and wire scan for beam characterization

### Run 7
**Duration**: 3.9 minutes
**Total entries**: 3 (1 unique)
**Activities**:
- Vertical wire scan, 10 mm downstream. Profile looks much better now, melting the wire at 7 mm distance after all? In [13]: RE(bp.daq_dscan([],x.sam_y,-0.01,0.010,101,events=10,record=True))

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: Vertical wire scan for beam profile measurement

### Run 8
**Duration**: 3.9 minutes
**Total entries**: 30 (10 unique)
**Activities**:
- Horizontal scan, upstream, 10 mm, 5e-3 T In [15]: RE(bp.daq_dscan([],x.sam_x,-0.01,0.010,101,events=10,record=True))
- We see that the wire did not come back into focus when we moved back the Z motor. This will influence the accuracy of our wire scans significantly. Motor settings for this Z motor were not changed
- Is it because we are too close to the Z motor limit?
- Going in +Z does seem to be rather reproducible, so think we are trying to go too far upstream. Next try we will go to lower T
- Cannot seem to hit the wire horizontally
- Going to lower transmission and stay closer to the wire
- Going to change back all motor settings to what we used for scan yesterday, don't like reproducibility with only some of the settings changed
- Z position with best focus on wire
- Changing to 5 mm delta, 10 mm seems to affect Z motor reproducibility
- Reduced transmission, averaging over 2 shots

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: Horizontal wire scan and focus position determination

### Run 9
**Duration**: 4.6 minutes
**Total entries**: 12 (4 unique)
**Activities**:
- Going to repeat series of wire scans. Lower transmission, changed AMI1 settings to average for better view, updated motor settings, now taking smaller Z steps (possible because of lower T) RE(bp.daq_d...
- Still seeing focus change. Going to try 2e-4 T and even smaller steps
- New best Z
- Waiting for XCS to repoint

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: Repeated wire scans with adjusted transmission and motor settings

### Run 10
**Duration**: 4.6 minutes
**Total entries**: 6 (2 unique)
**Activities**:
- Going to repeat series of wire scans, again. Now using 5e-4 T, moved 3 mm upstream. RE(bp.daq_dscan([],x.sam_x,-0.01,0.010,101,events=10,record=True))
- We had Z motor reproducibility issues at least twice. I made sure not to get too close to the motor limit, but even then we had a few 100 microns offset in the middle of a scan. Will double check moto...

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: Wire scans with adjusted transmission and position to address motor reproducibility issues

### Run 11
**Duration**: 4.7 minutes
**Total entries**: 5 (2 unique)
**Activities**:
- Horizontal scan, now 3 mm downstream In [21]: RE(bp.daq_dscan([],x.sam_x,-0.01,0.010,101,events=10,record=True))
- So far motor came back each time, seems the motor is happier with 3 mm step vs 5 or 10

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: Horizontal scan with adjusted motor step size

### Run 12
**Duration**: 4.2 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- Moved 3 mm upstream, vertical scan In [23]: RE(bp.daq_dscan([],x.sam_y,-0.01,0.010,101,events=10,record=True))

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: Vertical scan after upstream movement

### Run 13
**Duration**: 4.1 minutes
**Total entries**: 10 (5 unique)
**Activities**:
- Moved 3 mm downstream, vertical scan In [25]: RE(bp.daq_dscan([],x.sam_y,-0.01,0.010,101,events=10,record=True))
- Fitting the wire scans shows beam size is 2.19 um X upstream, 2.13 um X downstream, 3.69 Y upstream, 4.07 um downstream. We are spot on horizontally. Will move vertical focus 150 um downstream using W...
- WFS before adjusting vertical mirror pitch
- KB2 mirror positions before changing vertical mirror pitch
- Overlapped vertical and horizontal, leading to vertical moving downstream by about 150 um (helping to remove small astigmatism identified in wire scan). RMS did not significantly change

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: Vertical scan and beam focus adjustment based on wire scan results

### Run 14
**Duration**: 2.2 minutes
**Total entries**: 10 (5 unique)
**Activities**:
- WFS recording with new VFM pitch motor position
- New KB2 mirror positions
- Latest Z motor position in which wire is in focus
- Changing to 120 Hz rate, taking Zyla out of partition
- Moving detector to 82 mm distance, Z = -495

**Run classification**: alignment_run
**Confidence**: high
**Key evidence**: WFS recording with new VFM pitch and detector positioning

### Run 15
**Duration**: 2.4 minutes
**Total entries**: 8 (4 unique)
**Activities**:
- DARK
- ============================================================ KNIFE-EDGE TEST ANALYSIS SUMMARY ============================================================ Generated: 2025-06-27 09:59:36 Experiment: cx...
- Void run 16, no X-ray
- Scattering from He chamber with 1e-3 T, seeing some shadow, probably from metal frame

**Run classification**: calibration_run
**Confidence**: high
**Key evidence**: DARK measurement and knife-edge test analysis

### Run 17
**Duration**: 1.8 minutes
**Total entries**: 4 (2 unique)
**Activities**:
- Fly scan with 1e-3 T
- Scan only seeing 13 events?

**Run classification**: test_run
**Confidence**: medium
**Key evidence**: Fly scan with transmission setting and issues with event recording

### Run 18
**Duration**: 1.5 minutes
**Total entries**: 8 (4 unique)
**Activities**:
- DAQ again not recording
- Void run 19, troubleshooting DAQ
- Failing DAQ node
- First real run, except for that I forgot to hit the record button :)

**Run classification**: test_run
**Confidence**: high
**Key evidence**: DAQ troubleshooting and recording issues

### Run 20
**Duration**: 14.4 minutes
**Total entries**: 8 (4 unique)
**Activities**:
- First real run, now with data being recorded! Starting at 1e-3 T, will slowly ramp up
- x.dumbSnake(xStart=9.5,xEnd=39.1, yDelta=0.04, zStart=-1.376 , zEnd=-1.376 , nRoundTrips=300, sweepTime=3)
- Seeing mostly salt diffraction. Staying at 20% T for now. Confirmed that shadowing is indeed coming from the metal frame
- This sample seems a bit salty, haven't really seen protein diffraction yet. Gabby working on getting a new sample ready, this one has probably been hanging around for too long

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: First real data collection run with transmission ramping and snake scan pattern

### Run 21
**Duration**: 5.4 minutes
**Total entries**: 30 (15 unique)
**Activities**:
- First sample, stuck on 20% T because of salt crystals x.dumbSnake(xStart=9.5,xEnd=39.1, yDelta=0.04, zStart=-1.376 , zEnd=-1.376 , nRoundTrips=25, sweepTime=3)
- <1 um crystal, proteinase K, did not see diffraction (other than salt) unfortunately. Probably dried out
- New sample, proteinase K, again <1 um, starting at 20% T x.dumbSnake(xStart=9.5,xEnd=39.1, yDelta=0.04, zStart=-1.376 , zEnd=-1.376 , nRoundTrips=25, sweepTime=3)
- Another scan on same sample, now with X position offset, because we were hitting the metal, creating strong Bragg peaks. Starting at 20% T, will see if we can slowly ramp up x.dumbSnake(xStart=9.8,xEn...
- Now at 50% T
- Seeing some shadow from the sample holder
- Sarah's guess is 800 - 900 nm for these crystals
- Full transmission! Same proteinase K sample x.dumbSnake(xStart=9.8,xEnd=39.3, yDelta=0.04, zStart=-1.376 , zEnd=-1.376 , nRoundTrips=25, sweepTime=3)
- Beautiful!
- Beautiful diffraction
- Stopping run briefly, need to readjust X, seeing metal again
- We see the holes getting punched in the membranes!
- Resuming run, now with X slightly offset x.dumbSnake(xStart=9.5,xEnd=39.0, yDelta=0.04, zStart=-1.376 , zEnd=-1.376 , nRoundTrips=25, sweepTime=3)
- Adjusting X again. Noticing that as we go down, we see the shadow of the sample holder move up, as expected. Likely helium scatter from upstream of the sample holder
- Failing node

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Multiple sample measurements of proteinase K crystals with diffraction data collection

### Run 34
**Duration**: 49.5 seconds
**Total entries**: 6 (3 unique)
**Activities**:
- DARK
- Server that keeps having issues: cxi-daq:~> netconfig search 172.21.26.66 ioc-cxi-cam2-fez: subnet: fez-cxi.pcdsn Ethernet Address: d8:5e:d3:87:a2:7c IP: 172.21.26.66 Contact: uid=oter1234,ou=People,d...
- Rotation stage value at which both top and bottom are in focus. Encoded?

**Run classification**: calibration_run
**Confidence**: medium
**Key evidence**: DARK measurement and server troubleshooting

### Run 35
**Duration**: 5.3 minutes
**Total entries**: 18 (9 unique)
**Activities**:
- Now also scanning in Z. 20%T on large proteinase K samples x.dumbSnake(xStart=9.5,xEnd=38.5, yDelta=0.04, zStart=-0.217, zEnd=-0.617, nRoundTrips=25, sweepTime=3)
- Starting run 35: new sample, larger proteinase K samples. 5 - 15 um
- Increased to 50% T
- Switching to full T
- Found out we can shots in membrane for focusing really nicely x.dumbSnake(xStart=9.5,xEnd=38.5, yDelta=0.04, zStart=-1.017, zEnd=-0.617, nRoundTrips=25, sweepTime=3)
- Checking alignment on DG1 for XCS
- Beam before repointing
- Repointed -5 in Y, -15 in X
- No beam

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: New sample of larger proteinase K crystals with Z scanning and transmission adjustments

### Run 51
**Duration**: 5.3 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- Seeing quite a bit of salt diffraction Rbr sample x.dumbSnake(xStart=10,xEnd=38.8, yDelta=0.04, zStart=0.882, zEnd=-0.2, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Rbr sample measurement with salt diffraction observation

### Run 52
**Duration**: 5.3 minutes
**Total entries**: 6 (3 unique)
**Activities**:
- Using holes in the film for better focusing, was around 1 mm off.
- So far only measured sample at 50% T because of large number of salt crystals
- Going to swap samples, only saw salt :(

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Continued sample measurement with focus adjustment and salt crystal observation

### Run 59
**Duration**: 5.3 minutes
**Total entries**: 12 (6 unique)
**Activities**:
- Going back to proteinase K, using seeds this time x.dumbSnake(xStart=9.6,xEnd=38.3, yDelta=0.04, zStart=1.4, zEnd=2.7, nRoundTrips=25, sweepTime=3)
- Proteinase K seeds: so far no diffraction from protein
- Adjusted Z in -X direction, was off by a mm In [79]: x.dumbSnake(xStart=9.9,xEnd=38.9, yDelta=-0.04, zStart=-0.1, zEnd=2.7, nRoundTrips=25, sweepTime=3)
- We still see hits, but the focus is fluctuating in this sample. Because the chip was mounted a bit crooked, the Z offset was significant and a few cycles are skipped
- Need to take a break for Tim to test slotted foil
- N2 compressor was still running...

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Proteinase K with seeds measurement and focus adjustments

### Run 71
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- Proteinase-k nanocrystals; took T down to .5

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Proteinase-k nanocrystals measurement with transmission adjustment

### Run 72
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 10% transmission same sample

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Same sample measurement with 10% transmission

### Run 73
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 5.5% same transmission

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Same sample measurement with 5.5% transmission

### Run 74
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 1.02% transmission same sample In [93]: x.dumbSnake(xStart=9.7,xEnd=38.7, yDelta=0.04, zStart=-2.15, zEnd=-2.15, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Same sample measurement with 1.02% transmission

### Run 75
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 0.5% transmission In [94]: x.dumbSnake(xStart=9.7,xEnd=38.7, yDelta=0.04, zStart=-2.15, zEnd=-2.15, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Same sample measurement with 0.5% transmission

### Run 76
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- .1% transmission! In [95]: x.dumbSnake(xStart=9.7,xEnd=38.7, yDelta=0.04, zStart=-2.15, zEnd=-2.15, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Same sample measurement with 0.1% transmission

### Run 77
**Duration**: 5.4 minutes
**Total entries**: 4 (2 unique)
**Activities**:
- 100% transmission In [96]: x.dumbSnake(xStart=9.7,xEnd=38.7, yDelta=0.04, zStart=-2.15, zEnd=-2.15, nRoundTrips=25, sweepTime=3)
- 50% T x.dumbSnake(xStart=9.7,xEnd=38.7, yDelta=0.04, zStart=-2.35, zEnd=-2.35, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Same sample measurement with 100% and 50% transmission

### Run 79
**Duration**: 5.3 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 10%T x.dumbSnake(xStart=9.7,xEnd=38.7, yDelta=0.04, zStart=-2.35, zEnd=-2.35, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Sample measurement with 10% transmission using dumbSnake scanning pattern

### Run 80
**Duration**: 4.3 minutes
**Total entries**: 4 (2 unique)
**Activities**:
- 5% T In [99]: x.dumbSnake(xStart=9.7,xEnd=38.7, yDelta=0.04, zStart=-2.35, zEnd=-2.35, nRoundTrips=25, sweepTime=3)
- Chip finished! Another one of the proteinase K nanocrystals

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Sample measurement with 5% transmission of proteinase K nanocrystals

### Run 81
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 5% T x.dumbSnake(xStart=9.8,xEnd=39.0, yDelta=0.04, zStart=-0.65, zEnd=-0.65, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Sample measurement with 5% transmission using dumbSnake scanning pattern

### Run 82
**Duration**: 6.2 minutes
**Total entries**: 8 (4 unique)
**Activities**:
- 1% T x.dumbSnake(xStart=9.8,xEnd=39.0, yDelta=0.04, zStart=-1.05, zEnd=-1.05, nRoundTrips=25, sweepTime=3)
- Ignore run 81, forgot to change to 1% T
- Void run 84, beam down
- [Repeated 3 times: 1% T x.dumbSnake(xStart=9.8,xEnd=39.0, yDelta=0.04...]

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Sample measurement with 1% transmission using dumbSnake scanning pattern

### Run 84
**Duration**: 7.7 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 0.1% T x.dumbSnake(xStart=9.8,xEnd=39.0, yDelta=0.04, zStart=-1.25, zEnd=-1.25, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Sample measurement with 0.1% transmission using dumbSnake scanning pattern

### Run 85
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 5e-4 T x.dumbSnake(xStart=9.8,xEnd=39.0, yDelta=0.04, zStart=-1.45, zEnd=-1.45, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Sample measurement with 5e-4 transmission using dumbSnake scanning pattern

### Run 86
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 0.1% T In [108]: x.dumbSnake(xStart=9.8,xEnd=39.0, yDelta=0.04, zStart=-1.45, zEnd=-1.45, nRoundTrips=25, sweepTime=3

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Sample measurement with 0.1% transmission using dumbSnake scanning pattern

### Run 87
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 0.5% T In [109]: x.dumbSnake(xStart=9.8,xEnd=39.0, yDelta=0.04, zStart=-1.65, zEnd=-1.65, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Sample measurement with 0.5% transmission using dumbSnake scanning pattern

### Run 89
**Duration**: 5.4 minutes
**Total entries**: 2 (1 unique)
**Activities**:
- 5% T In [112]: x.dumbSnake(xStart=9.8,xEnd=39.0, yDelta=0.04, zStart=-1.85, zEnd=-1.85, nRoundTrips=25, sweepTime=3)

**Run classification**: sample_run
**Confidence**: high
**Key evidence**: Sample measurement with 5% transmission using dumbSnake scanning pattern


<!-- Processing metadata: {"processed_at": "2025-08-14T17:35:46.086672", "total_runs": 39, "total_logbook_entries": 309, "instrument": "CXI"} -->
