import sqlite3
import os
import json
from datetime import datetime
import threading

class DatabaseManager:
    def __init__(self, db_name="kids_python_app.db"):
        """Initialize the database connection"""
        self.db_name = db_name
        self._local = threading.local()
        self.initialize_database()
        
    def connect(self):
        """Connect to the database in a thread-safe way"""
        # Always create a new connection for each request to avoid threading issues
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        return conn, cursor
        
    def disconnect(self, conn=None, cursor=None):
        """Disconnect from the database"""
        if conn:
            conn.close()
            
    def initialize_database(self):
        """Create database tables if they don't exist"""
        conn, cursor = self.connect()
        
        # Create users table with profile information
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            parent_name TEXT,
            dob TEXT,
            class TEXT,
            section TEXT,
            school TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        ''')
        
        # Create progress table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            points INTEGER DEFAULT 0,
            completed_tutorials TEXT DEFAULT '[]',
            completed_challenges TEXT DEFAULT '[]',
            emoji_collection TEXT DEFAULT '[]',
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Create events table to track user activity
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            event_details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Create certificates table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            certificate_type TEXT NOT NULL,
            issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            certificate_code TEXT UNIQUE,
            completed_date TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        conn.commit()
        self.disconnect(conn)
        
    # User management functions
    def add_user(self, username, password_hash, profile_data=None):
        """
        Add a new user to the database
        
        Args:
            username (str): User's chosen username
            password_hash (str): Hashed password
            profile_data (dict, optional): Dictionary containing user profile information
        """
        conn, cursor = self.connect()
        try:
            if profile_data:
                cursor.execute(
                    """
                    INSERT INTO users (
                        username, password_hash, full_name, parent_name, 
                        dob, class, section, school
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        username, password_hash, 
                        profile_data.get('full_name', ''),
                        profile_data.get('parent_name', ''),
                        profile_data.get('dob', ''),
                        profile_data.get('class', ''),
                        profile_data.get('section', ''),
                        profile_data.get('school', '')
                    )
                )
            else:
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )
            
            user_id = cursor.lastrowid
            
            # Create an empty progress record for the user
            cursor.execute(
                "INSERT INTO user_progress (user_id) VALUES (?)",
                (user_id,)
            )
            
            # Log user creation event
            self.log_event(user_id, "user_created", f"User account created for {username}")
            
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            # Username already exists
            return None
        finally:
            self.disconnect(conn)
            
    def get_user(self, username):
        """Get user details by username"""
        conn, cursor = self.connect()
        try:
            cursor.execute(
                """
                SELECT id, username, password_hash, full_name, parent_name, 
                dob, class, section, school
                FROM users WHERE username = ?
                """,
                (username,)
            )
            user = cursor.fetchone()
            if user:
                return {
                    "id": user[0],
                    "username": user[1],
                    "password_hash": user[2],
                    "full_name": user[3],
                    "parent_name": user[4],
                    "dob": user[5],
                    "class": user[6],
                    "section": user[7],
                    "school": user[8]
                }
            return None
        finally:
            self.disconnect(conn)
            
    def update_last_login(self, user_id):
        """Update user's last login timestamp"""
        conn, cursor = self.connect()
        try:
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (user_id,)
            )
            conn.commit()
        finally:
            self.disconnect(conn)
            
    # Progress tracking functions
    def get_user_progress(self, user_id):
        """Get user's progress"""
        conn, cursor = self.connect()
        try:
            cursor.execute(
                "SELECT points, completed_tutorials, completed_challenges, emoji_collection FROM user_progress WHERE user_id = ?",
                (user_id,)
            )
            progress = cursor.fetchone()
            if progress:
                return {
                    "points": progress[0],
                    "completed_tutorials": json.loads(progress[1]),
                    "completed_challenges": json.loads(progress[2]),
                    "emoji_collection": json.loads(progress[3])
                }
            return {
                "points": 0,
                "completed_tutorials": [],
                "completed_challenges": [],
                "emoji_collection": []
            }
        finally:
            self.disconnect(conn)
            
    def update_user_progress(self, user_id, points, completed_tutorials, completed_challenges, emoji_collection):
        """Update user's progress"""
        conn, cursor = self.connect()
        try:
            cursor.execute(
                """
                UPDATE user_progress 
                SET points = ?, 
                    completed_tutorials = ?, 
                    completed_challenges = ?, 
                    emoji_collection = ?,
                    last_updated = CURRENT_TIMESTAMP
                WHERE user_id = ?
                """,
                (
                    points, 
                    json.dumps(completed_tutorials), 
                    json.dumps(completed_challenges), 
                    json.dumps(emoji_collection),
                    user_id
                )
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating progress: {str(e)}")
            return False
        finally:
            self.disconnect(conn)
            
    # Event logging
    def log_event(self, user_id, event_type, event_details=None):
        """Log a user event"""
        conn, cursor = self.connect()
        try:
            cursor.execute(
                "INSERT INTO user_events (user_id, event_type, event_details) VALUES (?, ?, ?)",
                (user_id, event_type, event_details)
            )
            conn.commit()
        except Exception as e:
            print(f"Error logging event: {str(e)}")
        finally:
            self.disconnect(conn)
                
    def get_user_events(self, user_id, limit=50):
        """Get recent events for a user"""
        conn, cursor = self.connect()
        try:
            cursor.execute(
                """
                SELECT event_type, event_details, timestamp 
                FROM user_events 
                WHERE user_id = ? 
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (user_id, limit)
            )
            events = cursor.fetchall()
            return [
                {
                    "event_type": event[0],
                    "event_details": event[1],
                    "timestamp": event[2]
                }
                for event in events
            ]
        finally:
            self.disconnect(conn)
            
    # Certificate management
    def create_certificate(self, user_id, certificate_type):
        """Create a certificate for a user"""
        import uuid
        certificate_code = str(uuid.uuid4())
        
        conn, cursor = self.connect()
        try:
            cursor.execute(
                """
                INSERT INTO certificates 
                (user_id, certificate_type, certificate_code) 
                VALUES (?, ?, ?)
                """,
                (user_id, certificate_type, certificate_code)
            )
            conn.commit()
            
            # Log certificate creation event
            self.log_event(
                user_id, 
                "certificate_created", 
                f"Certificate of type '{certificate_type}' created with code {certificate_code}"
            )
            
            return certificate_code
        except Exception as e:
            print(f"Error creating certificate: {str(e)}")
            return None
        finally:
            self.disconnect(conn)
            
    def complete_certificate(self, certificate_code):
        """Mark a certificate as completed"""
        conn, cursor = self.connect()
        try:
            cursor.execute(
                """
                UPDATE certificates 
                SET completed_date = CURRENT_TIMESTAMP
                WHERE certificate_code = ?
                """,
                (certificate_code,)
            )
            conn.commit()
            
            # Get user id for the certificate
            cursor.execute(
                "SELECT user_id, certificate_type FROM certificates WHERE certificate_code = ?",
                (certificate_code,)
            )
            result = cursor.fetchone()
            if result:
                user_id, cert_type = result
                # Log certificate completion event
                self.log_event(
                    user_id, 
                    "certificate_completed", 
                    f"Certificate of type '{cert_type}' with code {certificate_code} completed"
                )
            
            return True
        except Exception as e:
            print(f"Error completing certificate: {str(e)}")
            return False
        finally:
            self.disconnect(conn)
            
    def get_user_certificates(self, user_id):
        """Get all certificates for a user"""
        conn, cursor = self.connect()
        try:
            cursor.execute(
                """
                SELECT certificate_type, issue_date, certificate_code, completed_date
                FROM certificates
                WHERE user_id = ?
                ORDER BY issue_date DESC
                """,
                (user_id,)
            )
            certificates = cursor.fetchall()
            return [
                {
                    "certificate_type": cert[0],
                    "issue_date": cert[1],
                    "certificate_code": cert[2],
                    "completed_date": cert[3],
                    "is_completed": cert[3] is not None
                }
                for cert in certificates
            ]
        finally:
            self.disconnect(conn)
            
    def verify_certificate(self, certificate_code):
        """Verify a certificate by its code"""
        conn, cursor = self.connect()
        try:
            cursor.execute(
                """
                SELECT c.certificate_type, c.issue_date, c.completed_date, u.username,
                       u.full_name, u.parent_name, u.dob, u.class, u.section, u.school, u.id
                FROM certificates c
                JOIN users u ON c.user_id = u.id
                WHERE c.certificate_code = ?
                """,
                (certificate_code,)
            )
            result = cursor.fetchone()
            if result:
                # Create a profile data dictionary from the user information
                profile_data = {
                    'full_name': result[4] or '',
                    'parent_name': result[5] or '',
                    'dob': result[6] or '',
                    'class': result[7] or '',
                    'section': result[8] or '',
                    'school': result[9] or ''
                }
                
                return {
                    "certificate_type": result[0],
                    "issue_date": result[1],
                    "completed_date": result[2],
                    "username": result[3],
                    "profile_data": profile_data,
                    "user_id": result[10],
                    "is_completed": result[2] is not None,
                    "is_valid": True
                }
            return {"is_valid": False}
        finally:
            self.disconnect(conn)
            
    # Helper function to migrate from JSON files to database
    def migrate_data_from_json(self):
        """Migrate user data from JSON files to the database"""
        # Check if users.json exists
        if os.path.exists("users.json"):
            try:
                # Load users data
                with open("users.json", "r") as f:
                    users_data = json.load(f)
                
                # Migrate each user
                for username, user_info in users_data.items():
                    # Add user to database
                    user_id = self.add_user(username, user_info["password"])
                    
                    if user_id:
                        # Load progress data for the user
                        if os.path.exists(f"progress_{username}.json"):
                            with open(f"progress_{username}.json", "r") as f:
                                progress_data = json.load(f)
                                
                            # Update progress in database
                            self.update_user_progress(
                                user_id,
                                progress_data.get("points", 0),
                                progress_data.get("completed_tutorials", []),
                                progress_data.get("completed_challenges", []),
                                progress_data.get("emoji_collection", [])
                            )
                
                return True
            except Exception as e:
                print(f"Error migrating data: {str(e)}")
                return False
        return False

def migrate_from_json_if_needed():
    """Check if migration is needed and perform it"""
    try:
        db_manager = DatabaseManager()
        # Check if we need to migrate by checking if any users exist in the database
        conn, cursor = db_manager.connect()
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            # If no users, try to migrate from JSON
            if user_count == 0:
                print("No users found in database, attempting migration from JSON files...")
                if db_manager.migrate_data_from_json():
                    print("Migration successful")
                else:
                    print("No JSON data to migrate or migration failed")
            else:
                print(f"Found {user_count} users in database, no migration needed")
                
        finally:
            db_manager.disconnect(conn)
    except Exception as e:
        print(f"Error migrating data: {str(e)}")
def inspect_database(self):
    """Print database tables and their contents"""
    conn, cursor = self.connect()
    try:
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        info = {}
        for table in tables:
            table_name = table[0]
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            # Get table contents
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            sample_data = cursor.fetchall()
            
            info[table_name] = {
                'columns': [col[1] for col in columns],
                'sample_data': sample_data
            }
            
        return info
    finally:
        self.disconnect(conn)
