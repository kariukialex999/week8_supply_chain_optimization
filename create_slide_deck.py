"""
Generate Quarterly Operations Review Slide Deck PDF
Week 8 Supply Chain Optimization Project
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = landscape(LETTER)

def create_slide_deck():
    """Create the quarterly operations review slide deck."""
    
    doc = SimpleDocTemplate(
        "Week8_Quarterly_Ops_Review.pdf",
        pagesize=landscape(LETTER),
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a365d'),
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#2c5282'),
        alignment=TA_CENTER,
        spaceAfter=15
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Heading2'],
        fontSize=22,
        textColor=colors.HexColor('#1a365d'),
        alignment=TA_LEFT,
        spaceAfter=15,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#2d3748'),
        alignment=TA_LEFT,
        spaceAfter=10,
        leading=18
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#2d3748'),
        alignment=TA_LEFT,
        leftIndent=20,
        spaceAfter=8,
        leading=20
    )
    
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#276749'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        spaceAfter=10
    )
    
    story = []
    
    # ========== SLIDE 1: Title Slide ==========
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("Quarterly Operations Review", title_style))
    story.append(Paragraph("Q3 2026 Performance & Strategic Outlook", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Supply Chain & Operations Analytics Team", body_style))
    story.append(Paragraph("September 21, 2026", body_style))
    story.append(Spacer(1, 1*inch))
    
    # Key metrics preview
    metrics_data = [
        ['Forecast Accuracy', 'Service Level', 'Cost Savings', 'Safety Index'],
        ['92.4%', '97.8%', '$847K', '98.2%']
    ]
    metrics_table = Table(metrics_data, colWidths=[2.2*inch]*4)
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#c6f6d5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#276749')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, 1), 18),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
    ]))
    story.append(metrics_table)
    story.append(PageBreak())
    
    # ========== SLIDE 2: Executive Summary (BLUF) ==========
    story.append(Paragraph("Executive Summary", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>Bottom Line Up Front (BLUF)</b>", header_style))
    story.append(Spacer(1, 0.2*inch))
    
    bluf_text = """
    Our supply chain optimization initiative has delivered <b>$847K in annual savings</b> through 
    improved demand forecasting and inventory management. Key achievements:
    """
    story.append(Paragraph(bluf_text, body_style))
    story.append(Spacer(1, 0.2*inch))
    
    bullets = [
        "<bullet>&bull;</bullet> <b>Forecast accuracy improved to 92.4%</b> (MAPE of 7.6%) using Prophet model with holiday/promotion regressors",
        "<bullet>&bull;</bullet> <b>Service level increased from 89% to 97.8%</b> through optimized safety stock policy",
        "<bullet>&bull;</bullet> <b>Distribution costs reduced by 15%</b> via linear programming optimization",
        "<bullet>&bull;</bullet> <b>Stockout incidents reduced by 78%</b> compared to previous quarter"
    ]
    for bullet in bullets:
        story.append(Paragraph(bullet, bullet_style))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Recommendation:</b> Approve full deployment of optimized inventory policy across all 5 distribution centers.", highlight_style))
    story.append(PageBreak())
    
    # ========== SLIDE 3: Safety Performance ==========
    story.append(Paragraph("Safety & Equipment Health", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Safety Performance (Weeks 6-7 Recap)</b>", header_style))
    
    safety_data = [
        ['Metric', 'Target', 'Actual', 'Status'],
        ['TRIR (Total Recordable Incident Rate)', '< 2.0', '1.4', 'On Track'],
        ['Near-Miss Reports', '> 50/month', '67', 'Exceeds'],
        ['Safety Training Completion', '100%', '98.2%', 'On Track'],
        ['Equipment Downtime', '< 3%', '2.1%', 'On Track'],
        ['Predictive Maintenance Alerts', 'N/A', '23 resolved', 'Active']
    ]
    
    safety_table = Table(safety_data, colWidths=[3*inch, 1.5*inch, 1.5*inch, 1.2*inch])
    safety_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('BACKGROUND', (3, 1), (3, -1), colors.HexColor('#c6f6d5')),
    ]))
    story.append(safety_table)
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Key Insights:</b>", header_style))
    
    safety_bullets = [
        "<bullet>&bull;</bullet> Zero lost-time injuries for 127 consecutive days",
        "<bullet>&bull;</bullet> Predictive maintenance reduced unplanned downtime by 34%",
        "<bullet>&bull;</bullet> Forklift fleet health at 96% - scheduled Q4 maintenance for aging units"
    ]
    for bullet in safety_bullets:
        story.append(Paragraph(bullet, bullet_style))
    story.append(PageBreak())
    
    # ========== SLIDE 4: Equipment Health Details ==========
    story.append(Paragraph("Equipment Health Dashboard", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Critical Equipment Status</b>", header_style))
    
    equipment_data = [
        ['Equipment', 'Health Score', 'Next Service', 'Risk Level'],
        ['Conveyor System A', '94%', 'Oct 15', 'Low'],
        ['Conveyor System B', '87%', 'Sep 28', 'Medium'],
        ['Packaging Line 1', '96%', 'Nov 1', 'Low'],
        ['Packaging Line 2', '91%', 'Oct 8', 'Low'],
        ['Forklift Fleet (12 units)', '89%', 'Rolling', 'Medium'],
        ['HVAC - Warehouse', '82%', 'Sep 25', 'Medium']
    ]
    
    equip_table = Table(equipment_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    equip_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
    ]))
    story.append(equip_table)
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Action Items:</b>", header_style))
    action_bullets = [
        "<bullet>&bull;</bullet> Priority: HVAC maintenance scheduled for Sep 25 to prevent Q4 issues",
        "<bullet>&bull;</bullet> Conveyor B bearing replacement planned - parts on order",
        "<bullet>&bull;</bullet> Budget request: $45K for forklift battery replacements (3 units)"
    ]
    for bullet in action_bullets:
        story.append(Paragraph(bullet, bullet_style))
    story.append(PageBreak())
    
    # ========== SLIDE 5: Supply Chain - Forecast Results ==========
    story.append(Paragraph("Supply Chain: Demand Forecasting", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Prophet Model Performance</b>", header_style))
    
    forecast_data = [
        ['Metric', 'Value', 'Industry Benchmark', 'Assessment'],
        ['MAPE', '7.6%', '< 15%', 'Excellent'],
        ['RMSE', '48.2 units', 'N/A', 'Good'],
        ['Forecast Horizon', '60 days', '30-90 days', 'Standard'],
        ['External Factors', 'Holidays + Promotions', 'Varies', 'Enhanced']
    ]
    
    forecast_table = Table(forecast_data, colWidths=[2.2*inch, 1.8*inch, 1.8*inch, 1.4*inch])
    forecast_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#276749')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('BACKGROUND', (3, 1), (3, 1), colors.HexColor('#c6f6d5')),
    ]))
    story.append(forecast_table)
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Key Findings:</b>", header_style))
    forecast_bullets = [
        "<bullet>&bull;</bullet> Weekly seasonality: 20% higher demand Mon-Fri vs weekends",
        "<bullet>&bull;</bullet> Q4 holiday uplift: 25-35% above baseline (Nov-Dec)",
        "<bullet>&bull;</bullet> Promotion events drive 25% demand spikes - now predictable",
        "<bullet>&bull;</bullet> Weather integration planned for Q4 (potential 3% accuracy gain)"
    ]
    for bullet in forecast_bullets:
        story.append(Paragraph(bullet, bullet_style))
    story.append(PageBreak())
    
    # ========== SLIDE 6: Inventory Optimization ==========
    story.append(Paragraph("Supply Chain: Inventory Optimization", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Safety Stock & Reorder Point Analysis</b>", header_style))
    
    inventory_data = [
        ['Parameter', 'Old Policy', 'New Policy', 'Impact'],
        ['Service Level Target', '90%', '95%', '+5%'],
        ['Safety Stock', '892 units', '1,247 units', '+355 units'],
        ['Reorder Point', '4,392 units', '4,747 units', '+355 units'],
        ['Stockout Days/Year', '38 days', '8 days', '-79%'],
        ['Annual Holding Cost', '$651K', '$912K', '+$261K'],
        ['Annual Stockout Cost', '$1,425K', '$300K', '-$1,125K']
    ]
    
    inv_table = Table(inventory_data, colWidths=[2.2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    inv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#744210')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('BACKGROUND', (3, 4), (3, 4), colors.HexColor('#c6f6d5')),
        ('BACKGROUND', (3, 6), (3, 6), colors.HexColor('#c6f6d5')),
    ]))
    story.append(inv_table)
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>NET ANNUAL SAVINGS: $864,000</b>", highlight_style))
    story.append(Paragraph("(Stockout cost reduction minus additional holding cost)", body_style))
    story.append(PageBreak())
    
    # ========== SLIDE 7: Distribution Optimization ==========
    story.append(Paragraph("Supply Chain: Distribution Network", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Linear Programming Optimization Results</b>", header_style))
    
    dist_data = [
        ['Route', 'Volume (units/day)', 'Cost/Unit', 'Daily Cost'],
        ['W1_Central -> Store_A', '800', '$2.50', '$2,000'],
        ['W2_North -> Store_B', '650', '$2.00', '$1,300'],
        ['W2_North -> Store_D', '550', '$2.50', '$1,375'],
        ['W3_South -> Store_C', '900', '$2.00', '$1,800'],
        ['W3_South -> Store_E', '700', '$2.50', '$1,750'],
        ['TOTAL', '3,600', 'Avg: $2.28', '$8,225']
    ]
    
    dist_table = Table(dist_data, colWidths=[2.5*inch, 1.8*inch, 1.3*inch, 1.5*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#553c9a')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e2e8f0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
    ]))
    story.append(dist_table)
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Optimization Impact:</b>", header_style))
    dist_bullets = [
        "<bullet>&bull;</bullet> 15% cost reduction vs. previous equal-distribution policy",
        "<bullet>&bull;</bullet> Warehouse utilization balanced: 67% (W1), 80% (W2), 89% (W3)",
        "<bullet>&bull;</bullet> Sensitivity analysis: Network can absorb 18% demand surge before capacity constraints"
    ]
    for bullet in dist_bullets:
        story.append(Paragraph(bullet, bullet_style))
    story.append(PageBreak())
    
    # ========== SLIDE 8: Strategic Recommendations ==========
    story.append(Paragraph("Strategic Recommendations", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Recommendation 1
    story.append(Paragraph("<b>1. Deploy Optimized Safety Stock Policy Enterprise-Wide</b>", header_style))
    rec1_data = [
        ['Investment', 'Expected ROI', 'Payback', 'Risk'],
        ['$261K (holding cost increase)', '$864K net savings/year', '3.6 months', 'Low']
    ]
    rec1_table = Table(rec1_data, colWidths=[2.5*inch, 2.2*inch, 1.5*inch, 1*inch])
    rec1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
    ]))
    story.append(rec1_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Recommendation 2
    story.append(Paragraph("<b>2. Expand W2_North Warehouse Capacity by 500 Units</b>", header_style))
    rec2_data = [
        ['Investment', 'Expected ROI', 'Payback', 'Risk'],
        ['$125K (infrastructure)', '$180K/year (growth capacity)', '8.3 months', 'Medium']
    ]
    rec2_table = Table(rec2_data, colWidths=[2.5*inch, 2.2*inch, 1.5*inch, 1*inch])
    rec2_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
    ]))
    story.append(rec2_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Recommendation 3
    story.append(Paragraph("<b>3. Integrate Weather Data into Forecasting Model</b>", header_style))
    rec3_data = [
        ['Investment', 'Expected ROI', 'Payback', 'Risk'],
        ['$35K (API + development)', '$95K/year (accuracy gains)', '4.4 months', 'Low']
    ]
    rec3_table = Table(rec3_data, colWidths=[2.5*inch, 2.2*inch, 1.5*inch, 1*inch])
    rec3_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
    ]))
    story.append(rec3_table)
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>TOTAL PROJECTED ANNUAL VALUE: $1.14M</b>", highlight_style))
    story.append(PageBreak())
    
    # ========== SLIDE 9: Q&A / CFO Question ==========
    story.append(Paragraph("Anticipated Questions", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph('<b>CFO Question: "Why do we need so much safety stock? That ties up working capital."</b>', header_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Response:</b>", body_style))
    response_text = """
    Great question. The safety stock increase of 355 units represents a $261K increase in holding costs annually. 
    However, our simulation data shows this investment prevents an estimated $1.125M in stockout costs - 
    that's a <b>4.3:1 return ratio</b>.
    """
    story.append(Paragraph(response_text, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>The math breaks down as follows:</b>", body_style))
    cfo_bullets = [
        "<bullet>&bull;</bullet> <b>Without safety stock:</b> 38 stockout days/year = $1.425M lost (expediting + lost sales)",
        "<bullet>&bull;</bullet> <b>With optimized safety stock:</b> 8 stockout days/year = $300K lost",
        "<bullet>&bull;</bullet> <b>Additional holding cost:</b> $261K/year",
        "<bullet>&bull;</bullet> <b>Net benefit:</b> $1.125M - $261K = <b>$864K annual savings</b>"
    ]
    for bullet in cfo_bullets:
        story.append(Paragraph(bullet, bullet_style))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("""
    Additionally, our 95% service level protects customer relationships. Each stockout event risks 
    losing a customer permanently - the lifetime value impact isn't captured in these numbers but 
    represents significant additional downside protection.
    """, body_style))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Working capital impact is offset by 3.6-month payback period.</b>", highlight_style))
    
    # Build the PDF
    doc.build(story)
    print("Slide deck PDF created: Week8_Quarterly_Ops_Review.pdf")

if __name__ == "__main__":
    create_slide_deck()
