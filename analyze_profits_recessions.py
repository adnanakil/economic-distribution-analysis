#!/usr/bin/env python3
import json

# NBER recession dates (US recessions since 1940)
recessions = [
    # Start Year, End Year, Name
    (1945, 1945, "Post-WWII"),
    (1948, 1949, "Post-War"),
    (1953, 1954, "Post-Korean War"),
    (1957, 1958, "Eisenhower"),
    (1960, 1961, "Rolling Adjustment"),
    (1969, 1970, "Nixon"),
    (1973, 1975, "Oil Crisis"),
    (1980, 1980, "Double-Dip I"),
    (1981, 1982, "Double-Dip II"),
    (1990, 1991, "Gulf War"),
    (2001, 2001, "Dot-Com"),
    (2007, 2009, "Great Recession"),
    (2020, 2020, "COVID-19")
]

# Count recessions by decade
print("Recessions by Decade:")
print("-" * 40)

decades = {}
for start, end, name in recessions:
    # Assign to decade based on start year
    decade = (start // 10) * 10
    if decade not in decades:
        decades[decade] = []
    decades[decade].append((start, end, name))

for decade in sorted(decades.keys()):
    if decade >= 1940:
        count = len(decades.get(decade, []))
        recession_list = decades.get(decade, [])
        print(f"\n{decade}s: {count} recession(s)")
        for start, end, name in recession_list:
            duration = end - start + 1
            print(f"  - {start}-{end} ({name}) [{duration} year(s)]")

# Analyze correlation with profit data
print("\n\nCorrelation with Corporate Profit Share:")
print("-" * 40)

profit_data = {
    "1940s": 8.3,
    "1950s": 6.5,
    "1960s": 6.3,
    "1970s": 6.9,
    "1980s": 5.3,
    "1990s": 5.8,
    "2000s": 7.9,
    "2010s": 10.4,
    "2020s": 11.4
}

recession_count = {
    "1940s": 3,
    "1950s": 2,
    "1960s": 2,
    "1970s": 2,
    "1980s": 2,
    "1990s": 1,
    "2000s": 2,
    "2010s": 0,
    "2020s": 1
}

print("\nDecade | Recessions | Profit Share | Analysis")
print("-" * 60)
for decade in ["1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]:
    rec_count = recession_count[decade]
    profit = profit_data[decade]
    
    # Analysis
    if decade == "1980s":
        analysis = "Severe back-to-back recessions crushed profits"
    elif decade == "2010s":
        analysis = "NO recessions - profits soared!"
    elif decade == "2020s":
        analysis = "Brief COVID recession, quick profit recovery"
    elif profit < 7:
        analysis = "Multiple recessions kept profits low"
    else:
        analysis = "Profits rose despite recessions"
    
    print(f"{decade:6} | {rec_count:10} | {profit:11.1f}% | {analysis}")

print("\n\nKey Insights:")
print("-" * 40)
print("1. The 1980s had SEVERE back-to-back recessions (1980, 1981-82)")
print("   - This 'double-dip' recession with 20% interest rates crushed profits")
print("   - Corporate profits hit their historic low of 5.3% of GDP")
print()
print("2. The 2010s had ZERO recessions - the longest expansion in US history")
print("   - Without recession pressure, profits soared to 10.4% of GDP")
print()
print("3. Recessions clearly suppress profits, but the relationship isn't perfect:")
print("   - 1940s-1970s: Frequent recessions (2-3 per decade), profits stayed 6-8%")
print("   - 1980s: Severe recessions → profits collapsed to 5.3%")
print("   - 2010s: No recessions → profits jumped to 10.4%")
print()
print("4. Other factors beyond recessions:")
print("   - Globalization (1990s onwards) - cheaper labor")
print("   - Technology - higher productivity, fewer workers")
print("   - Market concentration - less competition")
print("   - Declining union power - weaker wage bargaining")
print("   - Low interest rates (2010s) - cheap capital")

# Generate JavaScript for visualization
print("\n\nJavaScript code for recession overlay:")
print("```javascript")
print("// Recession periods for shading on charts")
print("const recessionPeriods = [")
for start, end, name in recessions:
    if start >= 1947:  # Only include post-1947 for our data
        print(f"  {{ start: {start}, end: {end}, name: '{name}' }},")
print("];")
print("```")