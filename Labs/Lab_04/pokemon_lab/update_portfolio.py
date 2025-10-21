#!/usr/bin/env python3
import os
import json
import pandas as pd
import sys

#try:
#    data = json.loads(sys.stdin.read())
#except json.JSONDecodeError:
#    print("Error: Invalid JSON received from the pipe.", file=sys.stderr)
#py    sys.exit(1)

def _load_lookup_data(lookup_dir):
    all_lookup_df = []
    for filename in os.listdir(lookup_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(lookup_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
            df = pd.json_normalize(data['data'], errors='ignore')
            #print("checkpoint!")
            df['card_market_value'] = (
                df['tcgplayer.prices.holofoil.market']
                .fillna(df['tcgplayer.prices.normal.market'])
                .fillna(0.0)
            )
            df = df.rename(columns={
                'id': 'card_id',
                'name': 'card_name',
                'number': 'card_number',
                'set.id': 'set_id',
                'set.name': 'set_name'
            })
            
            required_cols = ['card_id', 'card_name', 'card_number', 'set_id', 'set_name', 'card_market_value']
            df_filtered = df[required_cols]
            all_lookup_df.append(df_filtered.copy())
    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    lookup_df = (
        lookup_df
        .sort_values(by='card_market_value', ascending=False)
        .drop_duplicates(subset=['card_id'], keep='first')
        .reset_index(drop=True)
    )
    return lookup_df

def _load_inventory_data(inventory_dir):
    inventory_data = []
    for filename in os.listdir(inventory_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(inventory_dir, filename)
            df = pd.read_csv(filepath)
            inventory_data.append(df)
    if not inventory_data:
        return pd.DataFrame()
    inventory_df = pd.concat(inventory_data, ignore_index=True)
    inventory_df['card_id'] = inventory_df['set_id'].astype(str) + '-' + inventory_df['card_number'].astype(str)
    return inventory_df 

def update_portfolio(inventory_dir, lookup_dir, output_file):
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    if inventory_df.empty:
        print("No inventory data found.", file=sys.stderr)
        final_cols = ['card_id', 'card_name', 'set_name', 'card_number', 'quantity', 'card_market_value', 'total_value']
        empty_df = pd.DataFrame(columns=final_cols)
        empty_df.to_csv(output_file, index=False)
        return 
    
    merged_df = pd.merge(
        inventory_df,
        lookup_df[['card_id', 'set_name', 'card_market_value']],
        on='card_id',
        how='left'
    )
    merged_df['card_market_value'] = merged_df['card_market_value'].fillna(0.0)
    merged_df['set_name'] = merged_df['set_name'].fillna('NOT_FOUND')

    merged_df['index'] = (
        merged_df['binder_name'].astype(str) + '_' +
        merged_df['page_number'].astype(str) + '_' +
        merged_df['slot_number'].astype(str)
    )

    final_cols = [
        'card_name', 'set_id', 'set_name', 'card_number',
        'card_market_value', 'binder_name', 'page_number',
        'slot_number', 'index'
    ]
    final_df = merged_df[final_cols]
    final_df.to_csv(output_file, index=False)
    print("Portfolio updated successfully.")

def main():
    update_portfolio(
        inventory_dir="./card_inventory/",
        lookup_dir="./card_set_lookup/",
        output_file="card_portfolio.csv"
    )


def test():
    update_portfolio(
        inventory_dir="./card_inventory_test/",
        lookup_dir="./card_set_lookup_test/",
        output_file="card_portfolio_test.csv"
    )
if __name__ == "__main__":
    print("Script Starting in Test Mode", file=sys.stderr)
    test()