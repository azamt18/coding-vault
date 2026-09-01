## What should be done

**Façade. Task:** 

To build a system to place an order. There are 3 separate services which can be used to place an order.  

ProductCatalog – This service contains all available products.  

	interface ProductCatalog 
	{ 
		Product GetProductDetails(string productId); 
	} 

This service allows you to load product by Id.  

PaymentSystem – The system provides an interface to make payments.  

	interface PaymentSystem 
	{ 
		bool MakePayment(Payment payment); 
	} 

InvoiceSystem – The system provides an interface to send an invoice.  

	interface InvoiceSystem 
	{ 
		void SendInvoice(Invoice invoice); 
	} 

Implement Façade to place order.  

Place order algorithm:  

1. Load product by product Id. Use ProductCatalog service. 
2. Make payment for the product from ProductCatalog service using service PaymentSystem.  
3. Make invoice payment using InvoiceSystem.  

Interface for Order Façade:  

	void PlaceOrder(string productId, int quantity, string email) 

**Score board:** 

_**0-59%**_ – 1-2 of 4 tasks have been completed and implementation meets all requirements. 

_**60-79%**_ – 3 of 4 tasks have been completed, implementation meets all requirements with one major remark related to the patterns’ implementation or clean code principles at most.  

_**80-100%**_ – All 4 tasks have been completed, implementation meets all requirements, and there are no major remarks related to the defined patterns’ implementation and clean code principles.
