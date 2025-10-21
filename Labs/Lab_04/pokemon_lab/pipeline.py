#!/usr/bin/env python3
import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    print("Running production pipeline...", file=sys.stderr)
    print("Updating portfolio...", file=sys.stderr)
    update_portfolio.main()
    print("Reporting portfolio summary...", file=sys.stderr)
    generate_summary.main()
    print("Completed portfolio summary report...", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()