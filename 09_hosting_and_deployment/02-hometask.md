## What should be done

**Task 1**

Prerequisites:

- .NET Core is installed on your machine (preferably, the latest version). Create a new ASP.NET Core application using dotnet cli, e.g., _dotnet new Web API._ Run the newly created app via dotnet run command to make sure it starts and works.

**Task 1: Deploy your ASP.Net Core application to your local IIS server.**

- [Enable IIS](https://docs.microsoft.com/en-us/aspnet/core/host-and-deploy/iis/development-time-iis-support?view=aspnetcore-6.0%23enable-iis) in your local machine.
- Deploy your asp.net core application to your local machine’s IIS. Verify that it was successfully deployed by opening a home page/calling home endpoint in the browser.

**Task 2: Deploy your ASP.Net Core application to Azure App Service.**

1. Via Visual Studio:
    1. Open your application in Visual Studio. Deploy the application to Azure App service using visual studio (choose F1 app service plan because it is free).
    2. Login to [Azure Portal](https://portal.azure.com/) and verify that all resources were created. Find your App Service and open the app link on the browser to verify it is up and running as expected.

2. Via Azure CLI:
    1. Login into your azure account via Azure CLI.
    2. Create a new resource group.
    3. Create an azure webapp.
    4. Publish your app to a newly created azure webapp.
    5. Login to [Azure Portal](https://portal.azure.com/) and verify that all resources were created. Find your App Service and open the app link in the browser to verify it is up and running as expected.

**Task 3: Deploy your ASP.Net Core application with Docker.**

_Prerequisites_: Docker Desktop and Azure CLI are installed on your local machine.

- In your project’s root folder create a .Dockerfile with all the necessary instructions.
- Build an image from your newly created Dockerfile via command line.
- Build and run a container from your newly built image.
- Push the image you just created into Azure Container Registry or Docker Hub so that your mentor can download  and run it.
- Create Azure App Service from your published images and run it using Azure CLI.
- Login to [Azure Portal](https://portal.azure.com/) and verify all resources were created. Find your App Service and open the app link on the browser to verify it is up and running as expected.

**Score board:**

_**0-59%**_ – Only one of the tasks has been fully completed with minor issues. 

_**60-79%**_ – 2 of 3 tasks have been completed. 

_**80-100%**_ – All 3 tasks have been completed without serious issues.
