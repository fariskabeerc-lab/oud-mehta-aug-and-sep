import streamlit as st
import pandas as pd
import plotly.express as px

# --- Authentication Setup ---
def login():
    st.title("🔐 Login to Sales Insights Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "almadina" and password == "12345":
            st.session_state["authenticated"] = True
            st.success("✅ Login successful! Access granted.")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# --- Run Login Check ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()

# ===========================================================
# --- Dashboard Code (only runs after login) ---
# ===========================================================

# --- Page Setup ---
st.set_page_config(page_title="Sales Insights Dashboard", layout="wide")
st.title("📊SAFA oud mehta AUG&SEP Sales Insights")

# --- Load Data ---
df = pd.read_excel("sales of oud mehta aug and sep.Xlsx")   # change filename if needed

# --- Ensure numeric columns ---
numeric_cols = ["Qty Sold", "Total Sales", "Total Profit"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Add GP% ---
df["GP%"] = (df["Total Profit"] / df["Total Sales"]) * 100

# --- Aggregate per Item including GP% ---
item_summary = (
    df.groupby(["Item Code", "Items"])
    .agg({
        "Qty Sold": "sum",
        "Total Sales": "sum",
        "Total Profit": "sum"
    })
    .reset_index()
)

# --- Calculate GP% at item level ---
item_summary["GP%"] = (item_summary["Total Profit"] / item_summary["Total Sales"]) * 100

# --- Overall KPIs ---
total_sales = item_summary["Total Sales"].sum()
total_profit = item_summary["Total Profit"].sum()
total_qty = item_summary["Qty Sold"].sum()

st.markdown("### 📌 Key Highlights")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"{total_sales:,.0f}")
col2.metric("📈 Total Profit", f"{total_profit:,.0f}")
col3.metric("📦 Total Quantity Sold", f"{total_qty:,.0f}")

st.markdown("---")

# --- Function to Plot Top 30 Horizontal Bar ---
def plot_top(df, metric, title, color):
    top = df.sort_values(metric, ascending=False).head(30)
    fig = px.bar(
        top,
        x=metric,
        y="Items",
        orientation="h",
        text=metric,
        color=metric,
        color_continuous_scale=color,
        title=title,
        hover_data={
            "Item Code": True,
            "Qty Sold": ":,.0f",
            "Total Sales": ":,.0f",
            "Total Profit": ":,.0f",
            "GP%": ":.2f",
            metric: False
        }
    )
    fig.update_traces(texttemplate='%{text:,.0f}', textposition="outside")
    fig.update_layout(
        height=900,
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=10, t=40, b=10),
        coloraxis_showscale=False
    )
    return fig, top

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["💰 Sales", "📈 Profit", "📦 Quantity", "⚠️ High Sales, Low Profit"])

# --- Tab 1: Sales ---
with tab1:
    fig_sales, top_sales = plot_top(item_summary, "Total Sales", "Top 30 Items by Sales", "Blues")
    st.plotly_chart(fig_sales, use_container_width=True)
    st.markdown("#### 🔎 Insights")
    st.write(f"- 🏆 **{top_sales.iloc[0]['Items']}** is the highest with **{top_sales.iloc[0]['Total Sales']:,.0f}** sales.")
    st.write(f"- Top 5 items contribute **{top_sales['Total Sales'].head(5).sum()/total_sales:.1%}** of overall sales.")
    st.markdown("#### 📄 Dataset")
    st.dataframe(top_sales[["Item Code", "Items", "Qty Sold", "Total Sales", "Total Profit", "GP%"]])

# --- Tab 2: Profit ---
with tab2:
    fig_profit, top_profit = plot_top(item_summary, "Total Profit", "Top 30 Items by Profit", "Greens")
    st.plotly_chart(fig_profit, use_container_width=True)
    st.markdown("#### 🔎 Insights")
    st.write(f"- 💹 **{top_profit.iloc[0]['Items']}** generated the most profit (**{top_profit.iloc[0]['Total Profit']:,.0f}**).")
    st.write(f"- Top 5 items account for **{top_profit['Total Profit'].head(5).sum()/total_profit:.1%}** of total profit.")
    st.markdown("#### 📄 Dataset")
    st.dataframe(top_profit[["Item Code", "Items", "Qty Sold", "Total Sales", "Total Profit", "GP%"]])

# --- Tab 3: Quantity ---
with tab3:
    fig_qty, top_qty = plot_top(item_summary, "Qty Sold", "Top 30 Items by Quantity Sold", "Oranges")
    st.plotly_chart(fig_qty, use_container_width=True)
    st.markdown("#### 🔎 Insights")
    st.write(f"- 📦 **{top_qty.iloc[0]['Items']}** is the most sold item (**{top_qty.iloc[0]['Qty Sold']:,.0f} units**).")
    st.write(f"- Top 5 items represent **{top_qty['Qty Sold'].head(5).sum()/total_qty:.1%}** of total quantity sold.")
    st.markdown("#### 📄 Dataset")
    st.dataframe(top_qty[["Item Code", "Items", "Qty Sold", "Total Sales", "Total Profit", "GP%"]])

# --- Tab 4: High Sales, Low Profit ---
with tab4:
    qty_threshold = item_summary["Qty Sold"].quantile(0.75)
    profit_threshold = item_summary["Total Profit"].quantile(0.25)

    problem_items = item_summary[
        (item_summary["Qty Sold"] >= qty_threshold) & 
        (item_summary["Total Profit"] <= profit_threshold)
    ].sort_values("Qty Sold", ascending=False)

    st.subheader("⚠️ Items with High Quantity Sold but Low Profit")
    if not problem_items.empty:
        fig_problem = px.bar(
            problem_items.head(30),
            x="Qty Sold",
            y="Items",
            orientation="h",
            text="Qty Sold",
            color="Total Profit",
            color_continuous_scale="Reds",
            title="High Sales, Low Profit Items",
            hover_data={
                "Item Code": True,
                "Qty Sold": ":,.0f",
                "Total Sales": ":,.0f",
                "Total Profit": ":,.0f",
                "GP%": ":.2f"
            }
        )
        fig_problem.update_traces(texttemplate='%{text:,.0f}', textposition="outside")
        fig_problem.update_layout(
            height=900,
            yaxis=dict(autorange="reversed"),
            margin=dict(l=10, r=10, t=40, b=10),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_problem, use_container_width=True)

        st.markdown("#### 📄 Dataset")
        st.dataframe(problem_items[["Item Code", "Items", "Qty Sold", "Total Sales", "Total Profit", "GP%"]])

        st.markdown("#### 🔎 Insights")
        st.write(f"- Found **{len(problem_items)} items** with high sales but weak profit.")
        st.write(f"- Example: **{problem_items.iloc[0]['Items']}** sold **{problem_items.iloc[0]['Qty Sold']:,.0f} units** but only made profit of **{problem_items.iloc[0]['Total Profit']:,.0f}** (GP: {problem_items.iloc[0]['GP%']:.2f}%).")
    else:
        st.info("✅ No items found where sales are high but profit is low based on thresholds.")

st.markdown("---")

# --- Download Option ---
st.subheader("📥 Download Detailed Report")
with pd.ExcelWriter("Top_Items_Report.xlsx") as writer:
    top_qty.to_excel(writer, sheet_name="Top Qty Sold", index=False)
    top_sales.to_excel(writer, sheet_name="Top Sales", index=False)
    top_profit.to_excel(writer, sheet_name="Top Profit", index=False)
    problem_items.to_excel(writer, sheet_name="High Sales Low Profit", index=False)

with open("Top_Items_Report.xlsx", "rb") as f:
    st.download_button("⬇️ Download Excel Report", f, file_name="Top_Items_Report.xlsx")
