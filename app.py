import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Punjab School Census Dashboard", layout="wide")
st.title("Punjab Annual School Census — Infrastructure Dashboard")

conn = sqlite3.connect("punjab_schools.db")

# ---------------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------------
st.sidebar.header("Filters")

districts = pd.read_sql_query(
    "SELECT DISTINCT district FROM schools ORDER BY district", conn
)['district'].tolist()

selected_district = st.sidebar.selectbox("Select District", ["All"] + districts)

if selected_district != "All":
    schools_in_district = pd.read_sql_query(
        f"SELECT DISTINCT school_name FROM schools WHERE district = ? ORDER BY school_name",
        conn, params=(selected_district,)
    )['school_name'].dropna().tolist()
    selected_school = st.sidebar.selectbox("Select School", ["All"] + schools_in_district)
else:
    selected_school = "All"
    st.sidebar.selectbox("Select School", ["Select a district first"], disabled=True)

# ---------------------------------------------------------------
# STATE 1: SPECIFIC SCHOOL SELECTED -> DETAIL CARD
# ---------------------------------------------------------------
if selected_school != "All":
    school_df = pd.read_sql_query(
        "SELECT * FROM schools WHERE district = ? AND school_name = ?",
        conn, params=(selected_district, selected_school)
    )
    st.subheader(f"School Details: {selected_school}")

    if len(school_df) == 0:
        st.warning("No data found for this school.")
    else:
        row = school_df.iloc[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Enrollment", int(row['enrollment']) if pd.notna(row['enrollment']) else "N/A")
        col2.metric("Teachers", int(row['Teachers']) if pd.notna(row['Teachers']) else "N/A")
        col3.metric("Electricity", row['electricity'] if pd.notna(row['electricity']) else "N/A")

        col4, col5, col6 = st.columns(3)
        col4.metric("Drinking Water", row['drink_water'] if pd.notna(row['drink_water']) else "N/A")
        col5.metric("Boundary Wall", row['boundary_wall'] if pd.notna(row['boundary_wall']) else "N/A")
        col6.metric("Toilets", row['toilets'] if pd.notna(row['toilets']) else "N/A")

        st.markdown("---")
        st.dataframe(school_df)

# ---------------------------------------------------------------
# STATE 2: DISTRICT SELECTED, NO SPECIFIC SCHOOL -> PER-SCHOOL BREAKDOWN
# ---------------------------------------------------------------
elif selected_district != "All":
    st.subheader(f"All Schools in {selected_district}")

    q_schools = """
    SELECT school_name, enrollment, Teachers, electricity, drink_water, boundary_wall, toilets
    FROM schools
    WHERE district = ?
    ORDER BY enrollment DESC
    """
    df_schools = pd.read_sql_query(q_schools, conn, params=(selected_district,))

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Schools", len(df_schools))
    col2.metric("Total Enrollment", int(df_schools['enrollment'].sum(skipna=True)))
    col3.metric("Total Teachers", int(df_schools['Teachers'].sum(skipna=True)))

    fig_enroll = px.bar(
        df_schools.head(30), x="school_name", y="enrollment",
        title=f"Top 30 Schools by Enrollment in {selected_district}"
    )
    fig_enroll.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_enroll, use_container_width=True)

    st.dataframe(df_schools)

# ---------------------------------------------------------------
# STATE 3: NO FILTERS -> ALL-DISTRICT COMPARISON DASHBOARD
# ---------------------------------------------------------------
else:
    # Query 1: Electricity / water access by district
    q1 = """
    SELECT district,
           COUNT(*) AS total_schools,
           ROUND(100.0*SUM(CASE WHEN electricity='No' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_no_electricity,
           ROUND(100.0*SUM(CASE WHEN drink_water='No' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_no_water
    FROM schools
    GROUP BY district
    ORDER BY pct_no_electricity DESC
    """
    df1 = pd.read_sql_query(q1, conn)

    st.subheader("Electricity & Water Access by District")
    fig1 = px.bar(df1.head(15), x="district", y="pct_no_electricity",
                  title="% of Schools Without Electricity (Top 15 Worst Districts)")
    st.plotly_chart(fig1, use_container_width=True)
    st.dataframe(df1)

    st.markdown("---")

    # Query 2: Boundary wall / toilets by school gender
    q2 = """
    SELECT school_gender,
           COUNT(*) AS total_schools,
           ROUND(100.0*SUM(CASE WHEN boundary_wall='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_boundary_wall,
           ROUND(AVG(total_toilets),1) AS avg_toilets
    FROM schools
    GROUP BY school_gender
    """
    df2 = pd.read_sql_query(q2, conn)

    st.subheader("Infrastructure: Boys vs Girls Schools")
    col1, col2 = st.columns(2)
    with col1:
        fig2a = px.bar(df2, x="school_gender", y="pct_boundary_wall",
                        title="% of Schools with Boundary Wall")
        st.plotly_chart(fig2a, use_container_width=True)
    with col2:
        fig2b = px.bar(df2, x="school_gender", y="avg_toilets",
                        title="Average Toilets per School")
        st.plotly_chart(fig2b, use_container_width=True)
    st.dataframe(df2)

    st.markdown("---")

    # Query 3: Infrastructure by school type
    q3 = """
    SELECT school_type_grouped,
           COUNT(*) AS total_schools,
           ROUND(AVG(total_computers),1) AS avg_computers,
           ROUND(AVG(total_books),1) AS avg_books,
           ROUND(100.0*SUM(CASE WHEN science_lab='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_science_lab
    FROM schools
    GROUP BY school_type_grouped
    ORDER BY avg_computers DESC
    """
    df3 = pd.read_sql_query(q3, conn)

    st.subheader("Resources by School Type")
    fig3 = px.bar(df3, x="school_type_grouped", y="avg_computers",
                  title="Average Computers per School, by School Type")
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(df3)

    st.markdown("---")

    # Query 4: Student-teacher ratio by district
    q4 = """
    SELECT district,
           SUM(enrollment) AS total_enrollment,
           SUM(Teachers) AS total_teachers,
           ROUND(SUM(enrollment)*1.0/NULLIF(SUM(Teachers),0),1) AS student_teacher_ratio
    FROM schools
    GROUP BY district
    ORDER BY student_teacher_ratio DESC
    """
    df4 = pd.read_sql_query(q4, conn)

    st.subheader("Student-Teacher Ratio by District (Overcrowding)")
    fig4 = px.bar(df4.head(15), x="district", y="student_teacher_ratio",
                  title="Most Overcrowded Districts (Top 15)")
    st.plotly_chart(fig4, use_container_width=True)
    st.dataframe(df4)

    st.markdown("---")

    # Query 5: Enrollment ranking by district
    q5 = """
    SELECT district, SUM(enrollment) AS total_enrollment,
           RANK() OVER (ORDER BY SUM(enrollment) DESC) AS rnk
    FROM schools
    GROUP BY district
    ORDER BY rnk
    """
    df5 = pd.read_sql_query(q5, conn)

    st.subheader("Districts Ranked by Total Enrollment")
    fig5 = px.bar(df5.head(15), x="district", y="total_enrollment",
                  title="Top 15 Districts by Total Enrollment")
    st.plotly_chart(fig5, use_container_width=True)
    st.dataframe(df5)

conn.close()