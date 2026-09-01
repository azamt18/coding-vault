## What should be done

**Task 1**

Here is an example of a method for generating password hash:

    public string GeneratePasswordHashUsingSalt(string passwordText, byte\[\] salt)
    {

        var iterate = 10000;

        var pbkdf2 = new Rfc2898DeriveBytes(passwordText, salt, iterate);

        byte\[\] hash = pbkdf2.GetBytes(20);

        byte\[\] hashBytes = new byte\[36\];

        Array.Copy(salt, 0, hashBytes, 0, 16);

        Array.Copy(hash, 0, hashBytes, 16, 20);

        var passwordHash = Convert.ToBase64String(hashBytes);

        return passwordHash;

    }

Try to review and optimize the code to improve the performance of the method. Do not reduce iterations’ number.

**Task 2**

Analyze ASP.NET MVC app from the [Profile Sample](./sources/ProfileSample) folder. Optimize the logic of retrieving images from the database. DB dump is stored in App\_Data folder.

**Task 3**

Optimize the code of application [GameOfLife](./sources/GameOfLife) folder. It contains memory leak and has poor performance. Try to resolve both issues.

**Task 4**

We have [DumpHomework](./sources/DumpHomework) application which caused an exception and you have a dump file for this exception. Define a place of the error and try to solve it.

**Score board:**

_**0-59%**_ – Constrains & Functional requirements in tasks 1 – 4 are met with minor issues (pay attention to Clean Code practices).

_**60-79%**_ – All functional and non-functional requirements in tasks 1 - 4 are met without issues and you can answer the “Self-check questions”.

_**80-100%**_ – You can provide an example of how principles learnt are applied (or potentially could be applied) to the current project.
