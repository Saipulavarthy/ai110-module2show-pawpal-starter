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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
