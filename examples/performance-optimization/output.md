## Result
Runtime: about 8 s → 0.15 s (~55×) on 12,000 signups, which includes interpreter startup. The 500,000-signup nightly size now takes 0.52 s for the report steps (`unique_emails`, `count_by_country`, `to_csv`), excluding the time to generate the fake input. The old code would have taken roughly 4 hours at that size, assuming the O(n²) scaling holds.

## Bottleneck
`cProfile` on the 12k run showed 97% of the time (49.0 of 50.5 s, inflated by profiler overhead) in `count_by_country`. For every unique email it rescanned the whole signup list. `unique_emails` was another 1.2 s, because `email not in seen` searched a list. Both were O(n²) and CPU-bound.

## Change
In `report.py`:
- **`unique_emails`:** `list(dict.fromkeys(...))`. This is O(n) and keeps first-seen order.
- **`count_by_country`:** one pass builds a map of email to the country of its first signup, then each unique email is tallied from that map. This matches the old "first match wins" behavior. An email missing from `signups` is still skipped, as before.

I did nothing to `to_csv`, which isn't on the hot path. A dict lookup was enough, so I didn't try anything more elaborate.

## Verified
- I re-ran `python report.py` on the same 12,000 signups and compared it to `baseline.txt`. There are 0 differences.
- The 500k timing is a single run. At that size, 489,616 of the emails are unique.
- Only the 12k output was compared to the baseline. I didn't run the old code at 500k, so I haven't confirmed the two versions agree there.

I also left an `after.txt` in the directory from the comparison. You can delete it.