using System;

namespace Expressions.Task3.E3SQueryProvider.Attributes
{
    [AttributeUsage(AttributeTargets.Class, AllowMultiple = false, Inherited = false)]
    public class E3SMetaTypeAttribute : Attribute
    {
        public string Name { get; private set; }

        public E3SMetaTypeAttribute(string name)
        {
            Name = name;
        }
    }
}
