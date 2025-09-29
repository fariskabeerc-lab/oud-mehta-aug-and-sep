# --- Function to Plot Top N Horizontal Bar ---
def plot_top(df, metric, title, color, n=50):   # default = 50
    top = df.sort_values(metric, ascending=False).head(n)
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
        height=1200,  # taller for 50 bars
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=10, t=40, b=10),
        coloraxis_showscale=False
    )
    return fig, top


# --- Tab 1: Sales ---
with tab1:
    fig_sales, top_sales = plot_top(item_summary, "Total Sales", "Top 50 Items by Sales", "Blues", n=50)
    st.plotly_chart(fig_sales, use_container_width=True)
    st.markdown("#### 🔎 Insights")
    st.write(f"- 🏆 **{top_sales.iloc[0]['Items']}** is the highest with **{top_sales.iloc[0]['Total Sales']:,.0f}** sales.")
    st.write(f"- Top 5 items contribute **{top_sales['Total Sales'].head(5).sum()/total_sales:.1%}** of overall sales.")
    st.markdown("#### 📄 Dataset (Top 100)")
    st.dataframe(
        item_summary.sort_values("Total Sales", ascending=False).head(100)[
            ["Item Code", "Items", "Qty Sold", "Total Sales", "Total Profit", "GP%"]
        ]
    )

# --- Tab 2: Profit ---
with tab2:
    fig_profit, top_profit = plot_top(item_summary, "Total Profit", "Top 50 Items by Profit", "Greens", n=50)
    st.plotly_chart(fig_profit, use_container_width=True)
    st.markdown("#### 🔎 Insights")
    st.write(f"- 💹 **{top_profit.iloc[0]['Items']}** generated the most profit (**{top_profit.iloc[0]['Total Profit']:,.0f}**).")
    st.write(f"- Top 5 items account for **{top_profit['Total Profit'].head(5).sum()/total_profit:.1%}** of total profit.")
    st.markdown("#### 📄 Dataset (Top 100)")
    st.dataframe(
        item_summary.sort_values("Total Profit", ascending=False).head(100)[
            ["Item Code", "Items", "Qty Sold", "Total Sales", "Total Profit", "GP%"]
        ]
    )

# --- Tab 3: Quantity ---
with tab3:
    fig_qty, top_qty = plot_top(item_summary, "Qty Sold", "Top 50 Items by Quantity Sold", "Oranges", n=50)
    st.plotly_chart(fig_qty, use_container_width=True)
    st.markdown("#### 🔎 Insights")
    st.write(f"- 📦 **{top_qty.iloc[0]['Items']}** is the most sold item (**{top_qty.iloc[0]['Qty Sold']:,.0f} units**).")
    st.write(f"- Top 5 items represent **{top_qty['Qty Sold'].head(5).sum()/total_qty:.1%}** of total quantity sold.")
    st.markdown("#### 📄 Dataset (Top 100)")
    st.dataframe(
        item_summary.sort_values("Qty Sold", ascending=False).head(100)[
            ["Item Code", "Items", "Qty Sold", "Total Sales", "Total Profit", "GP%"]
        ]
    )

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
            problem_items.head(50),
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
            height=1200,
            yaxis=dict(autorange="reversed"),
            margin=dict(l=10, r=10, t=40, b=10),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_problem, use_container_width=True)

        st.markdown("#### 📄 Dataset (Top 100)")
        st.dataframe(problem_items.head(100)[["Item Code", "Items", "Qty Sold", "Total Sales", "Total Profit", "GP%"]])
