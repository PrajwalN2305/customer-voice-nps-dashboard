import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda():
    cleaned_path = 'data/processed/customer_voice_cleaned.csv'
    eda_dir = 'screenshots/eda'
    
    if not os.path.exists(cleaned_path):
        raise FileNotFoundError(f"Cleaned CSV not found at {cleaned_path}")
        
    os.makedirs(eda_dir, exist_ok=True)
    
    df = pd.read_csv(cleaned_path)
    df['survey_date'] = pd.to_datetime(df['survey_date'])
    
    # Classify NPS Category
    def get_nps_category(score):
        if score >= 9:
            return 'Promoter'
        elif score >= 7:
            return 'Passive'
        else:
            return 'Detractor'
            
    df['nps_category'] = df['nps_score'].apply(get_nps_category)
    
    # Set global plotting style
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['axes.edgecolor'] = '#CCCCCC'
    plt.rcParams['axes.linewidth'] = 0.8
    
    palette_nps = {'Promoter': '#10B981', 'Passive': '#F59E0B', 'Detractor': '#EF4444'}
    primary_color = '#3B82F6'
    
    # ----------------------------------------------------
    # 1. NPS Score Distribution
    # ----------------------------------------------------
    plt.figure(figsize=(9, 5))
    nps_counts = df['nps_score'].value_counts().sort_index()
    colors = ['#EF4444']*7 + ['#F59E0B']*2 + ['#10B981']*2
    bars = plt.bar(nps_counts.index, nps_counts.values, color=colors, edgecolor='none', alpha=0.9)
    plt.title('NPS Score Frequency Distribution (0-10)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('NPS Score', fontsize=12)
    plt.ylabel('Response Count', fontsize=12)
    plt.xticks(range(11))
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 10, f'{int(yval)}', ha='center', va='bottom', fontsize=10)
        
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, 'nps_distribution.png'), dpi=300)
    plt.close()
    
    # ----------------------------------------------------
    # 2. CSAT Score Distribution
    # ----------------------------------------------------
    plt.figure(figsize=(8, 5))
    csat_counts = df['csat_score'].value_counts().sort_index()
    csat_labels = ['1 (Very Dissatisfied)', '2 (Dissatisfied)', '3 (Neutral)', '4 (Satisfied)', '5 (Very Satisfied)']
    bars = plt.bar(range(1, 6), csat_counts.values, color='#6366F1', alpha=0.85, width=0.55)
    plt.title('CSAT Rating Frequency Distribution (1-5)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('CSAT Score', fontsize=12)
    plt.ylabel('Response Count', fontsize=12)
    plt.xticks(range(1, 6), csat_labels, rotation=15)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 15, f'{int(yval)} ({yval/len(df)*100:.1f}%)', ha='center', va='bottom', fontsize=10)
        
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, 'csat_distribution.png'), dpi=300)
    plt.close()
    
    # ----------------------------------------------------
    # 3. Promoter / Passive / Detractor Distribution
    # ----------------------------------------------------
    plt.figure(figsize=(7, 5))
    cat_counts = df['nps_category'].value_counts()[['Promoter', 'Passive', 'Detractor']]
    wedges, texts, autotexts = plt.pie(
        cat_counts.values,
        labels=cat_counts.index,
        autopct='%1.1f%%',
        colors=['#10B981', '#F59E0B', '#EF4444'],
        startangle=140,
        explode=(0.04, 0.02, 0.04),
        textprops=dict(fontsize=11, fontweight='bold')
    )
    plt.title('NPS Customer Sentiment Composition', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, 'promoter_passive_detractor_distribution.png'), dpi=300)
    plt.close()
    
    # Helper to calculate net NPS by group
    def calc_nps(group):
        prom = (group == 'Promoter').sum()
        det = (group == 'Detractor').sum()
        total = len(group)
        return ((prom - det) / total) * 100 if total > 0 else 0

    # ----------------------------------------------------
    # 4. Net NPS by Region
    # ----------------------------------------------------
    plt.figure(figsize=(9, 5))
    region_nps = df.groupby('region')['nps_category'].apply(calc_nps).sort_values(ascending=True)
    bars = plt.barh(region_nps.index, region_nps.values, color='#0EA5E9', height=0.55)
    plt.title('Net NPS (%) by Customer Region', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Net NPS (%)', fontsize=12)
    
    for bar in bars:
        xval = bar.get_width()
        offset = 0.8 if xval >= 0 else -3.5
        plt.text(xval + offset, bar.get_y() + bar.get_height()/2.0, f'{xval:+.1f}%', ha='left' if xval>=0 else 'right', va='center', fontsize=10, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, 'nps_by_region.png'), dpi=300)
    plt.close()
    
    # ----------------------------------------------------
    # 5. Net NPS by Customer Segment
    # ----------------------------------------------------
    plt.figure(figsize=(8, 5))
    seg_nps = df.groupby('customer_segment')['nps_category'].apply(calc_nps).sort_values(ascending=False)
    bars = plt.bar(seg_nps.index, seg_nps.values, color='#8B5CF6', width=0.5)
    plt.title('Net NPS (%) by Customer Segment', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Net NPS (%)', fontsize=12)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f'{yval:+.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, 'nps_by_customer_segment.png'), dpi=300)
    plt.close()

    # ----------------------------------------------------
    # 6. Net NPS by Service Category
    # ----------------------------------------------------
    plt.figure(figsize=(9, 5))
    cat_nps = df.groupby('service_category')['nps_category'].apply(calc_nps).sort_values(ascending=True)
    colors_cat = ['#EF4444' if v < 0 else '#10B981' for v in cat_nps.values]
    bars = plt.barh(cat_nps.index, cat_nps.values, color=colors_cat, height=0.55)
    plt.title('Net NPS (%) by Service Category', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Net NPS (%)', fontsize=12)
    plt.axvline(0, color='#666666', linestyle='--', linewidth=0.8)
    
    for bar in bars:
        xval = bar.get_width()
        plt.text(xval + (0.5 if xval>=0 else -2.5), bar.get_y() + bar.get_height()/2.0, f'{xval:+.1f}%', ha='left' if xval>=0 else 'right', va='center', fontsize=10, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, 'nps_by_service_category.png'), dpi=300)
    plt.close()

    # ----------------------------------------------------
    # 7. Response Volume Over Time (Monthly Trend)
    # ----------------------------------------------------
    plt.figure(figsize=(10, 5))
    df['year_month'] = df['survey_date'].dt.to_period('M').astype(str)
    monthly_vol = df.groupby('year_month').size()
    
    plt.plot(monthly_vol.index, monthly_vol.values, marker='o', color='#2563EB', linewidth=2.5, markersize=7)
    plt.fill_between(monthly_vol.index, monthly_vol.values, color='#3B82F6', alpha=0.15)
    plt.title('Monthly Survey Response Volume (2025)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Response Count', fontsize=12)
    plt.xticks(rotation=45)
    
    for i, txt in enumerate(monthly_vol.values):
        plt.annotate(str(txt), (monthly_vol.index[i], monthly_vol.values[i] + 8), ha='center', fontsize=9)
        
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, 'response_volume_trend.png'), dpi=300)
    plt.close()

    # ----------------------------------------------------
    # 8. Response Channel Distribution
    # ----------------------------------------------------
    plt.figure(figsize=(8, 5))
    channel_counts = df['response_channel'].value_counts()
    bars = plt.bar(channel_counts.index, channel_counts.values, color='#F97316', width=0.5)
    plt.title('Response Volume Distribution by Channel', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Channel', fontsize=12)
    plt.ylabel('Response Count', fontsize=12)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 15, f'{yval:,} ({yval/len(df)*100:.1f}%)', ha='center', va='bottom', fontsize=10)
        
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, 'response_channel_distribution.png'), dpi=300)
    plt.close()

    # ----------------------------------------------------
    # 9. Resolution Days by NPS Category
    # ----------------------------------------------------
    plt.figure(figsize=(8, 5))
    res_by_nps = df.groupby('nps_category')['resolution_days'].mean()[['Promoter', 'Passive', 'Detractor']]
    bars = plt.bar(res_by_nps.index, res_by_nps.values, color=['#10B981', '#F59E0B', '#EF4444'], width=0.5)
    plt.title('Average Resolution Days by NPS Category', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('NPS Category', fontsize=12)
    plt.ylabel('Average Resolution Days', fontsize=12)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{yval:.2f} days', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, 'resolution_days_by_nps.png'), dpi=300)
    plt.close()

    print(f"EDA execution completed successfully. Charts saved in {eda_dir}")

if __name__ == '__main__':
    run_eda()
