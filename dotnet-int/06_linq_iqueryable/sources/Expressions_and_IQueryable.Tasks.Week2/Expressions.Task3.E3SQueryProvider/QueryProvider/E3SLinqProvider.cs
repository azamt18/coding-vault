using Expressions.Task3.E3SQueryProvider.Helpers;
using Expressions.Task3.E3SQueryProvider.Services;
using System;
using System.Linq;
using System.Linq.Expressions;

namespace Expressions.Task3.E3SQueryProvider.QueryProvider
{
    public class E3SLinqProvider : IQueryProvider
    {
        private readonly E3SSearchService _e3SClient;

        public E3SLinqProvider(E3SSearchService client)
        {
            _e3SClient = client;
        }

        public IQueryable CreateQuery(Expression expression)
        {
            throw new NotImplementedException();
        }

        public IQueryable<TElement> CreateQuery<TElement>(Expression expression)
        {
            return new E3SQuery<TElement>(expression, this);
        }

        public object Execute(Expression expression)
        {
            throw new NotImplementedException();
        }

        public TResult Execute<TResult>(Expression expression)
        {
            Type itemType = TypeHelper.GetElementType(expression.Type);

            var translator = new ExpressionToFtsRequestTranslator();
            string queryString = translator.Translate(expression);

            return (TResult)_e3SClient.SearchFts(itemType, queryString);
        }
    }
}
