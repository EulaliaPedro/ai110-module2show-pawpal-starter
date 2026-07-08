# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  The inital UML includes: 
       - see and add/edit/remove tasks
       - view daily schedule 
       - enter basic pet and user information 
- What classes did you include, and what responsibilities did you assign to each?
   Classes that would be included: 
     - class userInfo - will get the information of the user (pet owner) and pet. Should there be a seperate on for each?
     - class viewTask - this would get all the informatino and print it for the user to view when they want 
     - class createTask - this would have user input task details: task name, duration, date, and any other notes
     - class viewSchedule - allows users to view the the created Schedule 
     - class generateSchedule - based on the users prefernces the schedule will generated 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
  One change that was made was using methods rather than classes for the information. For example an owner can create a task, while a pet can be added a task. Reducing any redundancy and tasked where placed to match what the  expected actions of users.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
  Priority was determined by the time of the task. For example if a task was at 3:00 PM, the task with a 9:00 AM time would take priority, but only if it is the same day. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
  One tradeoff that I made was removing the rescheduling feature that was put into the code, as I belived it would not align well with an actual scheduler. For exapmle, if the task was to the vet, the app would not be able to reschedule as it is something the  owners need to figure out. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
  I tried to create prompts that followed the instructions and found that they were helpful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
  There was one section where I allowed AI to change the code, but did not like it becuase it rearranged the schedule automatically, which I think would not be the most accurate when it comes to schedules.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  Test for multiple animals and schedule conflicts.
- Why were these tests important?
  These test were important because they allowed me to check if the program was acting correctly.

**b. Confidence**
  
- How confident are you that your scheduler works correctly?
  I am not the most confident, but it does run for the test.
- What edge cases would you test next if you had more time?
  I would test for multiple users and tasks may have conflicted but more than one person was completing the task. 
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am satisfied with the testing as it seems to work well. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would improve the UI of the project as well as adding a calender festure to see the days each task would land on, which can also be usefull for the reoccuring tasks

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  I learned that AI can be pretty helpful when designing a system, but can also over complicate things. 