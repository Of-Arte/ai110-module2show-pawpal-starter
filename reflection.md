# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  - My diagram uses a one-to-many relationship between Owner and Pet where the owner has a name attribute, an availability attribute and a list of pets with methods to add, remove or display all pets.
  - Each pet has a name, species, breed and age attribute with a list of tasks and add, remove and display methods.
- What classes did you include, and what responsibilities did you assign to each?
  - The Scheduler class has an owner and date attribute with a list for scheduled tasks and a list for skipped tasks. It also has methods to generate a plan, sort tasks, filter by date and explain the reasoning of the plan.

**b. Design changes**

- Did your design change during implementation?
  - Originally the scheduler object received the owner and a specific pet, but to plan tasks for all pets of the owner, I changed the scheduler to rely on the pets list inside owner.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - My scheduler considers the time the owner has available and the priority of the tasks, with only tasks that are due today being considered.
- How did you decide which constraints mattered most?
  - I decided that time and priority mattered most because they are the most important factors in determining a schedule.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  - The scheduler only sorts tasks by priority and ignores the time the tasks are due.
- Why is that tradeoff reasonable for this scenario?
  - It might be more important to complete high-priority tasks like providing critical medication rather than low-priority tasks like playing fetch, even if the low-priority tasks are due earlier.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
  - I used AI coding agents to help me design the system, generate code, test the code, add documentation, and organize my commits.
- What kinds of prompts or questions were most helpful?
  - When I was unsure about the design of the system, I asked the AI coding agent to suggest a design using the problem description for guidance. I noticed that the agents' suggestions leaned towards petcare specific solutions which sometimes conflicted with OOP principles, but provided helpful insights into what I should consider.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  - When the agent suggested using the scheduler to retrieve pets of the owner, I rejected the change because I felt that it went against the OOP principle of encapsulation. It is not the scheduler's job to know about the owner's pets.
- How did you evaluate or verify what the AI suggested?
  - For each change made by the coding agent, I reviewed the code differences and evaluated if I agreed with the changes. If I did not agree, I would either reject the change or ask the agent to make changes to the suggested code.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  - I tested if tasks could be added and removed from pets correctly, if tasks could be sorted by priority and if tasks could be scheduled within the owner's time limit.
- Why were these tests important?
  - These tests ensure that the system is working as expected and that the scheduler follows the same logic that was designed in the UML diagram.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  - I am confident that my scheduler works correctly.
- What edge cases would you test next if you had more time?
  - I would test the scheduler with more edge cases, such as tasks with different priorities and time limits, and tasks that are due on different days.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  - I am most satisfied with the testing framework and the fact that I was able to implement a scheduling algorithm that works correctly.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  - If I had another iteration, I would add more features to the smart scheduler, such as connecting it to a calendar app, using a user's existing schedule to determine the best time to walk the dog and to provide reminders for tasks.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  - Working on this project helped me understand the tradeoffs between design principles and the ability to meet user's needs.
