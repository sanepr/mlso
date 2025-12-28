# 🗄️ MLflow PostgreSQL Database Access Guide

**Date:** December 28, 2025  
**Status:** ✅ **PostgreSQL Database Running and Accessible**

---

## 📊 Database Connection Information

### Container Details
- **Container Name:** `mlflow-postgres`
- **Image:** `postgres:15-alpine`
- **Status:** Running (healthy)
- **Port Mapping:** `5432:5432` (host:container)

### Connection Credentials
```
Host: localhost (or 127.0.0.1)
Port: 5432
Database: mlflow
Username: mlflow
Password: mlflow_password
```

### Connection String
```
postgresql://mlflow:mlflow_password@localhost:5432/mlflow
```

---

## 🔧 Access Methods

### Method 1: Using Docker Exec (Simplest) ✅

#### Interactive psql Shell
```bash
docker exec -it mlflow-postgres psql -U mlflow -d mlflow
```

**You'll get a psql prompt:**
```
mlflow=# 
```

**Common Commands:**
```sql
-- List all tables
\dt

-- Describe a table
\d experiments
\d runs
\d params
\d metrics

-- Show databases
\l

-- Show current database
\c

-- Exit
\q
```

#### Execute Single Query
```bash
# List all experiments
docker exec mlflow-postgres psql -U mlflow -d mlflow -c "SELECT * FROM experiments;"

# Count runs
docker exec mlflow-postgres psql -U mlflow -d mlflow -c "SELECT COUNT(*) FROM runs;"

# List all tables
docker exec mlflow-postgres psql -U mlflow -d mlflow -c "\dt"
```

---

### Method 2: Using psql Client (Local Installation)

If you have PostgreSQL client installed locally:

```bash
psql -h localhost -p 5432 -U mlflow -d mlflow
# Enter password when prompted: mlflow_password
```

Or with password in connection string:
```bash
PGPASSWORD=mlflow_password psql -h localhost -p 5432 -U mlflow -d mlflow
```

**Install psql (if not installed):**

**macOS:**
```bash
brew install postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql-client
```

---

### Method 3: Using Python (psycopg2)

```python
import psycopg2
from psycopg2.extras import RealDictCursor

# Connection parameters
conn_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mlflow',
    'user': 'mlflow',
    'password': 'mlflow_password'
}

# Connect to database
conn = psycopg2.connect(**conn_params)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Query experiments
cursor.execute("SELECT * FROM experiments")
experiments = cursor.fetchall()
for exp in experiments:
    print(f"Experiment: {exp['name']} (ID: {exp['experiment_id']})")

# Query runs
cursor.execute("SELECT COUNT(*) as count FROM runs")
result = cursor.fetchone()
print(f"Total runs: {result['count']}")

# Close connection
cursor.close()
conn.close()
```

**Install psycopg2:**
```bash
pip install psycopg2-binary
```

---

### Method 4: Using Python with SQLAlchemy

```python
from sqlalchemy import create_engine, text
import pandas as pd

# Create connection
engine = create_engine('postgresql://mlflow:mlflow_password@localhost:5432/mlflow')

# Query using pandas
df_experiments = pd.read_sql("SELECT * FROM experiments", engine)
print(df_experiments)

# Query with SQLAlchemy
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM runs LIMIT 5"))
    for row in result:
        print(row)
```

**Install SQLAlchemy:**
```bash
pip install sqlalchemy psycopg2-binary
```

---

### Method 5: Using GUI Tools

#### DBeaver (Free, Cross-platform)

1. **Download:** https://dbeaver.io/download/
2. **Install and open DBeaver**
3. **Create New Connection:**
   - Click "New Database Connection"
   - Select "PostgreSQL"
   - Enter connection details:
     ```
     Host: localhost
     Port: 5432
     Database: mlflow
     Username: mlflow
     Password: mlflow_password
     ```
4. **Test Connection** and click "Finish"

#### pgAdmin (Official PostgreSQL GUI)

1. **Download:** https://www.pgadmin.org/download/
2. **Install and open pgAdmin**
3. **Add Server:**
   - Right-click "Servers" → "Register" → "Server"
   - General tab: Name = "MLflow PostgreSQL"
   - Connection tab:
     ```
     Host: localhost
     Port: 5432
     Database: mlflow
     Username: mlflow
     Password: mlflow_password
     ```
4. **Save** and connect

#### TablePlus (macOS, Clean UI)

1. **Download:** https://tableplus.com/
2. **Create Connection:**
   - Click "Create a new connection"
   - Select "PostgreSQL"
   - Enter details (same as above)
3. **Connect**

---

## 📋 Database Schema

### MLflow Tables (16 tables)

```
alembic_version         - Database migration version
datasets                - Dataset information
experiment_tags         - Tags for experiments
experiments             - Experiment metadata
input_tags              - Input data tags
inputs                  - Input data metadata
latest_metrics          - Latest metric values per run
metrics                 - All metric values with history
model_version_tags      - Tags for model versions
model_versions          - Registered model versions
params                  - Run parameters
registered_model_aliases - Model aliases
registered_model_tags   - Tags for registered models
registered_models       - Registered models
runs                    - All runs data
tags                    - Run tags
```

---

## 🔍 Useful Queries

### View All Experiments
```sql
SELECT 
    experiment_id,
    name,
    lifecycle_stage,
    creation_time,
    last_update_time
FROM experiments
ORDER BY creation_time DESC;
```

### View All Runs
```sql
SELECT 
    run_uuid,
    experiment_id,
    status,
    start_time,
    end_time,
    lifecycle_stage
FROM runs
ORDER BY start_time DESC
LIMIT 10;
```

### View Parameters for a Run
```sql
SELECT 
    r.run_uuid,
    p.key,
    p.value
FROM runs r
JOIN params p ON r.run_uuid = p.run_uuid
WHERE r.run_uuid = 'YOUR_RUN_ID'
ORDER BY p.key;
```

### View Metrics for a Run
```sql
SELECT 
    r.run_uuid,
    m.key,
    m.value,
    m.timestamp,
    m.step
FROM runs r
JOIN metrics m ON r.run_uuid = m.run_uuid
WHERE r.run_uuid = 'YOUR_RUN_ID'
ORDER BY m.key, m.step;
```

### View Latest Metrics per Run
```sql
SELECT 
    r.run_uuid,
    lm.key,
    lm.value
FROM runs r
JOIN latest_metrics lm ON r.run_uuid = lm.run_uuid
ORDER BY r.start_time DESC, lm.key;
```

### View Registered Models
```sql
SELECT 
    name,
    creation_time,
    last_updated_time
FROM registered_models
ORDER BY creation_time DESC;
```

### View Model Versions
```sql
SELECT 
    rm.name as model_name,
    mv.version,
    mv.current_stage,
    mv.status,
    mv.creation_time
FROM registered_models rm
JOIN model_versions mv ON rm.name = mv.name
ORDER BY rm.name, mv.version DESC;
```

### Join Experiments and Runs
```sql
SELECT 
    e.name as experiment_name,
    COUNT(r.run_uuid) as total_runs,
    COUNT(CASE WHEN r.status = 'FINISHED' THEN 1 END) as finished_runs,
    COUNT(CASE WHEN r.status = 'FAILED' THEN 1 END) as failed_runs
FROM experiments e
LEFT JOIN runs r ON e.experiment_id = r.experiment_id
GROUP BY e.experiment_id, e.name
ORDER BY total_runs DESC;
```

---

## 🚀 Quick Start Examples

### Example 1: Explore Database Structure
```bash
# Connect to database
docker exec -it mlflow-postgres psql -U mlflow -d mlflow

# List all tables
\dt

# Describe experiments table
\d experiments

# Show sample data
SELECT * FROM experiments LIMIT 5;

# Exit
\q
```

### Example 2: Query Run Data
```bash
docker exec mlflow-postgres psql -U mlflow -d mlflow << 'EOF'
-- Get all runs with their metrics
SELECT 
    r.run_uuid,
    e.name as experiment,
    lm.key as metric_name,
    lm.value as metric_value
FROM runs r
JOIN experiments e ON r.experiment_id = e.experiment_id
JOIN latest_metrics lm ON r.run_uuid = lm.run_uuid
WHERE lm.key LIKE '%test%'
ORDER BY r.start_time DESC;
EOF
```

### Example 3: Python Database Query
```python
import psycopg2
import pandas as pd

# Connect
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='mlflow',
    user='mlflow',
    password='mlflow_password'
)

# Query with pandas
query = """
SELECT 
    e.name as experiment,
    COUNT(r.run_uuid) as total_runs
FROM experiments e
LEFT JOIN runs r ON e.experiment_id = r.experiment_id
GROUP BY e.name
"""
df = pd.read_sql(query, conn)
print(df)

conn.close()
```

---

## 🔐 Security Considerations

### For Development:
✅ Current setup is fine (exposed only to localhost)

### For Production:
⚠️ **Change the default password!**

**Update docker-compose.mlflow.yml:**
```yaml
environment:
  POSTGRES_USER: mlflow
  POSTGRES_PASSWORD: YOUR_SECURE_PASSWORD  # Change this!
  POSTGRES_DB: mlflow
```

**Then update connection strings:**
```
postgresql://mlflow:YOUR_SECURE_PASSWORD@localhost:5432/mlflow
```

**Other Security Measures:**
- Use environment variables for credentials
- Don't expose port 5432 externally in production
- Use SSL connections in production
- Implement database user roles and permissions
- Regular backups

---

## 💾 Backup and Restore

### Backup Database
```bash
# Backup entire database
docker exec mlflow-postgres pg_dump -U mlflow mlflow > mlflow_backup.sql

# Backup specific tables
docker exec mlflow-postgres pg_dump -U mlflow -t experiments -t runs mlflow > mlflow_partial_backup.sql

# Compressed backup
docker exec mlflow-postgres pg_dump -U mlflow mlflow | gzip > mlflow_backup.sql.gz
```

### Restore Database
```bash
# Restore from backup
docker exec -i mlflow-postgres psql -U mlflow -d mlflow < mlflow_backup.sql

# Restore from compressed backup
gunzip -c mlflow_backup.sql.gz | docker exec -i mlflow-postgres psql -U mlflow -d mlflow
```

---

## 📊 Database Statistics

### Check Database Size
```sql
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
WHERE datname = 'mlflow';
```

### Check Table Sizes
```sql
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Check Row Counts
```bash
docker exec mlflow-postgres psql -U mlflow -d mlflow << 'EOF'
SELECT 
    'experiments' as table_name, COUNT(*) as row_count FROM experiments
UNION ALL
SELECT 'runs', COUNT(*) FROM runs
UNION ALL
SELECT 'params', COUNT(*) FROM params
UNION ALL
SELECT 'metrics', COUNT(*) FROM metrics
UNION ALL
SELECT 'registered_models', COUNT(*) FROM registered_models
UNION ALL
SELECT 'model_versions', COUNT(*) FROM model_versions;
EOF
```

---

## 🛠️ Troubleshooting

### Issue 1: Cannot Connect

**Check if container is running:**
```bash
docker ps | grep postgres
```

**Check container logs:**
```bash
docker logs mlflow-postgres
```

**Restart container:**
```bash
docker restart mlflow-postgres
```

### Issue 2: Permission Denied

**Solution:**
Use the correct username and password:
```
Username: mlflow
Password: mlflow_password
```

### Issue 3: Port Already in Use

**Check what's using port 5432:**
```bash
lsof -i :5432
```

**Change port in docker-compose.mlflow.yml:**
```yaml
ports:
  - "5433:5432"  # Use different host port
```

Then connect to `localhost:5433`

---

## 📝 Create Analysis Script

Save this as `analyze_mlflow_db.py`:

```python
#!/usr/bin/env python3
"""
MLflow Database Analysis Script
Analyzes the MLflow PostgreSQL database and prints statistics.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

def connect_db():
    """Connect to MLflow database."""
    return psycopg2.connect(
        host='localhost',
        port=5432,
        database='mlflow',
        user='mlflow',
        password='mlflow_password'
    )

def print_statistics():
    """Print database statistics."""
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    print("=" * 80)
    print("MLFLOW DATABASE STATISTICS")
    print("=" * 80)
    
    # Experiments
    cursor.execute("SELECT COUNT(*) as count FROM experiments")
    print(f"\nExperiments: {cursor.fetchone()['count']}")
    
    # Runs
    cursor.execute("SELECT COUNT(*) as count FROM runs")
    print(f"Runs: {cursor.fetchone()['count']}")
    
    # Parameters
    cursor.execute("SELECT COUNT(*) as count FROM params")
    print(f"Parameters: {cursor.fetchone()['count']}")
    
    # Metrics
    cursor.execute("SELECT COUNT(*) as count FROM metrics")
    print(f"Metrics: {cursor.fetchone()['count']}")
    
    # Registered Models
    cursor.execute("SELECT COUNT(*) as count FROM registered_models")
    print(f"Registered Models: {cursor.fetchone()['count']}")
    
    # Model Versions
    cursor.execute("SELECT COUNT(*) as count FROM model_versions")
    print(f"Model Versions: {cursor.fetchone()['count']}")
    
    print("\n" + "=" * 80)
    print("EXPERIMENTS DETAILS")
    print("=" * 80)
    
    cursor.execute("""
        SELECT 
            e.name,
            COUNT(r.run_uuid) as total_runs,
            MAX(r.start_time) as last_run
        FROM experiments e
        LEFT JOIN runs r ON e.experiment_id = r.experiment_id
        GROUP BY e.experiment_id, e.name
        ORDER BY total_runs DESC
    """)
    
    for row in cursor.fetchall():
        print(f"\n📊 {row['name']}")
        print(f"   Runs: {row['total_runs']}")
        if row['last_run']:
            last_run = datetime.fromtimestamp(row['last_run'] / 1000)
            print(f"   Last Run: {last_run}")
    
    cursor.close()
    conn.close()
    print("\n" + "=" * 80)

if __name__ == "__main__":
    print_statistics()
```

**Run it:**
```bash
python analyze_mlflow_db.py
```

---

## ✅ Quick Reference

### Connection String
```
postgresql://mlflow:mlflow_password@localhost:5432/mlflow
```

### Quick Connect
```bash
docker exec -it mlflow-postgres psql -U mlflow -d mlflow
```

### List Tables
```bash
docker exec mlflow-postgres psql -U mlflow -d mlflow -c "\dt"
```

### Count Records
```bash
docker exec mlflow-postgres psql -U mlflow -d mlflow -c "
SELECT 
    'experiments' as table_name, COUNT(*) FROM experiments
UNION ALL SELECT 'runs', COUNT(*) FROM runs
UNION ALL SELECT 'registered_models', COUNT(*) FROM registered_models;"
```

---

## 📊 Summary

| Aspect | Details |
|--------|---------|
| **Container** | mlflow-postgres |
| **Host** | localhost |
| **Port** | 5432 |
| **Database** | mlflow |
| **Username** | mlflow |
| **Password** | mlflow_password |
| **Status** | ✅ Running (healthy) |
| **Tables** | 16 (MLflow schema) |
| **Access Methods** | Docker exec, psql, Python, GUI tools |

---

**Report Generated:** December 28, 2025  
**Database Status:** ✅ Running and accessible  
**Connection:** postgresql://mlflow:mlflow_password@localhost:5432/mlflow  

🗄️ **Your MLflow PostgreSQL database is ready to query!**

