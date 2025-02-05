from location_manager import LocationManager

def test_refraction_levels():
    manager = LocationManager()
    test_values = [1.00, 1.02, 1.04, 1.07, 1.10, 1.15, 1.20, 1.25]
    
    print("\nTesting Refraction Levels:")
    print("-" * 50)
    for value in test_values:
        formatted = manager.format_refraction(value)
        print(f"Refraction {value:.2f} -> {formatted}")
    print("-" * 50)

if __name__ == "__main__":
    test_refraction_levels()
