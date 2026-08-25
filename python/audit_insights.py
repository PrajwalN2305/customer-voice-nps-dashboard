import pandas as pd

def calc_insights():
    df = pd.read_csv('data/processed/customer_voice_cleaned.csv')
    
    def get_cat(score):
        if score >= 9: return 'Promoter'
        elif score >= 7: return 'Passive'
        else: return 'Detractor'
        
    df['nps_cat'] = df['nps_score'].apply(get_cat)
    
    def nps_score(group):
        p = (group == 'Promoter').sum()
        d = (group == 'Detractor').sum()
        return round(((p - d) / len(group)) * 100, 2)
        
    print("=== 1. RESOLUTION DAYS BY NPS CATEGORY ===")
    res_by_nps = df.groupby('nps_cat')['resolution_days'].mean()
    for cat in ['Promoter', 'Passive', 'Detractor']:
        print(f"  {cat}: {res_by_nps[cat]:.2f} days")
        
    print("\n=== 2. NET NPS BY SERVICE CATEGORY ===")
    cat_nps = df.groupby('service_category')['nps_cat'].apply(nps_score).sort_values()
    for c, score in cat_nps.items():
        print(f"  {c}: {score:+.2f}")
        
    print("\n=== 3. NET NPS & CSAT BY CUSTOMER SEGMENT ===")
    seg_nps = df.groupby('customer_segment')['nps_cat'].apply(nps_score)
    seg_csat = df.groupby('customer_segment')['csat_score'].mean()
    for s in ['Enterprise', 'Mid-Market', 'SMB']:
        print(f"  {s}: NPS = {seg_nps[s]:+.2f}, CSAT = {seg_csat[s]:.2f}")
        
    print("\n=== 4. NET NPS & CSAT BY REGION ===")
    reg_nps = df.groupby('region')['nps_cat'].apply(nps_score).sort_values()
    reg_csat = df.groupby('region')['csat_score'].mean()
    for r, score in reg_nps.items():
        print(f"  {r}: NPS = {score:+.2f}, CSAT = {reg_csat[r]:.2f}")
        
    print("\n=== 5. CHANNEL DISTRIBUTION ===")
    chan_vol = df['response_channel'].value_counts()
    chan_csat = df.groupby('response_channel')['csat_score'].mean()
    chan_det = df.groupby('response_channel')['nps_cat'].apply(lambda x: (x=='Detractor').sum()/len(x)*100)
    for ch in chan_vol.index:
        print(f"  {ch}: Vol = {chan_vol[ch]} ({chan_vol[ch]/len(df)*100:.1f}%), CSAT = {chan_csat[ch]:.2f}, Detractor % = {chan_det[ch]:.2f}%")

if __name__ == '__main__':
    calc_insights()
