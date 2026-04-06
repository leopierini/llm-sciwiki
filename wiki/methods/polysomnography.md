---
type: method
title: "Polysomnography"
created: 2024-03-14
updated: 2024-03-15
tags: [sleep, EEG, recording, method]
---

# Polysomnography

## Description

Polysomnography (PSG) is the gold standard method for recording sleep physiology. It simultaneously records EEG (brain activity), EOG (eye movements), EMG (muscle tone), and often additional signals (ECG, respiration, oxygen saturation) to stage sleep and characterize sleep architecture.

## How It Works

Electrodes are placed on the scalp, face, and chin. Data is recorded continuously throughout a sleep session. Sleep stages (N1, N2, N3, REM) are scored in 30-second epochs according to standardized criteria (AASM). Specific features like [[concepts/sleep-spindles]] are detected via automated algorithms or manual scoring.

## Strengths

- Comprehensive, multi-modal sleep assessment
- Gold standard — well-validated, standardized scoring
- Allows detection of sleep architecture and specific oscillatory features

## Limitations

- Lab-based — may disrupt natural sleep ("first night effect")
- Labor-intensive setup and scoring
- Not easily scalable to large populations
- Home PSG alternatives sacrifice some signal quality

## Typical Use Cases

- Sleep disorder diagnosis
- Research on sleep oscillations and memory
- Clinical trials of sleep interventions

## Alternatives

- Actigraphy — less detailed but portable and longitudinal
- Home EEG — fewer channels, easier to scale
- A comparison page (PSG vs home EEG) would be valuable as the wiki grows

## Key Papers

- [[sources/chen-2023-sleep-memory]] — used PSG to measure spindle density
- [[sources/rodriguez-2024-spindle-stimulation]] — used PSG with closed-loop stimulation

## Used In Claims

- [[claims/claim-spindle-density-predicts-consolidation]] — spindle density measured via PSG
- [[claims/claim-spindle-enhancement-improves-memory]] — sleep recording during stimulation
