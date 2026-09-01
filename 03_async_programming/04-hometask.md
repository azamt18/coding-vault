## What should be done

- Open solution in the [sources/AsyncAwait.Tasks](./sources/AsyncAwait.Tasks) folder. Restore packages via “dotnet restore” if needed. Implement the tasks 1 and 2 using templates from the AsyncAwait.Tasks.sln.

**_Note_**: If “dotnet restore” does not work, please make sure the environment variable contains a link to dotnet

**Task 1. Asynchronous calculation and cancellation tokens (AsyncAwait.Task1.CancellationTokens.csproj)**:

Task:

- Here is a code for application designed to calculate the sum of integer numbers from 0 to N. Please rework the application code to satisfy the following conditions:

- The calculation should be asynchronous.
- N should be set from Console as user input. User should be able to change the upper limit N in the middle of the calculation process. This change should abort current calculation and start a new one with the new N.
- There should be neither any exceptions nor application falls if the process of calculation restarts.

**Task 2. ASP MVC challenge (AsyncAwait.Task2.CodeReviewChallenge.csproj)**:

Task:

- Please perform code review of the provided ASP.NET Core application. Pay attention to async operations usage issues.

About application:

- Web app contains 3 pages, which could be navigated from the main menu: Home, Privacy, Help. Besides that, each page collects statistics (how many times this page was visited).

![about application](./images/about-app.png)

- Probably, the navigations counting code is not optimal and causes the pages loading slowly.

## What you need to do:

1. Review application code AsyncAwait.CodeReviewChallenge and paying attention to the wrong async code usage. Provide your ideas how these code issues could be resolved.

2. Improve the code according to your proposals. Verify that application works stable. (Good idea here is to make your changes in a separate branch and then compare both implementations).

This solution also contains a project named _CloudServices_. This app emulates multiple calls to the third-party services. As it is a third-party library, you shouldn’t change this code. All your changes should be made in AsyncAwait.CodeReviewChallenge project.

Discuss your ideas and results with your mentor. Be ready to describe how async code works in depth.

**Score board:**

_**0-59%**_ – Both required tasks have been completed, and implementation meets all requirements. 

_**60-79%**_ – In the second task, a mentee improved the code (didn't make it worse) and can explain why it was necessary. 

_**80-100%**_ – A mentee understands pros and cons of the provided solutions and there are no major remarks related to clean code principles (SOLID, KISS, DRY, etc.).
