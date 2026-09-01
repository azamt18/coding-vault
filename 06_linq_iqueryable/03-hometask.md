## What should be done

_**Note:**_ If you decide to implement **Complex Task**, the implementation of the first Task is optional. It might be helpful though, to get acquainted with it because some of its parts could be useful for **Complex Task**. 

**Prerequisites:** Load the _Expressions.Task3.E3SQueryProvider_ template from [Expressions_and_IQueryable.Tasks.Week2](./sources/Expressions_and_IQueryable.Tasks.Week2) folder. 

In the template you can find LINQ provider implemented under .net core 2.1 that was discussed during the lecture.

The project represents a set of classes to access E3S via IQueryable interface using LINQ Provider. The overall idea is simple – it accepts IQueryable as an input and provides API URL request as an output. 

**Task:** Complete the following LINQ provider. 

**Note:** Use Unit Tests from the Expressions.Task3.E3SQueryProvider.Test.csproj project to validate the task.   

It is required to do the following: 

1. Remove the expression operands ordering restriction. The following cases should be allowed:  
    - "filtered field name" == "constant" (only this one is allowed now)
    - "constant" == "filtered field name"

2. Test: FTSRequestTranslatorTests.cs, #region SubTask 1: operands order

    - Add include operations support (partial, not exact match). At the same time LINQ notations should look like string class methods calls: StartsWith, EndsWith, Contains.
    - Test: FTSRequestTranslatorTests.cs, #region SubTask 2: inclusion operations

3. Add AND operator support (requires extension of E3SsearchService itself, and probably it will be needed to actualize the existing tests). How to organize AND operator in the E3S request please check [in documentation](https://kb.epam.com/display/EPME3SDEV/Telescope+public+REST+for+data#TelescopepublicRESTfordata-FTSRequestSyntax) (FTS Request Syntax). Test: E3SAndOperatorSupportTests.cs, #region SubTask 3: AND operator support 

Please check the table below for the reference for the point 2: 

**Expression** 

**Translated into** 

**Where(e => e.workstation.StartsWith("EPRUIZHW006"))** 

Workstation:(EPRUIZHW006\*) 

**Where(e => e.workstation.EndsWith("IZHW0060"))** 

Workstation:(\*IZHW0060) 

**Where(e => e.workstation.Contains("IZHW006"))** 

Workstation:(\*IZHW006\*) 

**Note**: Currently, E3S API is closed for public access. Therefore, integration tests are marked as Ignored.   

For the tests in the following classes: 

- FTSRequestTranslatorTests.cs 
- E3SAndOperatorSupportTests.cs,   

Only two of them are executed successfully for now, but when the current task is finished, all of them should be green :  

![test explorer](./images/test-explorer-task-1.png)

 **Complex Task:**

Legend 

Let’s say you have a very specific database, and no LINQ Provider is implemented for it yet (not even saying about ORM). Your task is to implement LINQ Provider to access the data. 

**Task** 

Choose any database (for example MS SQL, Postgre, Oracle, etc.). Your LINQ Provider should allow to translate requests using IQueryable. The requests should support: 

1. Operators:  Select … From … Where  >, <, =  AND 

2. Data types:  Numeric  String  \* You also can use NoSQL with reworked request mentioned in the task. 

Expected result 

1\. Input: 

Something similar to the example from [basic task from Week2](https://epam.sharepoint.com/:w:/r/sites/NetMentoringprogramA2Belarus/Shared%20Documents/Module%203.%20Expressions%20and%20IQueryable/Tasks/Task%20for%20week%202.docx?d=w15d613e1bb324f23b7ce1982ad784735&csf=1&e=HzataF) (E3SProviderTests.cs), but for your database and corresponding the current task:

![code sample](./images/code-sample-2.png)

2\. Output: 

A set of data from the database which corresponds to the request. Create as a Unit test. 

The example of the final request: 

"SELECT \* FROM \[dbo\].\[products\] WHERE UnitPrice > 100 AND \[ProductType\]=’Customised Product’";   

**Note:** LINQ provider should be able to generate quite complex requests/operators or its analogs, specific forto the chosen database. Example: CustomEntitySet<T>:IQueryable<T> (or CustomDbSet), which uses the query:

var productSet = new CustomEntitySet<ProductEntity>(...); 

 List<ProductEntity> products =  productSet.Where(p => p.UnitPrice > 100 && p.ProductType == "Customised Product").ToList(); 

**Note**: if you don’t have enough time to set up the database and implement the data retrieval functionality (let’s say with ADO.NET), implement at least the general functionality, which would have a list of Entity as an input and a valid request string as an output, which you can copy and run on the database manually. 

**Score board:**

_**0-59%**_ – Home task is partially implemented.

_**60-79%**_ - Home task is implemented; all tests are green.

_**80-100%**_ - Complex task is implemented. 
