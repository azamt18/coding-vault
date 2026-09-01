## What should be done

**Composite. Task 1:** 

In one company there is a need to build xml generator. Developers build object hierarchy and then this hierarchy is converted to xml.  

Implement simple xml elements InputText and LabelText 

	public class InputText 
	{ 
		.... 
		public InputText(string name, string value) 
		{ 
			... 
		} 

		public string ConvertToString() 
		{ 
			... 
		} 
	} 

	public class LabelText 
	{ 
		... 
		public LabelText(string value) 
		{ 
			... 
		} 

		public string ConvertToString() 
		{ 
			... 
		}
	} 

InputText should look like this: \<inputText name='myInput' value='myInputValue'/>

InputText should look like this: \<label value='myLabel'/> 

**Composite. Task 2:** 

Implement form element, container for other elements.  

Form element should be able to add internal elements.  

	public class Form 
	{
		String name; 

		public Form(String name) 
		{ 
			this.name = name; 
		} 

		public void AddComponent(..) 
		{ 
			... 
		} 

		public string ConvertToString() 
		{ 
			... 
		} 
	} 

For example, if we add two elements to a form, string conversion should look like:  

	<form name='myForm'> 

		<label value='myLabel'/> 

		<inputText name='myInput' value='myInputValue'/> 

	</form> 

**Score board**: 

_**0-59%**_ – 1-2 of 4 tasks have been completed and implementation meets all requirements. 

_**60-79%**_ – 3 of 4 tasks have been completed, implementation meets all requirements with one major remark related to the patterns’ implementation or clean code principles at most.  

_**80-100%**_ – All 4 tasks have been completed, implementation meets all requirements, and there are no major remarks related to the defined patterns’ implementation and clean code principles.
