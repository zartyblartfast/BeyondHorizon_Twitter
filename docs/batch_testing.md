# Batch Testing Guide for BeyondHorizon Calculations

This guide explains how to set up and run batch tests comparing local calculations with the Azure Function API results.

## Prerequisites

1. Python environment with required packages:
   ```bash
   pip install requests pandas python-dotenv tabulate
   ```

2. Environment configuration:
   - Copy `config/.env.template` to `config/.env`
   - Set the following variables in `.env`:
     ```
     AZURE_FUNCTION_URL=https://beyondhorizoncalc.azurewebsites.net
     AZURE_FUNCTION_KEY=your_function_key_here
     ```

## Running the Tests

1. **Basic Test Run**
   ```bash
   python src/test_api_comparison.py
   ```
   This will:
   - Load test locations from GitHub
   - Run calculations for each location using both local and API methods
   - Display detailed comparison results in the console

2. **Generate CSV Comparison**
   ```bash
   python src/test_single_location.py
   ```
   This will test a single location (currently set to Fort Niagara to Toronto) and output detailed API response information.

## Output Files

The test scripts generate several output files in the project root directory:

1. `comparison_niagara_toronto.csv`
   - Contains detailed comparison for Fort Niagara to Toronto case
   - Includes human-friendly descriptions and units
   - Located at: `./comparison_niagara_toronto.csv`

2. Future CSV outputs will be stored in a dedicated `test_results` directory:
   ```
   BeyondHorizon_Twitter/
   ├── test_results/
   │   ├── batch_comparisons/      # For full batch test results
   │   └── single_location/        # For individual location tests
   ```

## Understanding the Output

The test script provides several types of output:

1. **Console Output**
   For each location tested, you'll see:
   - Location name and parameters
   - API calculation results
   - Local calculation results
   - Detailed differences between the two

2. **CSV Output**
   To generate a CSV comparison for a specific location:
   ```python
   python src/generate_comparison_csv.py --location "location_name"
   ```
   The CSV will include:
   - Observer height
   - Target height
   - Distance
   - Hidden height
   - Visible height
   - Apparent height
   - Perspective scaled height
   - Target visibility

## Test Data

The test script uses locations defined in the project's presets. Current test cases include:
- Pic de Finstrelles to Pic Gaspard
- Mount Dankova to Hindu Tagh
- K2 to Broad Peak
- Mount Everest to Kanchenjunga
- And several others

## Adding New Test Cases

To add new test cases:
1. Add the location to the presets JSON file
2. The test script will automatically include it in the next run

## Troubleshooting

Common issues and solutions:

1. **API Connection Errors**
   - Verify your Azure Function URL and key in `.env`
   - Check if the Azure Function is running

2. **Calculation Discrepancies**
   - The script will highlight differences between API and local calculations
   - Focus on the "Differences found" section in the output

3. **Missing Dependencies**
   - Run `pip install -r requirements.txt` to install all needed packages

## Maintenance

The test script may need updates when:
- New calculation parameters are added
- The API response format changes
- New test cases need to be added

## Future Improvements

Planned enhancements:
1. Add command-line arguments for:
   - Selecting specific locations to test
   - Controlling output format
   - Setting comparison tolerance
2. Generate visual comparisons (graphs)
3. Add automated regression testing
