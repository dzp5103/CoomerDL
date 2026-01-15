"""Tests for the download scheduler functionality."""
from __future__ import annotations

import os
import sqlite3
import tempfile
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from downloader.scheduler import (
    DownloadScheduler,
    ScheduledJob,
    ScheduleType,
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    yield db_path
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def scheduler(temp_db):
    """Create a scheduler instance with temporary database."""
    sched = DownloadScheduler(temp_db)
    yield sched
    # Cleanup
    if sched.is_running():
        sched.stop()


def test_scheduler_initialization(temp_db):
    """Test that scheduler initializes correctly."""
    scheduler = DownloadScheduler(temp_db)
    assert scheduler.db_path == temp_db
    assert not scheduler.is_running()
    assert len(scheduler.get_all_jobs()) == 0


def test_schedule_once_job(scheduler):
    """Test scheduling a one-time job."""
    future_time = datetime.now() + timedelta(seconds=5)
    
    job = ScheduledJob(
        job_id="test-once",
        urls=["https://example.com/test"],
        schedule_type=ScheduleType.ONCE,
        scheduled_time=future_time,
        enabled=True,
    )
    
    job_id = scheduler.schedule_job(job)
    assert job_id == "test-once"
    
    # Verify job is stored
    jobs = scheduler.get_all_jobs()
    assert len(jobs) == 1
    assert jobs[0].job_id == "test-once"
    assert jobs[0].schedule_type == ScheduleType.ONCE


def test_schedule_daily_job(scheduler):
    """Test scheduling a daily recurring job."""
    now = datetime.now()
    
    job = ScheduledJob(
        job_id="test-daily",
        urls=["https://example.com/daily"],
        schedule_type=ScheduleType.DAILY,
        scheduled_time=now,
        enabled=True,
    )
    
    job_id = scheduler.schedule_job(job)
    assert job_id == "test-daily"
    
    # Verify job is stored
    jobs = scheduler.get_all_jobs()
    assert len(jobs) == 1
    assert jobs[0].schedule_type == ScheduleType.DAILY


def test_schedule_weekly_job(scheduler):
    """Test scheduling a weekly recurring job."""
    now = datetime.now()
    
    job = ScheduledJob(
        job_id="test-weekly",
        urls=["https://example.com/weekly"],
        schedule_type=ScheduleType.WEEKLY,
        scheduled_time=now,
        enabled=True,
    )
    
    job_id = scheduler.schedule_job(job)
    assert job_id == "test-weekly"
    
    # Verify job is stored
    jobs = scheduler.get_all_jobs()
    assert len(jobs) == 1
    assert jobs[0].schedule_type == ScheduleType.WEEKLY


def test_schedule_interval_job(scheduler):
    """Test scheduling an interval-based job."""
    now = datetime.now()
    
    job = ScheduledJob(
        job_id="test-interval",
        urls=["https://example.com/interval"],
        schedule_type=ScheduleType.INTERVAL,
        scheduled_time=now,
        interval_minutes=30,
        enabled=True,
    )
    
    job_id = scheduler.schedule_job(job)
    assert job_id == "test-interval"
    
    # Verify job is stored
    jobs = scheduler.get_all_jobs()
    assert len(jobs) == 1
    assert jobs[0].schedule_type == ScheduleType.INTERVAL
    assert jobs[0].interval_minutes == 30


def test_cancel_job(scheduler):
    """Test canceling a scheduled job."""
    future_time = datetime.now() + timedelta(seconds=60)
    
    job = ScheduledJob(
        job_id="test-cancel",
        urls=["https://example.com/cancel"],
        schedule_type=ScheduleType.ONCE,
        scheduled_time=future_time,
        enabled=True,
    )
    
    scheduler.schedule_job(job)
    assert len(scheduler.get_all_jobs()) == 1
    
    # Cancel the job
    result = scheduler.cancel_job("test-cancel")
    assert result is True
    
    # Verify job is removed
    jobs = scheduler.get_all_jobs()
    assert len(jobs) == 0


def test_enable_disable_job(scheduler):
    """Test enabling and disabling jobs."""
    future_time = datetime.now() + timedelta(seconds=60)
    
    job = ScheduledJob(
        job_id="test-enable",
        urls=["https://example.com/enable"],
        schedule_type=ScheduleType.ONCE,
        scheduled_time=future_time,
        enabled=True,
    )
    
    scheduler.schedule_job(job)
    
    # Disable the job
    scheduler.enable_job("test-enable", False)
    jobs = scheduler.get_all_jobs()
    assert jobs[0].enabled is False
    
    # Enable the job
    scheduler.enable_job("test-enable", True)
    jobs = scheduler.get_all_jobs()
    assert jobs[0].enabled is True


def test_get_job_by_id(scheduler):
    """Test retrieving a specific job by ID."""
    future_time = datetime.now() + timedelta(seconds=60)
    
    job = ScheduledJob(
        job_id="test-get",
        urls=["https://example.com/get"],
        schedule_type=ScheduleType.ONCE,
        scheduled_time=future_time,
        enabled=True,
    )
    
    scheduler.schedule_job(job)
    
    # Get the job
    retrieved_job = scheduler.get_job("test-get")
    assert retrieved_job is not None
    assert retrieved_job.job_id == "test-get"
    assert retrieved_job.urls == ["https://example.com/get"]


def test_scheduler_start_stop(scheduler):
    """Test starting and stopping the scheduler."""
    assert not scheduler.is_running()
    
    scheduler.start()
    assert scheduler.is_running()
    
    scheduler.stop()
    # Give it a moment to stop
    time.sleep(0.2)
    assert not scheduler.is_running()


def test_multiple_jobs(scheduler):
    """Test scheduling multiple jobs."""
    future_time = datetime.now() + timedelta(seconds=60)
    
    for i in range(5):
        job = ScheduledJob(
            job_id=f"test-multi-{i}",
            urls=[f"https://example.com/test{i}"],
            schedule_type=ScheduleType.ONCE,
            scheduled_time=future_time,
            enabled=True,
        )
        scheduler.schedule_job(job)
    
    jobs = scheduler.get_all_jobs()
    assert len(jobs) == 5
    
    # Verify all job IDs are unique
    job_ids = [j.job_id for j in jobs]
    assert len(set(job_ids)) == 5


def test_job_persistence(temp_db):
    """Test that jobs persist across scheduler instances."""
    future_time = datetime.now() + timedelta(seconds=60)
    
    # Create first scheduler and add a job
    scheduler1 = DownloadScheduler(temp_db)
    job = ScheduledJob(
        job_id="test-persist",
        urls=["https://example.com/persist"],
        schedule_type=ScheduleType.ONCE,
        scheduled_time=future_time,
        enabled=True,
    )
    scheduler1.schedule_job(job)
    
    # Create second scheduler with same database
    scheduler2 = DownloadScheduler(temp_db)
    jobs = scheduler2.get_all_jobs()
    
    assert len(jobs) == 1
    assert jobs[0].job_id == "test-persist"


def test_event_callback(scheduler):
    """Test that event callbacks are triggered."""
    events = []
    
    def callback(event_type, job_id, message):
        events.append((event_type, job_id, message))
    
    scheduler.set_event_callback(callback)
    
    future_time = datetime.now() + timedelta(seconds=60)
    job = ScheduledJob(
        job_id="test-event",
        urls=["https://example.com/event"],
        schedule_type=ScheduleType.ONCE,
        scheduled_time=future_time,
        enabled=True,
    )
    
    scheduler.schedule_job(job)
    
    # Should have triggered SCHEDULED event
    assert len(events) >= 1
    assert events[0][0] == "SCHEDULED"
    assert events[0][1] == "test-event"


def test_manual_trigger(scheduler):
    """Test manually triggering a job."""
    future_time = datetime.now() + timedelta(hours=1)
    
    job = ScheduledJob(
        job_id="test-trigger",
        urls=["https://example.com/trigger"],
        schedule_type=ScheduleType.ONCE,
        scheduled_time=future_time,
        enabled=True,
    )
    
    scheduler.schedule_job(job)
    
    # Manually trigger the job
    result = scheduler.trigger_job_now("test-trigger")
    assert result is True


def test_invalid_job_id(scheduler):
    """Test operations with invalid job IDs."""
    # Try to cancel non-existent job
    result = scheduler.cancel_job("nonexistent")
    assert result is False
    
    # Try to get non-existent job
    job = scheduler.get_job("nonexistent")
    assert job is None
    
    # Try to trigger non-existent job
    result = scheduler.trigger_job_now("nonexistent")
    assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
