import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

def generate_dashboard_images():
    cleaned_path = 'data/processed/customer_voice_cleaned.csv'
    if not os.path.exists(cleaned_path):
        raise FileNotFoundError(f"Cleaned CSV not found at {cleaned_path}")
        
    df = pd.read_csv(cleaned_path)
    df['survey_date'] = pd.to_datetime(df['survey_date'])
    
    def get_nps_cat(s):
        if s >= 9: return 'Promoter'
        elif s >= 7: return 'Passive'
        else: return 'Detractor'
        
    df['nps_category'] = df['nps_score'].apply(get_nps_cat)
    
    total_responses = len(df)
    promoters = (df['nps_category'] == 'Promoter').sum()
    passives = (df['nps_category'] == 'Passive').sum()
    detractors = (df['nps_category'] == 'Detractor').sum()
    
    promoter_pct = (promoters / total_responses) * 100
    detractor_pct = (detractors / total_responses) * 100
    net_nps = promoter_pct - detractor_pct  # Score / Points (-100 to +100)
    avg_csat = df['csat_score'].mean()
    avg_res_days = df['resolution_days'].mean()
    
    # ----------------------------------------------------
    # PAGE 1: CUSTOMER EXPERIENCE OVERVIEW
    # ----------------------------------------------------
    fig = plt.figure(figsize=(16, 10), facecolor='#0F172A')
    gs = gridspec.GridSpec(3, 4, figure=fig, height_ratios=[0.8, 1.2, 1.2], hspace=0.35, wspace=0.25)
    
    # Header Banner
    ax_head = fig.add_axes([0.02, 0.92, 0.96, 0.06], facecolor='#1E293B')
    ax_head.axis('off')
    ax_head.text(0.02, 0.65, "Customer Voice & NPS Analytics", color='#F8FAFC', fontsize=20, fontweight='bold', va='center')
    ax_head.text(0.02, 0.25, "Customer Satisfaction | NPS | Operational Performance", color='#94A3B8', fontsize=12, va='center')
    ax_head.text(0.98, 0.45, "Filters: Region | Customer Segment | Service Category | Survey Date", color='#38BDF8', fontsize=10, fontweight='bold', ha='right', va='center')
    
    # KPI 1: Total Responses
    ax_kpi1 = fig.add_subplot(gs[0, 0], facecolor='#1E293B')
    ax_kpi1.axis('off')
    ax_kpi1.text(0.5, 0.70, "TOTAL RESPONSES", color='#94A3B8', fontsize=11, fontweight='bold', ha='center')
    ax_kpi1.text(0.5, 0.35, f"{total_responses:,}", color='#F8FAFC', fontsize=26, fontweight='bold', ha='center')
    
    # KPI 2: Net NPS (Point Score)
    ax_kpi2 = fig.add_subplot(gs[0, 1], facecolor='#1E293B')
    ax_kpi2.axis('off')
    ax_kpi2.text(0.5, 0.70, "NET NPS (SCORE)", color='#94A3B8', fontsize=11, fontweight='bold', ha='center')
    nps_color = '#EF4444' if net_nps < 0 else '#10B981'
    ax_kpi2.text(0.5, 0.35, f"{net_nps:+.1f}", color=nps_color, fontsize=26, fontweight='bold', ha='center')
    
    # KPI 3: Avg CSAT
    ax_kpi3 = fig.add_subplot(gs[0, 2], facecolor='#1E293B')
    ax_kpi3.axis('off')
    ax_kpi3.text(0.5, 0.70, "AVERAGE CSAT", color='#94A3B8', fontsize=11, fontweight='bold', ha='center')
    ax_kpi3.text(0.5, 0.35, f"{avg_csat:.2f}", color='#F8FAFC', fontsize=26, fontweight='bold', ha='center')

    # KPI 4: Promoter %
    ax_kpi4 = fig.add_subplot(gs[0, 3], facecolor='#1E293B')
    ax_kpi4.axis('off')
    ax_kpi4.text(0.5, 0.70, "PROMOTER SHARE", color='#94A3B8', fontsize=11, fontweight='bold', ha='center')
    ax_kpi4.text(0.5, 0.35, f"{promoter_pct:.1f}%", color='#10B981', fontsize=26, fontweight='bold', ha='center')

    # Chart 1: Monthly NPS Trend
    ax_c1 = fig.add_subplot(gs[1, 0:2], facecolor='#1E293B')
    df['ym'] = df['survey_date'].dt.to_period('M').astype(str)
    def calc_net_score(g):
        p = (g == 'Promoter').sum()
        d = (g == 'Detractor').sum()
        return round(((p - d) / len(g)) * 100, 1)
    monthly_nps = df.groupby('ym')['nps_category'].apply(calc_net_score)
    ax_c1.plot(monthly_nps.index, monthly_nps.values, marker='o', color='#38BDF8', linewidth=2.5)
    ax_c1.axhline(0, color='#64748B', linestyle='--', linewidth=1)
    ax_c1.set_title("Monthly NPS Trend (2025)", color='#F8FAFC', fontsize=12, fontweight='bold', loc='left', pad=10)
    ax_c1.tick_params(colors='#94A3B8', labelsize=8)
    ax_c1.set_xticks(range(len(monthly_nps)))
    ax_c1.set_xticklabels(monthly_nps.index, rotation=30)
    ax_c1.grid(True, color='#334155', linestyle=':', alpha=0.6)
    for i, txt in enumerate(monthly_nps.values):
        ax_c1.annotate(f"{txt:+.1f}", (i, txt + (1.5 if txt>=0 else -3.5)), color='#F8FAFC', fontsize=7, ha='center')

    # Chart 2: NPS by Region
    ax_c2 = fig.add_subplot(gs[1, 2:4], facecolor='#1E293B')
    reg_nps = df.groupby('region')['nps_category'].apply(calc_net_score).sort_values()
    bars = ax_c2.barh(reg_nps.index, reg_nps.values, color='#0EA5E9', height=0.55)
    ax_c2.set_title("NPS by Region", color='#F8FAFC', fontsize=12, fontweight='bold', loc='left', pad=10)
    ax_c2.tick_params(colors='#94A3B8', labelsize=9)
    ax_c2.grid(True, color='#334155', linestyle=':', alpha=0.6)
    for bar in bars:
        w = bar.get_width()
        ax_c2.text(w + (0.5 if w>=0 else -3.5), bar.get_y() + bar.get_height()/2.0, f"{w:+.1f}", color='#F8FAFC', fontsize=8, fontweight='bold', va='center')

    # Chart 3: NPS Category Distribution (Promoters vs Passives vs Detractors)
    ax_c3 = fig.add_subplot(gs[2, 0], facecolor='#1E293B')
    wedges, texts, autotexts = ax_c3.pie(
        [promoters, passives, detractors],
        labels=['Promoters', 'Passives', 'Detractors'],
        autopct='%1.1f%%',
        colors=['#10B981', '#F59E0B', '#EF4444'],
        startangle=140,
        pctdistance=0.75,
        textprops=dict(color='#F8FAFC', fontsize=8, fontweight='bold')
    )
    centre_circle = plt.Circle((0,0), 0.50, fc='#1E293B')
    ax_c3.add_artist(centre_circle)
    ax_c3.set_title("NPS Category Distribution", color='#F8FAFC', fontsize=11, fontweight='bold', loc='left', pad=10)

    # Chart 4: Avg CSAT by Customer Segment
    ax_c4 = fig.add_subplot(gs[2, 1:3], facecolor='#1E293B')
    seg_csat = df.groupby('customer_segment')['csat_score'].mean().sort_values(ascending=False)
    bars = ax_c4.bar(seg_csat.index, seg_csat.values, color='#8B5CF6', width=0.45)
    ax_c4.set_title("Average CSAT by Customer Segment", color='#F8FAFC', fontsize=12, fontweight='bold', loc='left', pad=10)
    ax_c4.set_ylim(0, 5)
    ax_c4.tick_params(colors='#94A3B8', labelsize=9)
    ax_c4.grid(True, color='#334155', linestyle=':', alpha=0.6)
    for bar in bars:
        h = bar.get_height()
        ax_c4.text(bar.get_x() + bar.get_width()/2.0, h + 0.1, f"{h:.2f}", color='#F8FAFC', fontsize=9, fontweight='bold', ha='center')

    # Chart 5: Response Volume by Channel
    ax_c5 = fig.add_subplot(gs[2, 3], facecolor='#1E293B')
    chan_vol = df['response_channel'].value_counts()
    bars = ax_c5.bar(chan_vol.index, chan_vol.values, color='#F97316', width=0.5)
    ax_c5.set_title("Response Volume by Channel", color='#F8FAFC', fontsize=11, fontweight='bold', loc='left', pad=10)
    ax_c5.tick_params(colors='#94A3B8', labelsize=8)
    ax_c5.grid(True, color='#334155', linestyle=':', alpha=0.6)
    for bar in bars:
        h = bar.get_height()
        ax_c5.text(bar.get_x() + bar.get_width()/2.0, h + 20, f"{h:,}", color='#F8FAFC', fontsize=8, ha='center')

    p1_path = 'screenshots/customer_experience_overview.png'
    plt.savefig(p1_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Page 1 screenshot regenerated at {p1_path}")

    # ----------------------------------------------------
    # PAGE 2: VOICE OF CUSTOMER ANALYSIS
    # ----------------------------------------------------
    fig2 = plt.figure(figsize=(16, 10), facecolor='#0F172A')
    gs2 = gridspec.GridSpec(3, 4, figure=fig2, height_ratios=[0.8, 1.2, 1.3], hspace=0.35, wspace=0.25)
    
    # Header Banner
    ax_head2 = fig2.add_axes([0.02, 0.92, 0.96, 0.06], facecolor='#1E293B')
    ax_head2.axis('off')
    ax_head2.text(0.02, 0.65, "Voice of Customer Analysis", color='#F8FAFC', fontsize=20, fontweight='bold', va='center')
    ax_head2.text(0.02, 0.25, "Service Category Diagnostics & Customer Feedback Detail", color='#94A3B8', fontsize=12, va='center')
    ax_head2.text(0.98, 0.45, "Filters: Service Category | Response Channel | NPS Category", color='#38BDF8', fontsize=10, fontweight='bold', ha='right', va='center')

    # Visual 1: Response Distribution by Service Category
    ax_v1 = fig2.add_subplot(gs2[0, 0:2], facecolor='#1E293B')
    cat_vol = df['service_category'].value_counts()
    bars = ax_v1.bar(cat_vol.index, cat_vol.values, color='#3B82F6', width=0.5)
    ax_v1.set_title("Response Distribution by Service Category", color='#F8FAFC', fontsize=11, fontweight='bold', loc='left', pad=10)
    ax_v1.tick_params(colors='#94A3B8', labelsize=8)
    ax_v1.grid(True, color='#334155', linestyle=':', alpha=0.6)
    for bar in bars:
        h = bar.get_height()
        ax_v1.text(bar.get_x() + bar.get_width()/2.0, h + 15, f"{h:,} ({h/total_responses*100:.1f}%)", color='#F8FAFC', fontsize=8, ha='center')

    # Visual 2: NPS by Service Category
    ax_v2 = fig2.add_subplot(gs2[0, 2:4], facecolor='#1E293B')
    cat_nps = df.groupby('service_category')['nps_category'].apply(calc_net_score).sort_values()
    colors_cat = ['#EF4444' if v < 0 else '#10B981' for v in cat_nps.values]
    bars = ax_v2.barh(cat_nps.index, cat_nps.values, color=colors_cat, height=0.5)
    ax_v2.set_title("NPS by Service Category", color='#F8FAFC', fontsize=11, fontweight='bold', loc='left', pad=10)
    ax_v2.axvline(0, color='#64748B', linestyle='--', linewidth=1)
    ax_v2.tick_params(colors='#94A3B8', labelsize=8)
    ax_v2.grid(True, color='#334155', linestyle=':', alpha=0.6)
    for bar in bars:
        w = bar.get_width()
        ax_v2.text(w + (0.5 if w>=0 else -4.5), bar.get_y() + bar.get_height()/2.0, f"{w:+.1f}", color='#F8FAFC', fontsize=8, fontweight='bold', va='center')

    # Visual 3: NPS by Customer Segment
    ax_v3 = fig2.add_subplot(gs2[1, 0:2], facecolor='#1E293B')
    seg_nps = df.groupby('customer_segment')['nps_category'].apply(calc_net_score).sort_values(ascending=False)
    bars = ax_v3.bar(seg_nps.index, seg_nps.values, color='#8B5CF6', width=0.45)
    ax_v3.set_title("NPS by Customer Segment", color='#F8FAFC', fontsize=11, fontweight='bold', loc='left', pad=10)
    ax_v3.tick_params(colors='#94A3B8', labelsize=8)
    ax_v3.grid(True, color='#334155', linestyle=':', alpha=0.6)
    for bar in bars:
        h = bar.get_height()
        ax_v3.text(bar.get_x() + bar.get_width()/2.0, h + (0.5 if h>=0 else -2), f"{h:+.1f}", color='#F8FAFC', fontsize=8, fontweight='bold', ha='center')

    # Visual 4: Resolution Days by NPS Category
    ax_v4 = fig2.add_subplot(gs2[1, 2:4], facecolor='#1E293B')
    res_nps = df.groupby('nps_category')['resolution_days'].mean()[['Promoter', 'Passive', 'Detractor']]
    bars = ax_v4.bar(res_nps.index, res_nps.values, color=['#10B981', '#F59E0B', '#EF4444'], width=0.45)
    ax_v4.set_title("Average Resolution Days by NPS Category", color='#F8FAFC', fontsize=11, fontweight='bold', loc='left', pad=10)
    ax_v4.tick_params(colors='#94A3B8', labelsize=8)
    ax_v4.grid(True, color='#334155', linestyle=':', alpha=0.6)
    for bar in bars:
        h = bar.get_height()
        ax_v4.text(bar.get_x() + bar.get_width()/2.0, h + 0.1, f"{h:.2f} days", color='#F8FAFC', fontsize=8, fontweight='bold', ha='center')

    # Visual 5 & 6: Low-NPS Customer Feedback Detail Table (NPS <= 6)
    ax_t = fig2.add_subplot(gs2[2, 0:4], facecolor='#1E293B')
    ax_t.axis('off')
    ax_t.set_title("Low-NPS Customer Feedback Detail Table (Detractor Escalations: NPS <= 6)", color='#F8FAFC', fontsize=12, fontweight='bold', loc='left', pad=10)
    
    low_nps_df = df[df['nps_score'] <= 6][['survey_date', 'region', 'customer_segment', 'service_category', 'nps_score', 'csat_score', 'resolution_days', 'issue_resolved', 'feedback_text']].head(6)
    low_nps_df['survey_date'] = low_nps_df['survey_date'].dt.strftime('%Y-%m-%d')
    
    table_data = [low_nps_df.columns.tolist()] + low_nps_df.values.tolist()
    
    table = ax_t.table(
        cellText=table_data,
        cellLoc='left',
        loc='center',
        bbox=[0, 0.05, 1, 0.88]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7.5)
    
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#334155')
        if row == 0:
            cell.set_facecolor('#0F172A')
            cell.set_text_props(color='#38BDF8', fontweight='bold')
        else:
            cell.set_facecolor('#1E293B' if row % 2 == 0 else '#0F172A')
            cell.set_text_props(color='#F8FAFC')
            
    p2_path = 'screenshots/voice_of_customer.png'
    plt.savefig(p2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Page 2 screenshot regenerated at {p2_path}")

if __name__ == '__main__':
    generate_dashboard_images()
