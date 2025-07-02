# Memos Module Brainstorming: Features and Workflow

This document outlines proposed features and workflow enhancements for the Memos module, focusing on the lifecycle of a memo from ingestion to action and completion, involving various user roles.

## Core Workflow: Memo Lifecycle

### 1. Memo Ingestion (Role: Mail User - "Receiver")

**Purpose:** Responsible for receiving physical or digital memos and accurately entering their details into the system.

**Key Features:**

*   **Create New Memo Form:**
    *   **Essential Fields:**
        *   `Title`/`Subject`: A clear and concise summary of the memo's content.
        *   `Reference Number`: Unique identifier (can be auto-generated or manually entered, e.g., "MEMO/2025/001").
        *   `Sender`:
            *   Internal: Link to existing `CustomUser` or `Department` records.
            *   External: Free-text fields for `Organization Name` and `Contact Person`.
        *   `Recipient(s)`:
            *   Internal: Multi-select for `CustomUser` or `Department` records.
            *   External: Free-text fields for `Organization Name(s)` and `Contact Person(s)`.
        *   `Date Received`/`Date Sent`: Date fields to track the memo's origin/receipt.
        *   `Memo Type`: Dropdown/selection (e.g., "Internal Communication", "External Request", "Directive", "Information").
        *   `Priority`: Dropdown/selection (e.g., "Urgent", "High", "Medium", "Low").
        *   `Confidentiality Flag`: Boolean checkbox. If checked, triggers additional access restrictions.
        *   `Description`/`Content`: Rich text editor for the full body of the memo.
        *   `Due Date`: Optional date field for when action/response is required.
        *   `Tags`/`Keywords`: Multi-select or free-text for categorization and search.
*   **Attachments:**
    *   **Multiple File Upload:** Ability to attach one or more files (documents, images, PDFs).
    *   **Google Drive Integration:** Leverage existing `document_management` module for storage.
    *   **Confidential Attachment Flag:** Option to mark individual attachments as confidential, inheriting or overriding memo's confidentiality.
*   **Initial Status Management:**
    *   Default status: `Draft` (while the Mail User is entering details).
    *   Upon submission by Mail User: Status changes to `Pending Review`.
*   **Automated Notifications:**
    *   Notify the designated "Director" (or a predefined review group/role) that a new memo is awaiting their attention.

### 2. Director's Review & Action (Role: Director / Reviewer)

**Purpose:** To review incoming memos, determine the primary course of action, and delegate tasks as necessary.

**Key Features:**

*   **"My Memos for Review" Dashboard/Inbox:**
    *   A dedicated section or filter displaying all memos with `Pending Review` status.
    *   Quick overview of memo details (title, sender, priority, due date).
*   **Action Options (for each memo):**
    *   **"Act On It":**
        *   Changes memo status to `In Progress`.
        *   Automatically assigns the memo to the Director.
        *   Director can add initial `Comments` or `Notes`.
    *   **"Assign To":**
        *   Allows selection of one or more `CustomUser` or `Department` as assignees.
        *   Changes memo status to `Assigned`.
        *   Fields for `Assigned Due Date` and `Instructions` for the assignee(s).
    *   **"Forward for Information":**
        *   Sends a read-only notification to selected users/departments.
        *   Does not change memo status or require action from forwarded parties.
    *   **"Reject/Return":**
        *   Sends the memo back to the `Mail User` or `Original Sender`.
        *   Requires a `Reason for Rejection` comment.
        *   Changes memo status to `Rejected`.
    *   **"Archive":**
        *   Marks the memo as `Archived` if no further action is required (e.g., purely informational, already handled externally).
*   **Commenting Functionality:**
    *   Director can add internal `Comments` or `Notes` during the review process.
*   **Automated Notifications:**
    *   Notify the `Mail User` of the Director's decision (assigned, rejected, archived).
    *   Notify `Assigned Staff` of new memo assignments.

### 3. Assigned Staff Action (Role: Assignee / Action Taker)

**Purpose:** To execute the required actions on the memo and provide updates.

**Key Features:**

*   **"Memos Assigned to Me" Dashboard/Inbox:**
    *   A personal view listing all memos assigned to the current user.
    *   Displays `Instructions` from the Director and `Assigned Due Date`.
*   **Status Update Options:**
    *   `In Progress`: Indicates active work on the memo.
    *   `Blocked`: Requires input/resolution from another party (e.g., "Waiting for Legal Advice").
    *   `Needs Clarification`: Allows the assignee to request more information from the Director or previous handler.
    *   `Completed`: Marks the memo's action as finished.
*   **Commenting Functionality:**
    *   Add `Progress Updates`, `Questions`, `Challenges`, and `Final Reports`.
    *   Comments can be marked as internal or visible to the Director/Sender.
*   **Attachments:**
    *   Upload `Supporting Documents` related to the action taken.
*   **Sub-assignment/Delegation (Optional, based on permissions):**
    *   Ability to further assign specific sub-tasks related to the memo to other users within their team/department.
*   **Request Approval:**
    *   For certain memo types or actions, allow the assignee to formally `Request Approval` from the Director before marking as `Completed`.
*   **Automated Notifications:**
    *   Notify the `Director`/`Assigner` of status changes (e.g., `In Progress`, `Blocked`, `Completed`).

## General / Cross-Cutting Features

*   **Comprehensive Audit Trail / History:**
    *   Detailed log of every action performed on a memo (creation, status changes, assignments, comments, attachment uploads/deletions).
    *   Records `Timestamp` and `User` responsible for each action.
    *   Accessible `History View` for each memo.
*   **Advanced Search & Filtering:**
    *   Search by keywords in `Title`, `Description`, `Content`, and `Comments`.
    *   Filter by `Status`, `Sender`, `Recipient`, `Assigned User`, `Department`, `Date Range`, `Priority`, `Confidentiality`.
*   **Reporting & Analytics:**
    *   Dashboard widgets for `Memos by Status` (e.g., "Pending Review", "In Progress", "Completed").
    *   Metrics for `Average Time to Action/Completion`.
    *   `Memo Volume` by `Department`, `Type`, or `Priority`.
    *   `Overdue Memos` report.
*   **Enhanced Notifications System:**
    *   **In-app Notifications:** (e.g., "New memo assigned to you", "Memo you sent has been completed").
    *   **Email Notifications:** For critical updates (e.g., "Urgent memo overdue", "Memo rejected").
*   **Integration Points:**
    *   **Tasks Module:** Option to convert a memo action into a formal `Task`, maintaining a link between the two.
    *   **Meetings Module:** Link a memo to a specific `Meeting` where it was discussed or where action was decided.
    *   **Document Management:** Seamless integration for handling attachments (leveraging existing `Document` model).
    *   **Calendar Integration:** Automatically add memo `Due Dates` to a user's calendar.
*   **Security & Permissions:**
    *   Granular access control based on roles (e.g., Mail User can create, Director can approve/assign, Assignee can update).
    *   Confidentiality flags to restrict viewing/editing to authorized personnel.
*   **Memo Templates:** (Existing feature) Utilize pre-defined templates for common memo types to ensure consistency and efficiency.
*   **Digital Signatures / Formal Approvals:** (Existing feature, can be enhanced) Support multi-level approval workflows for memos requiring formal sign-off.
