# check-sat-via-reg-match

 A Python script that constructs a regex pattern for checking whether a CNF formula is satisfied by a given assignment.

## Usage

```shell
python3 check_sat_via_regex_match.py
```

## References

This script was inspired by the core idea of the argument credited to Abigail in [Reduction of 3-CNF-SAT to Perl Regular Expression Matching](https://perl.plover.com/NPC/NPC-3SAT.html).

## Related reading

Discussion of the complexity of regex matching with back-references: [https://news.ycombinator.com/item?id=40430093](https://news.ycombinator.com/item?id=40430093)

Proof of concept implementation of a regex matcher that allows a fixed number of back-references, and runs in determinisitc polynomial time (w.r.t to the input size, for an arbitrary but fixed regex): [https://github.com/travisdowns/polyregex](https://github.com/travisdowns/polyregex).
