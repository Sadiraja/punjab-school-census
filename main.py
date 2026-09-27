import pandas as pd
import sqlite3

df = pd.read_excel("public-census_oct_2018.xlsx")

# 1. Binary/coded columns -> readable labels
map_binary = {1: 'Yes', 0: 'No', 2: 'Partial'}
for col in ['electricity', 'drink_water', 'toilets']:
    df[col] = df[col].map(map_binary)

df['boundary_wall'] = df['boundary_wall'].map({1: 'Yes', 0: 'No'})
df['internet'] = df['internet'].map({1: 'Yes', 0: 'No'})
df['science_lab'] = df['science_lab'].map({1: 'Yes', 0: 'No'})

# 2. Security - keep only clean text labels, legacy numeric codes -> NaN
security_map = {
    'Satisfying': 'Satisfying', 'Not Available': 'Not Available',
    'Not Satisfying': 'Not Satisfying', 'Available': 'Available'
}
df['security_clean'] = df['security'].map(security_map)

# 3. District - already clean, just standardize case for readability
df['district'] = df['district'].str.strip()

# 4. Numeric columns - force proper numeric type
num_cols = ['enrollment', 'Teachers', 'NonTeachers', 'total_computers',
            'total_books', 'total_toilets', 'usable_toilets']
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 5. school_type - group rare categories into "Other" for cleaner comparisons
main_types = ['Govt. School', 'Model School', 'PSSP School', 'Community School']
df['school_type_grouped'] = df['school_type'].apply(
    lambda x: x if x in main_types else ('Unknown' if pd.isna(x) else 'Other')
)

# 6. Drop rows with no district or no enrollment - can't analyze these
df_clean = df.dropna(subset=['district', 'enrollment'])
print(f"Kept {len(df_clean)} of {len(df)} rows")

# 7. Load into SQLite
conn = sqlite3.connect("punjab_schools.db")
df_clean.to_sql("schools", conn, if_exists="replace", index=False)
conn.close()
print("Loaded into punjab_schools.db")