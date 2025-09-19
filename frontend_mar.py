import streamlit as st
import pandas as pd
import json
from datetime import date

# Import the backend functions
from Backend_mar import (
    create_campaign, read_campaigns, update_campaign, delete_campaign,
    create_customer, read_customers, update_customer, delete_customer,
    create_segment, read_segments, update_segment, delete_segment,
    get_business_insights
)

# Set page configuration
st.set_page_config(layout="wide")

# Title and header
st.title("DBDWBI Programming Assistant - Marketing Campaign Manager")
st.subheader("DBDWBI - [Your Roll No.]") # Replace with your roll number

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Campaigns", "Customers", "Segments"])

# --- Dashboard Section (Business Insights) ---
if page == "Dashboard":
    st.header("📊 Real-time Campaign Dashboard")
    insights = get_business_insights()
    if insights:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric(label="Total Campaigns", value=insights.get("Total Campaigns", 0))
        with col2:
            st.metric(label="Total Budget", value=f"₹{insights.get('Total Budget', 0):,.2f}")
        with col3:
            st.metric(label="Avg. Campaign Budget", value=f"₹{insights.get('Average Budget', 0)}")
        with col4:
            st.metric(label="Total Emails Sent", value=f"{insights.get('Total Emails Sent', 0):,}")
        with col5:
            st.metric(label="Avg. CTR", value=insights.get('Average CTR', "N/A"))
    else:
        st.info("No data available to show insights. Please add some campaigns and metrics.")

    st.subheader("Active Campaigns Overview")
    campaigns_df = read_campaigns()
    if not campaigns_df.empty:
        st.dataframe(campaigns_df)
    else:
        st.info("No campaigns found.")

# --- Campaigns Section (CRUD) ---
elif page == "Campaigns":
    st.header("🎯 Campaign Management (CRUD)")

    # CREATE Operation
    st.subheader("Create New Campaign")
    with st.form(key='create_campaign_form'):
        name = st.text_input("Campaign Name")
        budget = st.number_input("Budget", min_value=0.0, format="%.2f")
        start_date = st.date_input("Start Date", date.today())
        end_date = st.date_input("End Date")
        description = st.text_area("Description")
        submit_button = st.form_submit_button(label='Create Campaign')
        if submit_button:
            create_campaign(name, budget, start_date, end_date, description)
            st.success(f"Campaign '{name}' created successfully!")
            st.experimental_rerun()

    # READ and UPDATE/DELETE Operations
    st.subheader("View, Update & Delete Campaigns")
    campaigns_df = read_campaigns()
    if not campaigns_df.empty:
        selected_campaign = st.selectbox("Select a Campaign to Edit/Delete", campaigns_df['name'])
        campaign_to_edit = campaigns_df[campaigns_df['name'] == selected_campaign].iloc[0]

        with st.form(key='update_campaign_form'):
            st.write(f"Editing Campaign: **{campaign_to_edit['name']}**")
            up_name = st.text_input("Name", value=campaign_to_edit['name'])
            up_budget = st.number_input("Budget", value=float(campaign_to_edit['budget']), format="%.2f")
            up_start_date = st.date_input("Start Date", value=campaign_to_edit['start_date'])
            up_end_date = st.date_input("End Date", value=campaign_to_edit['end_date'])
            up_description = st.text_area("Description", value=campaign_to_edit['description'])

            col_upd, col_del = st.columns(2)
            with col_upd:
                update_button = st.form_submit_button(label='Update Campaign')
            with col_del:
                delete_button = st.form_submit_button(label='Delete Campaign')

            if update_button:
                update_campaign(campaign_to_edit['campaign_id'], up_name, up_budget, up_start_date, up_end_date, up_description)
                st.success("Campaign updated successfully!")
                st.experimental_rerun()
            if delete_button:
                delete_campaign(campaign_to_edit['campaign_id'])
                st.warning("Campaign deleted.")
                st.experimental_rerun()
    else:
        st.info("No campaigns to display.")

# --- Customers Section (CRUD) ---
elif page == "Customers":
    st.header("👥 Customer Management (CRUD)")
    # Similar CRUD implementation as for Campaigns, but for customers.

# --- Segments Section (CRUD) ---
elif page == "Segments":
    st.header("🎯 Customer Segmentation (CRUD)")
    # Similar CRUD implementation as for Campaigns, but for segments.