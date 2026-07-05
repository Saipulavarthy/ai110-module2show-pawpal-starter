# PawPal+ Project Reflection

## 1. System Design
1. Add a pet: The owner can register a new pet by entering basic details such as name, species/breed, and any care notes. This creates a Pet object tied to the Owner.
2. Add a care task: The owner can create a task for a specific pet (e.g., "Morning walk," "Feed dinner," "Give medication"), specifying at least a duration and a priority level. This creates a Task object linked to that Pet.
3. View today's schedule: The owner can generate and view a daily plan that organizes all pending tasks across their pets, ordered by priority and/or time, so they know what needs to get done and when.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design includes four classes: Owner, Pet, Task, and Scheduler.

Owner represents the pet owner using the app. It holds a name and a list of Pet objects, and is responsible for adding new pets and providing access to all tasks across those pets (viewAllTasks()).
Pet represents an individual animal, storing basic details (name, species, breed) along with a list of its own Task objects. It's responsible for adding tasks and returning its task list.
Task represents a single care activity, such as a walk or feeding. It holds a description, time, duration, priority, frequency, and completion status, and is responsible for marking itself complete.
Scheduler acts as the "brain" of the system. Rather than owning any data itself, it operates on an Owner's pets and tasks — retrieving all tasks (getTasks), organizing them (organizeTasks), and generating a full daily schedule (generateDailySchedule).

The relationships are straightforward: an Owner has many Pets, and each Pet has many Tasks. The Scheduler doesn't own any of these objects — it just reads from and operates on them, keeping scheduling logic separate from the data model itself.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing my initial skeleton with my AI coding assistant, I made two targeted changes:

Added a pet_name field to Task. Originally, Task had no reference back to the Pet it belonged to. This meant that once Scheduler.generate_daily_schedule() returned a flat list of tasks, there was no way to tell which pet each task was for (e.g., "08:00 Morning walk" — but whose walk?). Adding pet_name directly to Task was the simplest fix, avoiding the need for a separate task-to-pet mapping structure.
Changed time from a string to datetime.time. I initially planned to store task times as strings (e.g., "08:00"). My AI assistant pointed out that this only works for sorting because ISO-formatted strings happen to sort correctly as text — but once I add durations, overlap detection, or recurring task calculations in Phase 4, I'd end up writing a manual parser to convert those strings back into usable time objects anyway. Switching to datetime.time now means sorting and time arithmetic will work natively without extra parsing logic.

I chose not to implement the reviewer's other two suggestions yet: a dedicated ScheduledItem output type and removing Frequency from the MVP. I decided the added complexity of a wrapper type wasn't worth it before I even have real scheduling logic, and I'm keeping Frequency as a stored field since Phase 4 explicitly requires implementing recurring tasks — removing it now would just mean adding it back later.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler currently considers two main constraints: time and completion/pet status. Every task carries a date and time, which the scheduler uses to order the day chronologically (sort_by_time) and to detect when two tasks land in the exact same slot (detect_conflicts). Tasks also carry a priority (LOW/MEDIUM/HIGH) and a pet_name, which the scheduler uses for filtering — so an owner can pull up just one pet's tasks, or just the tasks still outstanding.
I decided time mattered most because a daily planner is fundamentally about "what happens when" — without correct ordering, nothing else about the schedule is trustworthy. Conflict detection came next, since silently double-booking two pets at the same time is the kind of mistake a pet owner would actually want caught, not just displayed. Priority and pet filtering were treated as supporting constraints rather than scheduling drivers — right now priority is stored and displayed but doesn't reorder tasks or resolve conflicts on its own (e.g., a HIGH-priority task isn't automatically bumped ahead of a LOW-priority one at the same time). I chose to keep it that simple for the MVP rather than build priority-based conflict resolution, since exact-time conflicts are rare enough that a human glancing at the warning can decide which task to move.

That pairs cleanly with your existing 2b writeup on exact-match vs. overlap conflict detection. Once both are in, you're set for Step 6: Document and Merge.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My conflict detection groups tasks by exact (date, time) pairs rather than checking for overlapping time ranges. If one task runs 07:00–07:30 and another starts at 07:15, my scheduler won't flag them as conflicting, since it only catches tasks scheduled at the identical minute rather than reasoning about duration-based overlap. I chose this because true overlap detection would require treating duration as something that "blocks" a calendar slot, adding real complexity for a scheduler that doesn't yet reason about task duration in scheduling logic. For an MVP daily planner, catching tasks accidentally double-booked at the exact same time is the most common and useful case, so I accepted this narrower definition of "conflict" rather than building full interval-overlap math.
When I asked my AI assistant to simplify detect_conflicts further, its verdict was that the algorithm was already at the right complexity (O(n) grouping plus an O(k log k) sort) and didn't need a performance fix. It suggested two minor readability changes — using defaultdict instead of setdefault, and tightening the by_slot type hint — both of which I adopted since they cost nothing and slightly improved clarity. It explicitly recommended against collapsing the logic into a single comprehension, noting the loop stays more readable when building formatted warning strings. This was a useful reminder that "simplify" doesn't always mean "compress" — sometimes the right call is to leave working, readable code alone.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used my AI coding assistant across every phase of this project, but in distinctly different ways depending on the task. For design and planning (Phase 1 UML, Phase 4 algorithm planning, Phase 5 test planning), I used it as a brainstorming partner — asking it to suggest structures, edge cases, or improvements before I committed to an approach. For implementation, I relied on it to generate code from precise specifications I wrote myself, rather than open-ended requests — for example, giving it exact method signatures and behavior descriptions for sort_by_time, filter_tasks, and detect_conflicts rather than just saying "add sorting and filtering." For debugging and review, I used it to critique my own working code (e.g., asking it to review my class skeletons for missing relationships, or asking "how could this be simplified" on my finished detect_conflicts method).
The most helpful prompts were ones with tight, specific constraints — telling it exactly which fields to add, what the return type should be, and what not to change. Open-ended prompts tended to produce more code than I needed or introduced changes I hadn't asked for, while narrow, well-scoped prompts kept the codebase clean and easy to verify.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One clear example: after my initial class skeleton review, my AI assistant suggested four changes — adding a pet_name field to Task, switching time to datetime.time, introducing a ScheduledItem wrapper type for schedule output, and dropping Frequency from the MVP entirely. I accepted the first two because they solved real, immediate problems (no way to trace a task back to its pet; string-based time sorting would break down once I needed real time arithmetic). I rejected the other two: the ScheduledItem wrapper felt like premature complexity for a system that didn't have real scheduling logic yet, and dropping Frequency would have meant re-adding it later since Phase 4 explicitly required recurring task logic.
I verified this decision by weighing it against the project's actual roadmap rather than taking the suggestion at face value — since I could see recurring tasks were an upcoming requirement, keeping Frequency as a stub field was clearly the right call even though the AI's stated reasoning (avoiding an unused field) was technically sound in isolation. This taught me that AI suggestions are often locally correct but miss context about where the project is headed — that's a judgment call only I could make as the person holding the full project scope.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested the four core algorithmic behaviors I implemented: sorting tasks chronologically, filtering by pet name and completion status, recurring task generation (daily and weekly), and conflict detection for tasks scheduled at the same time. I also tested edge cases identified in a dedicated test-planning session with my AI assistant: a pet with no tasks, an owner with no pets, marking a ONCE-frequency task complete (which should not generate a recurrence), and two tasks with the same time but different dates (which should not be flagged as a conflict). These tests mattered because they cover both the "obvious" happy paths a user would hit constantly (viewing a sorted schedule) and the quieter edge cases that are easy to overlook but would cause real bugs — for example, without testing the same-time-different-date case, I might not have noticed that my sorting logic doesn't account for date at all, only time of day.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm fairly confident the scheduler works correctly for its intended scope — all 19 tests pass, covering sorting, filtering, recurrence, and conflict detection along with their edge cases. My confidence is a 4 out of 5, not a 5, because I know of specific limitations I haven't tested or resolved: conflict detection only catches exact time matches rather than true duration-based overlap, and sorting doesn't use date as a tiebreaker, meaning tasks on different days but the same time of day could interleave unexpectedly in a multi-day view. If I had more time, I'd test: multi-day schedules (to confirm the sorting limitation above is or isn't actually a problem in practice), a task with time=None if I ever allow "anytime" tasks, and a stress test with a larger number of pets/tasks to confirm performance holds at scale (though at the scale of a single household's daily tasks, this is unlikely to matter).

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the algorithmic layer — sorting, filtering, recurrence, and conflict detection all came together cleanly and are fully covered by tests. I also think the incremental, phase-by-phase approach (CLI-first before UI, planning before implementation) paid off: by the time I got to the Streamlit integration, my logic layer was already verified independently, so wiring it to the UI was mostly straightforward rather than a source of new bugs.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I did another iteration, I'd address the two known limitations directly: implement true duration-based overlap detection instead of exact-time matching, and make sorting date-aware so multi-day schedules order correctly. I'd also reconsider whether Frequency needs more nuanced handling — right now recurrence generates exactly one next occurrence, but a more complete system might need to expand out a whole week or month view at once.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest thing I learned is that being the "lead architect" means treating AI suggestions as informed input, not answers — the AI can flag a real problem (like pet_name being missing) or offer a technically valid suggestion that's still wrong for my project's specific roadmap (like dropping Frequency). My job wasn't to follow every suggestion or reject them out of skepticism, but to evaluate each one against the actual shape and future requirements of the system I was building — something only I had full visibility into.

