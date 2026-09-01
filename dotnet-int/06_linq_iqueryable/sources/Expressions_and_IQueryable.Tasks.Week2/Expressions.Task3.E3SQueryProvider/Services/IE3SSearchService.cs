using System;
using System.Collections;
using System.Collections.Generic;
using Expressions.Task3.E3SQueryProvider.Models.Entities;

namespace Expressions.Task3.E3SQueryProvider.Services
{
    public interface IE3SSearchService
    {
        IEnumerable<T> SearchFts<T>(string query, int start = 0, int limit = 0) where T : BaseE3SEntity;

        IEnumerable SearchFts(Type type, string query, int start = 0, int limit = 0);
    }
}
