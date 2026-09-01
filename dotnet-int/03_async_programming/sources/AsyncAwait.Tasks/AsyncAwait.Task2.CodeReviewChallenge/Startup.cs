using AsyncAwait.Task2.CodeReviewChallenge.Extensions;
using AsyncAwait.Task2.CodeReviewChallenge.Models.Support;
using AsyncAwait.Task2.CodeReviewChallenge.Services;
using CloudServices;
using CloudServices.Interfaces;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace AsyncAwait.CodeReviewChallenge;
public class Startup
{
    public Startup(IConfiguration configuration)
    {
        Configuration = configuration;
    }

    public IConfiguration Configuration { get; }

    // This method gets called by the runtime. Use this method to add services to the container.
    public void ConfigureServices(IServiceCollection services)
    {
        services.Configure<CookiePolicyOptions>(options =>
        {
            // This lambda determines whether user consent for non-essential cookies is needed for a given request.
            options.CheckConsentNeeded = context => true;
            options.MinimumSameSitePolicy = SameSiteMode.None;
        });

        services.AddSingleton<IStatisticService, CloudStatisticService>();
        services.AddSingleton<ISupportService, CloudSupportService>();
        services.AddSingleton<IPrivacyDataService, PrivacyDataService>();
        services.AddScoped<IAssistant, ManualAssistant>();

        services.AddMvc(options => options.EnableEndpointRouting = false);
    }

    // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        if (false && env.IsDevelopment())
            app.UseDeveloperExceptionPage();
        app.UseExceptionHandler("/Home/Error");

        app.UseStatistic();

        app.UseHttpsRedirection();
        app.UseStaticFiles();
        app.UseCookiePolicy();

        app.UseMvc(routes =>
        {
            routes.MapRoute(
                "default",
                "{controller=Home}/{action=Index}/{id?}");
        });
    }
}

// commits alignment 3