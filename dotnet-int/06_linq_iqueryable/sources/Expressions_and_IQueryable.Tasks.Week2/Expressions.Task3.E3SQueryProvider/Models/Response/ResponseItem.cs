namespace Expressions.Task3.E3SQueryProvider.Models.Response
{
    public class ResponseItem<T> where T : class
    {
        public T Data { get; set; }
    }
}
