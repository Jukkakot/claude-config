# Global knowledge

General knowledge that holds in any project: principles and facts with their sources. Project
topics live in each project's own `knowledge.md`; choices in the project's docs; facts about code
in the code. No configuration, versions or other things that go stale.

**Never read this whole file.** Find the topic in the index, then read only that section
(`grep -n '^## ' ~/.claude/knowledge.md` gives the line numbers). Add what new research taught,
with the source, and keep the index in step.

## Index

| Section | What is there |
|---|---|
| Charts | y-axis start and minimum span, one scale rule, time axis, dots by density, units, direction without colour |
| Data files | CSV/JSON, versioned extensible files, unique export names |

## Charts

- **Line charts may start above zero.** Unlike bars (length = value), a line encodes change, so
  the y-axis can cover just the data with some margin.
  ([Data Visualisation Guide](https://data.europa.eu/apps/data-visualisation-guide/scales-in-line-charts),
  [FlowingData](https://flowingdata.com/2024/03/06/line-chart-baselines))
- **But a too tight scale lies too.** Auto-scaling to min..max turns noise into a dramatic slope;
  give the axis a minimum span that matches the normal noise of the data, so a small change looks
  small. ([Observable](https://observablehq.com/blog/never-okay-crop-y-axis-except-when-it-is),
  [Chez Voila](https://chezvoila.com/blog/yaxis/))
- **Keep the same scale rule everywhere.** Charts of the same quantity on different screens or
  periods should use the same rule, otherwise equal changes look different.
- **Time on x spans the whole period**, also when the data covers only part of it; otherwise two
  days look like a month. Leave gaps (break the line) where there is no data for long.
- **Markers (dots) for sparse points, none on dense series.** Guides agree on the idea but give no
  number; a rule by room (enough width per point that dots never touch) works on every screen.
  ([Deckary](https://deckary.com/blog/line-chart-powerpoint),
  [The Bricks](https://thebricks.com/resources/guide-how-to-add-dots-to-a-line-graph-in-excel))
- **Units on every number and axis**; a bare number makes the reader guess.
- **Direction not by colour alone:** arrows or signs next to changes (accessibility, colour
  blindness); gain/loss colours stay neutral when the "good" direction depends on the user.
- **Trend line over noisy daily data: LOESS.** Locally weighted regression (tricube weights, 1–2
  robustness iterations) follows slow change, barely bends for one odd day, and has neither the lag
  of a trailing moving average nor the edge rules of a centred one. Tie the bandwidth to the period
  (e.g. a window of max(21, days/6)); break the line over long gaps. Apache Commons Math
  `LoessInterpolator` needs strictly increasing x and bandwidth·n ≥ 2.
  ([Cleveland 1979, JASA 74(368)](https://doi.org/10.1080/01621459.1979.10481038),
  [Commons Math LoessInterpolator](https://commons.apache.org/proper/commons-math/javadocs/api-3.6.1/org/apache/commons/math3/analysis/interpolation/LoessInterpolator.html))

## Data files

- **CSV and JSON** are what other apps import and export; CSV for spreadsheets, JSON for
  structured data (nested values). Recognise the format from the content, not the file name.
- **Versioned, extensible files:** a version marker and one part per data kind let a newer file
  still be read by an older reader, which skips and reports the parts it does not know.
- **Unique export names** with a timestamp to the millisecond (`name-export-yyyyMMdd-HHmmss-SSS`)
  never collide and sort by time.
