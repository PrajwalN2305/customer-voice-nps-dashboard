import random
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_synthetic_data(seed=42):
    np.random.seed(seed)
    random.seed(seed)
    
    total_records = 6000
    
    # 1. Base entities
    # Create ~4200 unique customers for 6000 responses (some repeat customers)
    customer_ids = [f"CUST-{1000 + i}" for i in range(4200)]
    
    regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East & Africa']
    region_weights = [0.40, 0.28, 0.18, 0.09, 0.05]
    
    segments = ['Enterprise', 'Mid-Market', 'SMB']
    segment_weights = [0.25, 0.45, 0.30]
    
    industries = ['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing']
    industry_weights = [0.35, 0.20, 0.22, 0.13, 0.10]
    
    channels = ['Email', 'Phone', 'Web', 'In-App']
    channel_weights = [0.42, 0.25, 0.21, 0.12]
    
    service_categories = ['Product', 'Delivery', 'Customer Support', 'Quality', 'Pricing']
    category_weights = [0.30, 0.22, 0.25, 0.13, 0.10]
    
    start_date = datetime(2025, 1, 1)
    
    # Text templates by sentiment/category
    detractor_feedback = [
        "Support response was extremely slow and unhelpful.",
        "Product keeps crashing after the latest update.",
        "Delivery took twice as long as promised.",
        "Pricing is way too high for the features provided.",
        "Quality has visibly degraded over the last few months.",
        "Issue took over a week to resolve, very frustrating.",
        "Customer service agent was rude and transferred me three times.",
        "Billing error was not resolved on time.",
        "Platform UI is slow and unintuitive.",
        "Frequent downtime impacted our business operations."
    ]
    
    passive_feedback = [
        "Product works fine, but missing key integrations.",
        "Support resolved the issue, but communication could be better.",
        "Average experience, nothing exceptional to report.",
        "Pricing is fair, but onboarding was slightly confusing.",
        "Delivery was on time, product packaging was slightly damaged.",
        "Acceptable response time, issue was eventually fixed.",
        "Decent features for SMBs, but needs better reporting tools.",
        "Service is okay, expecting more frequent software updates."
    ]
    
    promoter_feedback = [
        "Exceptional customer support! Issue resolved within an hour.",
        "Fantastic product! Has significantly improved our team productivity.",
        "Super fast delivery and pristine quality. Highly recommended!",
        "Great value for money and outstanding service reliability.",
        "The team went above and beyond to help us with our migration.",
        "Smooth experience from purchase to setup. Very satisfied!",
        "Top-tier enterprise platform with excellent security features.",
        "Best customer service team in the industry. Kudos!"
    ]

    records = []
    
    for i in range(total_records):
        resp_id = f"RSP-{i+1:04d}"
        cust_id = random.choice(customer_ids)
        
        # Date distribution across 365 days
        days_offset = random.randint(0, 364)
        s_date = (start_date + timedelta(days=days_offset)).strftime('%Y-%m-%d')
        
        region = np.random.choice(regions, p=region_weights)
        segment = np.random.choice(segments, p=segment_weights)
        industry = np.random.choice(industries, p=industry_weights)
        channel = np.random.choice(channels, p=channel_weights)
        category = np.random.choice(service_categories, p=category_weights)
        
        # Category specific satisfaction bias
        # Product & Customer Support have higher baseline, Pricing & Delivery have higher friction
        if category in ['Customer Support', 'Product']:
            nps_prob = [0.03, 0.03, 0.04, 0.04, 0.05, 0.06, 0.08, 0.15, 0.17, 0.18, 0.17]
        elif category in ['Pricing', 'Delivery']:
            nps_prob = [0.10, 0.09, 0.09, 0.10, 0.11, 0.11, 0.12, 0.10, 0.08, 0.06, 0.04]
        else:
            nps_prob = [0.05, 0.05, 0.06, 0.07, 0.08, 0.09, 0.12, 0.14, 0.14, 0.11, 0.09]
            
        nps = int(np.random.choice(range(11), p=nps_prob))
        
        # CSAT correlates with NPS
        if nps >= 9:
            csat = int(np.random.choice([4, 5], p=[0.2, 0.8]))
            res_days = int(np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1]))
            issue_res = np.random.choice(['Yes', 'No'], p=[0.97, 0.03])
            fb = random.choice(promoter_feedback)
        elif nps >= 7:
            csat = int(np.random.choice([3, 4, 5], p=[0.25, 0.60, 0.15]))
            res_days = int(np.random.choice([2, 3, 4, 5], p=[0.3, 0.4, 0.2, 0.1]))
            issue_res = np.random.choice(['Yes', 'No'], p=[0.88, 0.12])
            fb = random.choice(passive_feedback)
        else:
            csat = int(np.random.choice([1, 2, 3], p=[0.45, 0.40, 0.15]))
            res_days = int(np.random.choice([4, 5, 7, 10, 14, 21], p=[0.2, 0.25, 0.25, 0.15, 0.1, 0.05]))
            issue_res = np.random.choice(['Yes', 'No'], p=[0.65, 0.35])
            fb = random.choice(detractor_feedback)
            
        records.append({
            'response_id': resp_id,
            'customer_id': cust_id,
            'survey_date': s_date,
            'region': region,
            'customer_segment': segment,
            'industry': industry,
            'response_channel': channel,
            'service_category': category,
            'nps_score': nps,
            'csat_score': csat,
            'resolution_days': res_days,
            'issue_resolved': issue_res,
            'feedback_text': fb
        })
        
    df = pd.DataFrame(records)
    
    # ----------------------------------------------------
    # INTRODUCE CONTROLLED DATA-QUALITY ISSUES (Seeding)
    # ----------------------------------------------------
    
    # 1. Missing CSAT values (~90 records, ~1.5%)
    missing_csat_idx = random.sample(range(total_records), 90)
    for idx in missing_csat_idx:
        df.loc[idx, 'csat_score'] = np.nan
        
    # 2. Missing Industry values (~60 records, ~1.0%)
    missing_ind_idx = random.sample(range(total_records), 60)
    for idx in missing_ind_idx:
        df.loc[idx, 'industry'] = np.nan
        
    # 3. Missing Feedback text (~60 records, ~1.0%)
    missing_fb_idx = random.sample(range(total_records), 60)
    for idx in missing_fb_idx:
        df.loc[idx, 'feedback_text'] = np.nan
        
    # 4. Inconsistent category spellings / capitalization (~80 records)
    dirty_cat_idx = random.sample(range(total_records), 80)
    inconsistent_map = {
        'Customer Support': 'customer support',
        'Delivery': 'DELIVERY',
        'Product': 'Product ',
        'Pricing': 'pricing',
        'Quality': 'QUALITY '
    }
    for idx in dirty_cat_idx:
        orig = df.loc[idx, 'service_category']
        if orig in inconsistent_map:
            df.loc[idx, 'service_category'] = inconsistent_map[orig]
            
    # 5. Invalid NPS values outside 0-10 (~15 records)
    invalid_nps_idx = random.sample(range(total_records), 15)
    invalid_nps_vals = [-2, -1, 11, 12, 99]
    for i, idx in enumerate(invalid_nps_idx):
        df.loc[idx, 'nps_score'] = invalid_nps_vals[i % len(invalid_nps_vals)]
        
    # 6. Invalid CSAT values outside 1-5 (~12 records, excluding NaN)
    valid_csat_indices = [i for i in range(total_records) if i not in missing_csat_idx]
    invalid_csat_idx = random.sample(valid_csat_indices, 12)
    invalid_csat_vals = [0, 6, 7, 9]
    for i, idx in enumerate(invalid_csat_idx):
        df.loc[idx, 'csat_score'] = invalid_csat_vals[i % len(invalid_csat_vals)]
        
    # 7. Negative resolution_days values (~15 records)
    invalid_res_idx = random.sample(range(total_records), 15)
    invalid_res_vals = [-5, -3, -2, -1]
    for i, idx in enumerate(invalid_res_idx):
        df.loc[idx, 'resolution_days'] = invalid_res_vals[i % len(invalid_res_vals)]
        
    # 8. Missing or malformed survey dates (~10 records)
    invalid_date_idx = random.sample(range(total_records), 10)
    malformed_dates = ['2025-13-45', 'INVALID_DATE', '2025-02-30', '9999-99-99', '']
    for i, idx in enumerate(invalid_date_idx):
        df.loc[idx, 'survey_date'] = malformed_dates[i % len(malformed_dates)]

    # 9. Duplicate records (35 duplicate rows appended, maintaining EXACTLY 6,000 raw records total)
    # To keep total exact count 6,000 raw records: replace last 35 rows with exact duplicates of random earlier rows!
    dup_sources = random.sample(range(5000), 35)
    for i, src_idx in enumerate(dup_sources):
        target_idx = 5965 + i
        df.iloc[target_idx] = df.iloc[src_idx].copy()
        
    output_path = 'data/raw/customer_voice_raw.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} raw records at {output_path}")

if __name__ == '__main__':
    generate_synthetic_data()
