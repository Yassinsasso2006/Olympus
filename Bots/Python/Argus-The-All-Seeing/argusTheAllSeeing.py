import psycopg2
import time
import os
from dotenv import load_dotenv

load_dotenv()

def argus_watch():
    # Connect to the same DB as Node.js
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    
    print("👁️ Argus is analyzing the currents of the Lounge...")
    
    while True:
        # Example: Find the most active user who isn't flagged yet
        cur.execute("""
            SELECT "discordID", "numOfMessagesSent" 
            FROM argus.watchlist 
            WHERE "numOfMessagesSent" > 500
            ORDER BY "numOfMessagesSent" DESC LIMIT 5
        """)
        
        results = cur.fetchall()
        for row in results:
            print(f"Argus Insight: User {row[0]} has high activity ({row[1]} messages).")
            
        # Sleep for 10 minutes so we don't spam the DB
        time.sleep(600) 

if __name__ == "__main__":
    argus_watch()