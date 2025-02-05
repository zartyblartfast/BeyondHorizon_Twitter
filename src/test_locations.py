from location_manager import LocationManager

def main():
    manager = LocationManager()
    
    # Get and format a random location
    location = manager.get_random_location()
    tweet = manager.format_tweet(location)
    
    print("\nRandom Location Tweet:")
    print("-" * 50)
    print(tweet)
    print("-" * 50)
    print(f"Tweet length: {len(tweet)} characters")

if __name__ == "__main__":
    main()
