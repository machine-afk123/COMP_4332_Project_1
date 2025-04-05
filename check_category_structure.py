import json

def check_category_structure(data_file='data/product.json'):
    """
    Analyzes the product data to answer:
    1. Whether the data has category lists with a length greater than 3
    2. Whether for each list the first two values are always the same
    
    Returns a dictionary with the results and supporting data
    """
    # Load the data
    with open(data_file, 'r') as f:
        product_data_json = json.load(f)

    product_data_json_structured = {product_data_json[i]['ProductID']: product_data_json[i] 
                                  for i in range(len(product_data_json))}
    
    # Initialize analysis variables
    total_products = len(product_data_json_structured)
    products_with_long_categories = []
    first_elements = set()
    second_elements = set()
    
    # Keep track of the most common first two elements
    standard_first_element = None
    standard_second_element = None
    
    # Analyze each product
    for product_id, product_data in product_data_json_structured.items():
        category = product_data.get('category', [])
        
        if isinstance(category, list) and len(category) > 0:
            # Check for categories with length > 3
            if len(category) > 3:
                products_with_long_categories.append({
                    'product_id': product_id,
                    'category': category
                })
            
            # Track the first two elements (if available)
            if len(category) >= 1:
                first_elements.add(category[0])
                if standard_first_element is None:
                    standard_first_element = category[0]
                
            if len(category) >= 2:
                second_elements.add(category[1])
                if standard_second_element is None:
                    standard_second_element = category[1]
    
    # Determine if the first two elements are consistent
    has_consistent_first_two = len(first_elements) == 1 and len(second_elements) == 1
    
    # Compile results
    results = {
        'total_products': total_products,
        'has_categories_with_length_greater_than_3': len(products_with_long_categories) > 0,
        'count_categories_with_length_greater_than_3': len(products_with_long_categories),
        'first_two_elements_always_same': has_consistent_first_two,
        'unique_first_elements': list(first_elements),
        'unique_second_elements': list(second_elements),
        'examples_of_long_categories': products_with_long_categories[:5] if products_with_long_categories else []
    }
    
    return results

if __name__ == "__main__":
    results = check_category_structure()
    
    print("=== CATEGORY STRUCTURE ANALYSIS ===")
    print(f"Total products analyzed: {results['total_products']}")
    
    print(f"\nQ1: Does the data have category lists with length greater than 3?")
    print(f"A1: {'Yes' if results['has_categories_with_length_greater_than_3'] else 'No'}")
    print(f"   Number of products with long categories: {results['count_categories_with_length_greater_than_3']}")
    
    print(f"\nQ2: Are the first two values in each category list always the same?")
    print(f"A2: {'Yes' if results['first_two_elements_always_same'] else 'No'}")
    print(f"   Unique first elements: {results['unique_first_elements']}")
    print(f"   Unique second elements: {results['unique_second_elements']}")
    
    if results['examples_of_long_categories']:
        print("\nExamples of categories with length > 3:")
        for i, example in enumerate(results['examples_of_long_categories']):
            print(f"  {i+1}. Product {example['product_id']}: {example['category']}") 