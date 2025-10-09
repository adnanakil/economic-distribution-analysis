import requests
import pandas as pd

# Try the FRED series that showed up in web search
base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"

indicators = {
    'MEDSQUFEEUS': 'Median Home Size in Square Feet (Existing Homes)',
    'COMPSFLAM1FQ': 'Median Square Feet - New Construction Completions'
}

print("Fetching housing size data from FRED...\n")

data_frames = {}

for code, name in indicators.items():
    try:
        url = f"{base_url}?id={code}"
        df = pd.read_csv(url)
        df.columns = ['date', code]
        df['date'] = pd.to_datetime(df['date'])
        data_frames[code] = df
        print(f"✓ {name} ({code})")
        print(f"  Range: {df['date'].min().date()} to {df['date'].max().date()}")
        print(f"  First value: {df[code].iloc[0]}")
        print(f"  Latest value: {df[code].iloc[-1]}")
        print()
    except Exception as e:
        print(f"✗ Failed to fetch {name} ({code}): {e}\n")

# Based on web research, use known data points
print("\n=== HOUSING SIZE ADJUSTMENT ANALYSIS ===")
print("\nFrom Census Bureau data (web research):")
print("  1980: ~1,595 sq ft (median new home)")
print("  2024: ~2,146 sq ft (median new home)")
print("  Size increase: +35%\n")

# Now recalculate affordability with size adjustment
# From our previous data:
print("Price-to-Income Ratio Analysis:")
print("  Raw ratio 2024: 5.10x")
print("  Historical avg: 2.94x")
print("  Raw increase: 73%\n")

print("If we adjust for 35% larger homes:")
size_adjustment = 1.35
adjusted_current_ratio = 5.10 / size_adjustment
adjusted_increase = ((adjusted_current_ratio / 2.94) - 1) * 100

print(f"  Size-adjusted ratio 2024: {adjusted_current_ratio:.2f}x")
print(f"  Size-adjusted increase: {adjusted_increase:.1f}%\n")

print("Conclusion:")
print(f"  Even after adjusting for 35% larger homes,")
print(f"  housing is still {adjusted_increase:.1f}% less affordable than historical average.\n")

# Healthcare quality adjustment discussion
print("\n=== HEALTHCARE QUALITY ADJUSTMENT ===")
print("\nHealthcare CPI does NOT adjust for quality improvements:")
print("  - Medical care CPI up 4,323% since 1947")
print("  - But 1947 couldn't treat: many cancers, heart disease, diabetes as well")
print("  - Modern treatments: MRI, CT scans, advanced surgeries, biologics, etc.\n")

print("The 'hedonic quality adjustment' debate:")
print("  1. You're paying more but getting better outcomes")
print("  2. BUT: you have no choice - you can't buy '1980 healthcare' at 1980 prices")
print("  3. AND: Many cost increases are administrative, not quality-driven\n")

print("Key insight:")
print("  Even if healthcare is 'better', the affordability crisis is real")
print("  because people can't opt-out of modern healthcare prices.\n")

# Education quality adjustment
print("\n=== EDUCATION QUALITY ADJUSTMENT ===")
print("\nEducation CPI does NOT adjust for quality:")
print("  - Some argue education is better (more resources, technology)")
print("  - Others argue education quality has declined or stagnated")
print("  - Labor market returns to college degree have INCREASED")
print("    (suggesting either quality up OR credentialism up)\n")

print("Evidence on education quality is mixed:")
print("  + More student services, facilities, technology")
print("  - Grade inflation, administrative bloat")
print("  - Questionable if students learn more\n")

# Summary
print("\n=== SUMMARY: QUALITY-ADJUSTED AFFORDABILITY ===")
print("\n1. HOUSING:")
print("   Raw: 73% less affordable")
print("   Quality-adjusted (35% bigger): Still ~28% less affordable")
print("   Verdict: CRISIS REMAINS REAL\n")

print("2. HEALTHCARE:")
print("   Raw: 70% more expensive than wages")
print("   Quality: Better outcomes, but NO CHOICE to opt-out")
print("   Verdict: AFFORDABILITY CRISIS, even if value is better\n")

print("3. EDUCATION:")
print("   Raw: 40% more burdensome than 1993")
print("   Quality: Unclear if education quality improved")
print("   Verdict: LIKELY REAL CRISIS\n")

print("OVERALL CONCLUSION:")
print("  Quality adjustments reduce the magnitude but do NOT eliminate")
print("  the affordability crisis. Americans still face dramatically higher")
print("  barriers to housing, healthcare, and education than previous generations,")
print("  even accounting for quality/size improvements.")
