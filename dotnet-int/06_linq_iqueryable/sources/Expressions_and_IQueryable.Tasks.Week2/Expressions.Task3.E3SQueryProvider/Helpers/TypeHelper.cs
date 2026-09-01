using System;
using System.Collections.Generic;

namespace Expressions.Task3.E3SQueryProvider.Helpers
{
    internal static class TypeHelper
    {
        internal static Type GetElementType(Type seqType)
        {
            Type iEnum = FindIEnumerable(seqType);
            if (iEnum == null)
                return seqType;

            return iEnum.GetGenericArguments()[0];

        }

        private static Type FindIEnumerable(Type seqType)
        {
            if (seqType == null || seqType == typeof(string))
                return null;

            if (seqType.IsArray)
                return typeof(IEnumerable<>).MakeGenericType(seqType.GetElementType());

            if (seqType.IsGenericType)
            {
                foreach (Type arg in seqType.GetGenericArguments())
                {
                    Type iEnum = typeof(IEnumerable<>).MakeGenericType(arg);
                    if (iEnum.IsAssignableFrom(seqType))
                        return iEnum;
                }
            }

            Type[] iFaces = seqType.GetInterfaces();

            if (iFaces.Length > 0)
            {
                foreach (Type iFace in iFaces)
                {
                    Type iEnum = FindIEnumerable(iFace);
                    if (iEnum != null)
                        return iEnum;
                }

            }

            if (seqType.BaseType != null && seqType.BaseType != typeof(object))
            {
                return FindIEnumerable(seqType.BaseType);
            }

            return null;
        }
    }
}
