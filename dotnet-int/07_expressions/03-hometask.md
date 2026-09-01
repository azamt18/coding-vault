## What should be done

**Home Task.** Expression Transformation

Complete both tasks below. Templates are available in [Expressions_and_IQueryable.Tasks.Week1](./sources/Expressions_and_IQueryable.Tasks.Week1) folder. 

**(ExpressionTrees.Task1.ExpressionsTransformer.csproj)**

Create a transformer class based on ExpressionVisitor that performs the following 2 types of expression tree transformations:

- Replacing expressions like <variable> + 1 / <variable> - 1 with increment and decrement operations
    
- Replacing the parameters included in the lambda expression with constants (pass as parameters of such a transformation:
    
    - Source expression
    - List of pairs <parameter name: value to replace>

For control you can output the resulting tree to the console or watch the result under the debugger.

**You can use ExpressionTreeVisualizer or another visualizer here, or you can do it without a visualizer at all.**

**Complex Task**. Mappers. Extended

**Extend the logic from the previous task:**

- Provide the ability to customize the mapping of such fields that differ in names and data types.

- Discuss implementation details with mentor.

**Score board:**

_**0-59%**_ – Home task is partially implemented.

_**60-79%**_ - Home task is implemented; all tests are green. 

_**80-100%**_ - Complex task is implemented. 
