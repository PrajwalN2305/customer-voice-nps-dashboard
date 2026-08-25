import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def generate_architecture_image():
    out_path = 'docs/architecture.png'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(12, 14), facecolor='#0F172A')
    ax.set_facecolor('#0F172A')
    ax.axis('off')
    
    stages = [
        ("1. Data Ingestion Layer", "6,000 Synthetic Raw Records\n(customer_voice_raw.csv)", "#3B82F6"),
        ("2. Data Processing & Validation", "Python / Pandas\n(Profiling, Cleaning, EDA, Validation)", "#10B981"),
        ("3. Cleaned Data Storage", "Processed CSV (customer_voice_cleaned.csv)\n& SQLite DB (customer_voice.db)", "#6366F1"),
        ("4. Analytical Query Engine", "SQL Layer\n(schema.sql & analysis_queries.sql)", "#8B5CF6"),
        ("5. REST API Serving Layer", "FastAPI Backend\n(Endpoints: /api/health, /api/feedback)", "#F59E0B"),
        ("6. Ingestion & Transformation", "Power Query (M Code)\n(JSON Expansion, Schema Typing)", "#EC4899"),
        ("7. Analytical Data Model", "Power BI Data Model & DAX Measures\n(Star Schema, Dim_Date, Time Intelligence)", "#0EA5E9")
    ]
    
    y_start = 0.90
    box_height = 0.08
    box_width = 0.70
    x_center = 0.50
    
    for i, (title, desc, color) in enumerate(stages):
        y_pos = y_start - i * 0.11
        
        # Draw bounding box
        rect = patches.FancyBboxPatch(
            (x_center - box_width/2, y_pos - box_height/2),
            box_width, box_height,
            boxstyle="round,pad=0.02,rounding_size=0.02",
            linewidth=2,
            edgecolor=color,
            facecolor='#1E293B'
        )
        ax.add_patch(rect)
        
        # Add text
        ax.text(x_center, y_pos + 0.015, title, color='#F8FAFC', fontsize=12, fontweight='bold', ha='center', va='center')
        ax.text(x_center, y_pos - 0.018, desc, color='#94A3B8', fontsize=9, ha='center', va='center')
        
        # Draw connecting arrow
        if i < len(stages) - 1:
            arrow = patches.FancyArrow(
                x_center, y_pos - box_height/2 - 0.005,
                0, -0.02,
                width=0.008, head_width=0.025, head_length=0.012,
                length_includes_head=True,
                color='#64748B'
            )
            ax.add_patch(arrow)

    # Split into 2 final dashboards at the bottom
    y_dash = y_start - len(stages) * 0.11 - 0.02
    
    # Left Branch Arrow
    ax.add_patch(patches.FancyArrow(x_center - 0.1, y_dash + 0.07, -0.12, -0.03, width=0.006, head_width=0.02, head_length=0.01, color='#38BDF8'))
    # Right Branch Arrow
    ax.add_patch(patches.FancyArrow(x_center + 0.1, y_dash + 0.07, 0.12, -0.03, width=0.006, head_width=0.02, head_length=0.01, color='#38BDF8'))
    
    # Dashboard 1 Box
    d1 = patches.FancyBboxPatch(
        (0.08, y_dash - 0.05), 0.38, 0.08,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=2, edgecolor='#38BDF8', facecolor='#1E293B'
    )
    ax.add_patch(d1)
    ax.text(0.27, y_dash - 0.005, "Page 1: Customer Experience", color='#F8FAFC', fontsize=11, fontweight='bold', ha='center')
    ax.text(0.27, y_dash - 0.030, "Overview & KPI Performance", color='#94A3B8', fontsize=9, ha='center')
    
    # Dashboard 2 Box
    d2 = patches.FancyBboxPatch(
        (0.54, y_dash - 0.05), 0.38, 0.08,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=2, edgecolor='#38BDF8', facecolor='#1E293B'
    )
    ax.add_patch(d2)
    ax.text(0.73, y_dash - 0.005, "Page 2: Voice of Customer", color='#F8FAFC', fontsize=11, fontweight='bold', ha='center')
    ax.text(0.73, y_dash - 0.030, "Diagnostics & Detail Tables", color='#94A3B8', fontsize=9, ha='center')
    
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Architecture diagram generated at {out_path}")

if __name__ == '__main__':
    generate_architecture_image()
