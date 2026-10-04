---
title: Plot Check: a local document checker for my friend who buys plots in Karnataka
tags: devchallenge, weekendchallenge, hf26challenge
---

## What I Built
<!-- WRITE IN YOUR OWN WORDS. Who is the friend, what do they do, what goes wrong today. Only claims that are true. -->

## Demo
<!-- screen recording link. Fake documents only. -->

## Code
<!-- repo link -->

## How I Built It
- Tesseract OCR (English + Kannada) reads the page.
- Gemma 3 4B, running through Ollama on a 6 GB laptop GPU, turns the text into fields.
- Plain Python does every check: missing documents, survey/khata/owner mismatches, listed encumbrances, stale tax.
- Streamlit page. Rules live in one config file so a professional can correct them.

What failed: <!-- fill from real testing: the Kannada tax-date misread, name matching, real scans -->

## Why Does Open Innovation Matter?
Property papers carry names, survey numbers and mortgage details. With a local open-weight model they never
leave the laptop, it costs nothing per document, and the rules and model can be swapped.
<!-- Add what you actually observed vs a closed API. Don't claim comparisons you didn't run. -->

## What my friend said
<!-- ONLY the real reaction after he used it. If he hasn't, say so plainly. -->

## Prize Categories
Best Use of Gemma. <!-- add others only if truly used -->
