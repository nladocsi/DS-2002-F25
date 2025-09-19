.PHONY: all fetch analyze clean

analyze: fetch
	@echo "--- Analyze data ---"
	bash ./analyze_data.sh
	@echo "--- Pipeline complete ---"

fetch: 
	@echo "--- Fetching data ---"
	bash ./fetch_metars.sh
	@echo "--- Data Fetched into raw_metars ---"

clean:
	@echo "--- Cleaning up ---"
	rm -rf raw_metars/ weather_report.csv
	@echo "--- Cleaning and removing complete ---"
