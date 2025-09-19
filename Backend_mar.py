import psycopg2
import streamlit as st
import pandas as pd

# Database connection details
DB_NAME = "marketing_db"
DB_USER = "postgres"
DB_PASSWORD = "Shania2012*"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        st.error(f"Database connection failed: {e}")
        return None

# --- CRUD Operations for Campaigns ---

def create_campaign(name, budget, start_date, end_date, description):
    """CREATE: Adds a new campaign to the database."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO campaigns (name, budget, start_date, end_date, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, budget, start_date, end_date, description))
        conn.commit()
        conn.close()

def read_campaigns():
    """READ: Retrieves all campaigns from the database."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM campaigns ORDER BY start_date DESC")
            columns = [desc[0] for desc in cur.description]
            campaigns = cur.fetchall()
            conn.close()
            return pd.DataFrame(campaigns, columns=columns)
    return pd.DataFrame()

def update_campaign(campaign_id, name, budget, start_date, end_date, description):
    """UPDATE: Modifies an existing campaign."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE campaigns
                SET name = %s, budget = %s, start_date = %s, end_date = %s, description = %s
                WHERE campaign_id = %s
            """, (name, budget, start_date, end_date, description, campaign_id))
        conn.commit()
        conn.close()

def delete_campaign(campaign_id):
    """DELETE: Removes a campaign and its associated metrics and channels."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM campaigns WHERE campaign_id = %s", (campaign_id,))
        conn.commit()
        conn.close()

# --- CRUD Operations for Customers ---

def create_customer(name, email, demographics):
    """CREATE: Adds a new customer to the database."""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO customers (name, email, demographics)
                    VALUES (%s, %s, %s)
                """, (name, email, demographics))
            conn.commit()
        except psycopg2.IntegrityError as e:
            st.error(f"Error: A customer with this email already exists.")
            conn.rollback()
        finally:
            conn.close()

def read_customers():
    """READ: Retrieves all customers from the database."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM customers ORDER BY name")
            columns = [desc[0] for desc in cur.description]
            customers = cur.fetchall()
            conn.close()
            return pd.DataFrame(customers, columns=columns)
    return pd.DataFrame()

def update_customer(customer_id, name, email, demographics):
    """UPDATE: Modifies an existing customer."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE customers
                SET name = %s, email = %s, demographics = %s
                WHERE customer_id = %s
            """, (name, email, demographics, customer_id))
        conn.commit()
        conn.close()

def delete_customer(customer_id):
    """DELETE: Removes a customer."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
        conn.commit()
        conn.close()

# --- CRUD Operations for Segments ---

def create_segment(name, criteria):
    """CREATE: Adds a new segment."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO segments (name, criteria)
                VALUES (%s, %s)
            """, (name, criteria))
        conn.commit()
        conn.close()

def read_segments():
    """READ: Retrieves all segments."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM segments")
            columns = [desc[0] for desc in cur.description]
            segments = cur.fetchall()
            conn.close()
            return pd.DataFrame(segments, columns=columns)
    return pd.DataFrame()

def update_segment(segment_id, name, criteria):
    """UPDATE: Modifies an existing segment."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE segments
                SET name = %s, criteria = %s
                WHERE segment_id = %s
            """, (name, criteria, segment_id))
        conn.commit()
        conn.close()

def delete_segment(segment_id):
    """DELETE: Removes a segment."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM segments WHERE segment_id = %s", (segment_id,))
        conn.commit()
        conn.close()

# --- Business Insights ---

def get_business_insights():
    """Provides business insights using aggregate functions."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            # Total Campaigns
            cur.execute("SELECT COUNT(*) FROM campaigns")
            total_campaigns = cur.fetchone()[0]

            # Total Budget
            cur.execute("SELECT SUM(budget) FROM campaigns")
            total_budget = cur.fetchone()[0]

            # Average Budget
            cur.execute("SELECT AVG(budget) FROM campaigns")
            avg_budget = cur.fetchone()[0]

            # Max Budget
            cur.execute("SELECT MAX(budget) FROM campaigns")
            max_budget = cur.fetchone()[0]

            # Min Budget
            cur.execute("SELECT MIN(budget) FROM campaigns")
            min_budget = cur.fetchone()[0]

            # Total Emails Sent
            cur.execute("SELECT SUM(emails_sent) FROM campaign_metrics")
            total_emails_sent = cur.fetchone()[0]

            # Average Click-Through Rate (CTR) - a calculated metric
            cur.execute("SELECT SUM(clicks)::float / SUM(emails_opened) FROM campaign_metrics WHERE emails_opened > 0")
            avg_ctr = cur.fetchone()[0]

            conn.close()

            return {
                "Total Campaigns": total_campaigns,
                "Total Budget": total_budget,
                "Average Budget": f"{avg_budget:.2f}" if avg_budget else 0,
                "Max Budget": max_budget,
                "Min Budget": min_budget,
                "Total Emails Sent": total_emails_sent,
                "Average CTR": f"{avg_ctr:.2%}" if avg_ctr else "N/A"
            }
    return {}