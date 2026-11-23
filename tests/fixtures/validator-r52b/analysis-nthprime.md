
**nthprime:**
- Acceptance: nth_prime(1)==2 ... (1000)==7919 ✓ all in tests
- 0, -3 → ValueError ✓
- 2.0, "3", True → TypeError ✓
- Implementation: validates bool/non-int → TypeError; n<1 → ValueError; trial division with primes accumulated, break when p*p > candidate. Correct. Note: `for p in primes: if p*p > candidate: break` — standard optimization. For candidate=2, primes empty → is_prime True → append2. Correct.
- 4 test functions → checks-output "4 passed" ✓
- status: "4 passed in 0.01s" matches ✓; full-suite status141 vs checks-output 192 (mismatch as noted).
- Files: only nthprime.py and tests/test_nthprime.py ✓ no cross-imports ✓.
