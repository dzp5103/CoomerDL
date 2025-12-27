"""
Download History Database - Persistent storage for jobs and events.

Uses SQLite for thread-safe persistence of download history.
"""
import json
import os
import sqlite3
import threading
from typing import List, Optional
from pathlib import Path

from downloader.models import (
    DownloadJob, DownloadEvent, JobStatus, DownloadEventType
)


class DownloadHistoryDB:
    """
    SQLite-based persistent storage for download jobs and events.
    
    Thread-safe implementation using a lock for all database operations.
    """
    
    DEFAULT_DB_PATH = "resources/config/download_history.db"
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the history database.
        
        Args:
            db_path: Path to the SQLite database file.
                     Defaults to resources/config/download_history.db
        """
        self.db_path = db_path or self.DEFAULT_DB_PATH
        self._lock = threading.Lock()
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize database tables if they don't exist."""
        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                
                # Jobs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS jobs (
                        job_id TEXT PRIMARY KEY,
                        url TEXT NOT NULL,
                        engine TEXT NOT NULL,
                        status TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        started_at TEXT,
                        finished_at TEXT,
                        total_items INTEGER DEFAULT 0,
                        completed_items INTEGER DEFAULT 0,
                        failed_items INTEGER DEFAULT 0,
                        skipped_items INTEGER DEFAULT 0,
                        output_folder TEXT,
                        error_message TEXT,
                        options_json TEXT
                    )
                ''')
                
                # Events table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        job_id TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        type TEXT NOT NULL,
                        payload_json TEXT,
                        FOREIGN KEY (job_id) REFERENCES jobs(job_id)
                    )
                ''')
                
                # Create indexes for common queries
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_jobs_status 
                    ON jobs(status)
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_jobs_created_at 
                    ON jobs(created_at DESC)
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_events_job_id 
                    ON events(job_id)
                ''')
                
                conn.commit()
            finally:
                conn.close()
    
    def save_job(self, job: DownloadJob) -> None:
        """
        Save or update a job in the database.
        
        Args:
            job: The job to save.
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO jobs (
                        job_id, url, engine, status, created_at, started_at,
                        finished_at, total_items, completed_items, failed_items,
                        skipped_items, output_folder, error_message, options_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    job.id,
                    job.url,
                    job.engine,
                    job.status.value,
                    job.created_at,
                    job.started_at,
                    job.finished_at,
                    job.total_items,
                    job.completed_items,
                    job.failed_items,
                    job.skipped_items,
                    job.output_folder,
                    job.error_message,
                    json.dumps(job.options_snapshot)
                ))
                
                conn.commit()
            finally:
                conn.close()
    
    def append_event(self, event: DownloadEvent) -> None:
        """
        Append an event to the database.
        
        Args:
            event: The event to append.
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO events (job_id, timestamp, type, payload_json)
                    VALUES (?, ?, ?, ?)
                ''', (
                    event.job_id,
                    event.timestamp,
                    event.type.value,
                    json.dumps(event.payload)
                ))
                
                conn.commit()
            finally:
                conn.close()
    
    def list_jobs(
        self,
        limit: int = 200,
        status: Optional[JobStatus] = None,
        offset: int = 0
    ) -> List[DownloadJob]:
        """
        List jobs from the database.
        
        Args:
            limit: Maximum number of jobs to return.
            status: Filter by status (optional).
            offset: Number of jobs to skip for pagination.
            
        Returns:
            List of DownloadJob instances.
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if status:
                    cursor.execute('''
                        SELECT * FROM jobs 
                        WHERE status = ?
                        ORDER BY created_at DESC
                        LIMIT ? OFFSET ?
                    ''', (status.value, limit, offset))
                else:
                    cursor.execute('''
                        SELECT * FROM jobs 
                        ORDER BY created_at DESC
                        LIMIT ? OFFSET ?
                    ''', (limit, offset))
                
                rows = cursor.fetchall()
                return [self._row_to_job(row) for row in rows]
            finally:
                conn.close()
    
    def get_job(self, job_id: str) -> Optional[DownloadJob]:
        """
        Get a specific job by ID.
        
        Args:
            job_id: The job ID to look up.
            
        Returns:
            DownloadJob if found, None otherwise.
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute(
                    'SELECT * FROM jobs WHERE job_id = ?',
                    (job_id,)
                )
                
                row = cursor.fetchone()
                if row:
                    return self._row_to_job(row)
                return None
            finally:
                conn.close()
    
    def get_job_events(
        self,
        job_id: str,
        limit: int = 1000
    ) -> List[DownloadEvent]:
        """
        Get events for a specific job.
        
        Args:
            job_id: The job ID to look up events for.
            limit: Maximum number of events to return.
            
        Returns:
            List of DownloadEvent instances.
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM events 
                    WHERE job_id = ?
                    ORDER BY timestamp ASC
                    LIMIT ?
                ''', (job_id, limit))
                
                rows = cursor.fetchall()
                return [self._row_to_event(row) for row in rows]
            finally:
                conn.close()
    
    def delete_job(self, job_id: str) -> bool:
        """
        Delete a job and its events from the database.
        
        Args:
            job_id: The job ID to delete.
            
        Returns:
            True if job was deleted, False if not found.
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                
                # Delete events first (foreign key)
                cursor.execute(
                    'DELETE FROM events WHERE job_id = ?',
                    (job_id,)
                )
                
                # Delete job
                cursor.execute(
                    'DELETE FROM jobs WHERE job_id = ?',
                    (job_id,)
                )
                
                deleted = cursor.rowcount > 0
                conn.commit()
                return deleted
            finally:
                conn.close()
    
    def clear_completed_jobs(self, keep_last: int = 100) -> int:
        """
        Clear old completed jobs, keeping the most recent ones.
        
        Args:
            keep_last: Number of completed jobs to keep.
            
        Returns:
            Number of jobs deleted.
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                
                # Get IDs of jobs to delete
                cursor.execute('''
                    SELECT job_id FROM jobs 
                    WHERE status = ?
                    ORDER BY finished_at DESC
                    LIMIT -1 OFFSET ?
                ''', (JobStatus.COMPLETED.value, keep_last))
                
                job_ids = [row[0] for row in cursor.fetchall()]
                
                if not job_ids:
                    return 0
                
                # Delete events
                placeholders = ','.join('?' * len(job_ids))
                cursor.execute(
                    f'DELETE FROM events WHERE job_id IN ({placeholders})',
                    job_ids
                )
                
                # Delete jobs
                cursor.execute(
                    f'DELETE FROM jobs WHERE job_id IN ({placeholders})',
                    job_ids
                )
                
                deleted = len(job_ids)
                conn.commit()
                return deleted
            finally:
                conn.close()
    
    def get_stats(self) -> dict:
        """
        Get statistics about the download history.
        
        Returns:
            Dictionary with counts by status.
        """
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT status, COUNT(*) as count 
                    FROM jobs 
                    GROUP BY status
                ''')
                
                stats = {row[0]: row[1] for row in cursor.fetchall()}
                
                cursor.execute('SELECT COUNT(*) FROM jobs')
                stats['total'] = cursor.fetchone()[0]
                
                return stats
            finally:
                conn.close()
    
    def _row_to_job(self, row: sqlite3.Row) -> DownloadJob:
        """Convert a database row to a DownloadJob instance."""
        options = {}
        if row['options_json']:
            try:
                options = json.loads(row['options_json'])
            except json.JSONDecodeError:
                pass
        
        return DownloadJob(
            id=row['job_id'],
            url=row['url'],
            engine=row['engine'],
            status=JobStatus(row['status']),
            created_at=row['created_at'],
            started_at=row['started_at'],
            finished_at=row['finished_at'],
            total_items=row['total_items'],
            completed_items=row['completed_items'],
            failed_items=row['failed_items'],
            skipped_items=row['skipped_items'],
            output_folder=row['output_folder'] or '',
            error_message=row['error_message'],
            options_snapshot=options
        )
    
    def _row_to_event(self, row: sqlite3.Row) -> DownloadEvent:
        """Convert a database row to a DownloadEvent instance."""
        payload = {}
        if row['payload_json']:
            try:
                payload = json.loads(row['payload_json'])
            except json.JSONDecodeError:
                pass
        
        return DownloadEvent(
            type=DownloadEventType(row['type']),
            job_id=row['job_id'],
            timestamp=row['timestamp'],
            payload=payload
        )
