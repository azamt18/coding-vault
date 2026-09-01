## What should be done

**Adapter. Task:** 

Adopt existing class/interface to another one. You have a class which prints some important info about an object: 

	public class Printer 
	{ 
		public void Print<T>(IContainer<T> container) 
		{ 
			foreach (var item in container.Items) 
			{ 
				Console.WriteLine(item.ToString()); 
			} 
		} 
	} 


Here is IContainer interface: 

	public interface IContainer<T> 
	{ 
		IEnumerable<T> Items { get; } 
		int Count {get; } 
	} 

Let’s imagine you cannot change Printer code, but you can use only this version of a Printer to print. In your project you have a class which implements only the following interface: 

	public interface IElements<T> 
	{ 
		IEnumerable<T> GetElements(); 
	} 

You cannot change this class too, but you must print all the elements of this object. 

**Score board:** 

_**0-59%**_ – 1-2 of 4 tasks have been completed and implementation meets all requirements. 

_**60-79%**_ – 3 of 4 tasks have been completed, implementation meets all requirements with one major remark related to the patterns’ implementation or clean code principles at most.  

_**80-100%**_ – All 4 tasks have been completed, implementation meets all requirements, and there are no major remarks related to the defined patterns’ implementation and clean code principles.
