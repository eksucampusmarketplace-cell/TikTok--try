"""
Task Queue System for TikTok Automation Bot

Manages task queuing, persistence, and execution.
Provides better task management than simple ThreadPoolExecutor.
"""
import json
import os
import uuid
import logging
from typing import List, Dict, Optional, Callable, Any
from datetime import datetime
from queue import Queue, Empty
from threading import Thread, Lock
from dataclasses import dataclass, field

from shared_types import Task, TaskStatus, Account, Result

logger = logging.getLogger(__name__)


@dataclass
class TaskQueue:
    """Task queue with persistence and management."""
    
    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file
        self.tasks: List[Task] = []
        self.lock = Lock()
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from storage file."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task(**task) for task in data]
                logger.info(f"Loaded {len(self.tasks)} tasks from {self.storage_file}")
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to storage file."""
        try:
            with self.lock:
                with open(self.storage_file, 'w') as f:
                    data = [task.to_dict() for task in self.tasks]
                    json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")
    
    def add_task(self, task_type: str, account_email: str, data: Dict = None) -> Task:
        """
        Add a new task to the queue.
        
        Args:
            task_type: Type of task ('comment', 'follow', 'upload', etc.)
            account_email: Email of account to execute task with
            data: Additional task data
        
        Returns:
            Created Task object
        """
        task = Task(
            id=str(uuid.uuid4()),
            type=task_type,
            account_email=account_email,
            data=data or {},
            status=TaskStatus.PENDING
        )
        
        with self.lock:
            self.tasks.append(task)
            self.save_tasks()
        
        logger.info(f"Added task: {task.id} ({task_type}) for {account_email}")
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        with self.lock:
            for task in self.tasks:
                if task.id == task_id:
                    return task
        return None
    
    def get_pending_tasks(self, account_email: Optional[str] = None, 
                     task_type: Optional[str] = None) -> List[Task]:
        """
        Get all pending tasks.
        
        Args:
            account_email: Filter by account email (optional)
            task_type: Filter by task type (optional)
        
        Returns:
            List of pending tasks
        """
        with self.lock:
            tasks = [t for t in self.tasks if t.status == TaskStatus.PENDING]
            
            if account_email:
                tasks = [t for t in tasks if t.account_email == account_email]
            if task_type:
                tasks = [t for t in tasks if t.type == task_type]
            
            return tasks
    
    def update_task_status(self, task_id: str, status: TaskStatus, 
                          error: Optional[str] = None, result: Any = None) -> bool:
        """
        Update task status.
        
        Args:
            task_id: Task ID to update
            status: New status
            error: Error message if failed
            result: Task result if completed
        
        Returns:
            True if updated successfully
        """
        with self.lock:
            for task in self.tasks:
                if task.id == task_id:
                    task.status = status
                    task.error = error
                    
                    if status == TaskStatus.RUNNING:
                        task.started_at = datetime.now().isoformat()
                    elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                        task.completed_at = datetime.now().isoformat()
                        task.result = result
                    
                    self.save_tasks()
                    logger.info(f"Updated task {task_id} to {status}")
                    return True
        
        logger.warning(f"Task not found: {task_id}")
        return False
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task."""
        return self.update_task_status(task_id, TaskStatus.CANCELLED)
    
    def remove_task(self, task_id: str) -> bool:
        """
        Remove a task from the queue.
        
        Args:
            task_id: Task ID to remove
        
        Returns:
            True if removed successfully
        """
        with self.lock:
            for i, task in enumerate(self.tasks):
                if task.id == task_id:
                    self.tasks.pop(i)
                    self.save_tasks()
                    logger.info(f"Removed task: {task_id}")
                    return True
        
        logger.warning(f"Task not found: {task_id}")
        return False
    
    def clear_completed(self) -> int:
        """Remove all completed tasks."""
        with self.lock:
            original_count = len(self.tasks)
            self.tasks = [t for t in self.tasks if t.status not in 
                          [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]]
            self.save_tasks()
            removed = original_count - len(self.tasks)
            logger.info(f"Cleared {removed} completed tasks")
            return removed
    
    def clear_all(self) -> int:
        """Remove all tasks."""
        with self.lock:
            count = len(self.tasks)
            self.tasks = []
            self.save_tasks()
            logger.info(f"Cleared all {count} tasks")
            return count
    
    def get_statistics(self) -> Dict:
        """Get task queue statistics."""
        with self.lock:
            status_counts = {}
            for task in self.tasks:
                status = task.status.value if isinstance(task.status, TaskStatus) else task.status
                status_counts[status] = status_counts.get(status, 0) + 1
            
            type_counts = {}
            for task in self.tasks:
                type_counts[task.type] = type_counts.get(task.type, 0) + 1
            
            return {
                'total': len(self.tasks),
                'pending': len([t for t in self.tasks if t.status == TaskStatus.PENDING]),
                'running': len([t for t in self.tasks if t.status == TaskStatus.RUNNING]),
                'completed': len([t for t in self.tasks if t.status == TaskStatus.COMPLETED]),
                'failed': len([t for t in self.tasks if t.status == TaskStatus.FAILED]),
                'cancelled': len([t for t in self.tasks if t.status == TaskStatus.CANCELLED]),
                'by_status': status_counts,
                'by_type': type_counts
            }
    
    def get_tasks_by_account(self, account_email: str) -> List[Task]:
        """Get all tasks for a specific account."""
        with self.lock:
            return [t for t in self.tasks if t.account_email == account_email]
    
    def get_failed_tasks(self) -> List[Task]:
        """Get all failed tasks that can be retried."""
        with self.lock:
            return [t for t in self.tasks if t.status == TaskStatus.FAILED]


class TaskPriorityQueue(Queue):
    """Priority-based task queue."""
    
    def __init__(self):
        super().__init__()
        self.priority_map = {'high': 0, 'medium': 1, 'low': 2}
    
    def put(self, task: Task, priority: str = 'medium'):
        """
        Put task in queue with priority.
        
        Args:
            task: Task to add
            priority: 'high', 'medium', or 'low'
        """
        priority_value = self.priority_map.get(priority, 1)
        super().put((priority_value, task))
        logger.debug(f"Queued task {task.id} with priority {priority}")
    
    def get(self, timeout: Optional[float] = None) -> Optional[Task]:
        """Get highest priority task."""
        try:
            priority, task = super().get(timeout=timeout)
            return task
        except Empty:
            return None
    
    def size(self, priority: Optional[str] = None) -> int:
        """Get queue size, optionally filtered by priority."""
        if priority:
            priority_value = self.priority_map.get(priority, 1)
            return sum(1 for p, _ in self.queue if p == priority_value)
        return super().qsize()


def create_batch_tasks(queue: TaskQueue, task_type: str, 
                    accounts: List[Account], data: Dict = None) -> List[Task]:
    """
    Create multiple tasks for batch operations.
    
    Args:
        queue: TaskQueue instance
        task_type: Type of tasks
        accounts: List of accounts
        data: Shared data for all tasks
    
    Returns:
        List of created tasks
    """
    tasks = []
    
    for account in accounts:
        task_data = data.copy() if data else {}
        task_data['account'] = account.to_dict()
        
        task = queue.add_task(task_type, account.email, task_data)
        tasks.append(task)
    
    logger.info(f"Created {len(tasks)} batch tasks")
    return tasks
