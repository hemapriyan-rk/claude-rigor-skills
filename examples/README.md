# Examples

Real, unedited runs of the skills. Each folder has the input, the exact prompt, how it was run, what it cost, and the output. Where a result could be checked, such as a speedup or a test result, it was checked independently and the folder says how.

| Skill | Task | Result |
|---|---|---|
| [secure-code-review](secure-code-review/) | Flask auth module with 8 planted flaws and a public answer key | 7 of 8 found, 1 partial, plus a critical bug nobody planted |
| [slow-query-optimizer](slow-query-optimizer/) | Dashboard query with N+1 and a `date()` filter, 50,000 orders | 4.99 s → 4.3 ms, identical rows across every window tested |
| [memory-leak-hunter](memory-leak-hunter/) | Message worker whose memory climbs until it's killed | Leak traced to a never-unsubscribed handler; 322 MB → flat over 8,000 messages; the bounded cache correctly left alone |
| [ci-speedup](ci-speedup/) | Serial, uncached workflow and a test suite with sleeps | Test suite 8.85 s → 0.43 s, same 17 tests; all checks kept |
| [performance-optimization](performance-optimization/) | Report script that's slow on 12,000 rows | 7.5 s → 0.2 s, identical output |
| [test-architect](test-architect/) | Token-bucket rate limiter | 15 tests; 4 fail on real bugs, including a race that lets 50 concurrent calls through a 10-token bucket |
| [architecture-design](architecture-design/) | Live driver locations for ride-hailing | Numbers, trade-offs, failure and threat tables, break scenarios, and an unanswered dependency it flagged |
| [researcher](researcher/) | Phone-only acoustic indoor localization | Claim killed by a 2018 paper and a granted patent; gaps a narrower claim could target |
| [patent-novelty-evaluator](patent-novelty-evaluator/) | Drowsiness-detecting motorcycle helmet, filing in India | Weak: a 2014 paper discloses most elements; seven ways to strengthen the claim |

The failing tests in `test-architect/` fail on purpose: they expose bugs in `rate_limiter.py`, which is left unfixed so the result can be reproduced.
