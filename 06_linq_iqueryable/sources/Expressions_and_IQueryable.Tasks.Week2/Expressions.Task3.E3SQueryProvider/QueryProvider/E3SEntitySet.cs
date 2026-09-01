using Expressions.Task3.E3SQueryProvider.Services;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using Expressions.Task3.E3SQueryProvider.Models.Entities;

namespace Expressions.Task3.E3SQueryProvider.QueryProvider
{
    public class E3SEntitySet<T> : IQueryable<T> where T : BaseE3SEntity
    {
        protected readonly Expression Expr;
        protected readonly IQueryProvider QueryProvider;

        public E3SEntitySet(E3SSearchService client)
        {
            if (client == null)
            {
                throw new ArgumentNullException(nameof(client));
            }

            Expr = Expression.Constant(this);
            QueryProvider = new E3SLinqProvider(client);
        }

        #region public properties

        public Type ElementType => typeof(T);

        public Expression Expression => Expr;

        public IQueryProvider Provider => QueryProvider;

        #endregion

        #region public methods

        public IEnumerator<T> GetEnumerator()
        {
            return QueryProvider.Execute<IEnumerable<T>>(Expr).GetEnumerator();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return QueryProvider.Execute<IEnumerable>(Expr).GetEnumerator();
        }

        #endregion
    }
}