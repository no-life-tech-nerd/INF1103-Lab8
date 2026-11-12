2.2. Predict first: I predict that each Product can still display its supplier information, as there is still a reference to the supplier information in the Product and the `del supplier` only removes the reference in the test file rather than destroying the instance of the supplier.

3.2. Predict first: I predict that the Product can still work after it's removed from Inventory A as there is still a reference to the instance outside of Inventory A (in this case, within the test file).

4.3. Predict first: For the same Product added to 2 Orders, 2 OrderLine objects and 2 Product objects (1 per OrderLine). REFLECTION: upon testing it out, I realized that since we're creating a single Product instance first and assigning that to each of the Orders, they will reference the same already instantiated Product instance, hence only 1 Product object is created.

6.3. Diagnose: Yes, this violates LSP, since the expected behavior is that the update_stock function will work regardless of the subclass types, which falls under "A subclass should not unexpectedly reject valid inputs that the parent class accepts". I would change the subclass to conform to the expected behavior established by the parent class, and if that's not possible, I would reconsider the inheritance relationship since this shows that the relationship may be weaker than expected.

6.3. Review my code: One expectation is that display_information() will successfully run for all subclass types. It is expected that each of the subclasses either use the upstream display_information() function or extend it to account for all subclass-specific info to be displayed. 

7.2. Predict first: physical products will print "This product requires physical shipping." while digital products will print "This product is delivered digitally.".

7.3. Explain polymorphism: this demonstrates polymorphism because the same show_product_details function call will call the subclass "extended" display_information if it exists, else the parent display_information, and each subclass is expected to and does implement the appropriate get_fulfilment_info. LSP supports this design because the subclass' implemented methods preserves the expectations established by the parent class while allowing extensibility for each subclass to implement the method in a manner best fitting each subclass.

8. AI Use for UML: Yes, I did use GPT 6.1 Terra High to review my diagram. I changed Terra's interpretation that "The diagram shows that a product may belong to multiple inventories because the current code does not restrict sharing." which led it to use `Inventory "0..*" o-- "0..*" Product` while the intended design dictates `Inventory "0..1" o-- "0..*" Product` instead. I accepted Terra's interpretation that Supplier-Product is an association.
