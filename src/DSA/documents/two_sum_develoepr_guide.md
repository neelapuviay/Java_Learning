You’ve hit the exact core difference between **human intuition** and **algorithmic thinking**.

When you look at `[3, 2, 7]` and target `9`, your eyes take in all elements simultaneously in parallel. Your brain instantly spots `2 + 7 = 9`. A computer, however, is **nearsighted**—it can only look through a peephole at one memory address at a time.

Here is the mental model of how an experienced developer builds the bridge from human intuition to the $O(n)$ HashMap solution.

---

### Step 1: Realize What Your "Inner Eye" Is Actually Doing

When you see `2` and then look for `7`, what happened inside your head?

1. You looked at `2`.
2. You calculated what was missing: `9 - 2 = 7`.
3. You didn't ask: *"What two numbers add to 9?"* You asked: *"Where is the 7?"*

That reframing is key: **Turn an addition problem into a lookup problem.**
Instead of `a + b == target`, think:


$$\text{complement} = \text{target} - \text{current\_number}$$

Now the question becomes: *"Have I seen this complement before, or will I see it later?"*

---

### Step 2: Identify the Bottleneck in the Brute Force

In the nested loop version:

```java
for (int i = 0; i < nums.length; i++) {
    for (int j = i + 1; j < nums.length; j++) { ... }
}

```

Ask yourself: **What is the inner loop actually doing?**

* It is simply searching through an array to answer one question: *"Is the complement number here?"*
* Searching an unsorted array takes $O(n)$ time.
* Doing an $O(n)$ search for every one of the $n$ numbers causes $O(n \times n) = O(n^2)$ total time.

Whenever you see a nested loop that just **searches for a match**, you should immediately think:

> *"Can I replace this slow linear scan with a data structure that searches instantly?"*

---

### Step 3: Why Choose a HashMap?

How do different data structures perform lookups?

| Structure | Search Time | Notes |
| --- | --- | --- |
| **Array / List** | $O(n)$ | Must check element by element. |
| **Sorted Array (Binary Search)** | $O(\log n)$ | Fast, but sorting the array takes $O(n \log n)$ and loses original indices. |
| **HashSet** | $O(1)$ | Remembers: *"Have I seen $X$?"* (True/False). But the problem requires returning **indices**, not just booleans. |
| **HashMap** | $O(1)$ | Remembers: *"Have I seen $X$, and **where** was it located?"* (Key = value, Value = index). |

Because the problem asks for the **indices** of the pair, you need both the number and its position. A key-value store (`Map<Value, Index>`) is the natural fit.

---

### Step 4: Step-by-Step Execution Trace

Let’s trace the algorithm using your example:

`nums = [3, 2, 7]`, `target = 9`

`map` starts empty: `{}`

---

#### Iteration 1 ($i = 0$):

* **Current Element:** `nums[0] = 3`
* **What do I need to reach 9?** `complement = 9 - 3 = 6`
* **Check the Map:** *"Do I have 6 in my memory?"*
* `map.containsKey(6)` $\rightarrow$ **false** (Map is `{}`)


* **Record for the future:** *"I haven't found my match yet, but someone later might need me (3) at index 0."*
* `map.put(3, 0)`
* Current Map state: `{3: 0}`



---

#### Iteration 2 ($i = 1$):

* **Current Element:** `nums[1] = 2`
* **What do I need to reach 9?** `complement = 9 - 2 = 7`
* **Check the Map:** *"Do I have 7 in my memory?"*
* `map.containsKey(7)` $\rightarrow$ **false** (Map only has `{3: 0}`)


* **Record for the future:** *"Save me (2) at index 1."*
* `map.put(2, 1)`
* Current Map state: `{3: 0, 2: 1}`



---

#### Iteration 3 ($i = 2$):

* **Current Element:** `nums[2] = 7`
* **What do I need to reach 9?** `complement = 9 - 7 = 2`
* **Check the Map:** *"Do I have 2 in my memory?"*
* `map.containsKey(2)` $\rightarrow$ **true!**


* **Extract and Return:**
* Where was 2 located? `map.get(2)` $\rightarrow$ index `1`
* Where is the current number (7)? index `2`
* Return `[1, 2]`. Done!



---

### The Developer's Mental Checklist for Future Problems

When approaching array or lookup problems, run through this mental sequence:

1. **Write the brute-force equation:**
$a + b = \text{target} \implies b = \text{target} - a$.
2. **Classify the cost:**
*"My outer loop visits each element once ($O(n)$). My inner loop searches blindly ($O(n)$)."*
3. **Ask the caching question:**
*"Can I trade extra memory (space) to save time?"*
4. **Select the tool by contract:**
* Need existence only? $\rightarrow$ `HashSet`
* Need existence + metadata (like index, frequency)? $\rightarrow$ `HashMap`
* Need sorted order or range lookups? $\rightarrow$ `TreeSet` / `TreeMap` / Binary Search