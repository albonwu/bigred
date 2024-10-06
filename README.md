<h1 align="center">
Respoke
</h1>

<p align="center">Formulas made accessible.</p>

## Inspiration
Reading out of an digital physics book in online school illuminated the shortcomings of screen-readers when it comes to textbook formulas. In most cases, the readers would skip over the equations or say something incomprehensible - which would particularly affect people who rely on text-to-speech technologies, perhaps due to visual impairment.

## What it does
Respoke improves accessibility in academia by providing clear, fluent natural language readings of equations and formulas.

## How we built it
We fine-tuned Gemini 1.5 Flash on GCP's Vertex AI Platform. To acquire data for this purpose, we thought about conventions and stylistic patterns that balanced between concision and clarity when describing complex mathematical equations written in LaTeX. Below are some patterns and rules we took into consideration:

- ``\sqrt{n}`` -> “square root of (the quantity) n”
- ``\frac{a}{b}`` -> “fraction with numerator (the quantity) a and denominator (the quantity) b”
- ``\sum_{i = 0}^\infty f(i)`` -> “sum from i equals 0 to infinity of (the quantity) f(i)”
- ``\binom{a}{b}`` -> “binomial coefficient with upper index (the quantity) a and lower index (the quantity) b”

*Append “followed by” if character immediately after } is not }*

*Append “followed by \[structure\]” if multiple “followed by”s are consecutive*

We then wrote a Python script to construct expressions of varying complexity, simulating ones likely to appear across different fields of math. With the dataset constructed, we fine-tuned Gemini 1.5 with it, after which we deployed the new model using a Vertex endpoint.

Building the front-end involved creating a browser extension to extract MathML and LaTeX from existing equations, sending it to the backend, and inserting audio elements for equations.

## Challenges we ran into
Integrating with Cartesia's TTS API meant we had to learn a lot about server side events and audio encoding to bring our descriptions to life.

When fine-tuning Gemini, we thought hard about how to strike a balance between brevity and clarity. We didn't want the model to be so concise it became vague, nor so detailed that its translation was cumbersome. As shown above, we had to construct a list of general patterns and principles that motivated the construction of the fine-tuning dataset.

## Accomplishments that we're proud of
Quickly learning how to build a web extension that extracts equation information from webpages was a first for us.

## What we learned
How easy Pinata is to use and the importance of having a low-friction file system in developing quickly.

## What's next for Respoke
Integration with computer vision to detect equations of any format, and decreasing latency.
