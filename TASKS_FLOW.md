### Simple and Effective Task Flow for the `tasks` Module

This document outlines a streamlined and effective workflow for managing tasks, focusing on assignment, status changes, and historical tracking. It leverages Django's built-in features and the recent improvements implemented in the `tasks` module.

---

#### **Core Principles:**

1.  **Automation:** History tracking and notifications are automated via Django signals, reducing manual effort and ensuring consistency.
2.  **Clarity:** User interface and historical records provide clear information about task status and changes.
3.  **Responsibility:** Clear roles (Creator, Assignee, Project Owner) define who can perform actions.
4.  **Simplicity:** Avoid overly complex workflows; focus on essential actions.

---

#### **Task Flow Stages:**

**1. Task Creation & Initial Assignment**

*   **Action:** A user (e.g., Project Owner, or anyone with appropriate permissions) creates a new task.
    *   **UI:** User navigates to a project's detail page and clicks "Add New Task" (or directly accesses the task creation form).
    *   **Inputs:** Task title, description, project, priority, due date, and optional assignees. A "Assign to myself" checkbox simplifies self-assignment.
*   **System Response (Automated):**
    *   **Task Creation:** The new `Task` object is saved to the database.
    *   **History Tracking:** A `TaskHistory` entry is automatically created via a `post_save` signal, with a `change_description` like: "Task created."
    *   **Email Notification:** If assignees are selected during creation, an email is sent to each newly assigned user, informing them of their new task.

**2. Task Lifecycle & Status Changes**

*   **Key Statuses:** `TODO`, `IN_PROGRESS`, `IN_REVIEW`, `DONE`, `BLOCKED`, `REJECTED`, `ON_HOLD`.
*   **Action:** An authorized user (Assignee, Creator, Project Owner) updates the task's status.
    *   **UI:** On the `TaskDetailView`, a dropdown allows selecting a new status.
*   **System Response (Automated):**
    *   **Status Update:** The `Task` object's status field is updated and saved.
    *   **History Tracking:** The `post_save` signal detects the status change and creates a `TaskHistory` entry with a `change_description` like: "Status changed from 'To Do' to 'In Progress'."
    *   **Email Notification:** An email is sent to the task's creator and all current assignees, notifying them of the status change.

**3. Task Reassignment**

*   **Action:** An authorized user (Creator, Project Owner, or a user with specific "can reassign task" permission) changes the assignees of a task.
    *   **UI:** User utilizes the "Reassign Task" modal on the task detail page, selecting new assignees and/or deselecting current ones.
*   **System Response (Automated):**
    *   **Assignee Update:** The `Task` object's `assignees` (Many-to-Many field) are updated. This action triggers the `post_save` signal for the `Task` model.
    *   **History Tracking:** The `post_save` signal detects changes in assignees and creates `TaskHistory` entries:
        *   For each newly assigned user: "User 'X' was assigned to the task."
        *   For each unassigned user: "User 'Y' was unassigned from the task."
    *   **Notifications:**
        *   An email is sent to each **newly assigned user**, informing them of their new task.
        *   An email is sent to each **unassigned user**, notifying them that they are no longer assigned to the task.
        *   (Optional) An email can be sent to the task's creator and/or project owner about the reassignment.
    *   **Status Adjustment (Automated):**
        *   If the task's previous status was `IN_PROGRESS` or `IN_REVIEW`, its status is automatically reverted to `TODO`. This ensures the new assignee explicitly picks up the task.
        *   If the task's status was `BLOCKED`, `ON_HOLD`, `APPROVED`, `REJECTED`, or `DONE`, its status remains unchanged.
        *   This status change (if it occurs) also triggers a separate `TaskHistory` entry and email notification (as per "Task Lifecycle & Status Changes" flow).

---